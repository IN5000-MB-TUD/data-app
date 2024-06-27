# A Framework for Identifying Evolution Patterns of Open-Source Software Projects - UI

IN5000 TU Delft - MSc Computer Science

This repository contains the UI to visualize the time series processed in the following repository:

https://github.com/IN5000-MB-TUD/data-analysis

## Requirements

- Python >= 3.10
- MongoDB (can be changed if needed but the scripts must be adapted)

Run in the terminal:

```shell
# Scripts requirements
pip install -r requirements.txt

# Scripts + code formatting requirements
pip install -r requirements-ci.txt
```

## Environment Variables

The following environment variables must be set in order to run the scripts:

```shell
MONGODB_HOST
MONGODB_PORT
MONGODB_DATABASE
MONGODB_USER
MONGODB_PASSWORD
MONGODB_QPARAMS
```

## Run

Open the terminal and run:

```shell
# Start the webserver
uvicorn main:app --reload --host 0.0.0.0 --port 8081
```

Open the browser at the url http://localhost:8081

## Code Formatting

To ensure high code quality, the Black formatted can be run as follows:

```shell
# Check formatting
black --check ./

# Format files
black ./
```

## Contributors

Project developed for the course IN5000 - Master's thesis of the 2023/2024 academic year at TU Delft.

Author:
- Mattia Bonfanti
- [m.bonfanti@student.tudelft.nl](mailto:m.bonfanti@student.tudelft.nl)
- Master's in Computer Science - Software Technology Track
