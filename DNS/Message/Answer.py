class Answer:
    def __init__(self, raw_data, data, offset, qtype):
        self.parsed_answer = []
        self.borders = {
            1: 2,
            2: 8,
            28: 4
        }
        self.qtype = qtype
        self.res = []
        self.raw_data = raw_data
        self.all_data = data
        name, self.offset = self.__parse_name(offset + 24)
        self.aname = name[:-1]
        self.__parse_other_data(self.offset)
#
        self.parsed_rdata = []
        if self.offset + self.rdlength_octs >= len(self.all_data) and self.rdlength_octs > 8:
            self.rdata = self.all_data[self.offset:self.offset + self.rdlength_octs]
            self.parsed_rdata = self.__parse_name(self.offset)[0]
            self.__pack_answer()
        else:
            self.__parse_records()
        b = 0

    def print_parsed_answer(self):
        for record in self.parsed_answer:
            for key, value in record.items():
                print(key, ': ', value, end=', ')
            print()

    def __pack_answer(self):
        self.record = {
            "Name": self.aname,
            "Type": self.atype,
            "Class": self.aclass,
            "TTL": int(self.ttl, 16),
            "Rdlength": str(int(self.rdlength, 16)),
            "Data": self.parsed_rdata
        }
        self.parsed_answer.append(self.record)
        a = 0
    # '0001818300010000000100000131013001300331323707696e2d61646472046172706100000c0001c016 0006 0001 00000489 0038 01620f696e2d616464722d73657276657273c01e056e73746c640469616e61036f7267007886a6af000007080000038400093a8000000e10'
    # '000281800001000100000000 06676f6f676c65 03636f6d 00 0001 0001 c00c 0001 0001 00000065 0004 d83ad1ce'
    def __parse_other_data(self, offset):

        self.atype = self.all_data[offset:offset + 4]
        self.aclass = self.all_data[offset + 4:offset + 8]
        self.ttl = self.all_data[offset + 8:offset + 16]
        self.rdlength = self.all_data[offset + 16:offset + 20]
        self.rdlength_octs = 2 * int(self.rdlength, 16)
        self.offset += 20

    # '00028180000100010000000006676f6f676c6503636f6d0000010001c00c00010001000000bf00048efa4a8e'
    def __parse_name(self, left_border):
        result = ''
        while True:
            cur_label = self.all_data[left_border: left_border + 2]

            if cur_label == '':
                return result, left_border
            if int(cur_label, 16) == 0:
                return result, left_border

            left_border += 2
            cur_label_bin = str(bin(int(cur_label, 16)))[2:]
            сur_label_bin_total = '0' * (8 - len(cur_label_bin)) + cur_label_bin
            cur_label_from_hex = 2 * int(cur_label, 16)
            if сur_label_bin_total[:2] == '11':
                link = 2 * int(cur_label_bin[4:] + str(bin(int(self.all_data[left_border:left_border + 2], 16)))[2:], 2)
                left_border += 2
                result += self.__parse_name(link)[0]
            elif cur_label_from_hex + left_border > len(self.all_data):
                result += self.__parse_for_type(self.borders[int(self.qtype, 16)])
                return result, left_border
            else:
                cur_data = self.all_data[left_border:left_border + cur_label_from_hex]
                part = bytes.fromhex(hex(int(cur_data, 16))[2:]).decode('ASCII') + '.'
                result += part
                left_border += cur_label_from_hex
#'000181830001000000010000 0131 0130 0130 03313237 07696e2d61646472 0461727061 00 000c 0001 c016 0006 0001 00000226 0038 01620f696e2d616464722d73657276657273c01e056e73746c640469616e61036f7267007886a6af000007080000038400093a8000000e10'
    def __parse_records(self):
        f = 0
        ttype = int(self.qtype, 16)
        match ttype:
            case 1:
                f = lambda: self.__parse_for_type(2)  # заменить на self.atype
            case 2:
                f = lambda: self.__parse_name(self.offset)
            case 28:
                f = lambda: self.__parse_for_type(4)
            case _:
                print("Неизвестный тип запроса")
                return

        self.__parse_rdata(f)

    def __parse_rdata(self, action):
        while self.offset < len(self.all_data):
            self.rdata = self.all_data[self.offset:self.offset + self.rdlength_octs]
            self.parsed_rdata = action()
            if int(self.qtype, 16) == 2:
                self.parsed_rdata = self.parsed_rdata[0]
                splited = self.parsed_rdata.split('.')
                self.parsed_rdata = 'Nameserver = ' + '.'.join(splited[:3])
            self.__pack_answer()
            self.offset += self.rdlength_octs
            if self.offset >= len(self.all_data):
                break
            self.name, self.offset = self.__parse_name(self.offset)
            self.__parse_other_data(self.offset)


    def __parse_for_type(self, border):
        tmp = ''
        res = ''
        for i in range(len(self.rdata) + 1):
            if i % border == 0 and i != 0:
                if int(self.qtype, 16) == 28:
                    res += tmp + ':'
                else:
                    res += str(int(tmp, 16)) + '.'
                tmp = ''
            if i == len(self.rdata):
                break
            tmp += self.rdata[i]

        return res[:-1]  # '2a00145040100c020000000000000066'

    def pack_data(self):
        return
