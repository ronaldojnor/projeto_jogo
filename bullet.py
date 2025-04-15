import pygame
import math
from settings import BULLET_SPEED, WHITE, WIDTH, HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        rad = math.radians(-angle)
        self.velocity = pygame.math.Vector2(math.cos(rad), math.sin(rad)) * BULLET_SPEED

    def update(self, dt):
        self.pos += self.velocity
        self.rect.center = self.pos
        if (self.rect.right < 0 or self.rect.left > WIDTH or
            self.rect.bottom < 0 or self.rect.top > HEIGHT):
            self.kill()
