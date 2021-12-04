class GameStats():
    #跟踪游戏的统计数据

    def __init__(self,ai_settings):
        self.game_active = False
        self.ai_settings = ai_settings
        self.reset_stats()
        self.high_score = 0

    def reset_stats(self):
        #初始化可能变化的信息
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1