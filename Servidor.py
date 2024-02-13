import threading
from Canal import Canal

# Configurar o servidor
host = 'localhost'
porta = 9000

# Criar um socket UDP
servidor_socket = Canal(host, porta)
servidor_socket.associarSocketPorta()

def enviarResposta(address):

    # Enviar uma resposta para o cliente
    servidor_socket.enviar(b"Ok", address)
    print(f"{address} - Resposta oK Enviada")

while True:
    
    print(f"Servidor UDP aguardando em {host}:{porta}")

    # Receber dados do cliente
    dados, endereco_cliente = servidor_socket.receber()
    print(f"{endereco_cliente} - Dados recebido: {dados.decode('utf-8')}")

    thread = threading.Thread(name=endereco_cliente, target=enviarResposta(endereco_cliente))
    thread.start()

    thread.join()
    servidor_socket.consolidarErros()
