import socket
from Canal import Canal

# Configurar o cliente
host = 'localhost'
porta = 9000

cliente_socket = Canal(host, porta)
cliente_socket.definirTimeout(3)

while True:
    # Obter dados do usuário
    mensagem = input("Digite uma mensagem para enviar ao servidor (ou 'exit' para sair): ")
    
    if mensagem.lower() == 'exit':
        break
    
    cliente_socket.enviar(mensagem.encode('utf-8'))
    print(f"Mensagem: '{mensagem}' Enviada ao servidor ({host} : {porta})")

    dados, address = cliente_socket.receber()
    if dados is not bytes():
        print(f"Dados recebidos: {dados.decode('utf-8')}")

cliente_socket.consolidarErros()