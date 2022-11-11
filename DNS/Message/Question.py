class Question:
    def __init__(self, data):
        self.data = data
        self.qname, self.offset = self.__parse__domain()
        self.qtype = self.data[self.offset:self.offset+4]
        self.qclass = self.data[self.offset+4:self.offset+8]
        self.offset += 8

    def __parse__domain(self):
        result = ''
        left_border = 0
        while True:
            count = 2 * int(self.data[left_border:left_border + 2])
            left_border += 2
            if count == 0:
                return result[:-1], left_border

            cur_data = self.data[left_border:left_border + count]
            part = bytes.fromhex(hex(int(cur_data, 16))[2:]).decode('ASCII') + '.'
            result += part
            left_border += count
            # 0131013001300331323707696e2d61646472046172706100000c0001
