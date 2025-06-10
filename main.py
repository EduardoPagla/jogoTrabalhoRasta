import pygame
import random
import os
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.desenharMapa import desenharMapa, gerarMapa, verificarColisaoComBlocos
import json
print("Inicializando o Jogo! Criado por Eduardo PH")
print("Aperte Enter para iniciar o jogo")
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
pygame.display.set_caption("Cabeça de Gelo!")
icone  = pygame.image.load("assets/icone.png")
pygame.display.set_icon(icone)
branco = (255,255,255)
preto = (0, 0 ,0 )
rasta = pygame.image.load("assets/rasta.png")
rasta = pygame.transform.scale(rasta, (120, 150))
fundoStart = pygame.image.load("assets/fundoStart.png")
fundoStart = pygame.transform.scale(fundoStart, (1000, 700))
fundoJogo = pygame.image.load("assets/fundoJogo.png")
fundoJogo = pygame.transform.scale(fundoJogo, (1000, 700))
fundoDead = pygame.image.load("assets/fundoDead.png")
blocoChao = pygame.image.load("assets/bloco_chao.png")
blocoChao = pygame.transform.scale(blocoChao, (100, 100))
mapa = gerarMapa(50, 0.05)
missel = pygame.image.load("assets/missile.png")
missileSound = pygame.mixer.Sound("assets/missile.wav")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
fonteMenu = pygame.font.SysFont("comicsans",18)
fonteMorte = pygame.font.SysFont("arial",120)
pygame.mixer.music.load("assets/ironsound.mp3")

