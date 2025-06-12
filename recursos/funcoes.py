import os, time, pygame
import json
from datetime import datetime


def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo

def mostrarMensagemMorte(tela, tamanho):
    overlay = pygame.Surface(tamanho)
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    tela.blit(overlay, (0, 0))

    fonteAlerta = pygame.font.SysFont("arial", 60, bold=True)
    textoAlerta = fonteAlerta.render("Olha a pedra!", True, (255, 255, 255))
    tela.blit(textoAlerta, (tamanho[0]//2 - textoAlerta.get_width()//2, tamanho[1]//2 - 30))

    pygame.display.update()
    pygame.time.delay(2000) 
