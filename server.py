#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pip install flask

import os
import threading
from flask import Flask, send_from_directory, send_file
from tkinter import Tk, Label, Button, Entry, StringVar, filedialog, messagebox

app = Flask(__name__)
server_thread = None
serve_folder = True
path_to_serve = ""

def start_server():
    app.run(host='0.0.0.0', port=80)

@app.route('/')
def serve():
    if serve_folder:
        return send_from_directory(path_to_serve, 'index.html')
    else:
        return send_file(path_to_serve)

def start_server_thread():
    global server_thread
    if server_thread is None or not server_thread.is_alive():
        server_thread = threading.Thread(target=start_server)
        server_thread.start()

def stop_server():
    global server_thread
    if server_thread and server_thread.is_alive():
        terminate_thread(server_thread)
        server_thread = None

def terminate_thread(thread):
    if not thread.is_alive():
        return

    import ctypes
    tid = ctypes.c_long(thread.ident)
    exctype = SystemExit
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def browse_folder():
    global serve_folder, path_to_serve
    path_to_serve = filedialog.askdirectory()
    if path_to_serve:
        serve_folder = True
        path_var.set(path_to_serve)

def browse_file():
    global serve_folder, path_to_serve
    path_to_serve = filedialog.askopenfilename()
    if path_to_serve:
        serve_folder = False
        path_var.set(path_to_serve)

def on_closing():
    stop_server()
    root.destroy()

# Interface Gráfica
root = Tk()
root.title("Servidor Web")

path_var = StringVar()

Label(root, text="Caminho a servir:").grid(row=0, column=0, padx=10, pady=10)
Entry(root, textvariable=path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
Button(root, text="Escolher Pasta", command=browse_folder).grid(row=1, column=0, padx=10, pady=10)
Button(root, text="Escolher Ficheiro", command=browse_file).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Ligar Servidor", command=start_server_thread).grid(row=2, column=0, padx=10, pady=10)
Button(root, text="Desligar Servidor", command=stop_server).grid(row=2, column=1, padx=10, pady=10)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
