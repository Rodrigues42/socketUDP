import threading
import socket
import requests
from Canal import Canal

# Configurar o servidor
host = '127.0.0.1'
porta = 9000

while True:
    try:
        portaServidor = int(input("Qual é a porta que o servidor vai escutar ? "))

        hostServidor = socket.gethostbyname(socket.gethostname())

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
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        servidor_socket.bind((host, portaServidor))
        servidor_socket.settimeout(10)

        # clientes
        clientes = {}

        # Canal
        canal = Canal(host, porta)

        eventoTimeout = threading.Event()

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
        monitor = canal.criarPropriedade()
        clientes[address] = monitor
    
    return monitor

def receberResposta(eventoTimeout):

    # Receber dados do cliente
    try:
        dados, endereco_cliente = servidor_socket.recvfrom(1024)

        print("---" * 20)
        print(f"{endereco_cliente} - Dados recebido: {dados.decode('utf-8')}")

        enviarResposta(endereco_cliente)

    except TimeoutError:
        print("Servidor Encerrado")
        eventoTimeout.set()

def enviarResposta(endereco_cliente):
        
    #Verificar se o cliente já enviou algo para o servidor e criar um monitor especifico para ele
    monitor = verificarMonior(endereco_cliente)

    # Enviar uma resposta para o cliente
    mensagem = b"Ok"
    servidor_socket.sendto(mensagem, (endereco_cliente[0], endereco_cliente[1]))

    monitor.consolidarErros(mensagem, endereco_cliente, True)

    print(f"{endereco_cliente} - Resposta oK Enviada")

while True:
    
    print("---" * 20)
    print(f"Servidor UDP aguardando em {host}:{porta}")

    receberResposta(eventoTimeout)

    if eventoTimeout.is_set():
        break

for address in clientes:
    monitor = clientes[address]
    print("---" * 18)
    print(f'''
            Cliente: {address}''')
    
    monitor.ImprimirErros()