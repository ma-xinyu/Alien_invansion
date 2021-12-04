import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    "对飞船发射子弹进行管理的类"
    def __init__(self,ai_settings,screen,ship):
        "relate ship"
        "继承"
        #super(Bullet,self).__init__()
        super().__init__()
        self.screen = screen

        "创建子弹 再确认位置"
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #bullets fly needed
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        #位置变化
        self.y -= self.speed_factor
        #更新位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)