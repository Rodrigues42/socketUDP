import threading
from Canal import Canal

# Configurar o servidor
host = 'localhost'
porta = 9000

# Criar um socket UDP
servidor_socket = Canal(host, porta)
servidor_socket.associarSocketPorta()

# clientes
clientes = {}

def enviarResposta(address):

    if address in clientes:
        monitor = clientes[address]
    else:
        monitor = servidor_socket.criarPropriedade()
        clientes[address] = monitor

    # Enviar uma resposta para o cliente
    servidor_socket.enviar(monitor, b"Ok", address)
    print(f"{address} - Resposta oK Enviada")

def receberResposta(address, evento):

    # Receber dados do cliente
    dados, endereco_cliente = servidor_socket.receber()
    print("---" * 20)
    print(f"{endereco_cliente} - Dados recebido: {dados.decode('utf-8')}")
    
    # Verificar se o cliente já enviou algo para o servidor e criar um monitor especifico para ele
    if endereco_cliente not in clientes:
        clientes[endereco_cliente] = servidor_socket.criarPropriedade()

    address.append(endereco_cliente)
    evento.set()


maximoRequisicap = 200
contador = 0

while True:

    contador += 1
    
    print("---" * 20)
    print(f"Servidor UDP aguardando em {host}:{porta}")

    address, evento = [], threading.Event()

    threadReceber = threading.Thread(target=receberResposta(address, evento))
    threadReceber.start()
    threadReceber.join()

    evento.wait()

    threadEnviar = threading.Thread(target=enviarResposta(address[0]))
    threadEnviar.start()
    threadEnviar.join()

    if contador >= maximoRequisicap:
        continua = input("Continuar (s/sair): ")
        if continua == 'sair':
            break

for address in clientes:
    monitor = clientes[address]
    print("---" * 18)
    print(f'''
            Cliente: {address}''')
    
    monitor.ImprimirErros()