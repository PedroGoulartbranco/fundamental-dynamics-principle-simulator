import pygame

class Carro(pygame.sprite.Sprite):
    def __init__(self, posicao_x, posicao_y, massa, cor):
        super().__init__()
        self.x = posicao_x
        self.y = posicao_y
        self.massa = massa
        self.velocidade = 0
        self.acelaracao = 0
        self.forca = 0

        self.comprimento = 60
        self.altura = 35

        self.image = pygame.Surface((self.comprimento, self.altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

LARGURA_TELA = 1000
ALTURA_TELA = 600

grupo_carros = pygame.sprite.Group()

carro_1 = Carro(posicao_x=150, posicao_y=500, massa=30, cor="#5c9feb")
carro_2 = Carro(posicao_x=790, posicao_y=500, massa=30, cor="#f34949")

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 15

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
clock = pygame.time.Clock()
rodando= True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tela.fill("black")

    grupo_carros.update()
    grupo_carros.draw(tela)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()