def jogar():
    larguraJanela = 300
    alturaJanela = 50
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    cameraX = 0
    velocidadeVertical = 0
    gravidade = 0.8
    pulando = False
    yChao = 620

    def obter_nome():
        global nome
        nome = entry_nome.get()  # Obtém o texto digitado
        if not nome:  # Se o campo estiver vazio
            messagebox.showwarning("Aviso", "Por favor, digite seu nome!")  # Exibe uma mensagem de aviso
        else:
            #print(f'Nome digitado: {nome}')  # Exibe o nome no console
            root.destroy()  # Fecha a janela após a entrada válida

    # Criação da janela principal
    root = tk.Tk()
    # Obter as dimensões da tela
    larguraTela = root.winfo_screenwidth()
    alturaTela = root.winfo_screenheight()
    posX = (larguraTela - larguraJanela) // 2
    posY = (alturaTela - alturaJanela) // 2
    root.geometry(f"{larguraJanela}x{alturaJanela}+{posX}+{posY}")
    root.title("Informe seu nickname")
    root.protocol("WM_DELETE_WINDOW", obter_nome)

    # Entry (campo de texto)
    entry_nome = tk.Entry(root)
    entry_nome.pack()

    # Botão para pegar o nome
    botao = tk.Button(root, text="Enviar", command=obter_nome)
    botao.pack()

    # Inicia o loop da interface gráfica
    root.mainloop()
    
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    pontos = 0
    larguraPersona = 120
    alturaPersona = 150
    larguraHitbox = larguraPersona
    alturaHitbox = alturaPersona
    larguraMissel  = 80
    alturaMissel  = 250
    dificuldade  = 30

    pausado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RIGHT:
                    movimentoXPersona = 15
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -15
                elif evento.key == pygame.K_SPACE and not pulando:
                    velocidadeVertical = -15
                    pulando = True
                elif evento.key == pygame.K_ESCAPE:
                    pausado = not pausado
            elif evento.type == pygame.KEYUP:
                if evento.key in [pygame.K_RIGHT, pygame.K_LEFT]:
                    movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona
        cameraX = posicaoXPersona - tamanho[0] // 2
        if cameraX < 0:
            cameraX = 0

        if pausado:
            tela.fill(branco)
            tela.blit(fundoJogo, (0,0) )
            tela.blit(rasta, (posicaoXPersona - cameraX, posicaoYPersona))
            tela.blit(missel, (posicaoXMissel - cameraX, posicaoYMissel))
            desenharMapa(tela, mapa, blocoChao, 650, cameraX)
            texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
            tela.blit(texto, (15,15))

            overlay = pygame.Surface(tamanho)
            overlay.set_alpha(180) 
            overlay.fill((0, 0, 0))
            tela.blit(overlay, (0, 0))

            fontePause = pygame.font.SysFont("arial", 50, bold=True)
            texto_pausa = fontePause.render("JOGO PAUSADO", True, (255, 255, 255))
            texto_instrucao = fonteMenu.render("Aperte ESC para continuar", True, (200, 200, 200))
            tela.blit(texto_pausa, (tamanho[0] // 2 - texto_pausa.get_width() // 2, 250))
            tela.blit(texto_instrucao, (tamanho[0] // 2 - texto_instrucao.get_width() // 2, 320))

            pygame.display.update()
            relogio.tick(15)
            continue     

        velocidadeVertical += gravidade
        posicaoYPersona += velocidadeVertical
       
        margemLateral = (larguraPersona - larguraHitbox) // 2

        if posicaoXPersona < -margemLateral:
            posicaoXPersona = -margemLateral
        
        tela.fill(branco)
        tela.blit(fundoJogo, (0,0) )
        desenharMapa(tela, mapa, blocoChao, yChao, cameraX)
        tela.blit(rasta, (posicaoXPersona - cameraX, posicaoYPersona))
        
        posicaoYMissel = posicaoYMissel + velocidadeMissel

        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos + 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(cameraX, cameraX + tamanho[0])
            pygame.mixer.Sound.play(missileSound)
            
        tela.blit(missel, (posicaoXMissel - cameraX, posicaoYMissel))

        
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (15,15))
        
        rect_persona = pygame.Rect(
        posicaoXPersona - cameraX,
        posicaoYPersona,
        larguraHitbox,
        alturaHitbox
    )

        if velocidadeVertical >= 0:
            blocoColidido = verificarColisaoComBlocos(mapa, blocoChao, rect_persona, yChao, cameraX)
            if blocoColidido:
                posicaoYPersona = blocoColidido.top - alturaPersona
                velocidadeVertical = 0
                pulando = False
                posicaoYPersona = blocoColidido.top - alturaPersona + 1 

        rect_missel = pygame.Rect(posicaoXMissel - cameraX, posicaoYMissel, larguraMissel, alturaMissel)

        if rect_persona.colliderect(rect_missel):
            escreverDados(nome, pontos)
            dead()

        else:
            print("Ainda Vivo")
        
        pygame.draw.rect(tela, (255, 0, 0), rect_persona, 2)

        pygame.draw.rect(tela, (0, 255, 0), pygame.Rect(
        rect_missel.x - cameraX, rect_missel.y, rect_missel.width, rect_missel.height), 2)

        # Gera novos blocos se o jogador estiver próximo do fim do mapa
        comprimentoMapaAtual = len(mapa)
        blocosVisiveis = tamanho[0] // 100 + 5  # Quantos blocos aparecem na tela
        ultimoBlocoVisivel = (cameraX // 100) + blocosVisiveis

        if ultimoBlocoVisivel >= comprimentoMapaAtual:
            novosBlocos = gerarMapa(10, 0.05)
            mapa.extend(novosBlocos)

        pygame.display.update()
        relogio.tick(60)

def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
        tela.fill(branco)
        tela.blit(fundoStart, (0,0) )

        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        
        pygame.display.update()
        relogio.tick(60)


def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    
    
    root = tk.Tk()
    root.title("Tela da Morte")

    # Adiciona um título na tela
    label = tk.Label(root, text="Log das Partidas", font=("Arial", 16))
    label.pack(pady=10)

    # Criação do Listbox para mostrar o log
    listbox = tk.Listbox(root, width=50, height=10, selectmode=tk.SINGLE)
    listbox.pack(pady=20)

    # Adiciona o log das partidas no Listbox
    log_partidas = open("base.atitus", "r").read()
    log_partidas = json.loads(log_partidas)
    for chave in log_partidas:
        listbox.insert(tk.END, f"Pontos: {log_partidas[chave][0]} na data: {log_partidas[chave][1]} - Nickname: {chave}")  # Adiciona cada linha no Listbox
    
    root.mainloop()
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
                    
    
        tela.fill(branco)
        tela.blit(fundoDead, (0,0) )

        
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))

    
        pygame.display.update()
        relogio.tick(60)


start()

