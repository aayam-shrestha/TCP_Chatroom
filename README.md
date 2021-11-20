# TCP Chat Client and Server

This is a TCP chat system that allows multiple users to chat interactively in a terminal window. One server must be running on a designated TCP port and any number of TCP clients can connect to the server, and then talk to each other interactively.

The command-line arguments for the server are:
| Name(s)       | Option      | Meaning                                    | Default value (if option not given) |
|---------------|-------------|--------------------------------------------|-------------------------------------|
| -v, --verbose |             | Turn on verbose printing to help debugging | False                               |
| -p, --port    | Port number | The TCP port the server is listening on    | 12345                               |

<br/>

The command-line arguments for the client are:
| Name(s)       | Option                    | Meaning                                        | Default value (if option not given)        |
|---------------|---------------------------|------------------------------------------------|--------------------------------------------|
| -v, --verbose |                           | Turn on verbose printing to help debugging     | False                                      |
| -s, --server  | Server name or IP address | The machine the server is running on           | 127.0.0.1 (i.e., localhost - this machine) |
| -p, --port    | Port number               | The TCP port the server is listening on        | 12345                                      |
| -n, --name    | A string                  | The name by which you are identified to others | Your machine name                          |