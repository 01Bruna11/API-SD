from flask import Flask, request, jsonify
import struct

app = Flask(__name__)

def processar_reserva(origem, destino, assento):
    return f"Reserva de {origem} para {destino}, Assento {assento} confirmada."

@app.route('/reservar', methods=['POST', 'GET', 'OPTIONS'])
def reservar_assento():
    if request.method == 'POST':
        data = request.get_data()
        origem, destino, assento = struct.unpack('!10s10s1s', data)
        origem = origem.decode('utf-8').strip()
        destino = destino.decode('utf-8').strip()
        assento = assento.decode('utf-8').strip()
        
        reply = processar_reserva(origem, destino, assento)
        
        return reply
    else:
        # Responda a solicitações OPTIONS com os cabeçalhos necessários para permitir CORS
        response = jsonify({'message': 'Method Not Allowed'})
        response.headers.add('Allow', 'POST, GET, OPTIONS')
        return response, 405

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
