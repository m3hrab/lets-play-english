import pygame
import settings


class Button:
    def __init__(self, text, x, y, width, height, font, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.action = action
        self.hovered = False

    def draw(self, screen):
        color = settings.HOVER_COLOR if self.hovered else settings.CYAN
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, settings.WHITE, self.rect.inflate(-5, -5), border_radius=10)
        text_surface = self.font.render(self.text, True, settings.BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            self.action()