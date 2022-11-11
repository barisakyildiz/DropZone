import socket
import struct
import sys
from binascii import hexlify
from textwrap import wrap

class PacketSniffer:
    def __init__(self):
        pass
    
    def initSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        while True:
            raw_data, addr = s.recvfrom(65535) #65565
            dest, src, proto, data = self.ethernetHead(raw_data=raw_data)
            print(dest + src, proto, data)
    def ethernetHead(self, raw_data):
        destination, source, prototype = struct.unpack('! 6s 6s H', raw_data[:14])
        destination_mac = str(hexlify(destination)); destination_mac = destination_mac[2:14]
        dest_list = wrap(destination_mac, 2)
        destination_mac = ":".join(dest_list)
        source_mac = str(hexlify(source)); source_mac = source_mac[2:14]
        src_list = wrap(source_mac, 2)
        source_mac = ":".join(src_list)
        proto = socket.htons(prototype)
        data = raw_data[14:]
        return destination_mac, source_mac, proto, data


def main():
    sniffer = PacketSniffer()
    sniffer.initSocket()

if __name__ == '__main__':
    main()