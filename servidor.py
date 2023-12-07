import socket
import numpy as np
import pickle
from concurrent.futures import ThreadPoolExecutor

def handle_client(client_socket):
    try:
        # Recebe a operação e os dados do cliente
        data = client_socket.recv(1024)
        operation, matrix_a, matrix_b = pickle.loads(data)

        # Realiza a operação solicitada
        if operation == "multiply":
            result = np.dot(matrix_a, matrix_b)
        elif operation == "add":
            result = np.add(matrix_a, matrix_b)
        else:
            result = "Operação não suportada"

        # Envia o resultado de volta ao cliente
        client_socket.send(pickle.dumps(result))
    except Exception as e:
        print(f"Erro no servidor: {e}")
    finally:
        client_socket.close()

def start_server():
    # Configuração do servidor
    host = '127.0.0.1'
    port = 12345

    # Cria o socket do servidor
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)

    print(f"Servidor escutando em {host}:{port}")

    # Usa ThreadPoolExecutor para processamento paralelo
    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            # Aguarda a conexão do cliente
            client, addr = server.accept()
            print(f"Conexão estabelecida com {addr[0]}:{addr[1]}")

            # Submete a tarefa ao executor para processamento paralelo
            executor.submit(handle_client, client)

if __name__ == "__main__":
    start_server()
