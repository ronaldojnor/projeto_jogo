import pygame
from player import Player
from bullet import Bullet
from enemy import Enemy
from spawner import Spawner
from wave_manager import WaveManager
from shop import Shop
from ui import UI, XPSystem
from settings import WIDTH, HEIGHT, FPS, BLACK

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# função para reiniciar tudo
def reset_game():
    global player, player_group, bullets, enemies, spawner, wave_manager
    global shop, ui, xp_system, recent_hits

    player = Player((WIDTH // 2, HEIGHT // 2))
    player_group = pygame.sprite.GroupSingle(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    spawner = Spawner(player)
    wave_manager = WaveManager()
    wave_manager.force_first_wave(spawner, enemies)
    shop = Shop()
    ui = UI(font)
    xp_system = XPSystem()
    recent_hits = set()

# inicia o jogo
reset_game()
running = True
game_over = False

while running:
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if ui.showing_shop and event.type == pygame.MOUSEBUTTONDOWN:
            upgrade = ui.handle_shop_click(event.pos)
            if upgrade:
                sucesso = shop.apply_upgrade(player, upgrade, xp_system)
                if sucesso:
                    ui.showing_shop = False
                    ui.shop_options = []
                    wave_manager.paused = False

        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            reset_game()
            game_over = False

    if game_over:
        screen.fill((0, 0, 0))
        text = font.render("GAME OVER", True, (255, 0, 0))
        text2 = font.render("Clique para recomeçar", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 40))
        screen.blit(text2, (WIDTH // 2 - 100, HEIGHT // 2))
        pygame.display.flip()
        continue

    if ui.showing_shop:
        screen.fill(BLACK)
        player_group.draw(screen)
        bullets.draw(screen)
        enemies.draw(screen)
        ui.draw(
            screen,
            player,
            xp_system.xp,
            xp_system.xp_needed,
            xp_system.coins,
            wave_manager.get_wave(),
            wave_manager.get_time_remaining()
        )
        pygame.display.flip()
        continue

    # Atualizações
    player_group.update(dt, bullets)
    bullets.update(dt)

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect):
            if enemy not in recent_hits:
                player.health -= enemy.damage
                recent_hits.add(enemy)
                if player.health <= 0:
                    game_over = True
                    wave_manager.paused = True
        else:
            recent_hits.discard(enemy)

    enemies.update(dt)
    wave_manager.update(dt, spawner, enemies)

    for bullet in bullets:
        hit_enemies = pygame.sprite.spritecollide(bullet, enemies, False)
        for enemy in hit_enemies:
            xp, coins = enemy.take_damage(player.damage)
            if xp > 0:
                xp_system.add(xp, coins)
            bullet.kill()

    if xp_system.check_level_up():
        options = shop.get_options()
        if options:
            ui.showing_shop = True
            ui.shop_options = options
            ui.shop_prices = {opt: shop.get_cost(opt) for opt in options}
            wave_manager.paused = True

    screen.fill(BLACK)
    player_group.draw(screen)
    bullets.draw(screen)
    enemies.draw(screen)
    ui.draw(
        screen,
        player,
        xp_system.xp,
        xp_system.xp_needed,
        xp_system.coins,
        wave_manager.get_wave(),
        wave_manager.get_time_remaining()
    )
    pygame.display.flip()

pygame.quit()
