import httpproxy
import argparse
import socket

def main():
    prsr = argparse.ArgumentParser(description="Auto-Defender by Barış Akyıldız",
                                   formatter_class=argparse.RawDescriptionHelpFormatter)
    prsr.add_argument("-i", "--ipaddress", help="The IP address of the machine that is going to be used in the modules")
    prsr.add_argument("-m", "--module", help="Desired module of the program to run:\n\
        (1) Add to Blacklist (Protect from Denial of Service attacks\n")
    args = prsr.parse_args()
    
    hostname = socket.gethostname()
    hostip = socket.gethostbyname(hostname)
    
if __name__ == '__main__':
    main()