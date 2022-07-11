#!/usr/bin/python3
import socket
import sys
import os
import argparse

'''
    Клиент для обмена данными с сервером и управления файлами на нём.
    Аргументы, которые можно вводить при запуске клиента:
        ip      -   IP-адрес сервера
        port    -   Порт сервера
        action  -   Желаемый запрос:
                        1) Передать файл на сервер
                        2) Загрузить файл с сервера
                        3) Скопировать файл в пределах сервера
                        4) Переместить файл в пределах сервера
                        5) Удалить файл на сервере
        path1   -   Полный путь к входному файлу
        path2   -   Полный путь к выходному файлу
        
    Разработчик - Амиран Беркаев (berkaevamiran@mail.ru)
'''
def parser_args():
    parser = argparse.ArgumentParser(description='Client for working with file system on a Linux server')
    parser.add_argument('--ip','-i', type=str, default='127.0.0.1', help='IP address of server')
    parser.add_argument('--port','-p', type=int, default='49322', help='Port number of server')
    parser.add_argument('--action','-a', type=int, default='0', help='\nChoose what you want to do: \
                                                                        \n   1) Write file to server \
                                                                        \n   2) Download file from server \
                                                                        \n   3) Copy file to another path \
                                                                        \n   4) Move file to another path \
                                                                        \n   5) Delete file from server\n\n')
    parser.add_argument('--path1','-p1', type=str, default='/home/ami/Downloads/123new.txt', help='Path to: \
                                                                        \n   1) Original file on your system \
                                                                        \n   2) Original file on server \
                                                                        \n   3) Original file on server \
                                                                        \n   4) Original file on server \
                                                                        \n   5) Original file on server\n\n')
    parser.add_argument('--path2','-p2', type=str, default='/home/ami/Downloads/123new.py', help='Path to: \
                                                                        \n   1) Folder on server \
                                                                        \n   2) Folder on your system \
                                                                        \n   3) New file on server \
                                                                        \n   4) New file on server \
                                                                        \n   5) Type "yes"\n\n')
    my_namespace = parser.parse_args()
    return my_namespace

# Функция чтения файла удаленно (сервер - клиент)
def read(path, client_sock):
    with open(path, 'rb') as file_to_send:
        for data in file_to_send:
            client_sock.sendall(data)
    client_sock.close()

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

# Основная функция, отвечающая за поведение клиента
def client(ip, port, action, path1, path2):
    # 127.0.0.1 49322 2 /home/ami/123.py /home/ami/Downloads/123new.txt
    # 127.0.0.1 49322 1 /home/ami/Downloads/123new.txt /home/ami/Downloads/123new.py
    # 127.0.0.1 49322 3 /home/ami/Downloads/123new.py  /home/ami/Downloads/123new.h
    # 127.0.0.1 49322 4 /home/ami/Downloads/123new.h /home/ami/Downloads/test/123new.h
    # 127.0.0.1 49322 5 /home/ami/Downloads/test/123new.h yes
    if action == 0:
        print('Enter pls [ip] [port] [action] [filepath1] [filepath2|confirmation] \
                \nAction list: \
                \n   1) Write file to server (filepath on you system and on server) \
                \n   2) Download file from server (filepath on server and on your system) \
                \n   3) Copy file to another path (filepath old and new on server) \
                \n   4) Move file to another path (filepath old and new on server) \
                \n   5) Delete file from server (filepath and please confirm the deletion \
                \n      of the file by writing "yes")\n\n')
        ip, port, action, path1, path2 = input().split()
        port = int(port)
        action = int(action)
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_sock.connect((ip, port))
    print(f'Connected to server with IP: {ip} and Port: {port}')
    
    client_sock.send((str(action) + " " + path1 + " " + path2).encode()) # имя файла с каталогом bytes 
    print(f'Action: {action}, filepath1: {path1}, filepath2: {path2}')
    
    if action == 1: # Запись файла на сервер  
        read(path1, client_sock)
    
    if action == 2: # Загрузка файла с сервера 
        write(path2, client_sock)



if __name__ == '__main__':
    args = parser_args()
    try:
        client(args.ip, args.port, args.action, args.path1, args.path2)
    except KeyboardInterrupt:
        print('\nInterrupted by keyboard!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
