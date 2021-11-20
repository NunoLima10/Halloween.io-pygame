
import pygame
from suporte import  importar_pasta_dicionario
from mapa_niveis import tamanho_bloco


class Bloco(pygame.sprite.Sprite):
    def __init__(self,pos,tamanho,tipo):
        super().__init__()

        self.importar_blocos_assets()
        self.image=self.blocos_assets[tipo]
        self.image=pygame.transform.scale(self.image,(tamanho,tamanho))
        self.rect=self.image.get_rect(topleft=pos)
        
        #para testes
        #self.image=pygame.Surface((tamanho,tamanho))
        #self.image.fill('grey')
        #self.rect=self.image.get_rect(topleft=pos)

    def importar_blocos_assets(self):

        diretorio_blocos='assets/mapaassets/blocos'
        self.blocos_assets=importar_pasta_dicionario(diretorio_blocos)
        
    def desenhar_blocos(self,tela):
     pass

    
    def update(self,deslocamento):
        self.rect.x+=deslocamento
        

class Decoracao(pygame.sprite.Sprite):
    def __init__(self,pos,tipo):
        super().__init__()

        self.importar_decoracao_assets()
        self.image=self.decoracao_assets[tipo]

        tamanho_x=pygame.Surface.get_width(self.image)
        tamanho_y=pygame.Surface.get_height(self.image)
        tamanho_x=int(tamanho_x/2)
        tamanho_y=int(tamanho_y/2)
        self.image=pygame.transform.scale(self.image,(tamanho_x,tamanho_y))

        self.rect=self.image.get_rect(midbottom=pos)
        
        self.rect.y=self.rect.y+tamanho_bloco
       

    def importar_decoracao_assets(self):

        diretorio_blocos='assets/mapaassets/decoracao'
        self.decoracao_assets=importar_pasta_dicionario(diretorio_blocos)
        
    
    def update(self,deslocamento):
        self.rect.x+=deslocamento
        