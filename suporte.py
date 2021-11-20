#importacoes
import pygame
from pygame import image
from pygame.constants import MOUSEBUTTONDOWN
from pygame.image import load
from os import truncate, walk 
from csv import reader
#modulo que da funcoes de sistema
#retorna informacoes sobre ficheiros 
#_ nao importa com o que esta sendo retornado

def importar_pasta_lista(pasta):
    lista_superfice=[]
    for _,__,img_infos in walk(pasta):
        for img in img_infos:
            caminho_img=pasta + '/' + img
            img_superfice=pygame.image.load(caminho_img).convert_alpha()
            lista_superfice.append(img_superfice)
    return lista_superfice

def importar_pasta_dicionario(pasta):
    dicionario_superfice={}
    for _,__,img_infos in walk(pasta):
        for img in img_infos:
            caminho_img=pasta + '/' + img
            img_superfice=pygame.image.load(caminho_img).convert_alpha()
            chave=img[0:len(img)-4]
            dicionario_superfice[chave]=img_superfice
    return dicionario_superfice

#crias teste caso nao for uma imagem
def  importar_csv(ficheiro):
        nivel_mapa=[]
        with open(ficheiro) as mapa:
            nivel=reader(mapa,delimiter=',')
            for linha in nivel:
                nivel_mapa.append(list(linha))
        return nivel_mapa
            
class Botao():
    def __init__(self,tamanho,pos):
        super().__init__()
        self.tamanho=tamanho
        self.pos=pos

 

    def desenhar(self,superfice):
        pygame.draw.rect(superfice,(255,0,0),(self.pos,self.tamanho),0)



    def contacto(self,pos):
        if pos[0]>self.pos[0]and pos[0]<self.tamanho[0]+self.pos[0]:
             if pos[1]>self.pos[1]and pos[1]<self.tamanho[1]+self.pos[1]:
                 return True
        return False



configuracao={'musica':True,'tecla_direita':'d','tecla_esquerda':'q'}





