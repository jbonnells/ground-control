# Ref for UDP: https://wiki.python.org/moin/UdpCommunication
# Ref for serializing: https://www.geeksforgeeks.org/python-convert-string-to-bytes/

import socket as _socket

# The target machine IP and port
ip = '127.0.0.1'
port = 4000

socket = _socket.socket(_socket.AF_INET, # Internet family
                        _socket.SOCK_DGRAM) # UDP
socket.settimeout(1)

def send(message: str):
    """Send the given message string"""
    socket.sendto(message.encode(), (ip, port))

def receive():
    """Wait until a message is received, then return it"""
    data, addr = socket.recvfrom(64)
    assert addr == (ip, port), f"Message from unknown sender: {addr}"
    msg = data.decode()
    return msg

def shutdown():
    """Handle cleanup and closing"""
    socket.close()
    print(f"\nClosed socket")
