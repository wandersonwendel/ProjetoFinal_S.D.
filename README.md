<h1 align="center"> Projeto Final - Sistemas Distribuídos. </h1>

## Introdução
Chat TCP utilizando a linguagem Python, Sockets e Arquitetura Cliente-Servidor. Teremos um servidor que hospeda o chat e vários clientes que se conectam a ele e se comunicam entre si.

## Arquitetura Cliente-Servidor
Para nossa aplicação, teremos vários clientes (os usuários) e um servidor central que hospeda tudo e fornece os dados para esses clientes.

Portanto, precisaremos escrever dois scripts Python. Um será para iniciar o servidor e o outro será para o cliente. Teremos que executar primeiro o servidor, para que haja um chat ao qual os clientes possam se conectar. Os próprios clientes não vão se comunicar diretamente entre si, mas através do servidor central.

## Implementando o Servidor

Agora vamos começar implementando o servidor primeiro. Para isso, precisaremos importar duas bibliotecas, a saber, socket e threading . O primeiro será usado para a conexão de rede e o segundo é necessário para executar várias tarefas ao mesmo tempo.

import socket
import threading

A próxima tarefa é definir nossos dados de conexão e inicializar nosso soquete. Vamos precisar de um endereço IP para o host e um número de porta livre para o nosso servidor. Neste exemplo, usaremos o endereço localhost (127.0.0.1) e a porta 55555. A porta é realmente irrelevante, mas você deve se certificar de que a porta que está usando é livre e não reservada. Se você estiver executando este script em um servidor real, especifique o endereço IP do servidor como o host. Confira esta lista de números de porta reservados para obter mais informações.

## Dados de Conexão
host = '127.0.0.1'
port = 55555


## Inicializando o Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


## Listas para Clientes e seus Apelidos
clients = []
apelidos = []

Quando definimos nosso socket, precisamos passar dois parâmetros. Estes definem o tipo de soquete que queremos usar. O primeiro ( AF_INET ) indica que estamos usando um soquete de internet em vez de um soquete unix. O segundo parâmetro representa o protocolo que queremos usar. SOCK_STREAM  indica que estamos usando TCP e não UDP.

Depois de definir o soquete, nós o ligamos ao nosso host e à porta especificada passando uma tupla que contém ambos os valores. Em seguida, colocamos nosso servidor no modo de escuta, para que ele aguarde a conexão dos clientes. Ao final criamos duas listas vazias, que usaremos para armazenar os clientes conectados e seus apelidos posteriormente.

## Enviando Mensagens Para Todos os Clientes Conectados
def broadcast(message):
    for client in clients:
        client.send(message)
        
Aqui definimos uma pequena função que vai nos ajudar a transmitir mensagens e tornar o código mais legível. O que ele faz é apenas enviar uma mensagem para cada cliente que está conectado e, portanto, na lista de clientes. Usaremos esse método nos outros métodos.

Agora vamos começar com a implementação da primeira função principal. Esta função será responsável por tratar as mensagens dos clientes.

## Processando as Mensagens dos Clientes 
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
            
Como você pode ver, esta função está sendo executada em um loop while. Ele não vai parar a menos que haja uma exceção por causa de algo que deu errado. A função aceita um cliente como parâmetro. Sempre que um cliente se conecta ao nosso servidor, executamos essa função para ele e ele inicia um loop infinito.

O que ele faz é receber a mensagem do cliente (se ele enviar alguma) e transmiti-la para todos os clientes conectados. Portanto, quando um cliente envia uma mensagem, todos os outros podem ver essa mensagem. Agora, se por algum motivo houver um erro na conexão com este cliente, removemos ele e seu apelido, fechamos a conexão e transmitimos que este cliente saiu do chat. Depois disso, quebramos o loop e esse fio chega ao fim. Bem simples. Estamos quase terminando o servidor, mas precisamos de uma função final.

## Função Receber/Ouvir
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
        
Quando estivermos prontos para executar nosso servidor, executaremos esta função de recebimento . Ele também inicia um loop infinito que aceita constantemente novas conexões de clientes. Uma vez que um cliente está conectado, ele envia a string  'NICK'  para ele, que dirá ao cliente que seu apelido foi solicitado. Depois disso, ele espera por uma resposta (que provavelmente contém o apelido) e acrescenta o cliente com o respectivo apelido às listas. Depois disso, imprimimos e transmitimos essas informações. Por fim, iniciamos uma nova thread que executa a função de manipulação implementada anteriormente para esse cliente específico. Agora podemos apenas executar esta função e nosso servidor está pronto.

Observe que estamos sempre codificando e decodificando as mensagens aqui. A razão para isso é que só podemos enviar bytes e não strings. Portanto, sempre precisamos codificar mensagens (por exemplo, usando ASCII), quando as enviamos e decodificá-las, quando as recebemos.

receive()

## Implementando o Cliente

Um servidor é bastante inútil sem clientes que se conectam a ele. Então agora vamos implementar nosso client. Para isso, precisaremos novamente importar as mesmas bibliotecas. Observe que este é agora um segundo script separado.

import socket
import threading

Os primeiros passos do cliente são escolher um apelido e se conectar ao nosso servidor. Precisamos saber o endereço exato e a porta na qual nosso servidor está sendo executado.

## Escolhendo os Apelidos
apelido = input("Escolha o seu apelido: ")

## Conectando ao Servidor
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 55555))

Como você pode ver, estamos usando uma função diferente aqui. Em vez de vincular os dados e ouvir, estamos nos conectando a um servidor existente.

Agora, um cliente precisa ter dois threads em execução ao mesmo tempo. O primeiro receberá constantemente dados do servidor e o segundo enviará nossas próprias mensagens ao servidor. Portanto, precisaremos de duas funções aqui. Vamos começar com a parte de recepção.

## Escutando o Servidor e Enviando os Apelidos
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
            
Novamente, temos um loop infinito aqui. Ele tenta constantemente receber mensagens e imprimi-las na tela. Se a mensagem for 'NICK' no entanto, ele não a imprime, mas envia seu apelido para o servidor. Caso haja algum erro, fechamos a conexão e quebramos o loop. Agora só precisamos de uma função para enviar mensagens e estamos quase terminando.

## Enviando Mensagens Ao Servidor
def write():
    while True:
        message = '{}: {}'.format(apelido, input(''))
        client.send(message.encode('ascii'))
        
A função de escrita é bastante curta. Ele também é executado em um loop infinito que está sempre esperando por uma entrada do usuário. Uma vez que obtém algum, combina-o com o apelido e envia-o para o servidor. É isso. A última coisa que precisamos fazer é iniciar dois threads que executam essas duas funções.

## Incializando as Threads para Escutar e Escrever
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start() 

E agora terminamos. Temos um servidor totalmente funcional e clientes em funcionamento que podem se conectar a ele e se comunicar uns com os outros.
