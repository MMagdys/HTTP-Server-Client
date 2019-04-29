import socket
import select


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
				self.inout = [self.server_socket]
			except ConnectionRefusedError:
				print("\n[-] Connection Establishment Error: Could not connect to "+ self.server_ip + ":" + str(self.server_port))
				return

			for i in range(2, len(self.request_lst)): self.request_lst[i] = self.request_lst[i].upper() 

			if self.request_lst[0] == "GET":

				if len(self.request_lst) == 2:
					self.request_lst.append("HTTP/1.0")
				
				self.request = " ".join(self.request_lst)
				self.server_socket.send(self.request.encode())
				self.response = self.server_socket.recv(65538)
				
				# while 1:
				# 	infds, outfds, errfds = select.select(self.inout, self.inout, [], 1)
				# 	print(len(infds), len(outfds))

				# 	if len(infds) != 0:
				# 		self.response += self.server_socket.recv(65538)
				# 	else:
				# 		break
				self.response = self.response.split(b'\r\n\n',1)
				with open("downloads/" + self.request_lst[1], "wb")as self.f:
					self.f.write(self.response[1])
				self.f.close()
				print(self.response[0])


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

