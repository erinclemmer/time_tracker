import os
import sys
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

# TODO
# Add auto backup capability, only hold 30 days of data and create new files for each month
# // GET / returns current months data
# Every day the old data is added to the month backup
# // POST /add-activity adds a new line of data to the csv
# POST /remove-activity removes a line of data from current month that matches it's exact start date

config = {}
if not os.path.exists('config.json'):
    raise Exception('config.json not found')

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.loads(f.read())

current_file = 'activities.csv'

def sync_activities(row: str):
    with open(current_file, 'w', encoding='utf-8') as f:
            f.write(row + '\n')

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        ret_data = ''
        if os.path.exists(current_file):
            with open(current_file, 'r', encoding='utf-8') as f:
                    ret_data = f.read()
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(ret_data.encode())

    def do_POST(self):
        err = False
        ret_data = 'blank'
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = json.loads(self.rfile.read(content_length).decode('utf-8'))
            if post_data['password'] != config['password']:
                ret_data = 'Unauthorized'
                raise Exception('Unauthorized')
            if self.path == '/sync':
                ret_data = 'synced'
                sync_activities(post_data['data'])
        except Exception as e:
            err = True
            print(e)
        finally:
            self.send_response(200 if not err else 401)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(ret_data.encode())

def run_server(port):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

run_server(config['server_port'])
