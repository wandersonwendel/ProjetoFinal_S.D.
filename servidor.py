import socket
import threading

# Connection Data
host = '192.168.0.106'
port = 55555

# Inicializando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas para Clientes e seus apelidos
clients = []
apelidos = []

# Enviando mensagens para todos os clientes conectados
def broadcast(message):
    for client in clients:
        client.send(message)

# Processando as mensagens dos clientes
def handle(client):
    while True:
        try:
            # Mensagens de Broadcasting/Transmissão
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removendo e fechando a lista Clientes
            index = clients.index(client)
            clients.remove(client)
            client.close()
            apelido = apelidos[index]
            broadcast('{} left!'.format(apelidos).encode('ascii'))
            apelidos.remove(apelido)
            break

# Função de receber/escutar
def receive():
    while True:
        # Aceitar conexão
        client, address = server.accept()
        print("Conectado com {}".format(str(address)))

        # Solicitar e armazenar apelido
        client.send('NICK'.encode('ascii'))
        apelido = client.recv(1024).decode('ascii')
        apelidos.append(apelido)
        clients.append(client)

        # Imprime o apelido e a transmissão
        print("Apelido é {}".format(apelido))
        broadcast("{} entrou!".format(apelido).encode('ascii'))
        client.send('Conectado ao servidor!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()