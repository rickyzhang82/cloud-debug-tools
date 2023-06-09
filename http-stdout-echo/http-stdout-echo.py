#!/usr/bin/env python3
'''Usage:
    python3 http-stdout-echo.py -a <bind-address> -p <bind-port>
   Examples:
    python3 http-stdout-echo.py # (will listen at 127.0.0.1:8080 by default)
    python3  http-stdout-echo.py -a 10.3.1.3 -p 5555'''

from http.server import HTTPServer, BaseHTTPRequestHandler


class DummyHTTPHandler(BaseHTTPRequestHandler):
    '''Simple HTTP server. Print to stdout every requests made to it.
    Useful for development or debbuging... At least for me!'''
    def __init__(self, request, client_address, server, read_from):
        if read_from != None:
            self.response = open(read_from).read()
        else:
            self.response = ''
        return super().__init__(request, client_address, server)

    def do_GET(self):
        print('### GET {} - {} - {}'.format(self.client_address, self.request_version, self.path))
        print('\n### Headers ###\n' + str(self.headers))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(self.response.encode('utf-8'))

    def do_POST(self):
        msg_length = int(self.headers['Content-Length'])
        print('### POST {} - {} - {}'.format(self.client_address, self.request_version, self.path))
        print('\n### Headers ###\n' + str(self.headers))
        print('\n### POST content ###\n{}'.format(self.rfile.read(msg_length)))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(self.response.encode('utf-8'))

    def do_OPTIONS(self):
        print('### OPTIONS {} - {} - {}'.format(self.client_address, self.request_version, self.path))
        print('\n### Headers ###\n' + str(self.headers))
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers')
        self.end_headers()
        self.wfile.write(self.response.encode('utf-8'))


if __name__ == '__main__':
    import argparse

    # Command line argument handling:
    parser = argparse.ArgumentParser(description='Dummy HTTP server. Prints everything to stdout')
    parser.add_argument('-a', '--address', help='default: 127.0.0.1')
    parser.add_argument('-p', '--port', help='default: 8080', type=int)
    parser.add_argument('-r', '--read_from', help='path to file to read and send as response', default=None, type=str)
    args = parser.parse_args()

    host = args.address or '127.0.0.1'
    port = args.port or 8080
    print(f'Starting http server {host} on port {port}')
    server = HTTPServer(
        (host, port),
        lambda request, client_address, server: DummyHTTPHandler(request, client_address, server, args.read_from),
    )

    server.serve_forever()