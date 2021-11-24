# importacoes
from random import choice
import pygame
from inimigos import Inimigo
from jogador import Jogador
from mapa_niveis import *
from blocos import Bloco, Decoracao
from mapa_niveis import tamanho_bloco
from suporte import importar_csv, configuracao


# calsse nivel
class Nivel:
    jogador: Jogador
    musica: pygame.mixer.Sound
    inimigos: pygame.sprite.Group
    bloco_final: pygame.sprite.GroupSingle
    blocos: pygame.sprite.Group
    barreiras: pygame.sprite.Group

    def __init__(self, nivel_mapa, superfice):
        self.superfice = superfice
        self.desenhar_mapa(nivel_mapa)
        self.deslocamento_mapa = 0
        self.pos_x_atual = 0

        self.bg_1 = pygame.image.load('assets/mapaassets/fundos/bg1.png')
        self.bg_2 = pygame.image.load('assets/mapaassets/fundos/bg2.png')
        self.bg_3 = pygame.image.load('assets/mapaassets/fundos/bg3.png')

        self.musicas = [pygame.mixer.Sound('assets/sons/musicas/musica1.mp3'),
                        pygame.mixer.Sound('assets/sons/musicas/musica2.mp3'),
                        pygame.mixer.Sound('assets/sons/musicas/musica3.mp3')]
        self.colocar_muscica()

        self.blocos_na_tela = pygame.sprite.Group()

    def colocar_muscica(self):
        if configuracao['musica']:
            self.musica = choice(self.musicas)
            self.musica.set_volume(0.2)
            self.musica.play()

    def animar_background(self, tela, fundo1, fundo2, velocidade):
        jogador = self.jogador.sprite
        if jogador.direcao.x > 0:
            fundo1.left += jogador.velocidade / velocidade
            fundo2.left += jogador.velocidade / velocidade
        elif jogador.direcao.x < 0:
            fundo1.left -= jogador.velocidade / velocidade
            fundo2.left -= jogador.velocidade / velocidade
        fundo1.right = 0 if fundo1.left >= tela_largura else fundo1.right
        fundo2.right = 0 if fundo1.left >= tela_largura else fundo2.right
        return [fundo1, fundo2]

    def desenhar_mapa(self, mapa_arquivos):
        configuracao = importar_csv(mapa_arquivos['configuracao'])
        self.configurar_mapa(configuracao)

        decoracao = importar_csv(mapa_arquivos['decoracao'])
        self.desenhar_decoracao(decoracao)

        mapa = importar_csv(mapa_arquivos['terreno'])
        self.desenhar_terreno(mapa)

    def configurar_mapa(self, configuracao):
        self.inimigos = pygame.sprite.Group()
        self.bloco_final = pygame.sprite.GroupSingle()
        self.barreiras = pygame.sprite.Group()

        for linha_index, linha in enumerate(configuracao):
            for coluna_index, coluna in enumerate(linha):
                x, y = coluna_index * tamanho_bloco, linha_index * tamanho_bloco
                if coluna != '-1':
                    if coluna == '3':
                        self.jogador = pygame.sprite.GroupSingle()
                        self.jogador.add(Jogador((x, y)))
                    elif coluna == '4':
                        self.bloco_final.add(Bloco((x, y), tamanho_bloco, '20'))  # bloco.image.fill('red')
                    elif coluna == '2':
                        self.inimigos.add(Inimigo((x, y), 2))
                    elif coluna == '0':
                        self.barreiras.add(Bloco((x, y), tamanho_bloco, '20'))  # bloco.image.fill('red')

    def desenhar_decoracao(self, decoracao):
        self.decoracao = pygame.sprite.Group()
        for linha_index, linha in enumerate(decoracao):
            for coluna_index, coluna in enumerate(linha):
                x, y = coluna_index * tamanho_bloco, linha_index * tamanho_bloco
                if coluna != '-1':
                    self.decoracao.add(Decoracao((x, y), coluna))

    def desenhar_terreno(self, mapa):
        self.blocos = pygame.sprite.Group()
        for linha_index, linha in enumerate(mapa):
            for coluna_index, coluna in enumerate(linha):
                x, y = coluna_index * tamanho_bloco, linha_index * tamanho_bloco
                if coluna != '-1':
                    self.blocos.add(Bloco((x, y), tamanho_bloco, coluna))

    def deslocar_mapa(self):
        jogador = self.jogador.sprite
        jogador_x = jogador.rect.centerx
        jogador_dir = jogador.direcao.x  # que direcao jogador ta se movendo
        if jogador_x < tela_largura / 4 and jogador_dir < 0:
            self.deslocamento_mapa = 8
            jogador.velocidade = 0
        elif jogador_x > tela_largura - (tela_largura / 4) and jogador_dir > 0:
            self.deslocamento_mapa = -8
            jogador.velocidade = 0
        else:
            self.deslocamento_mapa = 0
            jogador.velocidade = 8

    def colisao_horizontal(self):
        jogador = self.jogador.sprite
        jogador.rect.x += jogador.direcao.x * jogador.velocidade
        # verificando colisao com cada bloco
        for sprite in self.blocos.sprites():
            if sprite.rect.colliderect(jogador.rect):
                if jogador.direcao.x < 0:
                    jogador.rect.left = sprite.rect.right + 5
                    jogador.encostando_esq = True
                    self.pos_x_atual = jogador.rect.left
                    # caixa de colisao
                    # pygame.draw.rect(self.superfice,(255,0,0),jogador.rect,2)
                elif jogador.direcao.x > 0:
                    jogador.rect.right = sprite.rect.left - 5
                    jogador.encostando_dir = True
                    self.pos_x_atual = jogador.rect.right
                    # caixa de colisao
                    # pygame.draw.rect(self.superfice,(255,0,0),jogador.rect,2)
        # verificar se jogador ainda esta colidindo
        if jogador.encostando_esq and (jogador.rect.left < self.pos_x_atual or jogador.direcao.x >= 0):
            jogador.encostando_esq = False
        if jogador.encostando_dir and (jogador.rect.right > self.pos_x_atual or jogador.direcao.x <= 0):
            jogador.encostando_dir = False

    def colisao_vertical(self):
        jogador = self.jogador.sprite
        jogador.aplicar_gravidade()
        for sprite in self.blocos.sprites():
            if sprite.rect.colliderect(jogador.rect):
                if jogador.direcao.y > 0:
                    jogador.rect.bottom = sprite.rect.top
                    jogador.direcao.y = 0
                    jogador.encostando_chao = True
                    # caixa de colisao
                    # pygame.draw.rect(self.superfice,(255,0,0),jogador.rect,2)
                    jogador.velocidade = jogador.velocidade * 4 # voltando velocidade ao norma se tocar o chao
                elif jogador.direcao.y < 0:
                    jogador.rect.top = sprite.rect.bottom
                    jogador.direcao.y = 0
                    jogador.encostando_teto = True
                    # caixa de colisao
                    # pygame.draw.rect(self.superfice,(255,0,0),jogador.rect,2)
        # verificar se jogador ainda esta colidindo
        if jogador.encostando_chao and jogador.direcao.y < 0 or jogador.direcao.y > 1:
            jogador.encostando_chao = False
        if jogador.encostando_teto and jogador.direcao.y > 0:
            jogador.encostando_teto = False

    def game_over(self):
        jogador = self.jogador.sprite
        pos_final = self.bloco_final.sprite.rect
        if jogador.rect.y < -100 or jogador.rect.y > tela_altura + 100 or jogador.colisao_inimigo(self.inimigos):
            if configuracao['musica']:
                self.musica.fadeout(1000)
                perder_sfx = pygame.mixer.Sound('assets/sons/sfx/morto.mp3')
                perder_sfx.play()
            return 'perdeu'
        elif jogador.rect.colliderect(pos_final):
            if configuracao['musica']:
                self.musica.fadeout(1000)
            return 'ganhou'
        return 'jogando'

    def ver_blocos_na_tela(self):
        self.blocos_na_tela.empty()
        for bloco in self.blocos.sprites():
            if bloco.rect.left > -100 and bloco.rect.right < tela_largura + 100:
                self.blocos_na_tela.add(bloco)

    def atualizar(self):
        # Mapa
        self.blocos.update(self.deslocamento_mapa)
        self.ver_blocos_na_tela()
        self.blocos_na_tela.draw(self.superfice)

        self.decoracao.update(self.deslocamento_mapa)
        self.decoracao.draw(self.superfice)

        self.bloco_final.update(self.deslocamento_mapa)
        self.bloco_final.draw(self.superfice)

        self.inimigos.update(self.deslocamento_mapa, self.barreiras.sprites())
        self.inimigos.draw(self.superfice)

        self.barreiras.update(self.deslocamento_mapa)
        self.barreiras.draw(self.superfice)

        self.deslocar_mapa()

        # Jogador
        self.colisao_horizontal()
        self.colisao_vertical()
        self.jogador.update()
        self.jogador.draw(self.superfice)
        return self.game_over()
