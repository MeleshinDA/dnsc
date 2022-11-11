import socket
import pickle

from Cache import Cache
from DNS.DNSMessageHandler import MessageHandler


class Server:
    def __init__(self, local_ip, remote_ip, port):
        self.remote_ip = remote_ip
        self.local_ip = local_ip
        self.port = port

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((self.local_ip, self.port))
        cache = Cache()
        while True:
            try:
                # Query
                data, address = server.recvfrom(512)
                message_handler = MessageHandler(data)
                data_from_cache = cache.get_from_cache((message_handler.question.qname, message_handler.question.qtype))

                if data_from_cache:
                    print("Данные получены из кэша: ")
                    data_from_cache.print_parsed_answer()
                    data_to_send = data_from_cache.raw_data
                    try:
                        server.sendto(data_to_send, address)
                    except OSError:
                        continue
                else:
                    print("Данные получены от сервера")

                    auth_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    auth_server.sendto(data, (self.remote_ip, self.port))

                    dns_data, rem_address = auth_server.recvfrom(512)
                    message_handler = MessageHandler(dns_data)
                    message_handler.answer.print_parsed_answer()

                    server.sendto(dns_data, address)
                    cache.add_to_cache(message_handler.answer.aname, message_handler.question.qtype,
                                       message_handler.answer)

            except KeyboardInterrupt:
                break
            finally:
                cache.save()
