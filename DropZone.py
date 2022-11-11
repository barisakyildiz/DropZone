import httpproxy

def main():
    proxy = httpproxy.HTTPProxy(4444, 8192, 5)
    proxy.initSocket()

if __name__ == '__main__':
    main()