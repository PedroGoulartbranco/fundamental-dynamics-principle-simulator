import pygame
import matplotlib.pyplot as plt

PIXEL_POR_METRO = 100

class Carro(pygame.sprite.Sprite):
    def __init__(self, posicao_x, posicao_y, massa, cor, lado):
        super().__init__()
        self.x = (posicao_x / PIXEL_POR_METRO)
        self.y = posicao_y

        self.posicao_inicial_x = (posicao_x / PIXEL_POR_METRO)
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
        self.rect = self.image.get_rect(topleft=(self.x * 100, self.y))

        self.velocidade_final = 0

    def calcular_acelaracao(self, forca):
        self.acelaracao = (forca / self.massa)
    def update(self, dt):
        if self.lado == "esquerdo":
            self.velocidade += self.acelaracao * dt
        else:
            self.velocidade -= self.acelaracao * dt
        self.x += self.velocidade * dt

        self.rect.x = int(self.x * PIXEL_POR_METRO)
    def reiniciar(self):
        self.velocidade_final = self.velocidade
        self.velocidade = 0
        self.acelaracao = 0
    def realocar(self):
        self.x = self.posicao_inicial_x
        self.y = self.posicao_inicial_y

        self.rect.x = (self.x * PIXEL_POR_METRO)
        self.rect.y = self.y

def gerar_grafico(lista_x, lista_y_1, lista_y_2, titulo, legenda_x, legenda_y, massa_1, massa_2, forca):
    plt.figure(figsize=(8, 5))

    plt.plot(lista_x, lista_y_1, label="Carro 1", color="blue")
    plt.plot(lista_x, lista_y_2, label="Carro 2", color="red")

    plt.title(titulo)
    plt.xlabel(legenda_x)
    plt.ylabel(legenda_y)

    info_texto = (
        f"Parâmetros:\n• Força ($F$): {forca} N\n• Massa 1 ($m_1$):"
        f" {massa_1} kg\n• Massa 2 ($m_2$): {massa_2} kg"
    )

    plt.gca().text(
        0.03,
        0.65,
        info_texto,
        transform=plt.gca().transAxes,
        fontsize=10,
        verticalalignment="top",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="white", edgecolor="gray", alpha=0.9),
    )

    plt.legend(loc="upper right")
    plt.grid(True)
    plt.savefig("grafico_velocidade1.png", dpi=300, bbox_inches="tight")
    plt.show()

def reiniciar_simulacao(carro_1, carro_2, simulacao_ocorreu, comecou_simulacao, tempo_decorrido,  tempo_decorrido_pause, tempo_ultima_adicao_lista, lista_velocidade_carro_1, lista_velocidade_carro_2, lista_tempo):
    carro_1.realocar()
    carro_2.realocar()
    simulacao_ocorreu = False
    comecou_simulacao = False
    tempo_decorrido = 0
    tempo_decorrido_pause = 0
    tempo_ultima_adicao_lista = 0
    
    lista_velocidade_carro_1 = []
    lista_velocidade_carro_2 = []
    lista_tempo = []

    return simulacao_ocorreu, comecou_simulacao, tempo_decorrido,  tempo_decorrido_pause, tempo_ultima_adicao_lista, lista_velocidade_carro_1, lista_velocidade_carro_2, lista_tempo

LARGURA_TELA = 1000
ALTURA_TELA = 600

grupo_carros = pygame.sprite.Group()

massa_1 = 32
massa_2 = 32

carro_1 = Carro(posicao_x=150, posicao_y=500, massa=massa_1, cor="#5c9feb", lado="esquerdo")
carro_2 = Carro(posicao_x=790, posicao_y=500, massa=massa_2, cor="#f34949", lado="direito")

grupo_carros.add(carro_1)
grupo_carros.add(carro_2)

forca_elastico = 10

pygame.init()
clock = pygame.time.Clock()
pygame.key.set_repeat(300, 150)
tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Simulador Principio Fundamental da Dinamica")
clock = pygame.time.Clock()
fonte_lateral = pygame.font.SysFont("arial", 20)
rodando= True

comecou_simulacao = False
inicio_simulacao = fim_simulacao = tempo_decorrido = tempo_antes_pause = 0
simulacao_ocorreu = False
simulador_pausado = False
inicio_tempo_pause = fim_tempo_pause = tempo_decorrido_pause = 0

x_coluna_texto = 20
y_espacamento = 45
y_texto_inicial = 20

numero_carro_1_surface = fonte_lateral.render("1", True, "#070707")
rect_numero_1_carro = numero_carro_1_surface.get_rect()

numero_carro_2_surface = fonte_lateral.render("2", True, "#070707")
rect_numero_2_carro = numero_carro_1_surface.get_rect()

lista_tempo = []
tempo_ultima_adicao_lista = 0
intervalo_entre_adicoes_tempo = 0.01
lista_velocidade_carro_1 = []
lista_velocidade_carro_2 = []
pode_gerar_grafico = False

dt = 0 

def calcular_distancia():
    return (carro_2.rect.left - carro_1.rect.right) / PIXEL_POR_METRO
