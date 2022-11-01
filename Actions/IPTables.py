import os
import sys
import subprocess

class IPTables:
    def __init__(self):
        pass

    def addToBlacklist(self, ip):
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", str(ip), "-j", "DROP"])
    
    def addToWhiteList(self, ip):
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", str(ip), "-j", "ACCEPT"])


def main():
    iptables = IPTables()
    iptables.addToWhiteList("192.168.1.34")
    subprocess.run(["sudo", "iptables", "-L"])
    
if __name__ == '__main__':
    main()