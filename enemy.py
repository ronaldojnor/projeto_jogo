import pygame
import math
import settings



class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, target):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        # Cor do inimigo baseada no dano (quanto maior, mais escuro)
        max_dano = 100
        dano_ratio = min(1, settings.ENEMY_DAMAGE / max_dano)
        cor_base = (255, 0, 0)
        escurecimento = int(200 * dano_ratio)
        cor_final = (
            max(55, cor_base[0] - escurecimento),
            cor_base[1],
            cor_base[2]
        )

        # Criação da imagem com fundo transparente
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, cor_final, (0, 0, 30, 30))  # corpo do inimigo

        # Criar olho brilhante animado
        self.blink_timer = 0
        self.original_color = cor_final

        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.target = target
        self.health = settings.ENEMY_HEALTH
        self.damage = settings.ENEMY_DAMAGE  # cada inimigo carrega seu valor de dano

    def update(self, dt):
        direction = self.target.pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.pos += direction * settings.ENEMY_SPEED
        self.rect.center = self.pos
        # Piscar o olho brilhante
        self.blink_timer += dt
        alpha = 128 + int(127 * math.sin(self.blink_timer / 150))  # varia entre 1 e 255

        eye_color = (255, 255, 255, alpha)
        pygame.draw.circle(self.image, eye_color, (15, 15), 4)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return settings.XP_PER_ENEMY, settings.COINS_PER_ENEMY
        return 0, 0
