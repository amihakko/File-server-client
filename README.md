# File server-client
A server that provides an API for managing files and client for communicating with a server and managing files on it.

### Dependencies 
Python version 3.8 or higher

### Arguments of server:
    ip - server IP address
    port - Server port
    queue_size - Number of allowed incoming connection queue

### Arguments that can be entered when starting the client:
         ip - server IP address
         port - Server port
         action - Desired request:
                         1) Upload file to server
                         2) Download file from server
                         3) Copy the file within the server
                         4) Move the file within the server
                         5) Delete the file on the server
         path1 - Full path to the input file
         path2 - Full path to the output file

To use that node PyTorch +1.7 should be there with CUDA +11.0.

### Run Server
~~~
server.py --ip 127.0.0.1 --port 49322 --queue_size 5
~~~
### Run Client
~~~
client.py --ip 127.0.0.1 --port 49322 --action 2 --path1 File_on_server --path2 Path_to_save_file_on_you_system
~~~