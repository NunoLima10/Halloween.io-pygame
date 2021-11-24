import pygame
from suporte import importar_pasta_dicionario
from mapa_niveis import tamanho_bloco


class Bloco(pygame.sprite.Sprite):

    image: pygame.transform
    rect: pygame.Rect
    blocos_assets: dict

    def __init__(self, pos: tuple, tamanho: int, tipo: int):
        super().__init__()
        self.importar_blocos_assets()
        self.image = self.blocos_assets[tipo]
        self.image = pygame.transform.scale(self.image, (tamanho, tamanho))
        self.rect = self.image.get_rect(topleft=pos)

        # para testes
        # self.image=pygame.Surface((tamanho,tamanho))
        # self.image.fill('grey')
        # self.rect=self.image.get_rect(topleft=pos)

    def importar_blocos_assets(self) -> None:
        self.blocos_assets = importar_pasta_dicionario('assets/mapaassets/blocos')

    def update(self, deslocamento: int) -> None:
        self.rect.x += deslocamento


class Decoracao(pygame.sprite.Sprite):

    decoracao_assets: dict
    image: pygame.transform
    rect: pygame.Rect

    def __init__(self, pos: tuple, tipo: int) -> None:
        super().__init__()
        self.importar_decoracao_assets()
        self.image = self.decoracao_assets[tipo]
        # Declarando a imagem com um transform scale de acordo com os tamanhos
        # tanto em x como em y
        self.image = pygame.transform.scale(self.image, (int(pygame.Surface.get_width(self.image) / 2), \
                                                         int(pygame.Surface.get_height(self.image) / 2)))
        # Inicializando o rect da imagem
        self.rect = self.image.get_rect(midbottom=pos)
        self.rect.y = self.rect.y + tamanho_bloco

    def importar_decoracao_assets(self) -> None:
        self.decoracao_assets = importar_pasta_dicionario('assets/mapaassets/decoracao')

    def update(self, deslocamento: int) -> None:
        self.rect.x += deslocamento
