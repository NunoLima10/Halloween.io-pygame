import pygame
from sys import exit
from pygame.constants import MOUSEBUTTONDOWN
from mapa_niveis import *
from suporte import Botao
from pygame.locals import *
from telas import jogar, tela_estacica, ajuste, clock

__author__ = "Nuno Lima"
__copyright__ = "Copyright 2021, Nuno Lima"
__version__ = "0.0.1"
__maintainer__ = "Nuno Lima"
__email__ = ""
__status__ = "Production"

pygame.init()
pygame.mixer.pre_init()
nivel_inicial = 0

tela = pygame.display.set_mode((tela_largura, tela_altura))
pygame.display.set_caption('Halloween.io')
icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(icon)

# imagens
url_imagem = 'assets/menu/menu.png'
background = pygame.image.load(url_imagem).convert()

# sons
selecionar_sfx = pygame.mixer.Sound('assets/sons/sfx/selecionar.mp3')
clique_sfx = pygame.mixer.Sound('assets/sons/sfx/clique.mp3')
bg_musica = pygame.mixer.Sound('assets/sons/musicas/menubg.mp3')
bg_musica_on = False

# estados
jogo_on = True
clique = False

# botoes
botao1 = Botao((250, 80), (150, 290))  # jogar
botao2 = Botao((250, 80), (150, 400))  # ajuste
botao3 = Botao((250, 80), (150, 510))  # creditos

while jogo_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            jogo_on = False
            pygame.quit()
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                clique = True
    if not bg_musica_on:
        bg_musica_on = True
        bg_musica.play()

    mouse_pos = pygame.mouse.get_pos()
    # cursor selecionado
    if botao1.contacto(mouse_pos):
        if url_imagem != 'assets/menu/menujogar.png':
            selecionar_sfx.play()
        background = pygame.image.load('assets/menu/menujogar.png').convert()

    elif botao2.contacto(mouse_pos):
        if url_imagem != 'assets/menu/menuajuste.png':
            selecionar_sfx.play()
        background = pygame.image.load('assets/menu/menuajuste.png').convert()

    elif botao3.contacto(mouse_pos):
        if url_imagem != 'assets/menu/menucreditos.png':
            selecionar_sfx.play()
        background = pygame.image.load('assets/menu/menucreditos.png').convert()
    else:
        background = pygame.image.load('assets/menu/menu.png').convert()

    # cursor clique
    if botao1.contacto(mouse_pos) and clique:
        clique_sfx.play()
        bg_musica.fadeout(1000)
        bg_musica_on = False
        jogar(tela, nivel_inicial)

    elif botao2.contacto(mouse_pos) and clique:
        clique_sfx.play()
        configuracoa = ajuste(tela, 'assets/menu/ajuste.png', bg_musica)

    elif botao3.contacto(mouse_pos) and clique:
        clique_sfx.play()
        tela_estacica(tela, 'assets/menu/creditos.png')

    tela.blit(background, (0, 0))
    clique = False  # reset clique
    pygame.display.update()
    clock.tick(60)
