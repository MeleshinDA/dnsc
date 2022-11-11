from DNS.DNSServer import Server


def main():
    Server('127.0.0.1', '8.8.8.8', 53).run()


if __name__ == '__main__':
    main()
