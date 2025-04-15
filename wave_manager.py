import pygame

from settings import WAVE_INTERVAL

class WaveManager:
    def __init__(self):
        self.wave = 0
        self.timer = 0
        self.last_wave_time = 0
        self.spawn_timer = 0
        self.spawn_interval = 2  # tempo entre spawns dentro da wave

    def update(self, dt, spawner, enemy_group):
        seconds = dt / 1000
        self.timer += seconds
        self.spawn_timer += seconds

        # spawn contínuo durante a wave
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer = 0
            amount = 1 + self.wave  # mais inimigos por wave
            spawner.spawn_enemy(enemy_group, amount)

        # nova wave
        if self.timer - self.last_wave_time >= WAVE_INTERVAL:
            self.wave += 1
            self.last_wave_time = self.timer
            self.scale_difficulty()

    def scale_difficulty(self):
        import settings
        settings.ENEMY_HEALTH += 5 * self.wave
        settings.ENEMY_DAMAGE += 2 * self.wave  # novo parâmetro de dano

    def force_first_wave(self, spawner, enemy_group):
        self.wave = 1
        self.last_wave_time = 0
        self.timer = 0
        self.spawn_timer = 0
        self.scale_difficulty()
        spawner.spawn_enemy(enemy_group, self.wave)

    def get_time_remaining(self):
        remaining = WAVE_INTERVAL - (self.timer - self.last_wave_time)
        return max(0, int(remaining))

    def get_wave(self):
        return self.wave
