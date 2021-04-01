# To-do app

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a shell terminal (e.g. Git Bash on Windows):
```bash
$ source setup.sh
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

 The app must linked to a Github OAuth app, through the `CLIENT_ID` and `CLIENT_SECRET` env variables. Either obtain these from an existing Github OAuth app, or follow [these instructions](https://docs.github.com/en/developers/apps/creating-an-oauth-app) to create a new one.

 After logging in through Github, the app grants you different permissions based off of whether your Github username is associate with a "Writer" role (i.e. you have write priveledges), or the default "Reader" role. Currently these roles are assigned to Github usernames through a hardcoded list in `entity\user.py`.

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
