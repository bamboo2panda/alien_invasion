class GameStats:
    def __init__(self, ai_settings):
        # Инициализирует статистику
        self.ai_settings = ai_settings

        # Рекорд не должен сбрасываться
        self.high_score = 0

        # Игра запускается в активном режиме
        self.game_active = False

        self.reset_stats()

    def reset_stats(self):
        # Инициализирует статистику, изменяющиеся в ходе игры
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 0

    def start_game(self):
        self.game_active = True



