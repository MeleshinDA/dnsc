Кэширующий DNS сервер

Запуск:
1) Открыть cmd/powershell для запросов
[!image](https://github.com/MeleshinDA/dnsc/blob/master/Guide/1.png)
2) Открыть cmd/powershell для сервера и запустить там скрипт командой py main.py
[!image](https://github.com/MeleshinDA/dnsc/blob/master/Guide/2.png)
[!image](https://github.com/MeleshinDA/dnsc/blob/master/Guide/3.png)
4) В запросе ввести команду типа: nslookup -type=[a, aaaa, ns, ...] [google.com, ...] 127.0.0.1
5) В консоли для сервера будет выведена информация соответствующая типу запроса
6) В консоли с запросом будет выведено меньше информации
[!image](https://github.com/MeleshinDA/dnsc/blob/master/Guide/4.png)
