import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event,ai_settings,screen,ship,bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings,screen,ship,bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullets(ai_settings,screen,ship,bullets):
    #创建子弹
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings,screen,stats,paly_button,ship,aliens,bullets,sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship,bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,paly_button,ship,aliens,bullets,mouse_x,mouse_y,sb)

def update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets):
    bullets.update()
    #delete ultra bullets
    #copy:可修改
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets)

def check_bullet_alien_collision(ai_settings,screen,stats,sb,ship,aliens,bullets):
    #检查是否碰撞 有就delete bullet and alien
    collisions = pygame.sprite.groupcollide(bullets,aliens,True,True)
    #score
    if collisions:
        for aliens in collisions.values():
            #这里的len是碰撞的len，记录碰撞个数，与下面的不同
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats,sb)
    #aliens all dead
    if len(aliens) == 0:
        bullets.empty()
        #升级
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings,screen,ship,aliens)

def check_play_button(ai_settings,screen,stats,paly_button,ship,aliens,bullets,mouse_x,mouse_y,sb):
    #是否开始游戏
    button_clicked = paly_button.rect.collidepoint(mouse_x,mouse_y)
    if button_clicked and not stats.game_active:
        #reset
        ai_settings.initialize_dynamic_settings()
        #隐藏鼠标
        pygame.mouse.set_visible(False)
        #reset
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        #清空
        aliens.empty()
        bullets.empty()
        #创建新的
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()

def create_fleet(ai_settings,screen,ship,aliens):
    alien = Alien(ai_settings,screen)
    #列数
    number_aliens_x = get_number_aliens_x(ai_settings,alien.rect.width)
    #行数
    number_rows = get_number_rows(ai_settings,ship.rect.height,alien.rect.height)
    
    #循环列生成外星人
    for row_number in range(number_rows):
        #一行外星人
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings,alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings,ship_height,alien_height):
    available_space_y = ai_settings.screen_height - 7 * alien_height - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

#创建 任意位置的 外星人
def create_alien(ai_settings,screen,aliens,alien_number,row_number):
    alien = Alien(ai_settings,screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien_height + 2 * alien_height * row_number
    aliens.add(alien)

def check_fleet_edges(ai_settings,aliens):
    #碰边 改变
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings,aliens)
            break

def change_fleet_direction(ai_settings,aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullests):
    if stats.ships_left > 0:
        #alien and ship collision
        stats.ships_left -= 1
        sb.prep_ships()
        #reset
        aliens.empty()
        bullests.empty()
        #recreate
        create_fleet(ai_settings,screen,ship,aliens)
        ship.center_ship()
        #stop
        sleep(0.5)
    else:
        stats.game_active = False
        #游戏结束，鼠标显示
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #视为ship被撞
            ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
            break

def check_high_score(stats,sb):
    if stats.score > stats.high_score:
        #诞生了新的最高分
        stats.high_score = stats.score
        sb.prep_high_score()

def update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets):
    check_fleet_edges(ai_settings,aliens)
    #every alien update
    aliens.update()
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,stats,sb,screen,ship,aliens,bullets)
        #print("Ship hit!!!")
    check_aliens_bottom(ai_settings,stats,sb,screen,ship,aliens,bullets)

def update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,paly_button):
        screen.fill(ai_settings.bg_color)
        #sprites return 列表
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)
        sb.show_score()
        #游戏是否开始
        if not stats.game_active:
            paly_button.draw_button()
        pygame.display.flip()