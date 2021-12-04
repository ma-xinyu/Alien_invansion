import sys
import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import game_functions as gf
from pygame.sprite import Group

def run_game():
    #初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("外星人入侵")
    #创建paly按钮
    paly_button = Button(ai_settings,screen,"Play")
    #创建一个用于存储游戏统计信息的实例
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings,screen,ship,aliens)
    #计算个数：print((ai_settings.screen_width-(2*alien_width))/(2*alien_width))

    #主循环
    while True:
        #event
        gf.check_events(ai_settings,screen,stats,paly_button,ship,aliens,bullets,sb)
        #还有游戏次数才能游戏
        if stats.game_active:
            ship.update() 
            gf.update_bullets(ai_settings,screen,stats,sb,ship,aliens,bullets)
            gf.update_aliens(ai_settings,stats,sb,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,stats,sb,ship,aliens,bullets,paly_button)

run_game()