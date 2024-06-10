
This project has been developed with:
- ruff for linter, and formatter,
- mypy for type checking,
- pytest for unit-test,
- poetry for package manager

code lives in mathserver package.

# Getting started

You need poetry to setup the project.

For nix user a nix file is provided which install poetry and set FHS env for ruff. 
Just run nix-shell from the project root

Install the project:

```
poetry install
```

Then, you can run server with:

```
poetry run server
```

The server will listen, by default, on `localhost:9999`. But this can be overloaded with
`SERVER_LISTEN_ADDRESS` and `SERVER_PORT` environment variables.

The client can be runned with:

```
$ poetry run client --help
usage: Arithmetic client [-h] host port input_file output_file

A client for the arithmetic server

positional arguments:
  host
  port
  input_file
  output_file

options:
  -h, --help   show this help message and exit
```

By example if the server is listening on `localhost:9000` one can run:

```
poetry run client localhost 9999 operations.txt result.txt
```

The script will read operations from `operations.txt` and write their results in `result.txt`.


# Develop

run the test:

```
pytest
```

check code:
```
ruff check
```

format code:

```
ruff format
```

type checking:

```
mypy .
```



# Todo

## requirements

* [x] Develop a client which is able to send the information given at operations.7z:
  - [x] send the information using sockets to the service,
  - [x] receive information through the sockets and store the results in a file,
* [x] Develop a service in Python which is built with the following features:
  - [x] receive information using sockets,
  - [x] It is built by 2 different processes (at least). Consider having more processes to speed calculations,
  - [x] Processes must be able to exchange information using pipes. Please DO NOT use Threading or Pool,
  - [x] Parent process must create and destroy child process for the arithmetic operations given at operations.7z,
  - [x] Once the arithmetic operation is finished on the second process, such process should be destroyed by the parent process,
  - [x] Consider that operations should not be calculated using eval(),
  - [x] Consider using logging instead of console prints.
* [x] parser
