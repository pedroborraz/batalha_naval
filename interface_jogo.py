import pygame


def criar_janela():
    pygame.init()
    tela_jogo = pygame.display.set_mode((600, 680))
    pygame.display.set_caption("Batalha Naval")
    relogio_jogo = pygame.time.Clock()
    fonte_pequena = pygame.font.SysFont(None, 20)
    fonte_grande = pygame.font.SysFont(None, 28)
    sons_jogo = carregar_sons()
    return tela_jogo, relogio_jogo, fonte_pequena, fonte_grande, sons_jogo


def carregar_sons():
    sons_jogo = {"acerto": None,
                 "erro": None,
                 "trilha": None,
                 "guerra": None,
                 "mar": None,
                 "colocou": None,
                 "vitoria": None}

    pygame.mixer.init()
    sons_jogo["acerto"] = pygame.mixer.Sound("./sons/acertou.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["acerto"], 0.4)
    sons_jogo["erro"] = pygame.mixer.Sound("./sons/agua.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["erro"], 0.8)
    sons_jogo["trilha"] = pygame.mixer.Sound("./sons/trilha.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["trilha"], 0.2)
    sons_jogo["mar"] = pygame.mixer.Sound("./sons/mar.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["mar"], 0.4)
    sons_jogo["colocou"] = pygame.mixer.Sound("./sons/radar.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["colocou"], 0.5)
    sons_jogo["vitoria"] = pygame.mixer.Sound("./sons/vitoria.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["vitoria"], 0.6)
    sons_jogo["guerra"] = pygame.mixer.Sound("./sons/war.mp3")
    pygame.mixer.Sound.set_volume(sons_jogo["guerra"], 0.1)

    return sons_jogo


def tocar_som(sons_jogo, chave_som, loop=0):
    sons_jogo[chave_som].play(loop)


def obter_parte_navio(tabuleiro, coluna, linha):
    id_navio = tabuleiro[linha][coluna]
    if id_navio == 0:
        return 0
    
    primeira_coluna = coluna
    while primeira_coluna > 0 and tabuleiro[linha][primeira_coluna - 1] == id_navio:
        primeira_coluna -= 1
    
    return coluna - primeira_coluna + 1


def desenhar_grade(tela_jogo, fonte_pequena, tabuleiro, tiros_jogador, esconder=False, celula_ativa=None):
    cor_agua = (9, 36, 59)
    cor_navio = (253, 166, 0)
    cor_acerto = (162, 26, 3)
    cor_erro = (8, 6, 20)
    cor_borda = (0, 0, 0)
    cor_texto = (224, 243, 247)
    imagem_barco = {1: pygame.image.load("./imagens/barco_1.png").convert_alpha(),
                    2: pygame.image.load("./imagens/barco_2.png").convert_alpha(),
                    3: pygame.image.load("./imagens/barco_3.png").convert_alpha()}
    imagem_barco_destruido = {1: pygame.image.load("./imagens/barco_destruido_1.png").convert_alpha(),
                              2: pygame.image.load("./imagens/barco_destruido_2.png").convert_alpha(), 
                              3: pygame.image.load("./imagens/barco_destruido_3.png").convert_alpha()}

    for linha in range(10):
        for coluna in range(10):
            pos_x = 40 + coluna * 52
            pos_y = 40 + linha * 52
            quadrado = pygame.Rect(pos_x, pos_y, 52, 52)
            celula_tem_navio = tabuleiro[linha][coluna] != 0
            celula_foi_atirada = (coluna, linha) in tiros_jogador

            if celula_foi_atirada and celula_tem_navio:
                pygame.draw.rect(tela_jogo, cor_acerto, quadrado)
                parte_navio = obter_parte_navio(tabuleiro, coluna, linha)
                tela_jogo.blit(imagem_barco_destruido[parte_navio], quadrado)
            elif celula_foi_atirada:
                pygame.draw.rect(tela_jogo, cor_erro, quadrado)
            elif celula_tem_navio and not esconder:
                pygame.draw.rect(tela_jogo, cor_navio, quadrado)
                parte_navio = obter_parte_navio(tabuleiro, coluna, linha)
                tela_jogo.blit(imagem_barco[parte_navio], quadrado)
            else:
                pygame.draw.rect(tela_jogo, cor_agua, quadrado)

            pygame.draw.rect(tela_jogo, cor_borda, quadrado, 1)

    if celula_ativa and not esconder:
        coluna_ativa, linha_ativa = celula_ativa
        for parte in range(1, 4):
            coluna = coluna_ativa + parte - 1
            if coluna < 10:
                pos_x = 40 + coluna * 52
                pos_y = 40 + linha_ativa * 52
                tela_jogo.blit(imagem_barco[parte], (pos_x, pos_y))
                pygame.draw.rect(tela_jogo, cor_texto, (pos_x, pos_y, 52, 52), 2)

    letras = "ABCDEFGHIJ"
    for indice in range(10):
        texto_letra = fonte_pequena.render(letras[indice], True, cor_texto)
        tela_jogo.blit(texto_letra, (40 + indice * 52 + (52 - texto_letra.get_width()) // 2, 20)) 
        texto_numero = fonte_pequena.render(str(indice + 1), True, cor_texto)
        tela_jogo.blit(texto_numero, (20, 40 + indice * 52 + (52 - texto_numero.get_height()) // 2)) 


def desenhar_info(tela_jogo, fonte_grande, texto_info):
    cor_fundo = (9, 36, 59)
    cor_texto = (224, 243, 247)
    pygame.draw.rect(tela_jogo, cor_fundo, (0, 600, 600, 80))
    texto_renderizado = fonte_grande.render(texto_info, True, cor_texto)
    tela_jogo.blit(texto_renderizado, (40, 600 + (80 - texto_renderizado.get_height()) // 2))


def tela_inicial(tela_jogo):
    imagem_tela_inicial = pygame.image.load("./imagens/inteiro/tela_inicial.png").convert()
    imagem_tela_inicial = pygame.transform.scale(imagem_tela_inicial, (600, 680))
    tela_jogo.blit(imagem_tela_inicial, (0, 0))


def trans_p2(tela_jogo):
    imagem_trans_p2 = pygame.image.load("./imagens/inteiro/trans_p2.jpeg").convert()
    imagem_trans_p2 = pygame.transform.scale(imagem_trans_p2, (600, 680))
    tela_jogo.blit(imagem_trans_p2, (0, 0))


def trans_batalha(tela_jogo):
    imagem_trans_batalha = pygame.image.load("./imagens/inteiro/trans_batalha.jpeg").convert()
    imagem_trans_batalha = pygame.transform.scale(imagem_trans_batalha, (600, 680))
    tela_jogo.blit(imagem_trans_batalha, (0, 0))


def trans_2(tela_jogo):
    imagem_trans1 = pygame.image.load("./imagens/inteiro/trans_2.jpeg").convert()
    imagem_trans1 = pygame.transform.scale(imagem_trans1, (600, 680))
    tela_jogo.blit(imagem_trans1, (0, 0))


def trans_1(tela_jogo):
    imagem_trans1 = pygame.image.load("./imagens/inteiro/trans_1.jpeg").convert()
    imagem_trans1 = pygame.transform.scale(imagem_trans1, (600, 680))
    tela_jogo.blit(imagem_trans1, (0, 0))


def vitoria(tela_jogo, jogador_vencedor):
    imagem_vitoria = pygame.image.load(f"./imagens/inteiro/vitoria_{jogador_vencedor}.jpeg").convert()
    imagem_vitoria = pygame.transform.scale(imagem_vitoria, (600, 680))
    tela_jogo.blit(imagem_vitoria, (0, 0))
