* [ ] Develop a client which is able to send the information given at operations.7z:
  - [ ] send the information using sockets to the service,
  - [ ] receive information through the sockets and store the results in a file,

* [ ] Develop a service in Python which is built with the following features:
  - [ ] receive information using sockets,
  - [ ] It is built by 2 different processes (at least). Consider having more processes to speed calculations,
  - [ ] Processes must be able to exchange information using pipes. Please DO NOT use Threading or Pool,
  - [ ] Parent process must create and destroy child process for the arithmetic operations given at operations.7z,
  - [ ] Once the arithmetic operation is finished on the second process, such process should be destroyed by the parent process,
  - [ ] Consider that operations should not be calculated using eval(),
  - [ ] Consider using logging instead of console prints.
