import random
from enemy import Enemy
from settings import WIDTH, HEIGHT

class Spawner:
    def __init__(self, target):
        self.target = target

    def spawn_enemy(self, enemy_group, amount):
        for _ in range(amount):
            side = random.choice(['top', 'bottom', 'left', 'right'])
            if side == 'top':
                pos = (random.randint(0, WIDTH), -30)
            elif side == 'bottom':
                pos = (random.randint(0, WIDTH), HEIGHT + 30)
            elif side == 'left':
                pos = (-30, random.randint(0, HEIGHT))
            else:
                pos = (WIDTH + 30, random.randint(0, HEIGHT))
            enemy = Enemy(pos, self.target)
            enemy_group.add(enemy)
