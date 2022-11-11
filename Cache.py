import pickle
import time

class Cache:
    def __init__(self):
        self.cache = dict()
        try:
            with open('cache.txt', 'rb') as file:
                self.cache = pickle.load(file)
                updated_cache = dict()
                for key in self.cache.keys():
                    fresh_cache_data = self.__get_cache_without_outdated(self.cache[key])
                    if fresh_cache_data:
                        updated_cache[key] = (fresh_cache_data, self.cache[key][1])
                self.cache = updated_cache.copy()

                a = 0
        except IOError:
            with open('cache.txt', 'w') as file:
                print("Кэш создан")
        except EOFError:
            print("Кэш пуст")

    def save(self):
        with open('cache.txt', 'wb') as file:
            pickle.dump(self.cache, file)

    def add_to_cache(self, name, atype, data):
        self.cache[(name, atype)] = (data, time.time())
        self.save()

    def get_from_cache(self, key):
        if key in self.cache:
            return self.__get_cache_without_outdated(self.cache[key])
        return None

    def __get_cache_without_outdated(self, cached):
        outdated = []
        for i in range(len(cached[0].parsed_answer)):
            cur_time = time.time()
            ttl = cached[0].parsed_answer[i]["TTL"]
            time_to_erase = ttl + cached[1]
            if time_to_erase < cur_time:
                outdated.append(i)
        outdated.sort(reverse=True)
        for i in outdated:
            cached[0].parsed_answer.pop(i)
        return cached[0]

    '''
    1) Посмотреть как там кэшируется всё - проблема с ns почему-то удаляет 3 записи, хотя ttl большой
    2) Не отправляются на сервер данные
    '''