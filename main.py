import pygame
import time

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
    def reiniciar(self):
        self.velocidade = 0
        self.acelaracao = 0

LARGURA_TELA = 1000
ALTURA_TELA = 600

grupo_carros = pygame.sprite.Group()

massa_1 = 30
massa_2 = 30

carro_1 = Carro(posicao_x=150, posicao_y=500, massa=massa_1, cor="#5c9feb", lado="esquerdo")
carro_2 = Carro(posicao_x=790, posicao_y=500, massa=massa_2, cor="#f34949", lado="direito")

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 15

pygame.init()
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Simulador Principio Fundamental da Dinamica")
clock = pygame.time.Clock()
rodando= True

comecou_simulacao = False
inicio_simulacao = fim_simulacao = tempo_decorrido = 0

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
                        inicio_simulacao = time.perf_counter()
                print(comecou_simulacao)
    tela.fill("black")
    pygame.draw.rect(tela, "white", (0, 535, 1000, 10))

    grupo_carros.draw(tela)

    if comecou_simulacao:
        grupo_carros.update()
        if carro_1.rect.colliderect(carro_2.rect):
            fim_simulacao = time.perf_counter()
            comecou_simulacao = False
            tempo_decorrido = fim_simulacao - inicio_simulacao
            print(tempo_decorrido)
            carro_1.reiniciar()
            carro_2.reiniciar()

            sobreposicao = carro_1.rect.right - carro_2.rect.left

            massa_total = carro_1.massa + carro_2.massa

            proporcao_1 = carro_2.massa / massa_total
            proporcao_2 = carro_1.massa / massa_total

            carro_1.rect.x -= sobreposicao * proporcao_1
            carro_1.x = carro_1.rect.x

            carro_2.rect.x += sobreposicao * proporcao_2
            carro_2.x = carro_2.rect.x

    pygame.display.flip()

    clock.tick(30)

pygame.quit()