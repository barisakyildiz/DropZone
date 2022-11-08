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
            s.bind('', self.listen_port)
            s.listen(self.max_conn)
            print("[!] Initializing Socket...\n\
                   [!] Socket Binded Successfully.\n\
                   [!] Proxy Server Started Listening Port [{}]".format(self.listen_port))
        except Exception as e:
            print("An exception occured during initialization: {}".format(e))
            sys.exit(2)
        self.listen_port(s)
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
            first_line = data.split("\n")[0]
            url = first_line.split(" ")[1]
            http_pos = url.find("://")
            if http_pos == -1:
                temp = url
            else:
                temp = url[(http_pos + 3):]
            port_pos = temp.find(":")
            webserver_pos = temp.find("/")

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
                pass
        except:
            pass
        
    

def main():
    test = HTTPProxy(80, 8192, 5)
    test.conn_string(5, 5, 5)

if __name__ == '__main__':
    main()
