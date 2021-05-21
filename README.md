# To-do app

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a shell terminal (e.g. Git Bash on Windows):
```bash
$ source scripts/setup.sh
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Environment variables

For the app to run successfully, you will need the correct environment variables in a `.env` file at the root of the project. The `.env.template` shows you which environment variables you will need.

 ## OAuth

 By default, the app is run with OAuth which protects every endpoint. To disable this, set `LOGIN_DISABLED=TRUE` in your `.env` file.

 The app must linked to a Github OAuth app, through the `CLIENT_ID` and `CLIENT_SECRET` env variables. Either obtain these from an existing Github OAuth app, or follow [these instructions](https://docs.github.com/en/developers/apps/creating-an-oauth-app) to create a new one. The callback route is `/login/callback`.

 After logging in through Github, the app grants you different permissions based off of whether your Github username is associate with a "Writer" role (i.e. you have write privileges), or the default "Reader" role. Currently these roles are assigned to Github usernames through a hardcoded list in `entity\user.py`.

 We aren't using https locally, and so in your `.env` you will need `OAUTHLIB_INSECURE_TRANSPORT=1`.
 
## Run on a VM

### Vagrant

You can run this on a VM by running `vagrant up` at the root. Once the command has finished, as above you can visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app. Any logs from this are saved to `app_logs.log`.

### Docker

To run the app on Docker in development mode (with hot reloading), run `docker-compose up dev-app`. To run it in production mode, run `docker-compose up prod-app`. Once again the app can then be found at [`http://localhost:5000/`](http://localhost:5000/).

## Testing

### Prerequisites

You will need a `chromedriver.exe` file at the project root, and Chrome installed.

### Running the tests

To run all tests, run `pytest`.

To run unit tests, run `pytest test`.

To run integration tests, run `pytest integration_tests`.

To run end-to-end tests, run `pytest e2e_tests`.

### Running the tests in a Docker container 

To run the tests in a Docker container, run  `docker build --tag test --target test .` to build the container and
 * `docker run test test` to run all the unit tests
 * `docker run test integration_tests` to run all the integration tests
 * `docker run --env-file .env test e2e_tests` to run all the end-to-end tests
 * `docker run --env-file .env test` to run all the tests

 ## Infrastructure

 The application is hosted on Azure, with the infrastructure described by Terraform.

 ### Making changes to the infrastructure

 To make changes to the infrastructure, you should edit the terraform files and apply the changes rather than making changes in Azure directly. To do this:
 1. Run `terraform init` in the root of the project
 2. Make your changes to the terraform files
 3. Preview your changes with the `terraform plan` command
 4. Apply your changes with the `terraform apply` command
 
 Note that when running `terraform plan` or `terraform apply`, you will need to provide variable values. To do this, you can either create a `.tfvars` file based off of `.tfvars.template` with your secret values and use that by running 
 ```
 terraform plan -var-file [FILE NAME].tfvars
 ```
 or provide them individually by running
 ```
 terraform plan var="some_var_value=[FIRST VALUE]" -var="another_var_value=[SECOND VALUE]" ...
```
where `some_var_value`, `another_var_value` etc. are the variables listed in `.tfvars.template`.

### State storage

The Terraform state is stored in a blob container in Azure. The setup for this was done by running `scripts/configure-tf-state-storage.sh`, and so this script will also tell you how to find the state. Note that this script should *not* be run again unless the state needs to be set up again for some reason, but is left for documentation reasons and future reference.
