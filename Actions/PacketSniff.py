import socket
import struct
from binascii import hexlify
from textwrap import wrap

class PacketSniffer:
    def __init__(self):
        pass

    def getIp(address):
        return '.'.join(map(str, address))
    
    def initSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        while True:
            raw_data, addr = s.recvfrom(65535) #65565
            dest, src, proto, data = self.ethernetHead(raw_data=raw_data)
            print("--- Ethernet Frame Results --- \nDestination {}, Source: {}\nData: {}\nProtocol: {}\n\n\n".format(dest, src, data, proto))
            if proto == 8:
                ipv4_head = self.ipv4Head(data)
                print('\t - ' + 'IPv4 Packet Results:')
                print('\t\t - ' + 'Version: {}, Header Length: {}, TTL: {}'.format(ipv4_head[0], ipv4_head[1], ipv4_head[2]))
                print('\t\t - ' + 'Protocol: {}, Source: {}, Target: {}'.format(ipv4_head[3], ipv4_head[4], ipv4_head[5]))

    def ethernetHead(self, raw_data): #Parsing the Ethernet Frames
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
    
    def ipv4Head(self, raw_data): #For parsing the IP Headers
        version_header_len = raw_data[0]
        version = version_header_len >> 4
        header_length = (version_header_len & 15) * 4
        timetolive, protocol, source, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        data = raw_data[header_length:]
        source = self.getIp(source); target = self.getIp(target)
        return version, header_length, timetolive, protocol, source, target, data



def main():
    sniffer = PacketSniffer()
    sniffer.initSocket()

if __name__ == '__main__':
    main()