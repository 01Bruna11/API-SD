import asyncio
import tkinter as tk
from tkinter import ttk
import struct

async def reservar_assento_async_helper():
    origem = origem_entry.get()
    destino = destino_entry.get()
    assento = assento_entry.get()

    request_data = struct.pack('!10s10s1s', origem.encode('utf-8'), destino.encode('utf-8'), assento.encode('utf-8'))

    try:
        reader, writer = await asyncio.open_connection(host, port)

        # Envia solicitação
        writer.write(request_data)
        await writer.drain()

        # Recebe resposta
        response = await reader.read(1024)

        # Atualiza a interface gráfica
        root.event_generate("<<UpdateResultLabel>>", when="tail", data=response.decode())

    except Exception as e:
        # Atualiza a interface gráfica em caso de erro
        root.event_generate("<<UpdateResultLabel>>", when="tail", data=f"Erro: {e}")
    finally:
        writer.close()
        await writer.wait_closed()

async def reservar_assento_async():
    loop = asyncio.get_running_loop()
    await loop.create_task(reservar_assento_async_helper())

# Função para atualizar o rótulo de resultado na interface gráfica
def update_result_label(event):
    result_label.config(text=event.data)

# Configuração da janela
root = tk.Tk()
root.title("Reserva de Assento")

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

reservar_button = ttk.Button(root, text="Reservar Assento", command=lambda: asyncio.run(reservar_assento_async()))
reservar_button.grid(row=3, column=0, columnspan=2, pady=20)

result_label = ttk.Label(root, text="")
result_label.grid(row=4, column=0, columnspan=2)

# Associa o evento <<UpdateResultLabel>> à função de atualização
root.bind("<<UpdateResultLabel>>", update_result_label)

# Configuração do servidor
host = '192.168.100.94'
port = 5000

root.mainloop()
