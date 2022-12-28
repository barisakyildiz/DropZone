import subprocess

def addToBlacklist(ip):
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", str(ip), "-j", "DROP"])
    
def addToWhiteList(ip):
    subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", str(ip), "-j", "ACCEPT"])


def main():
    addToWhiteList("192.168.1.34")
    subprocess.run(["sudo", "iptables", "-L"])

if __name__ == '__main__':
    main()