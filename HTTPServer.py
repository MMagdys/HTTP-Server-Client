import socket
import re
from requests_toolbelt.multipart import decoder
import cgi
import requests
import base64

class HttpServer(object):

	def __init__(self, port=80, ip_addr="127.0.0.1"):
		self.addr = ip_addr
		self.port = port


	def start(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((self.addr, self.port))
		self.server.listen()


		while 1:
			conn, addr = self.server.accept()
			print(conn, addr)
			self.http_parser(conn, addr)
			conn.close()
			print("CONN CLOSED")


	def http_parser(self, conn, addr):

		request = conn.recv(65538)
		request = request.decode("utf-8").split("\r\n")
		print(request)
		# Handling lost packets
		try:
			method, page, protocol = request[0].split()
		except ValueError:
			return
		
		print(method)
		if method == "GET":
			if page[-1] == "/": page += "index.html"
			try:
				with open("public"+page, "rb")as p:
					data = p.read()
				p.close()
				conn.sendall(b"HTTP/1.0 200 OK\r\n\n"+data)

			except FileNotFoundError:
				conn.sendall(b"HTTP/1.0 404 Not Found\r\n\nPage Not Found")

		elif method == "POST":
			encode_file = conn.recv(65538)
			

			# print(encode_file)
			# print("==============")
			boundry = encode_file.decode("utf-8").split("\r\n")[0]
			form_fields = encode_file.decode("utf-8").split(boundry)
			# print(boundry)
			# print("----------------")
			# print(form_fields)

			for field in form_fields:

				data = field.split("\r\n")
				if len(data) > 3:
					print(data)

					try:
						filename = re.search('filename="(.*)"', data[1]).group(1)

					except AttributeError:
						filename = re.search('name="(.*)"', data[1]).group(1)

					if data[2]: body = '\n'.join(data[4:])
					else: body = '\n'.join(data[3:])
					fb = open("public/uploads/"+filename, "w")
					fb.write(body)
					fb.close()
					conn.sendall(b"HTTP/1.0 200 OK\r\n\nUploaded Sucessfully!")


		

s = HttpServer()
s.start()