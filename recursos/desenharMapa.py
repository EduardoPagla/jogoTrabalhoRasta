import pygame, random

blocoChao = pygame.image.load("assets/bloco_chao.png")
blocoChao = pygame.transform.scale(blocoChao, (100, 100))

def gerarMapa(tamanho, probBuraco=0.1):

    mapa = []
    for _ in range(tamanho):
        if random.random() < probBuraco:
            mapa.append(0)  
        else:
            mapa.append(1) 
    return mapa

def desenharMapa(tela, mapa, blocoChao, yChao, cameraX):
    for i, bloco in enumerate(mapa):
        if bloco == 1:
            x = i * blocoChao.get_width()
            tela.blit(blocoChao, (x - cameraX, yChao))

def verificarColisaoComBlocos(mapa, blocoImg, personagemRect, yChao, cameraX):
    bloco_width = blocoImg.get_width()
    bloco_height = blocoImg.get_height()
    
    world_persona_rect = personagemRect.move(cameraX, 0)
    
    start_block = max(0, (world_persona_rect.left // bloco_width) - 1)
    end_block = min(len(mapa), (world_persona_rect.right // bloco_width) + 2)
    
    for i in range(start_block, end_block):
        if i < len(mapa) and mapa[i] == 1:
            bloco_rect = pygame.Rect(i * bloco_width, yChao, bloco_width, bloco_height)
            
            if world_persona_rect.colliderect(bloco_rect):
                return pygame.Rect(i * bloco_width - cameraX, yChao, bloco_width, bloco_height)
    
    return None



