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
			file_len = int(request[3].split(":")[1])
			encode_file = conn.recv(file_len)
			

			print(encode_file)

			try:
				# TXT File decoding
				data = encode_file.decode("utf-8").split("\r\n")
				filename = re.search('filename="(.*)"', data[1]).group(1)
				body = '\n'.join(encode_file.decode("utf-8").split("\r\n")[4:-6])
				fb = open("public/uploads/"+filename, "w")
				fb.write(body)
				fb.close()
				conn.sendall(b"HTTP/1.0 200 OK\r\n\nUploaded Sucessfully!")

			except UnicodeDecodeError:

				# print(encode_file)
				# body = base64.b64decode(encode_file)
				# print(base64.b64decode(encode_file).split(base64.b64encode("\r\n")))
				fb = open("file", "w")
				fb.write(str(encode_file))
				fb.close()


			# base64.b64encode(encode_file)
			# encode_file = encode_file.body.decode('base64')
			# print(encode_file)
			# 
			
			# encode_file.save()
			# f = decoder.MultipartDecoder.from_response(encode_file)
			# print(f)
			
			# print(f)

			# form = cgi.FieldStorage(encode_file)
			# print("+++++++++++++++++++++++++++")
			# print(form)
			# print(request[-1].split("&"))

			


s = HttpServer()
s.start()