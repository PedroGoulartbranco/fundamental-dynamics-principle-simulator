import pygame

class Carro():
    def __init__(self, posicao_x, posicao_y, massa):
        self.x = posicao_x
        self.y = posicao_y
        self.massa = massa
        self.velocidade = 0
        self.acelaracao = 0
        self.forca = 0

LARGURA_TELA = 900
ALTURA_TELA = 800

grupo_carros = pygame.sprite.Group()

carro_1 = Carro(posicao_x=100, posicao_y=500, massa=30)
carro_2 = Carro(posicao_x=100, posicao_y=500, massa=30)

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 15

pygame.init()
tela = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
rodando= True

while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tela.fill("black")

    pygame.display.flip()

    clock.tick(30)

pygame.quit()