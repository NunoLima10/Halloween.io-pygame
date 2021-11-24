# importacoes
import pygame
from niveis import Nivel
from pygame.constants import MOUSEBUTTONDOWN
from suporte import Botao, configuracao
from mapa_niveis import nivel_0, nivel_1, nivel_2
from pygame.locals import *

clock = pygame.time.Clock()

pygame.init()


def jogar(tela, _nivel):
    niveis = [nivel_0, nivel_1, nivel_2]
    nivel_atual = _nivel
    nivel = Nivel(niveis[nivel_atual], tela)

    # camda 0
    # fundo_estatico=pygame.image.load('assets/mapaassets/fundos/fundoestatico.png').convert_alpha()
    fundo_estatico = pygame.image.load('assets/mapaassets/bg1.png').convert_alpha()
    x_pos = 0
    y_pos = -50

    # camada1
    # fundo1=pygame.image.load('assets/mapaassets/fundos/fundo1.png').convert_alpha()
    # fundo2=pygame.image.load('assets/mapaassets/fundos/fundo1.png').convert_alpha()
    # vel_fundo=50
    # pos_fundo1=fundo1.get_rect()
    # pos_fundo2=fundo2.get_rect()
    # pos_fundo2.right-=1251

    # camada2
    # frente1=pygame.image.load('assets/mapaassets/fundos/frente.png').convert_alpha()

    # frente2=pygame.image.load('assets/mapaassets/fundos/frente.png').convert_alpha()
    # vel_frente=30
    # pos_frente1=frente1.get_rect()
    # pos_frente2=frente2.get_rect()
    # pos_frente2.left+=1251

    on = True
    while on:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                nivel.musica.fadeout(1000)
                on = False

        tela.blit(fundo_estatico, (x_pos, y_pos))

        # animar camada 1

        # pos_fundos=nivel.animar_background(tela,pos_fundo1,pos_fundo2,vel_fundo)
        # pos_fundo1=pos_fundos[0]
        # pos_fundo2=pos_fundos[1]
        # tela.blit(fundo1,pos_fundo1)
        # tela.blit(fundo2,pos_fundo2)

        # animar camda 2

        # pos_frentes=nivel.animar_background(tela,pos_frente1,pos_frente2,vel_frente)
        # pos_frente1=pos_frentes[0]
        # pos_frente2=pos_frentes[1]
        # tela.blit(frente1,pos_frente1)
        # tela.blit(frente2,pos_frente2)

        game_over = nivel.atualizar()
        if game_over == 'perdeu':
            return
        elif game_over == 'ganhou':
            if nivel_atual == len(niveis) - 1:
                ganhar_sfx = pygame.mixer.Sound('assets/sons/sfx/ganhar.mp3')
                ganhar_sfx.set_volume(0.3)
                ganhar_sfx.play()
                return
            else:
                nivel_atual += 1
                nivel = Nivel(niveis[nivel_atual], tela)
                x_pos -= 500
        pygame.display.update()


def tela_estatica(tela, imagem):
    background = pygame.image.load(imagem).convert()
    go = True
    while go:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                go = False
            if event.type == pygame.QUIT:
                exit()
        tela.blit(background, (0, 0))
        pygame.display.update()


def ajuste(tela, imagem, musica):
    background = pygame.image.load(imagem).convert()
    clique_sfx = pygame.mixer.Sound('assets/sons/sfx/clique.mp3')
    botao_sair = Botao((60, 60), (5, 12))
    botao_azert = Botao((50, 50), (707, 502))
    botao_qazert = Botao((50, 50), (975, 500))
    botao_musica = Botao((50, 50), (375, 500))

    if configuracao['tecla_esquerda'] == 'a':
        botao_img = pygame.image.load('assets/menu/qzert.png').convert_alpha()
    else:
        botao_img = pygame.image.load('assets/menu/azert.png').convert_alpha()

    on = True
    while on:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and botao_sair.contacto(mouse_pos):
                    clique_sfx.play()
                    on = False
                if botao_musica.contacto(mouse_pos) and configuracao['musica']:
                    configuracao['musica'] = False
                    musica.fadeout(1000)
                    clique_sfx.play()
                elif botao_musica.contacto(mouse_pos) and not configuracao['musica']:
                    configuracao['musica'] = True
                    clique_sfx.play()
                    musica.play(-1)
                elif event.button == 1 and botao_azert.contacto(mouse_pos):
                    botao_img = pygame.image.load('assets/menu/azert.png').convert_alpha()
                    clique_sfx.play()
                    configuracao['tecla_direita'] = 'd'
                    configuracao['tecla_esquerda'] = 'q'
                elif event.button == 1 and botao_qazert.contacto(mouse_pos):
                    botao_img = pygame.image.load('assets/menu/qzert.png').convert_alpha()
                    clique_sfx.play()
                    configuracao['tecla_direita'] = 'd'
                    configuracao['tecla_esquerda'] = 'a'

        tela.blit(background, (0, 0))
        tela.blit(botao_img, (0, 0))
        if configuracao['musica']:
            musica_on = pygame.image.load('assets/menu/commusica.png').convert_alpha()
            tela.blit(musica_on, (0, 0))
        # botoes
        # botao_sair.desenhar(tela)
        # botao_azert.desenhar(tela)
        # botao_qazert.desenhar(tela)
        # botao_musica.desenhar(tela)
        pygame.display.update()
