import tkinter as tk
from tkinter import scrolledtext
import tkinter.ttk as ttk
from client import Client
import errno
import sys

#app specific details
APP_NAME = "Chat App"
WIDTH = 620
HEIGHT = 480
#sockets specific details
PORT = 1234
IP = "127.0.0.1"


class App:
    def __init__(self,name,parent):
        self.name = name
        self.parent = parent
        self.config()
        self.create_gui()
        self.client = Client()
        self.connect()

    def connect(self):
        self.client.connect(self.name, IP, PORT)

    def config(self):
        self.parent.config(bg='gold')
        self.parent.title(APP_NAME)
        w = (self.parent.winfo_screenwidth() - WIDTH)//2
        h = (self.parent.winfo_screenheight() - HEIGHT)//2
        self.parent.geometry(f"{WIDTH}x{HEIGHT}+{w}+{h}")

    def create_gui(self):
        self.send_msg_gui()
        self.buffer_gui()

    def send_msg_gui(self):
        frame = tk.Frame(self.parent,width=WIDTH,height=35)
        frame.pack(side='bottom',fill='x')
        frame.pack_propagate(False)
        tk.Label(frame,text='>> ').pack(side='left')
        tk.Button(frame,text="send",command=self.send_msg).pack(side='right')
        self.msg_box = scrolledtext.ScrolledText(frame,font='-size 14',wrap=tk.WORD,pady=5)
        self.msg_box.pack(fill='both')

    def buffer_gui(self):
        frame = tk.Frame(self.parent,width=WIDTH,height=HEIGHT-35)
        frame.pack(side='top',fill='both',expand=True)
        frame.pack_propagate(False)
        self.show_box = scrolledtext.ScrolledText(frame,state='disabled')
        self.show_box.pack(fill='both',expand=True)

    def send_msg(self):
        msg = self.msg_box.get(1.0,tk.END)
        if msg:
            self.client.send_msg(msg)
        self.msg_box.delete(1.0,tk.END)

    def check(self):
        try:
            msg = self.client.recieve_msg()
            if msg is False:
                self.client.close()
                sys.exit()
            self.show_box.config(state='normal')
            self.show_box.insert(tk.END,msg)
            self.show_box.config(state='disabled')
            # print("Msg:",msg)
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print("Reading Error",str(e))
                self.client.close()
                sys.exit()
        except Exception as e:
            print("General Error",str(e))
            self.client.close()
            sys.exit()

    def run(self):
        while True:
            msg = self.check()
            self.parent.update_idletasks()
            self.parent.update()

    def exit(self):
        print("Exiting....")
        sys.exit()

if __name__=="__main__":
    root = tk.Tk()
    name = input("Enter Your Name: ")
    App(name,root).run()
