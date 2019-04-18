import socket

class HTTPClient(object):

	def __init__(self, server_ip="127.0.0.1", server_port=80):

		self.server_ip = server_ip
		self.server_port = server_port


	def server_connect(self):

		try:
			self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.server_socket.connect((self.server_ip, self.server_port))
		except ConnectionRefusedError:
			print("\n[-] Connection Establishment Error: Could not connect to "+ self.server_ip + ":" + str(self.server_port))
			return

		while 1:
			print("[" + self.server_ip + "]>")
			self.request = input().upper()
			if self.request == "EXIT": break
			print(self.request)
			self.server_socket.send(self.request.encode())
			self.response = self.server_socket.recv(65538)
			print(self.response)

		
		self.server_socket.close()




c  = HTTPClient()
c.server_connect()