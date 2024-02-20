import threading
import socket
import requests
from Canal import Canal

# Configurar o servidor
host = 'localhost'
porta = 9000

while True:
    try:
        portaServidor = int(input("Qual é a porta que o servidor vai escutar ? "))

        host = socket.gethostbyname(socket.gethostname())

        response = requests.get('https://ipinfo.io')
        public_ip = response.json()['ip']
        cidade = response.json()['city']
        regiao = response.json()['region']
        pais = response.json()['country']
        localizacao = response.json()['loc']

        print('---' * 18)
        print(f"servidor: ({host} : {portaServidor})")
        print('---' * 18)
        # Exibir informações de geolocalização
        print(f"Endereço IP publico: {public_ip}")
        print("Informações de Geolocalização:")
        print(f"  País: {pais}")
        print(f"  Região: {regiao}")
        print(f"  Cidade: {cidade}")
        print(f"  Latitude/Longitude: {localizacao}")
        print('---' * 18)

        # Criar um socket UDP
        servidor_socket = Canal(public_ip, porta)
        servidor_socket.associarSocketPorta('0.0.0.0', porta)
        servidor_socket.definirTimeout(10)

        # clientes
        clientes = {}

        break

    except Exception as e:
        print(f"Erro ao estabelecer conexão: {str(e)}")
        continue
    except:
        print("Revisar dados informados")
        continue

def verificarMonior(address):

    if address in clientes:
        monitor = clientes[address]
    else:
        monitor = servidor_socket.criarPropriedade()
        clientes[address] = monitor
    
    return monitor

def enviarResposta(address):

    monitor = verificarMonior(address)

    # Enviar uma resposta para o cliente
    servidor_socket.enviar(monitor, b"Ok", address)
    print(f"{address} - Resposta oK Enviada")

def receberResposta(address, eventoCliente, eventoTimeout):

    # Receber dados do cliente
    try:
        dados, endereco_cliente = servidor_socket.receber()

        print("---" * 20)
        print(f"{endereco_cliente} - Dados recebido: {dados.decode('utf-8')}")
        
        # Verificar se o cliente já enviou algo para o servidor e criar um monitor especifico para ele
        if endereco_cliente not in clientes:
            clientes[endereco_cliente] = servidor_socket.criarPropriedade()

        address.append(endereco_cliente)
        eventoCliente.set()
    except:
        print("Servidor Encerrado")
        eventoTimeout.set()

while True:
    
    print("---" * 20)
    print(f"Servidor UDP aguardando em {host}:{porta}")

    address, eventoCliente, eventoTimeout = [], threading.Event(), threading.Event()

    threadReceber = threading.Thread(target=receberResposta(address, eventoCliente, eventoTimeout))
    threadReceber.start()
    threadReceber.join()

    if eventoTimeout.is_set():
        break

    eventoCliente.wait()

    threadEnviar = threading.Thread(target=enviarResposta(address[0]))
    threadEnviar.start()
    threadEnviar.join()

for address in clientes:
    monitor = clientes[address]
    print("---" * 18)
    print(f'''
            Cliente: {address}''')
    
    monitor.ImprimirErros()