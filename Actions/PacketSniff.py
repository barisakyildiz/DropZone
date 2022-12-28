import socket
import struct
from binascii import hexlify
from textwrap import wrap
from time import time
import IPTables

class PacketSniffer:
    def __init__(self):
        self.TAB_1 = "\t - "
        self.TAB_2 = "\t\t - "
        self.TAB_3 = "\t\t\t - "
        self.TAB_4 = "\t\t\t\t - "
        self.MAX_PACKET_PER_5SECS = 5000

    def getIp(self, address):
        return '.'.join(map(str, address))
    
    def initSocket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        total_time = 0
        dict_of_ips = {}
        while True:
            start = time()
            raw_data, addr= s.recvfrom(65565) #65565
            print("raw_data: {}     addr: {}     sizeof: {}\n\n".format(raw_data, addr, len(raw_data)))
            ipv4_head = self.ipv4Head(raw_data=raw_data)
            print(self.TAB_1 + 'IPv4 Packet Results:')
            print(self.TAB_2 + 'Version: {}, Header Length: {}, TTL: {}'.format(ipv4_head[0], ipv4_head[1], ipv4_head[2]))
            print(self.TAB_2 + 'Protocol: {}, Source: {}, Target: {}\n\n\n'.format(ipv4_head[3], ipv4_head[4], ipv4_head[5]))
            if ipv4_head[3] == 6:
                tcp = self.tcpHead(ipv4_head[6])
                print(self.TAB_1 + 'TCP Segment Results:')
                print(self.TAB_1 + 'Source Port: {}, Destination Port: {}'.format(tcp[0], tcp[1]))
                print(self.TAB_2 + 'Sequence: {}, Acknowledgement: {}'.format(tcp[2], tcp[3]))
                print(self.TAB_2 + 'Flags:')
                print(self.TAB_3 + 'URG: {}, ACK: {}, PSH: {}'.format(tcp[4], tcp[5], tcp[6]))
                print(self.TAB_3 + 'RST: {}, SYN: {}, FIN: {}'.format(tcp[7], tcp[8], tcp[9]))
                try:
                    dict_of_ips[str(addr[0])] = dict_of_ips[str(addr[0])] + 1
                except Exception as e:
                    print("Adding new ip to the tracking list...")
                    dict_of_ips[str(addr[0])] = 1
                if len(tcp[10]) > 0:
                    #HTTP REQUEST
                    if tcp[1] == 80 or tcp[1] == 443:
                        print(self.TAB_3+ 'HTTP Data:')
                    else:
                        print(self.TAB_2 + 'TCP Data:')
                        print(self.TAB_3 + str(tcp[10]))
            stop = time()
            total_time += stop - start
            if total_time <= 5 and dict_of_ips[str(addr[0])] >= self.MAX_PACKET_PER_5SECS:
                IPTables.addToBlacklist() #solve this
            if total_time > 5:
                dict_of_ips = {}
            print(total_time)
            print(dict_of_ips)
            

    def ethernetHead(self, raw_data): #Parsing the Ethernet Frames
        destination, source, prototype = struct.unpack("!6s6sH", raw_data[:14])
        destination_mac = str(hexlify(destination)); destination_mac = destination_mac[2:14]
        dest_list = wrap(destination_mac, 2)
        destination_mac = ":".join(dest_list)
        source_mac = str(hexlify(source)); source_mac = source_mac[2:14]
        src_list = wrap(source_mac, 2)
        source_mac = ":".join(src_list)
        proto = socket.htons(prototype)
        data = raw_data[14:]
        return destination, source, proto, data
    
    def ipv4Head(self, raw_data): #For parsing the IP Headers
        version_header_len = raw_data[0]
        version = version_header_len >> 4
        header_length = (version_header_len & 15) * 4
        timetolive, protocol, source, target = struct.unpack('! 8x B B 2x 4s 4s', raw_data[:20])
        data = raw_data[header_length:]
        source = self.getIp(source); target = self.getIp(target)
        return version, header_length, timetolive, protocol, source, target, data

    def tcpHead(self, raw_data):
        source_port, destination_port, sequence, acknowledgement, offset_reserved_flags = struct.unpack('! H H L L H', raw_data[:14])
        offset = (offset_reserved_flags >> 12) * 4
        flag_urg = (offset_reserved_flags & 32) >> 5
        flag_ack = (offset_reserved_flags & 16) >> 4
        flag_psh = (offset_reserved_flags & 8) >> 3
        flag_rst = (offset_reserved_flags & 4) >> 2
        flag_syn = (offset_reserved_flags & 2) >> 1
        flag_fin = offset_reserved_flags & 1
        data = raw_data[offset:]
        return source_port, destination_port, sequence, acknowledgement, flag_urg, flag_ack, flag_psh, flag_rst, flag_syn, flag_fin, data



def main():
    sniffer = PacketSniffer()
    sniffer.initSocket()

if __name__ == '__main__':
    main()