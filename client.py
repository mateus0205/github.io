import socket
import numpy as np
import pickle

def send_request(operation, matrix_a, matrix_b):
    # Configuração do cliente
    host = '127.0.0.1'
    port = 12345

    # Cria o socket do cliente
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Envia a operação e os dados para o servidor
    data = pickle.dumps((operation, matrix_a, matrix_b))
    client.send(data)

    # Recebe o resultado do servidor
    result_data = client.recv(1024)
    result = pickle.loads(result_data)

    # Fecha a conexão com o servidor
    client.close()

    return result

if __name__ == "__main__":
    # Exemplo de uso com matrizes maiores
    matrix_size = 3

    matrix_a = np.random.randint(1, 10, size=(matrix_size, matrix_size))
    matrix_b = np.random.randint(1, 10, size=(matrix_size, matrix_size))

    print("Matriz A:")
    print(matrix_a)
    print("\nMatriz B:")
    print(matrix_b)

    # Operação de multiplicação
    result_multiply = send_request("multiply", matrix_a, matrix_b)
    print("\nResultado da multiplicação:")
    print(result_multiply)

    # Operação de adição
    result_add = send_request("add", matrix_a, matrix_b)
    print("\nResultado da adição:")
    print(result_add)
