import logging
import socket
import random
import time
import json
import os
from datetime import datetime

caminho_arquivo = "EP1\\config.json"

# Ler o arquivo JSON
if os.path.exists(caminho_arquivo):
    with open(os.getcwd() + "\\" + caminho_arquivo) as arquivo:
        dados_config = json.load(arquivo)

        # Obter valores do arquivo de configuração
        prob_eliminar_mensagem = dados_config['Probabilidades']['eliminar_mensagem']
        prob_duplicar_mensagem = dados_config['Probabilidades']['duplicar_mensagem']
        prop_corromper_byte = dados_config['Probabilidades']['corromper_byte']
        milesegundos_delay = dados_config['Tempo']['delay']
        cortar_bytes = dados_config['Bytes']['cortar']
else:
    print(f'O arquivo {caminho_arquivo} não foi encontrado.')

class Canal():
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = None

    def associarSocketPorta(self):
        # Vincular o socket ao endereço e porta
        self.__socket.bind((self.host, self.port))
    
    def definirTimeout(self, timeout: float):
        self.__socket.settimeout(timeout)

    def enviar(self, monitor, mensagem: bytes, address: tuple = None):
        '''Envia dados ao servidor/cliente e aguarda uma resposta'''

        mensagemEliminada, mensagem = monitor.consolidarErros(mensagem, address)
        
        if mensagemEliminada:
            return 0

        if address is None:
            return self.__socket.sendto(mensagem, (self.host, self.port))
        else:
            return self.__socket.sendto(mensagem, (address[0], address[1]))
    
    def receber(self) -> tuple:
        ''' Recebe dados do servidor/cliente e retorna o endereço do servidor/cliente '''

        dados, socket_address = bytes(), self.address
        
        try:
            dados, socket_address = self.__socket.recvfrom(1024)

            self.address = socket_address

        except socket.timeout as e:
            logging.error(f"Timeout ao esperar retorno do servidor: {e}")
            print("---" * 20)

        except socket.error as e:
            logging.error(f"Erro de socket: {e}")

        except Exception as e:
            logging.error(f"Outro exceção: {e}")

        finally:
            return dados, socket_address

    def criarPropriedade(self):
        return self.Propiedades()

    def juntarPropriedadeGeralComParcial(self, monitorGeral, monitorParcial):
        monitorGeral.mensagensTotal += monitorParcial.mensagensTotal
        monitorGeral.mensagensEliminadas += monitorParcial.mensagensEliminadas
        monitorGeral.mensagensAtrasadas += monitorParcial.mensagensAtrasadas
        monitorGeral.mensagensDuplicadas += monitorParcial.mensagensDuplicadas
        monitorGeral.mensagensCorrompidas += monitorParcial.mensagensCorrompidas
        monitorGeral.mensagensCortadas += monitorParcial.mensagensCortadas

    class Propiedades():
        def __init__(self):
            super().__init__()
            self.mensagensTotal = 0
            self.mensagensEliminadas = 0
            self.mensagensAtrasadas = 0
            self.mensagensDuplicadas = 0
            self.mensagensCorrompidas = 0
            self.mensagensCortadas = 0
            self.mensagens = []

        def __eliminarMensagem(self, probabilidade: float) -> bool:
            '''Pocentagem de 0 a 100'''

            resultado = random.uniform(0, 1)
            
            if resultado <= (probabilidade/100):

                self.mensagensEliminadas += 1

                return True
            
            return False

        def __delay(self, mile: float) -> None:
            '''delay de milesegundos'''
            
            time.sleep(mile/1000)
            self.mensagensAtrasadas += 1

        def __duplicarSegmento(self, probabilidade: float, dado: bytes) -> bytes:
            '''Pocentagem de 0 a 100'''

            resultado = random.uniform(0, 1)
            
            if resultado <= (probabilidade/100):
                
                self.mensagensDuplicadas += 1

                return dado + dado, True
            
            return dado, False

        def __corromperByte(self, probabilidade: float, dado: bytes):
            '''Corrompe 1 byte do dado aleatoriamente'''
            
            resultado = random.uniform(0, 1)
            
            if resultado <= (probabilidade/100):
                
                dadoComrrompido = list(dado)

                index = dadoComrrompido.index(dadoComrrompido[random.randint(0, len(dadoComrrompido) - 1)])
                #dadoComrrompido[index] = random.randint(0, 255) tratar para aceitar dessa maneira
                dadoComrrompido[index] += 1

                self.mensagensCorrompidas += 1

                return bytes(dadoComrrompido), True
            
            return dado, False

        def __cortarBytes(self, tamanho: int, dado: bytes):
            ''' Corta o dados maiores que tamanho em bytes'''
            
            dadoCortado = dado
            dadoList = list(dado)
            
            if len(dadoList) > tamanho:
                
                dadoCortado = dadoList[0:tamanho]

                self.mensagensCortadas += 1

                return bytes(dadoCortado), True
            
            return dado, False

        def consolidarErros(self, dados: bytes, address: tuple) -> tuple:

            self.mensagensTotal += 1

            eliminarMensagem = self.__eliminarMensagem(prob_eliminar_mensagem)
            if eliminarMensagem:
                self.mensagens.append("Eliminada")
                print(f"{address} - Erros adicionados na mensagem: [{self.Cor.VERMELHO}{", ".join(self.mensagens)}{self.Cor.RESET}]")
                self.mensagens = []
                return 1, dados

            self.__delay(milesegundos_delay)
            self.mensagens.append("Delay")

            dados, duplicado = self.__duplicarSegmento(prob_duplicar_mensagem, dados)
            if duplicado:
                self.mensagens.append("Duplicada")

            dados, corrompido = self.__corromperByte(prop_corromper_byte, dados)
            if corrompido:
                self.mensagens.append("Corrompida")

            dados, cortada = self.__cortarBytes(cortar_bytes, dados)
            if cortada:
                self.mensagens.append("Cortada")

            print(f"{address} - Erros adicionados na mensagem: [{self.Cor.VERMELHO}{", ".join(self.mensagens)}{self.Cor.RESET}]")
            self.mensagens = []
            
            return 0, dados

        def ImprimirErros(self):
            print( "\n" + "---" * 5 + " Consolidação de erros " + "---" * 5)
            print(f'''
            Total de mensagens enviadas: {self.mensagensTotal}
            Total de mensagens eliminadas: {self.mensagensEliminadas}
            Total de mensagens atrasadas: {self.mensagensAtrasadas}
            Total de mensagens duplicadas: {self.mensagensDuplicadas}
            Total de mensagens corrompidas: {self.mensagensCorrompidas}
            Total de mensagens cortadas: {self.mensagensCortadas}
            ''')
            print("---" * 18)

        class Cor:
            RESET = '\033[0m'
            VERMELHO = '\033[91m'
            VERDE = '\033[92m'
            AMARELO = '\033[93m'
            AZUL = '\033[94m'
            ROXO = '\033[95m'
            CIANO = '\033[96m'
            BRANCO = '\033[97m'
