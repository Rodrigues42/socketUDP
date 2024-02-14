
import threading
from Canal import Canal

# Configurar o cliente
host = 'localhost'
porta = 9000

cliente_socket = Canal(host, porta)
cliente_socket.definirTimeout(5)

monitorGeral = cliente_socket.criarPropriedade()

def enviar(mensagem):

    monitor  = cliente_socket.criarPropriedade()

    # Enviar dados ao servidor
    address = (host, porta)
    cliente_socket.enviar(monitor, mensagem.encode('utf-8'), address)
    print(f"('{host}', {porta}) - Mensagem: '{mensagem}' Enviada ao servidor")

    cliente_socket.juntarPropriedadeGeralComParcial(monitorGeral, monitor)

    dados, address = cliente_socket.receber()
    if dados is not bytes():
        print(f"('{host}', {porta}) - Dados recebidos: {dados.decode('utf-8')}")
        print("---" * 20)

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

    quantidadeMensagem = int(input("Quantas mensagens deseja enviar ao servidor? "))
    forma = input("Qual a forma de envio sequencial ou paralelo? (sequencial (S) ou paralelo (P)): ")
    mensagens = list()

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
