import pygame
from suporte import importar_pasta_lista
from random import choice, randint


class Inimigo(pygame.sprite.Sprite):

    animacoes: dict
    frame_index: int
    animacao_vel: int
    estado: str
    face_direita: bool
    zombi_sfx: pygame.mixer.Sound

    def __init__(self, pos: tuple, velociade: int):
        super().__init__()
        # animacao
        self.animacoes = {'correr': [], 'morrer': []}
        self.importar_assets_inimigo()
        self.frame_index = 0
        self.animacao_vel = 0.10
        # estado
        self.estado = 'correr'
        self.image = self.animacoes['correr'][self.frame_index]
        self.face_direita = True
        # ajuste pos
        self.pos = pos
        self.rect = self.image.get_rect(topleft=self.pos)
        self.rect.y -= 14
        # sons
        self.zombi_sfx = [pygame.mixer.Sound('assets/sons/sfx/zombi1.mp3'),
                          pygame.mixer.Sound('assets/sons/sfx/zombi2.mp3')]
        # movimentaçao
        self.velocidade = velociade

    def animar_inimigo(self) -> None:
        self.frame_index += self.animacao_vel
        if self.frame_index > len(self.animacoes[self.estado]):
            self.frame_index = 0
        self.image = self.animacoes[self.estado][int(self.frame_index)]
        if not self.face_direita:
            self.image = pygame.transform.flip(self.image, True, False)

    def importar_assets_inimigo(self) -> None:
        self.animacoes = {'correr': [], 'morrer': []}
        for animacao in self.animacoes.keys():
            caminho_compelto = 'assets/zumbi/' + animacao
            self.animacoes[animacao] = importar_pasta_lista(caminho_compelto)

    def efeito_sonoro(self) -> None:
        if randint(1, 250) == 1:
            som = choice(self.zombi_sfx)
            som.play()

    def verificar_face(self, barreiras: list) -> None:
        for barreira in barreiras:
            if self.rect.colliderect(barreira) and self.face_direita:
                self.face_direita = False
            elif self.rect.colliderect(barreira) and not self.face_direita:
                self.face_direita = True

    def update(self, deslocamento: int, barreiras: list) -> None:
        self.animar_inimigo()
        self.efeito_sonoro()
        self.verificar_face(barreiras)
        self.rect.x += deslocamento
        if self.face_direita:
            self.rect.x += self.velocidade
        else:
            self.rect.x -= self.velocidade
