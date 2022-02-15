# pyflycli

**pyflycli** is a command-line interface application built with [Typer](https://typer.tiangolo.com/) that allows you to view flights above your location.


1. Download the application's source code.
```sh
$ git clone https://github.com/k-zehnder/pyflycli
```
2. Use Poetry to set up environment.

```sh
$ cd pyflicli/
$ pip install poetry
$ poetry shell 
$ poetry install
```
3. Initialize the application
```sh 
$ poetry run pyfly init
```
4. List Responses
```sh 
$ poetry run pyfly list
```

## Example Image
Note: One-to-many relationship between Response (one) --> Detailedflight (many). Each time the data is pulled (cron job running every 30 min) from Flight Radar API (see: https://github.com/k-zehnder/fastapi-aviation-async-postgres) a Response object is created, which holds a relationship to DetailedFlight objects. This way, for each period in time, we can gather the flights that were overhead at that period in time. This also means a DetailedFlight -- (many) in the one-to-many with Response (one) -- could be contained in multiple Responses, because in theory that plane could be overhead throughout multiple "pulls" of the data.
![Work in progress](https://github.com/k-zehnder/pyflycli/blob/main/demo.png)
