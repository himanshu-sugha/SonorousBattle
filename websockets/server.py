# import socket

# server = socket.socket()

# server.bind(( 'localhost' ,9999))

# server.listen(1)
# print('waiting for connection')

# while True:
#     c,address=server.accept()
#     name=c.recv(1024).decode()
#     print("Connected With",address,name)
#     c.send(bytes("Connection Established",'utf-8'))
#     c.close()

