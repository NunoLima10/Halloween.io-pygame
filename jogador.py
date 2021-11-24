import pygame
from suporte import importar_pasta_lista


class Jogador(pygame.sprite.Sprite):

    animacoes: dict
    frame_index: int
    animacao_vel: int
    estado: str
    face_direita: bool
    estados: list
    gravidade: float
    atura_pulo: int
    direcao: pygame.math.Vector2


    def __init__(self, pos: tuple) -> None:
        super().__init__()
        # sons
        self.pulo_sfx = pygame.mixer.Sound('assets/sons/sfx/pulo.mp3')
        # animacao
        self.importar_assets_jogador()
        self.frame_index = 0
        self.animacao_vel = 0.12
        self.image = self.animacoes['parado'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        # movimentaçao
        self.velocidade = 8
        self.gravidade = 0.8
        self.atura_pulo = -16
        self.direcao = pygame.math.Vector2(0, 0)
        # estados
        self.estado = 'parado'
        self.face_direita = True
        self.estados = {
            "face_direita": True,
            "encostando_chao": False,
            "encostando_teto": False,
            "encostando_dir": False,
            "encostando_esq": False
        }

    def importar_assets_jogador(self) -> None:
        self.animacoes = {'andar': [], 'caindo': [], 'correr': [], 'morrer': [], 'parado': [], 'pulo': []}
        for animacao in self.animacoes.keys():
            self.animacoes[animacao] = importar_pasta_lista('assets/jogador/' + animacao)

    def animar_jogador(self) -> None:
        self.frame_index += self.animacao_vel
        if self.frame_index > len(self.animacoes[self.estado]):
            self.frame_index = 0
        self.image = self.animacoes[self.estado][int(self.frame_index)]
        if not self.face_direita:
            self.image = pygame.transform.flip(self.image, True, False)

        # no chao
        if self.estados["encostando_chao"] and self.estados["encostando_dir"]:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.estados["encostando_chao"] and self.estados["encostando_esq"]:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.estados["encostando_chao"]:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        # no teto
        elif self.estados["encostando_teto"] and self.estados["encostando_dir"]:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.estados["encostando_teto"] and self.estados["encostando_esq"]:
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
        elif self.estados["encostando_teto"]:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def evento_teclado(self) -> None:
        if pygame.key.get_pressed()[pygame.K_d]:
            self.face_direita = True
            self.direcao.x = 1
        elif pygame.key.get_pressed()[pygame.K_q]:
            self.face_direita = False
            self.direcao.x = -1
        else:
            self.direcao.x = 0
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.estados["encostando_chao"]:
                self.velocidade = self.velocidade / 4
                self.pular()

    def obter_estado(self) -> None:
        if self.direcao.y < 0:
            self.estado = 'pulo'
            self.animacao_vel = 0

        elif self.direcao.y > 1:  # apenas colocar a animaçao se cair de lugar alto
            self.estado = 'caindo'
            self.animacao_vel = 0
        else:
            if self.direcao.x != 0:
                self.estado = 'correr'
                self.animacao_vel = 0.22
            else:
                self.estado = 'parado'
                self.animacao_vel = 0.12

    def colisao_inimigo(self, inimigos) -> None:
        for inimigo in inimigos:
            if self.rect.colliderect(inimigo):
                return True
        return False

    def aplicar_gravidade(self) -> None:
        self.direcao.y += self.gravidade
        self.rect.y += self.direcao.y

    def pular(self) -> None:
        self.direcao.y += self.atura_pulo
        self.pulo_sfx.play()

    def update(self) -> None:
        self.evento_teclado()
        self.obter_estado()
        self.animar_jogador()
