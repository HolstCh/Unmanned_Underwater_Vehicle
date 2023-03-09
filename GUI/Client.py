import socket

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the server's address and port
print(socket.gethostbyname("raspberrypi.local"))
server_address = (socket.gethostbyname("raspberrypi.local"), 5000)
client_socket.connect(server_address)

try:
    # Send data
    message = 'Hello, world!'
    print('Sending {!r}'.format(message))
    client_socket.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)

    while amount_received < amount_expected:
        data = client_socket.recv(1024)
        amount_received += len(data)
        print('Received {!r}'.format(data.decode()))

finally:
    # Clean up the connection
    client_socket.close()