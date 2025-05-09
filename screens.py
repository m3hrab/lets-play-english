import pygame
import settings
from button import Button
from quiz_game import QuizGame
from memory_game import MemoryGame

class Screen:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def draw(self, screen):
        pass

    def update(self):
        pass

    def handle_events(self, event):
        pass

class MainMenu(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, settings.FONT_LARGE_SIZE)
        self.button = Button("Start", settings.WIDTH // 2 - 100, settings.HEIGHT // 2 + 62, 200, 64, self.font, self.start_game)
        self.bg = pygame.image.load("assets/1.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        self.bg_rect = self.bg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        
    def start_game(self):
        self.game_manager.set_screen("game_selection")

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        # self.button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)

    def handle_events(self, event):
        self.button.handle_event(event)

class GameSelection(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.bg = pygame.image.load("assets/2.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        self.bg_rect = self.bg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.font = pygame.font.Font(None, settings.FONT_MEDIUM_SIZE)
        self.buttons = [
            Button("Quiz Game", settings.WIDTH // 2 - 135, settings.HEIGHT // 2 - 67, 268, 60, self.font, self.start_quiz),
            Button("Memory Game", settings.WIDTH // 2 - 135, settings.HEIGHT // 2 + 7, 268, 60, self.font, self.start_memory)
        ]

    def start_quiz(self):
        self.game_manager.set_screen("level_selection")

    def start_memory(self):
        self.game_manager.set_screen("memory_level_selection")

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        # for button in self.buttons:
        #     button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_events(self, event):
        for button in self.buttons:
            button.handle_event(event)

class LevelSelection(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 48)  # Bigger font for kids
        self.levels = ["Numbers", "Colours", "Family Members", "Animals", "Routines"]
        self.buttons = []
        for i, level in enumerate(self.levels):
            button_y = settings.HEIGHT // 2 - 132 + i * 65
            button = Button(level, settings.WIDTH // 2 - 130, button_y, 260, 60, self.font, lambda idx=i: self.start_level(idx))
            self.buttons.append(button)
        self.bg = pygame.image.load("assets/3.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        self.bg_rect = self.bg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))

    def start_level(self, level_index):
        self.game_manager.set_quiz_level(level_index)
        self.game_manager.set_screen("quiz_game")

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        # for button in self.buttons:
        #     button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_events(self, event):
        for button in self.buttons:
            button.handle_event(event)

class MemoryLevelSelection(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, 48)  # Bigger font for kids
        self.levels = ["Food", "Colors", "Animals"]
        self.buttons = []
        for i, level in enumerate(self.levels):
            button_y = settings.HEIGHT // 2 - 100 + i * 70
            button = Button(level, settings.WIDTH // 2 - 130, button_y, 260, 60, self.font, lambda idx=i: self.start_level(idx))
            self.buttons.append(button)
        self.bg = pygame.image.load("assets/7.png").convert()  
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        self.bg_rect = self.bg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))

    def start_level(self, level_index):
        self.game_manager.set_memory_level(level_index)
        self.game_manager.set_screen("memory_game")

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        # for button in self.buttons:
        #     button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_events(self, event):
        for button in self.buttons:
            button.handle_event(event)

class MemoryGameScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.game_instance = MemoryGame()
        self.bg = pygame.image.load("assets/6.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))
        self.bg_rect = self.bg.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))

    def draw(self, screen):
        screen.blit(self.bg, self.bg_rect)
        self.game_instance.draw(screen)

    def update(self):
        self.game_instance.update()
        if self.game_instance.is_game_over():
            score = self.game_instance.get_score()
            total = self.game_instance.get_total_questions()
            self.game_manager.set_screen("result", score=score, total=total)

    def handle_events(self, event):
        self.game_instance.handle_events(event)

class ResultScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font_large = pygame.font.Font("assets/font/PlaypenSans-Bold.ttf", settings.FONT_LARGE_SIZE)
        self.font_medium = pygame.font.Font("assets/font/PlaypenSans-SemiBold.ttf", settings.FONT_MEDIUM_SIZE)
        self.score = 0
        self.total = 0
        self.button = Button("Main Menu", settings.WIDTH // 2 - 130, settings.HEIGHT // 2 + 40, 260, 60, self.font_medium, self.back_to_menu)
        self.bg = pygame.image.load("assets/5.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))

    def back_to_menu(self):
        self.game_manager.set_screen("main_menu")

    def set_score(self, score, total):
        self.score = score
        self.total = total

    def draw(self, screen):
        screen.blit(self.bg, (0, 0))
        game_over_text = self.font_large.render("Level Completed", True, settings.HEADER_COLOR)
        score_text = self.font_medium.render(f"Your Score: {self.score}/{self.total}", True, settings.HEADER_COLOR)
        game_over_rect = game_over_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)

    def handle_events(self, event):
        self.button.handle_event(event)

class GameScreen(Screen):
    def __init__(self, game_manager, game_instance):
        super().__init__(game_manager)
        self.game_instance = game_instance

    def draw(self, screen):
        self.game_instance.draw(screen)

    def update(self):
        self.game_instance.update()
        if self.game_instance.is_game_over():
            score = self.game_instance.get_score()
            total = self.game_instance.get_total_questions()
            self.game_manager.set_screen("result", score=score, total=total)

    def handle_events(self, event):
        self.game_instance.handle_events(event)