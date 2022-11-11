

class Header:
    def __init__(self, data):
        self.header = data
        self.trans_id = self.header[:4]
        self.flags = self.__parse_flags()

        self.qdcount = self.header[8:12]
        self.ancount = self.header[12:16]
        self.nscount = self.header[16:20]
        self.arcount = self.header[20:24]

    def __parse_flags(self):
        flags = self.header[4:8]
        sum = 0
        for i in range(len(flags)):
            sum += int(flags[i]) * (16 ** (len(flags) - (i + 1)))
        return '0' * (16 - len(str(bin(sum))[2:])) + str(bin(sum))[2:]

    def __normalize_data(self, data):
        counter = 0
        normalized = ''

        for byte in data:
            if counter == 2:
                counter = 0
                normalized += ' '
            normalized += byte

            counter += 1
        return normalized.split(' ')