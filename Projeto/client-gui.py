#!/usr/bin/env python3
import socket
from threading import Thread
import tkinter
import sys

def receive():
    while True:
        try:
            msg = sock.recv(TAM_MSG).decode()
            if "@BREAK" in msg:
                message = msg.split('@BREAK')
                for i in range(len(message)):
                    msg_list.insert(tkinter.END,message[i])
            elif msg.upper() == "@QUIT":
                sock.close()
                top.quit()
            else:
                msg_list.insert(tkinter.END, msg)
        except OSError:
            break

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    sock.send(str.encode(msg))


def on_closing(event=None):
    my_msg.set("@QUIT")
    send()

top = tkinter.Tk()
top.title("ChatApp")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
scrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=30, width=100, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, width=90, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

if len(sys.argv) > 1:
    HOST = sys.argv[1].split(':')[0]
    PORT = int(sys.argv[1].split(':')[1])
else:
    HOST = input('Enter host: ')
    PORT = input('Enter port: ')
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)

TAM_MSG = 1024
serv = (HOST, PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(serv)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()