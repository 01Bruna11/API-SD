import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import socket
import struct

class PassagensAereasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Passagens Aéreas")

        self.origem_label = ttk.Label(root, text="Origem:")
        self.origem_entry = ttk.Entry(root)

        self.destino_label = ttk.Label(root, text="Destino:")
        self.destino_entry = ttk.Entry(root)

        self.assento_label = ttk.Label(root, text="Assento:")
        self.assento_entry = ttk.Entry(root)

        self.reservar_button = ttk.Button(root, text="Reservar", command=self.reservar_passagem)

        self.origem_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
        self.origem_entry.grid(row=0, column=1, padx=10, pady=10)

        self.destino_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)
        self.destino_entry.grid(row=1, column=1, padx=10, pady=10)

        self.assento_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)
        self.assento_entry.grid(row=2, column=1, padx=10, pady=10)

        self.reservar_button.grid(row=3, column=0, columnspan=2, pady=10)

    def reservar_passagem(self):
        origem = self.origem_entry.get()
        destino = self.destino_entry.get()
        assento = self.assento_entry.get()

        try:
            assento = int(assento)
            if 1 <= assento <= 30:
                resposta = self.enviar_solicitacao(origem, destino, assento)
                if "ocupado" in resposta.lower():
                    messagebox.showerror("Erro", "Assento ocupado. Escolha outro assento.")
                else:
                    messagebox.showinfo("Reserva Concluída", resposta)
            else:
                messagebox.showerror("Erro", "Assento deve estar entre 1 e 30.")
        except ValueError:
            messagebox.showerror("Erro", "Assento deve ser um número inteiro.")

    def enviar_solicitacao(self, origem, destino, assento):
        host = '10.10.128.16'
        port = 5000

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((host, port))
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao servidor: {e}")
            return

        request_data = struct.pack('!10s10s1s', origem.encode('utf-8'), destino.encode('utf-8'), str(assento).encode('utf-8'))
        client_socket.send(request_data)
        response = client_socket.recv(1024).decode()

        client_socket.close()
        return response

if __name__ == "__main__":
    root = tk.Tk()
    app = PassagensAereasGUI(root)
    root.mainloop()
