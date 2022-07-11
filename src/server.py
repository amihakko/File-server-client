#!/usr/bin/python3
import socket
import sys
import os
import time
import argparse
import shutil
import _thread as thread    # TODO: Добавить многопоточность и возможность работы параллельно с несколькими клиентами

'''
    Сервер, обеспечивающий API для управления файлами.
    Аргументы:
        ip          -   IP-адрес сервера
        port        -   Порт сервера
        queue_size  -   Кол-во допустимой очереди входящих подключений
    
    Разработчик - Амиран Беркаев (berkaevamiran@mail.ru)
'''

def parser_args():
    parser = argparse.ArgumentParser(description='Server for working with file system on a Linux')
    parser.add_argument('--ip','-i', type=str, default='127.0.0.1', help='IP address of server')
    parser.add_argument('--port','-p', type=int, default='49322', help='Port number of server')
    parser.add_argument('--queue_size','-q', type=int, default='1', help='Incoming connection queue size')
    
    my_namespace = parser.parse_args()
    return my_namespace

# Функция чтения файла удаленно (сервер - клиент)
def read(path, client_sock):
    try:
        with open(path, 'rb') as file_to_send:
            for data in file_to_send:
                client_sock.sendall(data)
        client_sock.close()
    except:
        print("File doesn't exist!")
    
# Функция записи данных в файл удаленно (сервер - клиент)   
def write(path, client_sock):
    with open(os.path.join(path), 'wb') as file_to_write:
        while True:
            data = client_sock.recv(1024)
            if not data:
                break
            file_to_write.write(data)
        file_to_write.close()
    client_sock.close()
    
# Основная функция, отвечающая за поведение сервера
def server(ip, port, num_listen):
    # Интернет-протокол IPv4 - AF_INET, Интернет-протокол IPv6 - AF_INET6, 
    # Протокол TCP - SOCK_STREAM, Протокол UDP - SOCK_DGRAM
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
    serv_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Для переиспользования IP и Порта
    serv_sock.bind((ip, port))
    serv_sock.listen(num_listen)

    
    while True:
        # Обрабатываем входящие подключения в цикле
        client_sock, client_addr = serv_sock.accept()
        print(f'Connected by {client_addr} at {time.asctime()}')
        
        action, path1, path2 = client_sock.recv(1024).decode().split()
        # print(action)
        action = int(action)
        
        if action == 1:   # Запись файла на сервер     
            write(path2, client_sock)
        elif action == 2: # Загрузка файла с сервера           
            read(path1, client_sock)
        elif action == 3: # Копирование файла на сервере
            shutil.copy(path1, path2)
        elif action == 4: # Перемещение файла на сервере
            shutil.move(path1, path2)
        elif action == 5: # Удаление файла на сервере
            if path2 == 'yes':
                if os.path.exists(path1): 
                    os.remove(path1)
                else:
                    print("File doesn't exists!")
            else:
                print('Incorrect confirmation!')
                pass
        else:
            pass

            
if __name__ == '__main__':
    args = parser_args()
    print(f'Server starts with IP: {args.ip} and Port: {args.port}')
    try:
        server(args.ip, args.port, args.queue_size)
    except KeyboardInterrupt:
        print('\nInterrupted by keyboard!')
        try:
            socket.close()
            sys.exit(0)
        except SystemExit:
            socket.close()
            os._exit(0)
