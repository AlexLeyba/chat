from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread


def connection():
    """Обработка входящих клиентов"""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%sconnected" % client_address)
        client.send(bytes("Введите имя и нажмите Enter", "utf8"))
        addresses[client] = client_address
        Thread(target=join_client, args=(client,)).start()


def join_client(client):
    """Соединение с клиентом"""
    name = client.recv(MSIZE).decode("utf8")
    welcome = 'Добро пожальвать %s что бы выйти введите {quit}' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s Присоединился к чату!" % name
    broadcast(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(MSIZE)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s покинул нас..." % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    """Отправляет сообщения всем клиентам"""
    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
addresses = {}
HOST = ''
PORT = 9090
MSIZE = 1024
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == '__main__':
    SERVER.listen(5)
    print("Ожидание соединения...")
    ACCEPT_THREAD = Thread(target=connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
