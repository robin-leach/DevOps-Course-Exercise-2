# DevOps Apprenticeship: Project Exercise

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

## Trello Requirements

This app relies on being hooked up to a Trello board with the following column names: "To do", "Doing", "Done" (see `entity/list_name.py`).

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