import pygame
from settings import WHITE, GREEN, RED, BLUE, XP_BASE, XP_MULTIPLIER

class UI:
    def __init__(self, font):
        self.font = font
        self.showing_shop = False
        self.shop_options = []
        self.shop_rects = []

    def draw(self, screen, player, xp, xp_needed, coins, wave, wave_time):
        xp_bar_width = 200
        xp_ratio = xp / xp_needed if xp_needed else 1
        pygame.draw.rect(screen, RED, (10, 10, xp_bar_width, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, xp_bar_width * xp_ratio, 20))

        wave_text = self.font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(wave_text, (10, 110))

        wave_text = self.font.render(f"Wave: {wave}", True, WHITE)
        screen.blit(wave_text, (10, 110))

        time_text = self.font.render(f"Tempo p/ próxima: {wave_time}s", True, WHITE)
        screen.blit(time_text, (10, 135))

        xp_text = self.font.render(f"XP: {xp}/{int(xp_needed)}", True, WHITE)
        screen.blit(xp_text, (10, 35))

        coin_text = self.font.render(f"Coins: {coins}", True, BLUE)
        screen.blit(coin_text, (10, 60))

        vida_text = self.font.render(f"Vida: {int(player.health)}", True, RED)
        screen.blit(vida_text, (10, 85))

        if self.showing_shop:
            self.draw_shop_menu(screen)

    def draw_shop_menu(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), (200, 200, 400, 200))
        title = self.font.render("Escolha um upgrade:", True, WHITE)
        screen.blit(title, (220, 210))
        self.shop_rects = []
        for i, option in enumerate(self.shop_options):
            label = self.font.render(f"{i+1}. {option.replace('_', ' ').title()} - {self.shop_prices[option]} moedas", True, WHITE)
            pos = (220, 240 + i * 30)
            screen.blit(label, pos)
            self.shop_rects.append((pygame.Rect(pos[0], pos[1], 360, 30), option))

    def handle_shop_click(self, pos):
        for rect, option in self.shop_rects:
            if rect.collidepoint(pos):
                return option
        return None

class XPSystem:
    def __init__(self):
        self.level = 1
        self.xp = 0
        self.coins = 0
        self.xp_needed = XP_BASE

    def add(self, xp, coins):
        self.xp += xp
        self.coins += coins

    def check_level_up(self):
        leveled_up = False
        while self.xp >= self.xp_needed:
            self.xp -= self.xp_needed
            self.level += 1
            self.xp_needed = int(self.xp_needed * XP_MULTIPLIER)
            leveled_up = True
        return leveled_up