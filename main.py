import pygame
import settings
from quiz_game import QuizGame
from memory_game import MemoryGame
from screens import MainMenu, GameSelection, LevelSelection, MemoryLevelSelection, MemoryGameScreen, ResultScreen, GameScreen

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
        pygame.display.set_caption("Let's Play English")
        self.clock = pygame.time.Clock()
        self.quiz_game_instance = QuizGame()
        self.memory_game_instance = MemoryGame()
        self.screens = {
            "main_menu": MainMenu(self),
            "game_selection": GameSelection(self),
            "level_selection": LevelSelection(self),
            "memory_level_selection": MemoryLevelSelection(self),  # Added this line
            "quiz_game": GameScreen(self, self.quiz_game_instance),
            "memory_game": MemoryGameScreen(self),
            "result": ResultScreen(self)
        }
        self.current_screen = "main_menu"

    def set_quiz_level(self, level_index):
        self.quiz_game_instance.set_level(level_index)

    def set_memory_level(self, level_index):
        self.memory_game_instance.set_level(level_index)

    def set_screen(self, screen_name, score=None, total=None):
        if screen_name == "quiz_game":
            self.screens["quiz_game"].game_instance.reset()
        if screen_name == "memory_game":
            self.screens["memory_game"].game_instance = self.memory_game_instance
            self.memory_game_instance.reset()
        if screen_name == "result" and score is not None and total is not None:
            self.screens["result"].set_score(score, total)
        self.current_screen = screen_name

    def run(self):
        running = True
        while running:
            self.clock.tick(settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.screens[self.current_screen].handle_events(event)

            self.screens[self.current_screen].update()
            self.screens[self.current_screen].draw(self.screen)
            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    game = GameManager()
    game.run()