import pygame
import random

# Dimensiones de la pantalla
WIDTH = 800
HEIGHT = 600
# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clase para la paleta del jugador
class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

# Clase para la pelota
class Ball(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speed = 5
        self.dx = random.choice([-1, 1]) * self.speed
        self.dy = random.choice([-1, 1]) * self.speed

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        # Rebote en los bordes superior e inferior
        if self.rect.y <= 0 or self.rect.y >= HEIGHT - self.rect.height:
            self.dy *= -1

# Inicialización de Pygame
pygame.init()

# Configuración de la pantalla
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Pong")

fontPuntos = pygame.font.Font(None, 30)
fontTitulo = pygame.font.Font(None, 45)

# Creación de los sprites
all_sprites = pygame.sprite.Group()
paddle1 = Paddle(WHITE, 10, 100)
paddle1.rect.x = 20
paddle1.rect.y = HEIGHT // 2 - 50
paddle2 = Paddle(WHITE, 10, 100)
paddle2.rect.x = WIDTH - 30
paddle2.rect.y = HEIGHT // 2 - 50
ball = Ball(WHITE, 10, 10)
ball.rect.x = WIDTH // 2
ball.rect.y = HEIGHT // 2
all_sprites.add(paddle1, paddle2, ball)

clock = pygame.time.Clock()
done = False
puntos1 = 0
puntos2 = 0
total1 = 0
total2 = 0
ronda = 1
text_inicio = fontTitulo.render(f'Presiona espacio para jugar', True, WHITE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
           
    screen.blit(text_inicio, (200, HEIGHT//2-20))
    # Dibujar los sprites
    all_sprites.remove(ball)
    all_sprites.draw(screen)

    keys = pygame.key.get_pressed()
    pygame.display.flip()
    # Limitar el número de fotogramas por segundo
    clock.tick(60)
    if keys[pygame.K_SPACE]:
        break

all_sprites.add(ball)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True


    # Movimiento de las paletas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddle1.rect.y -= 5
    if keys[pygame.K_s]:
        paddle1.rect.y += 5
    if keys[pygame.K_UP]:
        paddle2.rect.y -= 5
    if keys[pygame.K_DOWN]:
        paddle2.rect.y += 5

    # Mantener las paletas dentro de la pantalla
    paddle1.rect.y = max(0, min(HEIGHT - paddle1.rect.height, paddle1.rect.y))
    paddle2.rect.y = max(0, min(HEIGHT - paddle2.rect.height, paddle2.rect.y))

    # Actualizar la posición de la pelota
    ball.update()

    if ball.rect.x > WIDTH - ball.rect.height:
        puntos1 += 1
        ball.rect.x = WIDTH // 2
        ball.rect.y = HEIGHT // 2
        if puntos1 == 10:
            puntos1 = 0
            puntos2 = 0
            ronda += 1
            total1 += 1


    if ball.rect.x < 0:
        puntos2 += 1
        ball.rect.x = WIDTH // 2
        ball.rect.y = HEIGHT // 2
        if puntos2 == 10:
            puntos2 = 0
            puntos1 = 0
            ronda += 1
            total2 += 1

    

    # Colisión con las paletas
    if pygame.sprite.collide_rect(ball, paddle1) or pygame.sprite.collide_rect(ball, paddle2):
        ball.dx *= -1

    # Limpiar la pantalla
    screen.fill(BLACK)
    # Dibujar los sprites
    all_sprites.draw(screen)

    #Mostrar textos
    text_inicio = fontTitulo.render(f'Ronda: {ronda}', True, WHITE)
    screen.blit(text_inicio, (350, 18))

    text_1 = fontPuntos.render(f'Jugador 1: {puntos1}', True, WHITE)
    screen.blit(text_1, (10, 18))

    text_2 = fontPuntos.render(f'Jugador 2: {puntos2}', True, WHITE)
    screen.blit(text_2, (WIDTH-150, 18))

    text_1 = fontPuntos.render(f'Total: {total1}', True, WHITE)
    screen.blit(text_1, (10, 38))

    text_2 = fontPuntos.render(f'Total: {total2}', True, WHITE)
    screen.blit(text_2, (WIDTH-150, 38))


    # Actualizar la pantalla
    pygame.display.flip()
    # Limitar el número de fotogramas por segundo
    clock.tick(75)

pygame.quit()
