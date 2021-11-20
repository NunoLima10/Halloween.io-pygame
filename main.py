#Importaçoes
import pygame 
from sys import exit
from pygame.constants import MOUSEBUTTONDOWN
from  mapa_niveis import *
from suporte import Botao
from pygame.locals import *
from telas import jogar,tela_estacica,ajuste,clock

#Nuno Lima 
#terminado primeira versao 03/11/21


#Inicializaçao
pygame.init()
pygame.mixer.pre_init()
nivel_inicial=0

tela =pygame.display.set_mode((tela_largura,tela_altura))
pygame.display.set_caption('Halloween.io')
icon=pygame.image.load('assets/logo.png')
pygame.display.set_icon(icon)

#imagens
imagem='assets/menu/menu.png'
background=pygame.image.load(imagem).convert()
 
#sons
selecionar_sfx=pygame.mixer.Sound('assets/sons/sfx/selecionar.mp3')
clique_sfx=pygame.mixer.Sound('assets/sons/sfx/clique.mp3')
bg_musica=pygame.mixer.Sound('assets/sons/musicas/menubg.mp3')
bg_musica_on=False

#estados
jogo_on=True
clique=False

#botoes
botao1=Botao((250,80),(150,290))#jogar
botao2=Botao((250,80),(150,400))#ajuste
botao3=Botao((250,80),(150,510))#creditos

while jogo_on:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            jogo_on=False 
            pygame.quit()
        if event.type==MOUSEBUTTONDOWN:
            if event.button==1:
                clique=True

    if not bg_musica_on:
        bg_musica_on=True
        bg_musica.play()
        
                
    
    try:
         mouse_pos=pygame.mouse.get_pos() 
    except:
            pass

      #cursor selecionado
    if botao1.contacto(mouse_pos):
          if imagem!='assets/menu/menujogar.png':
              selecionar_sfx.play()

          imagem='assets/menu/menujogar.png'
          background=pygame.image.load(imagem).convert()

    elif botao2.contacto(mouse_pos):
           if imagem!='assets/menu/menuajuste.png':
              selecionar_sfx.play()
              
           imagem='assets/menu/menuajuste.png'
           background=pygame.image.load(imagem).convert()

    elif botao3.contacto(mouse_pos):
         if imagem!='assets/menu/menucreditos.png':
             selecionar_sfx.play()

         imagem='assets/menu/menucreditos.png'
         background=pygame.image.load(imagem).convert()
    else:
        imagem='assets/menu/menu.png'
        background=pygame.image.load(imagem).convert()

     #cursor clique
    if botao1.contacto(mouse_pos) and clique:
         clique_sfx.play()

         bg_musica.fadeout(1000)
         bg_musica_on=False
         jogar(tela,nivel_inicial)

    elif botao2.contacto(mouse_pos) and clique:
        clique_sfx.play()

        image_tela='assets/menu/ajuste.png'
        configuracoa=ajuste(tela,image_tela,bg_musica)

    elif botao3.contacto(mouse_pos) and clique:
        clique_sfx.play()

        image_tela='assets/menu/creditos.png'
        tela_estacica(tela,image_tela)
          
    
    tela.blit(background,(0,0))
    #botoes
    #botao1.desenhar(tela)
    #botao2.desenhar(tela)
    #botao3.desenhar(tela)
    clique=False #reset clique 
    pygame.display.update() #atualizar a tela
    clock.tick(60)# limitar fps
    