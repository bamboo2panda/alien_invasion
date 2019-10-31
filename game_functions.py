import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_settings, screen, ship)
    elif event.key == pygame.K_q:
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens, bullets, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, stats, play_button, mouse_x, mouse_y, aliens, bullets, sb)
        

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # Кнопка Play отображается в том случае, если игра не активна
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Обновляет позциии пуль и удаляет старые пули
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collision(ai_settings, screen, stats, sb, ship, aliens, bullets):
    # Проверка попаданий в пришельцев
    # При обнаружении попадания удалить пулю и пришельца
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Уничтожение существующих пуль и создание нового флота
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)
        stats.level += 1
        sb.prep_level()


def fire_bullet(bullets, ai_settings, screen, ship):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_aliens_x(ai_settings, alien_width):
    # Вычисляет количество пришельцев в ряду
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (alien_width))
    return number_aliens_x


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # Создание пришельца и размещение его в ряду
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_x = alien_width + alien_width * alien_number
    alien.rect.x = alien_x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    # Создает флот пришельцев
    # Создание пришельца и вычисление количества пришельце в ряду
    # Интервал между соседними пришельцами равен одной ширине пришельца
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # Создание превого ряда пришельцев
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Создание пришельца и размещение его в ряду
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    # Определяет количество рядов, помещающихся на экране
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))

    return number_rows


def check_fleet_edges(ai_settings, aliens):
    # Реагирует на достижение пришельцем края экрана
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    # Опускает весь флот и меняет направление флота
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction = ai_settings.fleet_direction * (-1)


def update_aliens(ship, stats, screen, sb, ai_settings, aliens, bullets):
    # Проверяет достиг ли флот края экрана, после чего обновляет позиции всех пришельцев во флоте
    check_fleet_edges(ai_settings, aliens)
    aliens.update()
    # Проверка пришельцев, добравшихся до нижнего края
    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)
    # Проверка колизий "Пришелец - корабль"
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)


def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # Обрабатываем столкновение корабля с пришельцемF
    if stats.ships_left > 0:
        # Уменьшение ships_left
        stats.ships_left -= 1
        # Очистака списка пришельцев и пуль
        aliens.empty()
        bullets.empty()

        # Создание нового флота и размещение корабля в центре
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Пауза
        sleep(0.5)
        sb.prep_ship()
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets):
    # Проверяет, доброались ли пришельцы до нижнего крася экрана
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Происходит то, что при столкновении с кораблем
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break


def check_play_button(ai_settings, stats, play_button, mouse_x, mouse_y, aliens, bullets, sb):
    # Запускает новую игру при нажатии кнопки Play
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        # Сброс игровых настроек
        aliens.empty()
        bullets.empty()
        ai_settings.initialize_dynamic_settings()
        stats.start_game()
        stats.reset_stats()
        sb.prep_score()
        sb.prep_level()
        sb.prep_ship()
        pygame.mouse.set_visible(False)


def check_high_score(stats, sb):
    # Проверяет, появился ли новый рекорд
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()

