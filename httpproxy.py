import socket
import sys
from threading import *

class HTTPProxy:
    def __init__(self, listen_port, buffer_size, max_conn):
        self.listen_port = listen_port
        self.buffer_size = buffer_size
        self.max_conn = max_conn
    
    def initSocket(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind(('', self.listen_port))
            s.listen(self.max_conn)
            print("[!] Initializing Socket...\n\
            [!] Socket Binded Successfully.\n\
            [!] Proxy Server Started Listening Port [{}]".format(self.listen_port))
        except Exception as e:
            print("An exception occured during initialization: {}".format(e))
            sys.exit(2)
        self.listenOnPort(s)
        s.close()
    
    def listenOnPort(self, sock):
        while True:
            try:
                conn, adrr = sock.accept()
                data = conn.recv(self.buffer_size)
                t = Thread(target = self.conn_string, args=(conn, data, adrr))
                t.run()
            except KeyboardInterrupt:
                sock.close()
                print("\n Shutting down the server...")
                sys.exit(1)
    
    def conn_string(self, conn, data, adrr):
        try:
            first_line = data.split(b"\n")
            first_line = first_line[0]
            url = first_line.split(b" ")[1]
            http_pos = url.find(b"://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos + 3):]
            port_pos = temp.find(b":")
            webserver_pos = temp.find(b"/")
            if webserver_pos == -1:
                webserver_pos = len(temp)
            webserver = ""
            port = -1

            if port_pos == -1 or webserver_pos < port_pos:
                port = 80
                webserver= temp[:webserver_pos]
            else:
                port = int(temp[(port_pos + 1):][:webserver_pos - port_pos - 1])
                webserver = temp[:port_pos]
            print(webserver)
            self.proxy_server(webserver, port, conn, data, adrr)
        except Exception as e:
            print("An exception occured during process: {}".format(e))
        
    def proxy_server(self, webserver, port, conn, data, adrr):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((webserver, port))
            s.send(data)
            
            while True:
                reply = s.recv(self.buffer_size)
                if len(reply) > 0:
                    conn.send(reply)
                    dar = float(len(reply))
                    dar = float(dar / 1024)
                    dar = "{}.3s".format(dar)
                    print("[!] Request Done: {} => {} <= {}".format(adrr[0], dar, webserver))
                else:
                    break
            s.close()
            conn.close()
        except socket.error as e:
            s.close()
            conn.close()
            sys.exit(1)
        
    

def main():
    test = HTTPProxy(80, 8192, 5)
    test.conn_string(5, 5, 5)

if __name__ == '__main__':
    main()
