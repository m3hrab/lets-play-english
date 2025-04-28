import pygame
import settings
from button import Button
from quiz_game import QuizGame

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
        self.button = Button("Start", settings.WIDTH // 2 - 100, settings.HEIGHT // 2, 200, 60, self.font, self.start_game)

    def start_game(self):
        self.game_manager.set_screen("game_selection")

    def draw(self, screen):
        screen.fill(settings.YELLOW)
        title_text = self.font.render("Mini Games Hub", True, settings.BLACK)
        title_rect = title_text.get_rect(center=(settings.WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        self.button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.button.update(mouse_pos)

    def handle_events(self, event):
        self.button.handle_event(event)

class GameSelection(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, settings.FONT_MEDIUM_SIZE)
        self.buttons = [
            Button("Quiz Game", settings.WIDTH // 2 - 150, settings.HEIGHT // 2 - 50, 300, 60, self.font, self.start_quiz),
            Button("Memory Game", settings.WIDTH // 2 - 150, settings.HEIGHT // 2 + 50, 300, 60, self.font, self.start_memory)
        ]

    def start_quiz(self):
        self.game_manager.set_screen("quiz_game")

    def start_memory(self):
        self.game_manager.set_screen("memory_game")

    def draw(self, screen):
        screen.fill(settings.YELLOW)
        title_text = self.font.render("Select a Game", True, settings.BLACK)
        title_rect = title_text.get_rect(center=(settings.WIDTH // 2, 100))
        screen.blit(title_text, title_rect)
        for button in self.buttons:
            button.draw(screen)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update(mouse_pos)

    def handle_events(self, event):
        for button in self.buttons:
            button.handle_event(event)

class MemoryGame(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = pygame.font.Font(None, settings.FONT_MEDIUM_SIZE)

    def draw(self, screen):
        screen.fill(settings.YELLOW)
        placeholder_text = self.font.render("Memory Game (Not Implemented)", True, settings.BLACK)
        placeholder_rect = placeholder_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        screen.blit(placeholder_text, placeholder_rect)

    def update(self):
        # Placeholder: immediately end the game for now
        self.game_manager.set_screen("result", score=0, total=0)

    def handle_events(self, event):
        pass

class ResultScreen(Screen):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font_large = pygame.font.Font(None, settings.FONT_LARGE_SIZE)
        self.font_medium = pygame.font.Font(None, settings.FONT_MEDIUM_SIZE)
        self.score = 0
        self.total = 0
        self.button = Button("Back to Menu", settings.WIDTH // 2 - 150, settings.HEIGHT // 2 + 50, 300, 60, self.font_medium, self.back_to_menu)

    def back_to_menu(self):
        self.game_manager.set_screen("main_menu")

    def set_score(self, score, total):
        self.score = score
        self.total = total

    def draw(self, screen):
        screen.fill(settings.YELLOW)
        game_over_text = self.font_large.render("Game Over!", True, settings.BLACK)
        score_text = self.font_medium.render(f"Your Score: {self.score}/{self.total}", True, settings.BLACK)
        game_over_rect = game_over_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        self.button.draw(screen)

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