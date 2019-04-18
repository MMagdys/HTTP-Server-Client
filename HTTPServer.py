import socket
import re
import threading, select



class HTTPServer(object):

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
			threading.Thread(target=self.http_parser, args=(conn, addr,)).start()
			


	def http_parser(self, conn, addr):

		inout = [conn]
		try:
			request = conn.recv(65538)

		except socket.timeout as e:
			print("\n[-] Connection Timeout.")
			protocol = ""
			return
		
		request = request.decode("utf-8").split("\r\n")
		# print(request)
		# Handling lost packets
		try:
			method, page, protocol = request[0].split()
		except ValueError:
			return
		
		# print(method)
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

			# recieving the FIle
			encode_file = conn.recv(65538)
			while 1:
				infds, outfds, errfds = select.select(inout, inout, [], 1)
				print(len(infds), len(outfds))

				if len(infds) != 0:
					encode_file += conn.recv(65538)
				else:
					break
			
			# FIle multi/part form-data decoding
			boundry = encode_file.decode("utf-8").split("\r\n")[0]
			form_fields = encode_file.decode("utf-8").split(boundry)
		
			for field in form_fields:

				data = field.split("\r\n")
				if len(data) > 3:
					# print(data)
					try:
						filename = re.search('filename="(.*)"', data[1]).group(1)

					except AttributeError:
						filename = re.search('name="(.*)"', data[1]).group(1)

					if data[2]: body = '\n'.join(data[4:])
					else: body = '\n'.join(data[3:])
					with open("public/uploads/"+filename, "w")as fb:
						fb.write(body)
					fb.close()
					conn.sendall(b"HTTP/1.0 200 OK\r\n\nUploaded Sucessfully!")


		if protocol == "HTTP/1.1":
			conn.settimeout(3)
			self.http_parser(conn, addr)
		conn.close()
		print("CONN CLOSED")
		
