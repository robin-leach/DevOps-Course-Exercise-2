terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">=2.49"
    }
  }

  backend "azurerm" {
    resource_group_name   = "SoftwirePilot_RobinLeach_ProjectExercise"
    storage_account_name  = "rtltfstatesa"
    container_name        = "rta-tf-state-container"
    key                   = "terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "SoftwirePilot_RobinLeach_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-todo-app-rtl"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|robinleach/todo-app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL"  = "https://index.docker.io"
    "MONGO_DB_CONNECTION_STRING"  = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "MONGO_DB_DATABASE_NAME"      = azurerm_cosmosdb_mongo_database.main.name
    "LOGIN_DISABLED"              = var.login_disabled ? "TRUE" : "FALSE"
    "CLIENT_ID"                   = var.client_id
    "CLIENT_SECRET"               = var.client_secret
    "OAUTHLIB_INSECURE_TRANSPORT" = var.oathlib_insecure_transport ? 1 : 0
    "FLASK_APP"                   = var.flask_app
    "FLASK_ENV"                   = var.flask_env
    "LOG_LEVEL"                   = var.log_level
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "${var.prefix}-cosmos-account-rtl"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }

  capabilities {
    name = "EnableServerless"
  }

  capabilities {
    name = "EnableMongo"
  }

  lifecycle {
    create_before_destroy = true
    prevent_destroy = true
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "${var.prefix}-cosmos-database-rtl"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}
