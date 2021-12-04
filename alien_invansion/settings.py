class Settings():
    "存储所有设置的类"

    def __init__(self):

        #screen
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)

        #ship
        self.ship_limit = 3

        #bullet
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        #alien
        self.fleet_drop_speed = 8

        #等级提升
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        #方向 默认为右
        self.fleet_direction = 1
        #score
        self.alien_points = 50

    def increase_speed(self):
        #升级
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points *= self.score_scale