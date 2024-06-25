import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SHIP_SIZE = 30
ASTEROID_SIZE = 50
BULLET_SIZE = 5
SHIP_SPEED = 5
BULLET_SPEED = 10
ASTEROID_SPEED = 3

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((SHIP_SIZE, SHIP_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.speed = SHIP_SPEED
        self.angle = 0
        self.shoot_delay = 250  # milliseconds
        self.last_shot = pygame.time.get_ticks()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle += 5
        if keys[pygame.K_RIGHT]:
            self.angle -= 5
        if keys[pygame.K_UP]:
            rad = math.radians(self.angle)
            self.rect.x -= self.speed * math.sin(rad)
            self.rect.y -= self.speed * math.cos(rad)
        if keys[pygame.K_SPACE]:
            self.shoot()

        self.rect.x %= SCREEN_WIDTH
        self.rect.y %= SCREEN_HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            bullet = Bullet(self.rect.center, self.angle)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot = now

# Asteroid class
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((ASTEROID_SIZE, ASTEROID_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = ASTEROID_SPEED
        self.angle = random.randint(0, 360)

    def update(self):
        rad = math.radians(self.angle)
        self.rect.x += self.speed * math.sin(rad)
        self.rect.y += self.speed * math.cos(rad)
        self.rect.x %= SCREEN_WIDTH
        self.rect.y %= SCREEN_HEIGHT

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, angle):
        super().__init__()
        self.image = pygame.Surface((BULLET_SIZE, BULLET_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=position)
        self.speed = BULLET_SPEED
        self.angle = angle

    def update(self):
        rad = math.radians(self.angle)
        self.rect.x -= self.speed * math.sin(rad)
        self.rect.y -= self.speed * math.cos(rad)
        if not screen.get_rect().contains(self.rect):
            self.kill()

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player and asteroids
player = Player()
all_sprites.add(player)
for _ in range(10):
    asteroid = Asteroid()
    all_sprites.add(asteroid)
    asteroids.add(asteroid)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Collision detection
    hits = pygame.sprite.groupcollide(bullets, asteroids, True, True)
    if pygame.sprite.spritecollideany(player, asteroids):
        running = False

    screen.fill(BLACK)
    all_sprites.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
