import pygame

class Carro(pygame.sprite.Sprite):
    def __init__(self, posicao_x, posicao_y, massa, cor, lado):
        super().__init__()
        self.x = posicao_x
        self.y = posicao_y
        self.massa = massa
        self.velocidade = 0
        self.acelaracao = 0
        self.forca = 0
        self.lado =  lado

        self.comprimento = 60
        self.altura = 35

        self.image = pygame.Surface((self.comprimento, self.altura))
        self.image.fill(cor)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    def calcular_acelaracao(self, forca):
        self.acelaracao = forca / self.massa
    def update(self):
        if self.lado == "esquerdo":
            self.velocidade += self.acelaracao
        else:
            self.velocidade -= self.acelaracao
        self.x += self.velocidade

        self.rect.x = self.x

LARGURA_TELA = 1000
ALTURA_TELA = 600

grupo_carros = pygame.sprite.Group()

carro_1 = Carro(posicao_x=150, posicao_y=500, massa=30, cor="#5c9feb", lado="esquerdo")
carro_2 = Carro(posicao_x=790, posicao_y=500, massa=30, cor="#f34949", lado="direito")

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 15

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Simulador Principio Fundamental da Dinamica")
clock = pygame.time.Clock()
rodando= True

comecou_simulacao = False

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if comecou_simulacao is False:
                    comecou_simulacao =  not comecou_simulacao
                    for carro in grupo_carros:
                        carro.calcular_acelaracao(forca_elastico)
                print(comecou_simulacao)
    tela.fill("black")
    pygame.draw.rect(tela, "white", (0, 535, 1000, 10))

    grupo_carros.update()
    grupo_carros.draw(tela)

    pygame.display.flip()

    clock.tick(30)

pygame.quit()