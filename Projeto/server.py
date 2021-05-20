#!/usr/bin/env python3
import socket
import threading

def accept_incoming_connections():
    while True:
        con, client = sock.accept()
        print(f"{client[0]}:{client[1]} - CONECTADO.")
        con.send(str.encode("Bem-vindo, digite seu nome para iniar a conversa."))
        addresses[con] = client
        threading.Thread(target=handle_client, args=(con,)).start()

def handle_client(con):
    name = con.recv(TAM_MSG).decode("utf8")
    con.send(str.encode(f'Bem-vindo {name}'))
    con.send(str.encode(f'Digite @COMMANDS para ajuda.'))
    broadcast(str.encode(f"{name} entrou!"))
    clients[con] = name

    while True:
        try:
            msg = con.recv(TAM_MSG)
            if msg.decode().upper() == "@QUIT":
                con.send(str.encode("@QUIT"))
                del clients[con]
                del addresses[con]
                con.close()
                broadcast(str.encode(f"{name} saiu."))
                count = 0
                for i in clients:
                    count += 1
                if count == 0:
                    break
            elif msg.decode().upper() == "@LIST":
                con.send(str.encode('----- USUÁRIOS -----'))
                con.send(str.encode('@BREAK'))
                for i in clients:
                    con.send(str.encode(f'{clients[i]} | {addresses[i][1]}'))
                    con.send(str.encode('@BREAK'))
            elif msg.decode().upper() == "@COMMANDS":
                con.send(str.encode('------ COMANDOS -----'))
                con.send(str.encode('@BREAK'))
                con.send(str.encode('@LIST - Lista usuário e UIDs'))
                con.send(str.encode('@BREAK'))
                con.send(str.encode('@USER - Messagem Privada'))
                con.send(str.encode('@BREAK'))
                con.send(str.encode('@QUIT - Sair'))
                con.send(str.encode('@BREAK'))
            elif "@USER" in (msg).decode().upper().split(' '):
                if len((msg).decode().split(' ')) < 3:
                    con.send(str.encode('Preencha os campos para envio'))
                    con.send(str.encode("@user 'UID' mensagem"))
                else:
                    x = False
                    for i in clients:
                        if str(addresses[i][1]) == (msg).decode("utf8").split(' ')[1]:
                            x = True
                            i.send( str.encode(f'{name}-private: ' + " ".join((msg).decode("utf8").split(' ')[2:])) )
                    if x:
                        con.send( str.encode(f'{name}-private: ' + " ".join((msg).decode("utf8").split(' ')[2:])) )
                    else:
                        con.send(str.encode('UID inválido'))
            else:
                broadcast(msg, name+": ")
        except:
            break

def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(str.encode(prefix, "utf8")+msg)
        
clients = {}
addresses = {}

HOST = '0.0.0.0'
PORT = 8080
TAM_MSG = 1024
serv = (HOST, PORT)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(serv)

if __name__ == "__main__":
    sock.listen(50)
    print("Aguardando conexão")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    sock.close()