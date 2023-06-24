import socket
import threading

# Escolhendo apelido
apelido = input("Escolha o seu apelido: ")

# Conectando ao servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.0.106', 55555))

# Ouvindo o servidor e enviando o apelido
def receive():
    while True:
        try:
            # Recebe a mensagem do servidor
            # Se 'NICK' envia o apelido
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(apelido.encode('ascii'))
            else:
                print(message)
        except:
            # Fecha a conexão, caso der erro
            print("Ocorreu um erro!")
            client.close()
            break

# Enviando mensagem ao servidor
def write():
    while True:
        message = '{}: {}'.format(apelido, input(''))
        client.send(message.encode('ascii'))

# Inicializando threads para ler e escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()        