import socket
import struct
import tkinter as tk
from tkinter import ttk

def reservar_assento():
    origem = origem_entry.get()
    destino = destino_entry.get()
    assento = assento_entry.get()

    request_data = struct.pack('!10s10s1s', origem.encode('utf-8'), destino.encode('utf-8'), assento.encode('utf-8'))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(request_data)
    response = client_socket.recv(1024).decode()
    result_label.config(text=response)
    client_socket.close()

# Configuração da janela
root = tk.Tk()
root.title("Reserva de Assento")

# Componentes da interface
origem_label = ttk.Label(root, text="Origem:")
origem_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
origem_entry = ttk.Entry(root)
origem_entry.grid(row=0, column=1, padx=10, pady=10)

destino_label = ttk.Label(root, text="Destino:")
destino_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
destino_entry = ttk.Entry(root)
destino_entry.grid(row=1, column=1, padx=10, pady=10)

assento_label = ttk.Label(root, text="Assento:")
assento_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
assento_entry = ttk.Entry(root)
assento_entry.grid(row=2, column=1, padx=10, pady=10)

reservar_button = ttk.Button(root, text="Reservar Assento", command=reservar_assento)
reservar_button.grid(row=3, column=0, columnspan=2, pady=20)

result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Configuração do servidor
host = '172.25.238.106'
port = 5000

root.mainloop()