distancia_carrinhos = calcular_distancia()

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                if comecou_simulacao is False and simulacao_ocorreu is False:
                    comecou_simulacao =  not comecou_simulacao
                elif comecou_simulacao is True and simulacao_ocorreu is False:
                    simulador_pausado = not simulador_pausado
            elif evento.key == pygame.K_RETURN:
                if simulacao_ocorreu:
                    carro_1.realocar()
                    carro_2.realocar()
                    simulacao_ocorreu = False
                    comecou_simulacao = False
                    tempo_decorrido = 0
                    tempo_decorrido_pause = 0
                    tempo_ultima_adicao_lista = 0

                    lista_velocidade_carro_1 = []
                    lista_velocidade_carro_2 = []
                    lista_tempo = []

                    distancia_carrinhos = calcular_distancia()
                elif simulador_pausado:
                    simulacao_ocorreu, comecou_simulacao, tempo_decorrido,  tempo_decorrido_pause, tempo_ultima_adicao_lista, lista_velocidade_carro_1, lista_velocidade_carro_2, lista_tempo = reiniciar_simulacao(carro_1, carro_2, simulacao_ocorreu, comecou_simulacao, tempo_decorrido,  tempo_decorrido_pause, tempo_ultima_adicao_lista, lista_velocidade_carro_1, lista_velocidade_carro_2, lista_tempo)
                    simulador_pausado = False
            elif evento.key == pygame.K_LEFT:
                if forca_elastico > 1:
                    forca_elastico -= 1
            elif evento.key == pygame.K_RIGHT:
                forca_elastico += 1
            elif evento.key == pygame.K_g:
                if simulacao_ocorreu and pode_gerar_grafico:
                        gerar_grafico(lista_tempo, lista_velocidade_carro_1, lista_velocidade_carro_2, 
                            titulo="Gráfico 1: Velocidade vs. Tempo",
                            legenda_x="Tempo (s)",
                            legenda_y="Velocidade (m/s)",
                            massa_1=carro_1.massa,
                            massa_2=carro_2.massa,
                            forca=forca_elastico)
                        pode_gerar_grafico = False
                elif simulacao_ocorreu:
                    pode_gerar_grafico = True
                    gerar_grafico(lista_tempo, lista_velocidade_carro_1, lista_velocidade_carro_2, 
                                                titulo="Gráfico 1: Velocidade vs. Tempo",
                                                legenda_x="Tempo (s)",
                                                legenda_y="Velocidade (m/s)",
                                                massa_1=carro_1.massa,
                                                massa_2=carro_2.massa,
                                                forca=forca_elastico)
                    pode_gerar_grafico = False
            elif evento.key == pygame.K_UP:
                if (pygame.key.get_mods() & pygame.KMOD_SHIFT) :
                    carro_2.massa += 1
                else:
                    carro_1.massa += 1
            elif evento.key == pygame.K_DOWN:
                if (pygame.key.get_mods() & pygame.KMOD_SHIFT) :
                    carro_2.massa -= 1
                else:
                    carro_1.massa -= 1
    dt = clock.tick(60) / 1000.0

    tela.fill("black")
    for carro in grupo_carros:
        carro.calcular_acelaracao(forca_elastico)

    texto_lateral = [
        f"Tempo Duração: {tempo_decorrido:.2f}s",
        f"Pause: {simulador_pausado}",
        f"Massa 1: {carro_1.massa:.2f}Kg",
        f"Massa 2: {carro_2.massa:.2f}Kg",
        f"Força Aplicada: {forca_elastico:.1f}N",
        f"Aceleração 1: {carro_1.acelaracao:.2f} m/s²",
        f"Aceleração 2: {carro_2.acelaracao:.2f} m/s²",
    ]

    texto_lateral_direito = [
        f"Distância: {distancia_carrinhos:.2f}m",
        f"Velocidade 1: {carro_1.velocidade:.2f}m/s",
        f"Velocidade 2: {carro_2.velocidade:.2f}m/s"
    ]

    for i, linha in enumerate(texto_lateral):
        texto_surf = fonte_lateral.render(linha, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(x=x_coluna_texto, y=y_texto_inicial+ (i * y_espacamento))
        tela.blit(texto_surf, texto_rect)

    if simulacao_ocorreu:
        texto_lateral_direito.append(f"Velocidade Final 1: {carro_1.velocidade_final:.2f}m/s")
        texto_lateral_direito.append(f"Velocidade Final 2: {carro_2.velocidade_final:.2f}m/s")
    for i, linha in enumerate(texto_lateral_direito):
        texto_surf = fonte_lateral.render(linha, True, (255, 255, 255))
        texto_rect = texto_surf.get_rect(x=700, y=y_texto_inicial+ (i * y_espacamento))
        tela.blit(texto_surf, texto_rect)

    pygame.draw.rect(tela, "white", (0, 535, 1000, 10))

    grupo_carros.draw(tela)

    rect_numero_1_carro.center = carro_1.rect.center
    rect_numero_2_carro.center = carro_2.rect.center
    
    tela.blit(numero_carro_1_surface, rect_numero_1_carro)
    tela.blit(numero_carro_2_surface, rect_numero_2_carro)

    if comecou_simulacao:
        if simulador_pausado is False:
            grupo_carros.update(dt)
            distancia_carrinhos = calcular_distancia()
            if distancia_carrinhos < 0:
                distancia_carrinhos = 0
            tempo_decorrido += dt
            if tempo_decorrido - tempo_ultima_adicao_lista >= intervalo_entre_adicoes_tempo:
                lista_tempo.append(tempo_decorrido)
                lista_velocidade_carro_1.append(carro_1.velocidade)
                lista_velocidade_carro_2.append(carro_2.velocidade * -1)
                tempo_ultima_adicao_lista = tempo_decorrido
            if carro_1.rect.colliderect(carro_2.rect):
                comecou_simulacao = False
                simulacao_ocorreu = True
            
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

                pode_gerar_grafico = True

    pygame.display.flip()

pygame.quit()