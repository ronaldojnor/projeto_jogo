import pygame
import math
from settings import WIDTH, HEIGHT, PLAYER_SPEED
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 255, 0), [(20, 0), (40, 40), (0, 40)])
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.health = 100
        self.angle = 0
        self.last_shot = 0
        self.shot_interval = 500
        self.double_shot = False
        self.damage = 10  # ✅ novo: valor do dano que o jogador causa

    def update(self, dt, bullets_group):
        self.move()
        self.rotate()
        self.shoot(dt, bullets_group)

    def move(self):
        keys = pygame.key.get_pressed()
        direction = pygame.math.Vector2(0, 0)
        if keys[pygame.K_w]: direction.y = -1
        if keys[pygame.K_s]: direction.y = 1
        if keys[pygame.K_a]: direction.x = -1
        if keys[pygame.K_d]: direction.x = 1
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * PLAYER_SPEED
        self.pos.x = max(0, min(WIDTH, self.pos.x))
        self.pos.y = max(0, min(HEIGHT, self.pos.y))
        self.rect.center = self.pos

    def rotate(self):
        mouse_pos = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_pos[0] - self.pos.x, mouse_pos[1] - self.pos.y
        self.angle = math.degrees(math.atan2(-rel_y, rel_x))
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def shoot(self, dt, bullets_group):
        self.last_shot += dt
        if self.last_shot >= self.shot_interval:
            self.last_shot = 0
            if self.double_shot:
                angle_offset = 10
                bullets_group.add(Bullet(self.rect.center, self.angle - angle_offset))
                bullets_group.add(Bullet(self.rect.center, self.angle + angle_offset))
            else:
                bullets_group.add(Bullet(self.rect.center, self.angle))
