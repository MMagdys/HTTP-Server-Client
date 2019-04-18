import argparse
from HTTPServer import HTTPServer


def main():


	parser = argparse.ArgumentParser(description = "HTTP Server")

	parser.add_argument("port_number", type = int, help = "Port Number for Server to listen on.\nDefault Port is 80", default=False)

	args = parser.parse_args()

	if args.port_number: 
		s = HTTPServer(args.port_number)
	else: 
		s = HTTPServer()
	s.start()
	

if __name__ == '__main__':
	main()
