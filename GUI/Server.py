import socket

# Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_address = ('0.0.0.0', 5000)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server is listening on {}:{}'.format(*server_address))

    while True:
        # Wait for a connection
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()
        try:
            print('Connection from', client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                data = connection.recv(1024)
                print('Received {!r}'.format(data))
                if data:
                    print('Sending data back to the client')
                    connection.sendall(data)
                else:
                    print('No more data from', client_address)
                    break

        finally:
            # Clean up the connection
            connection.close()