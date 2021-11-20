#importacoes

import pygame
from pygame.constants import K_LEFT
from suporte import  importar_pasta_lista,configuracao



class Jogador(pygame.sprite.Sprite):
    def __init__(self,pos):
        super().__init__()
        #teclas
        self.tecla_direita=configuracao['tecla_direita']
        self.tecla_esquerda=configuracao['tecla_esquerda']

        #sons
        self.pulo_sfx=pygame.mixer.Sound('assets/sons/sfx/pulo.mp3')
        
        #animacao
        self.importar_assets_jogador()
        self.frame_index=0 
        self.animacao_vel=0.12
        self.image=self.animacoes['parado'][self.frame_index]
        self.rect =self.image.get_rect(topleft=pos)

        #movimentaçao 
        self.velocidade=8
        self.gravidade=0.8
        self.atura_pulo=-16
        self.direcao=pygame.math.Vector2(0,0)

        #estados
        self.estado='parado'
        self.face_direita=True
        self.encostando_chao=False
        self.encostando_teto=False
        self.encostando_dir=False
        self.encostando_esq=False

    def importar_assets_jogador(self):
        
        diretorio_sprites='assets/jogador/'
        self.animacoes={'andar':[],'caindo':[],'correr':[],'morrer':[],'parado':[],'pulo':[]}

        for animacao in self.animacoes.keys():
            caminho_compelto=diretorio_sprites + animacao  #adicionando o nome da chave
            self.animacoes[animacao]=importar_pasta_lista(caminho_compelto)
            
    def animar_jogador(self):

        animacao=self.animacoes[self.estado]
        self.frame_index+=self.animacao_vel

        if self.frame_index>len(animacao):
            self.frame_index=0

        try:
            self.image=animacao[int(self.frame_index)]
        except IndexError as erro:
            print("Ocorreu um erro de animacao")
            pass
        

        if not self.face_direita:
            self.image=pygame.transform.flip(self.image,True,False)

        #ajustar rect

        #no chao
        if self.encostando_chao and self.encostando_dir:
            self.rect=self.image.get_rect(bottomright=self.rect.bottomright)

        elif self.encostando_chao and self.encostando_esq:
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft)
       
        elif self.encostando_chao:
             self.rect=self.image.get_rect(midbottom=self.rect.midbottom)
       #no teto
        elif self.encostando_teto and self.encostando_dir:
            self.rect=self.image.get_rect(topright=self.rect.topright)

        elif self.encostando_teto and self.encostando_esq:
            self.rect=self.image.get_rect(topleft=self.rect.topleft)
       
        elif self.encostando_teto:
             self.rect=self.image.get_rect(midtop=self.rect.midtop)


    def evento_teclado(self):
        
        letras=pygame.key.get_pressed()

        if letras[pygame.key.key_code(self.tecla_direita)]:
            self.face_direita=True
            self.direcao.x=1

        elif letras[pygame.key.key_code(self.tecla_esquerda)]:
            self.face_direita=False
            self.direcao.x=-1

        else:
            self.direcao.x=0

        if letras[pygame.K_SPACE]:
            if self.encostando_chao:
             self.velocidade=self.velocidade/4
             self.pular() 


    def obter_estado(self):

        if self.direcao.y<0:
            self.estado='pulo'
            self.animacao_vel=0
            
        elif self.direcao.y>1:  #apenas colocar a animaçao se cair de lugar alto
             self.estado='caindo'
             self.animacao_vel=0
        else:
            if self.direcao.x!=0:
                self.estado='correr'
                self.animacao_vel=0.22
            else:
                self.estado='parado'
                self.animacao_vel=0.12

        
    def colisao_inimigo(self,inimigos):
        for inimigo in inimigos:
            if self.rect.colliderect(inimigo):
                return True
            else:
                return False
        
    def aplicar_gravidade(self):
         self.direcao.y+=self.gravidade
         self.rect.y+=self.direcao.y

    def pular(self):
        self.direcao.y+=self.atura_pulo
        self.pulo_sfx.play()



    def update(self):
        self.evento_teclado()
        self.obter_estado()
        self.animar_jogador()
        
       