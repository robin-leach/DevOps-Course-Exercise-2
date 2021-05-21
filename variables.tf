variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "client_id" {
  description = "OAuth client ID"
  type        = string
  sensitive   = true
}

variable "client_secret" {
  description = "OAuth client secret"
  type        = string
  sensitive   = true
}

variable "login_disabled" {
  description = "OAuth is used unless this is true"
  type        = bool
  default     = true
}

variable "oathlib_insecure_transport" {
  description = "Use insecure transport for OAuth"
  type        = bool
  default     = true
}

variable "flask_app" {
  description = "Standard Flask FLASK_APP env variable"
  type        = string
  default     = "app"
}

variable "flask_env" {
  description = "Standard Flask FLASK_ENV env variable"
  type        = string
  default     = "development"
}

variable "log_level" {
  description = "The log level for the recorded logs"
  type        = string
  default     = "DEBUG"
}
