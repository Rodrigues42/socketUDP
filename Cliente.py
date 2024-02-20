
import threading
import socket
from Canal import Canal

# Configurar o cliente
host = 'localhost'
portaServidor = 9000
portaCliente = 9001

while True:
    try:
        portaCliente = int(input("Qual é a porta do cliente que deseja conectar? "))
        host = input("Qual é o IP do servidor ? (Digite enter ou localhost para 127.0.0.1) ") 
        portaServidor = int(input("Qual é a porta do servidor ? "))

        if host == 'localhost' or host == '':
            host = '127.0.0.1'

        print('---' * 25)
        print(f"Cliente: ({socket.gethostbyname(socket.gethostname())} : {portaCliente}) | servidor: ({host} : {portaServidor})")

        servidor_socket = Canal(host, portaServidor)
        servidor_socket.associarSocketPorta('0.0.0.0', portaCliente)
        servidor_socket.definirTimeout(3)

        monitorGeral = servidor_socket.criarPropriedade()

        break
    except:
        print("Revisar dados informados")
        continue

def enviar(mensagem):

    monitor  = servidor_socket.criarPropriedade()

    # Enviar dados ao servidor
    address = (host, portaServidor)
    servidor_socket.enviar(monitor, mensagem.encode('utf-8'), address)
    print(f"('{host}', {portaServidor}) - Mensagem: '{mensagem}' Enviada ao servidor")

    try:
        dados, address = servidor_socket.receber(monitor)
        if dados is not bytes():
            print(f"('{host}', {portaServidor}) - Dados recebidos: {dados.decode('utf-8')}")
    except:
        pass

    print("---" * 20)
    servidor_socket.juntarPropriedadeGeralComParcial(monitorGeral, monitor)

def enviarParalelo(mensagens):
    
    print("----" * 14)
    print("Forma Paralela")
    print("----" * 14)

    threads = []

    for mensagem in mensagens:
        thread = threading.Thread(target=enviar, args=(mensagem,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

while True:

    print("----" * 20)

    try:
        quantidadeMensagem = int(input("Quantas mensagens deseja enviar ao servidor? "))
        forma = input("Qual a forma de envio sequencial ou paralelo? (sequencial (S) ou paralelo (P)): ")
        mensagens = list()
    except:
        continue

    for i in range(quantidadeMensagem):
        mensagem = input(f"{i+1}° Mensagem: ")
        mensagens.append(mensagem)

    if forma.upper() == 'S':
        print("----" * 14)
        print("Forma sequencial")
        print("----" * 14)
        
        for mensagem in mensagens:
            enviar(mensagem)
    else:
        enviarParalelo(mensagens)

    monitorGeral.ImprimirErros()
