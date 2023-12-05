import socket
import struct
from threading import Thread
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

assentos = {i: 'disponível' for i in range(1, 31)}
reservas = []

def processar_reserva(origem, destino, assento):
    try:
        assento = int(assento)
    except ValueError:
        return "Erro: Assento deve ser um número inteiro."

    reservas.append({'origem': origem, 'destino': destino, 'assento': assento})
    return f"Reserva de {origem} para {destino}, Assento {assento} confirmada."

@app.route('/reservar', methods=['POST', 'GET', 'OPTIONS'])
def reservar_assento():
    if request.method == 'POST':
        data = request.get_data()
        origem, destino, assento = struct.unpack('!10s10s1s', data)
        origem = origem.decode('utf-8').sstrip()
        destino = destino.decode('utf-8').strip()
        assento = assento.decode('utf-8').strip()

        reply = processar_reserva(origem, destino, assento)
 
        return reply
    else:
        # Responda a solicitações OPTIONS com os cabeçalhos necessários para permitir CORS
        response = jsonify({'message': 'Method Not Allowed'})
        response.headers.add('Allow', 'POST, GET, OPTIONS')
        return response, 405

@app.route('/reservados', methods=['GET'])
def assentos_reservados():
    return jsonify({'reservas': reservas})

def run_flask():
    app.run(host='10.10.133.188', port=5000)


if __name__ == '__main__':
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('10.10.133.188', 5000))
    server_socket.listen(1)
    print("Servidor escutando em 10.10.133.188:5000")

    # Inicie o servidor Flask em uma thread separada
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexão recebida de {client_address[0]}:{client_address[1]}")

        request_data = client_socket.recv(1024)

        if request_data:
            origem, destino, assento = struct.unpack('!10s10s1s', request_data[:21])
            origem = origem.decode('utf-8').strip()
            destino = destino.decode('utf-8').strip()
            assento = assento.decode('utf-8').strip()

            # Chame a função processar_reserva e envie a resposta de volta ao cliente
            reply = processar_reserva(origem, destino, assento)
            client_socket.send(reply.encode('utf-8'))
            print(reply)

        client_socket.close()
