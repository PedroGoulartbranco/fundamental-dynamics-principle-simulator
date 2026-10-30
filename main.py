import pygame
import time

class Carro(pygame.sprite.Sprite):
    def __init__(self, posicao_x, posicao_y, massa, cor, lado):
        super().__init__()
        self.x = posicao_x
        self.y = posicao_y

        self.posicao_inicial_x = posicao_x
        self.posicao_inicial_y = posicao_y

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

        self.velocidade_final = 0

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
        self.velocidade_final = self.velocidade
        self.velocidade = 0
        self.acelaracao = 0
    def realocar(self):
        self.x = self.posicao_inicial_x
        self.y = self.posicao_inicial_y

        self.rect.x = self.x
        self.rect.y = self.y

LARGURA_TELA = 1000
ALTURA_TELA = 600

grupo_carros = pygame.sprite.Group()

massa_1 = 40
massa_2 = 40

carro_1 = Carro(posicao_x=150, posicao_y=500, massa=massa_1, cor="#5c9feb", lado="esquerdo")
carro_2 = Carro(posicao_x=790, posicao_y=500, massa=massa_2, cor="#f34949", lado="direito")

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 10

pygame.init()
pygame.key.set_repeat(300, 150)
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Simulador Principio Fundamental da Dinamica")
clock = pygame.time.Clock()
fonte_lateral = pygame.font.SysFont("arial", 20)
rodando= True

comecou_simulacao = False
inicio_simulacao = fim_simulacao = tempo_decorrido = 0
simulacao_ocorreu = False

x_coluna_texto = 20
y_espacamento = 45
y_texto_inicial = 20

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if comecou_simulacao is False and simulacao_ocorreu is False:
                    comecou_simulacao =  not comecou_simulacao
                    inicio_simulacao = time.perf_counter()
            elif evento.key == pygame.K_RETURN:
                if simulacao_ocorreu:
                    carro_1.realocar()
                    carro_2.realocar()
                    simulacao_ocorreu = False
                    comecou_simulacao = False
            elif evento.key == pygame.K_LEFT:
                if forca_elastico > 1:
                    forca_elastico -= 1
            elif evento.key == pygame.K_RIGHT:
                forca_elastico += 1

    tela.fill("black")
    for carro in grupo_carros:
        carro.calcular_acelaracao(forca_elastico)

    texto_lateral = [
        f"Tempo Duração: {tempo_decorrido:.2f}s",
        f"Massa 1: {carro_1.massa:.1f}Kg",
        f"Massa 2: {carro_2.massa:.1f}Kg",
        f"Força Aplicada: {forca_elastico:.1f}N",
        f"Aceleração 1: {carro_1.acelaracao:.2f}",
        f"Aceleração 2: {carro_2.acelaracao:.2f}",
        f"Velocidade 1: {carro_1.velocidade:.2f}",
        f"Velocidade 2: {carro_2.velocidade:.2f}"
    ]

    for i, linha in enumerate(texto_lateral):
        texto_surf = fonte_lateral.render(linha, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(x=x_coluna_texto, y=y_texto_inicial+ (i * y_espacamento))
        tela.blit(texto_surf, texto_rect)

    if simulacao_ocorreu:
        texto_lateral_final = [
            f"Velocidade Final Carro 1: {carro_1.velocidade_final:.2f}",
            f"Velocidade Final Carro 2: {carro_2.velocidade_final:.2f}"
        ]
        for i, linha in enumerate(texto_lateral_final):
                texto_surf = fonte_lateral.render(linha, True, (255, 255, 255))
                texto_rect = texto_surf.get_rect(x=700, y=y_texto_inicial+ (i * y_espacamento))
                tela.blit(texto_surf, texto_rect)

    pygame.draw.rect(tela, "white", (0, 535, 1000, 10))

    grupo_carros.draw(tela)

    if comecou_simulacao:
        grupo_carros.update()
        tempo_decorrido = time.perf_counter() - inicio_simulacao
        if carro_1.rect.colliderect(carro_2.rect):
            fim_simulacao = time.perf_counter()
            comecou_simulacao = False
            simulacao_ocorreu = True
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

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
        if teclas[pygame.K_UP]:
            carro_2.massa += 1
        if teclas[pygame.K_DOWN]:
            if carro_2.massa > 1:
                carro_2.massa -= 1
    else:
        if teclas[pygame.K_UP]:
            carro_1.massa += 1
        if teclas[pygame.K_DOWN]:
            if carro_1.massa > 1:
                carro_1.massa -= 1

    pygame.display.flip()

    clock.tick(30)

pygame.quit()