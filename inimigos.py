
#importacoes
import pygame
from suporte import  importar_pasta_lista
from random import choice,randint

class Inimigo(pygame.sprite.Sprite):
    def __init__(self,pos,velociade):
        super().__init__()
        
        #animacao
        self.animacoes={'correr':[],'morrer':[]}
        self.importar_assets_inimigo()
        self.frame_index=0 
        self.animacao_vel=0.10

        #estado
        self.estado='correr'
        self.image=self.animacoes['correr'][self.frame_index]
        self.face_direita=True

        #ajuste pos
        self.pos=pos
        self.rect =self.image.get_rect(topleft=self.pos)
        self.rect.y-=14

        #sons
        self.zombi_sfx=[pygame.mixer.Sound('assets/sons/sfx/zombi1.mp3'),pygame.mixer.Sound('assets/sons/sfx/zombi2.mp3')]
    


        #movimentaçao 
        self.velocidade=velociade
        

    def animar_inimigo(self):
        animacao=self.animacoes[self.estado]
        self.frame_index+=self.animacao_vel

        if self.frame_index>len(animacao):
            self.frame_index=0

        try:
            self.image=animacao[int(self.frame_index)]

            if not self.face_direita:
                 self.image=pygame.transform.flip(self.image,True,False)
        except IndexError as erro:
            print("Ocorreu um erro de animacao-inimigo")
            pass   

    def importar_assets_inimigo(self):
        
        diretorio_sprites='assets/zumbi/'
        self.animacoes={'correr':[],'morrer':[]}

        for animacao in self.animacoes.keys():
            caminho_compelto=diretorio_sprites + animacao  
            self.animacoes[animacao]=importar_pasta_lista(caminho_compelto)

    def efeito_sonoro(self):
        if randint(1,250)==1:
            som=choice(self.zombi_sfx)  
            som.play()      
    def verificar_face(self,barreiras):
        for barreira in barreiras:
            if self.rect.colliderect(barreira)and self.face_direita:
                self.face_direita=False
            elif self.rect.colliderect(barreira)and not self.face_direita:
                self.face_direita=True
            else:
                pass

    def update(self,delocamento,barreiras):
        self.animar_inimigo()
        self.efeito_sonoro()
        self.verificar_face(barreiras)
        

        self.rect.x+=delocamento

        if self.face_direita:
            self.rect.x+=self.velocidade
        else:

            self.rect.x-=self.velocidade
        
        