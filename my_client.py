import argparse
from HTTPClient import HTTPClient


def main():


	parser = argparse.ArgumentParser(description = "HTTP Client")

	parser.add_argument("server_ip", type = str, help = "IP addr for Server to connect.\nDefault IP is 127.0.0.1")
	parser.add_argument("server_port", type = int, help = "Port Number for Server to connect.\nDefault Port is 80")


	args = parser.parse_args()

	c  = HTTPClient(args.server_ip, args.server_port)
	c.server_connect()
	

if __name__ == '__main__':
	main()
