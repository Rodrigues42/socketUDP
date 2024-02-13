import logging
import socket
import random
import time

prob_eliminar_mensagem = 4
prob_duplicar_segmento = 3
prop_corromper_byte = 2
milesegundos_delay = 80
cortar_bytes = 1024

class Canal():
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = None
        self.propriedades = Propiedades()

    def associarSocketPorta(self):
        # Vincular o socket ao endereço e porta
        self.__socket.bind((self.host, self.port))
    
    def definirTimeout(self, timeout: float):
        self.__socket.settimeout(timeout)

    def enviar(self, mensagem: bytes, address: tuple = None):
        '''Envia dados ao servidor/cliente e aguarda uma resposta'''

        mensagemEliminada, mensagem = self.propriedades.consolidarErros(mensagem)
        
        if mensagemEliminada:
            return 0

        if address is None:
            self.__socket.sendto(mensagem, (self.host, self.port))
        else:
            self.__socket.sendto(mensagem, (address[0], address[1]))

        return 1
    
    def receber(self) -> tuple:
        ''' Recebe dados do servidor/cliente e retorna o endereço do servidor/cliente '''

        dados, socket_address = bytes(), self.address
        
        try:
            dados, socket_address = self.__socket.recvfrom(1024)

            self.address = socket_address

        except socket.timeout as e:
            logging.error(f"Timeout ao esperar retorno do servidor: {e}")

        except socket.error as e:
            logging.error(f"Erro de socket: {e}")

        except Exception as e:
            logging.error(f"Outro exceção: {e}")

        finally:
            # if self.address is None:
            #     self.__socket.close()

            return dados, socket_address
 
    def consolidarErros(self):
        self.propriedades.consolidacao()

class Propiedades():
    def __init__(self):
        super().__init__()
        self.mensagens = 0
        self.mensagensEliminadas = 0
        self.mensagensAtrasadas = 0
        self.mensagensDuplicadas = 0
        self.mensagensCorrompidas = 0
        self.mensagensCortadas = 0

    def eliminarMensagem(self, probabilidade: float) -> bool:
        '''Pocentagem de 0 a 100'''

        resultado = random.uniform(0, 1)
        
        if resultado <= (probabilidade/100):
            
            print("Mensagem Eliminada")

            self.mensagensEliminadas += 1

            return True
        
        return False

    def delay(self, mile: float):
        '''delay de milesegundos'''
        
        print("Delay")
        time.sleep(mile/1000)
        self.mensagensAtrasadas += 1

    def duplicarSegmento(self, probabilidade: float, dado: bytes) -> bytes:
        '''Pocentagem de 0 a 100'''

        resultado = random.uniform(0, 1)
        
        if resultado <= (probabilidade/100):
            
            print("Segmento duplicado")

            self.mensagensDuplicadas += 1

            return dado + dado
        
        return dado

    def corromperByte(self, probabilidade: float, dado: bytes):
        '''Corrompe 1 byte do dado aleatoriamente'''
        
        resultado = random.uniform(0, 1)
        
        if resultado <= (probabilidade/100):
            
            dadoComrrompido = list(dado)

            index = dadoComrrompido.index(dadoComrrompido[random.randint(0, len(dadoComrrompido) - 1)])
            #dadoComrrompido[index] = random.randint(0, 255) tratar para aceitar dessa maneira
            dadoComrrompido[index] += 1

            print("Dados corrompidos")

            self.mensagensCorrompidas += 1

            return bytes(dadoComrrompido)
        
        return dado

    def cortarBytes(self, tamanho: int, dado: bytes):
        ''' Corta o dados maiores que tamanho em bytes'''
        
        dadoCortado = dado
        dadoList = list(dado)
        
        if len(dadoList) > tamanho:
            
            dadoCortado = dadoList[0:tamanho]
            print("Dados cortados")

            self.mensagensCortadas += 1

        return bytes(dadoCortado)

    def consolidarErros(self, dados: bytes) -> tuple:
        
        self.mensagens += 1

        self.delay(milesegundos_delay)

        dados = self.duplicarSegmento(prob_duplicar_segmento, dados)

        dados = self.corromperByte(prop_corromper_byte, dados)

        dados = self.cortarBytes(cortar_bytes, dados)

        eliminarMensagem = self.eliminarMensagem(prob_eliminar_mensagem)
        if eliminarMensagem:
            return 1, dados

        return 0, dados

    def consolidacao(self):
        print(f'''
            Total de mensagens enviadas: {self.mensagens}
            Total de mensagens eliminadas: {self.mensagensEliminadas}
            Total de mensagens atrasadas: {self.mensagensAtrasadas}
            Total de mensagens duplicadas: {self.mensagensDuplicadas}
            Total de mensagens corrompidas: {self.mensagensCorrompidas}
            Total de mensagens cortadas: {self.mensagensCortadas}
        ''')
