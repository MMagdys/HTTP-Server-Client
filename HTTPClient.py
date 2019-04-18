import socket

class HTTPClient(object):

	def __init__(self, server_ip="127.0.0.1", server_port=80):

		self.server_ip = server_ip
		self.server_port = server_port


	def server_connect(self):

		while 1:
			print("[" + self.server_ip + "]> ", end='')
			self.request = input()
			self.request_lst = self.request.split()
			self.request_lst[0] = self.request_lst[0].upper()

			if self.request_lst[0] == "EXIT": 
				self.server_socket.close()
				break
			# print(self.request)


			try:
				self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.server_socket.connect((self.server_ip, self.server_port))
			except ConnectionRefusedError:
				print("\n[-] Connection Establishment Error: Could not connect to "+ self.server_ip + ":" + str(self.server_port))
				return


			if self.request_lst[0] == "GET":
				self.request = self.request.upper()
				self.server_socket.send(self.request.encode())
				self.response = self.server_socket.recv(65538)
				print(self.response)


			elif self.request_lst[0] == "POST":
				try:
					with open(self.request_lst[1], "rb")as self.f:
						self.data = self.f.read()
					self.f.close()
					# print(self.data)

					from requests.packages.urllib3.filepost import encode_multipart_formdata
					(content, header) = encode_multipart_formdata([(self.request_lst[1], self.data)])
					# print(content)
					# print(header)
					
					self.request = self.request.upper()
					self.request += "\r\n"
					self.request_array = bytearray()
					self.request_array.extend(self.request.upper().encode())
					self.request_array.extend(header.encode())
					self.server_socket.sendall(self.request_array)
					self.server_socket.sendall(content)
					self.response = self.server_socket.recv(65538)
					print("[*] "+self.response.decode())



				except FileNotFoundError:
					print("[-] File Not Found.")
					


			else:
				print("[-] Unsporrted Request!")


		print("[-] Connection Closed")

