import pygame, random

blocoChao = pygame.image.load("assets/bloco_chao.png")
blocoChao = pygame.transform.scale(blocoChao, (100, 100))

def gerarMapa(tamanho, probBuraco=0.1, larguraBuracoMax=3, probPlataforma=0.15):
    mapa = []
    i = 0

    while i < tamanho:
        if random.random() < probBuraco:
            larguraBuraco = random.randint(1, larguraBuracoMax)
            for _ in range(larguraBuraco):
                if i < tamanho:
                    mapa.append({"chao": 0, "plataforma": 0})
                    i += 1
        else:
            bloco = {"chao": 1, "plataforma": 0}

            if random.random() < probPlataforma:
                larguraPlataforma = random.randint(2, 4)
                altura = random.randint(1, 2)  # Altura mais próxima do chão
                for j in range(larguraPlataforma):
                    if i + j < tamanho:
                        mapa.append({"chao": 1, "plataforma": altura})
                i += larguraPlataforma
                continue
            else:
                mapa.append(bloco)
                i += 1

    return mapa


def desenharMapa(tela, mapa, blocoChao, yChao, cameraX):
    for i, bloco in enumerate(mapa):
        x = i * blocoChao.get_width()

        # Desenha o chão
        if bloco["chao"] == 1:
            tela.blit(blocoChao, (x - cameraX, yChao))

        # Desenha a plataforma (altura 1 = mais próxima do chão, altura 3 = mais alta)
        if bloco["plataforma"] > 0:
            altura = bloco["plataforma"]
            yPlataforma = yChao - altura * 150  # Ajuste esse valor para controlar altura real
            tela.blit(blocoChao, (x - cameraX, yPlataforma))


def verificarColisaoComBlocos(mapa, blocoImg, personagemRect, yChao, cameraX, velocidadeVertical):
    bloco_width = blocoImg.get_width()
    bloco_height = blocoImg.get_height()
    
    # Converter para coordenadas do mundo
    world_persona_rect = personagemRect.move(cameraX, 0)
    
    # Calcular blocos relevantes para verificar
    start_block = max(0, (world_persona_rect.left // bloco_width) - 1)
    end_block = min(len(mapa), (world_persona_rect.right // bloco_width) + 2)
    
    for i in range(start_block, end_block):
        if i >= len(mapa):
            continue
        
        bloco = mapa[i]
        
        # Verificar colisão com chão
        if bloco["chao"] == 1:
            bloco_rect = pygame.Rect(i * bloco_width, yChao, bloco_width, bloco_height)
            if world_persona_rect.colliderect(bloco_rect):
                # Só considera colisão se estiver caindo e a base do personagem estiver acima do bloco
                if velocidadeVertical >= 0 and (world_persona_rect.bottom - bloco_rect.top) <= 20:
                    return {
                        "rect": pygame.Rect(i * bloco_width - cameraX, yChao, bloco_width, bloco_height),
                        "tipo": "chao"
                    }
        
        # Verificar colisão com plataformas
        if bloco["plataforma"] > 0:
            altura = bloco["plataforma"]
            yPlataforma = yChao - altura * 150
            plataforma_rect = pygame.Rect(i * bloco_width, yPlataforma, bloco_width, bloco_height)
            if world_persona_rect.colliderect(plataforma_rect):
                # Verifica se está caindo e se está vindo de cima
                if velocidadeVertical >= 0 and (world_persona_rect.bottom - plataforma_rect.top) <= 20:
                    return {
                        "rect": pygame.Rect(i * bloco_width - cameraX, yPlataforma, bloco_width, bloco_height),
                        "tipo": "plataforma"
                    }
    
    return None




