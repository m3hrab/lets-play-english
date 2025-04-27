import pygame
import json

# Initialize Pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Whiz")

# Fonts
font_title = pygame.font.SysFont(None, 70)
font_question = pygame.font.SysFont(None, 35)
font_option = pygame.font.SysFont(None, 30)
font_small = pygame.font.SysFont(None, 25)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 220, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 150, 255)
BACKGROUND = (255, 215, 0)

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

current_question = 0
correct_answers = 0
results = []

# Button class
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, surface):
        pygame.draw.rect(surface, CYAN, self.rect, border_radius=10)
        txt_surf = font_option.render(self.text, True, BLACK)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

# Create buttons
buttons = []
start_y = 330
for i in range(4):
    buttons.append(Button(430, start_y + i*55, 300, 40, ""))

# Draw top smileys and crosses
def draw_result_icons(surface):
    start_x = 200
    for idx, res in enumerate(results):
        color = GREEN if res else RED
        pygame.draw.circle(surface, color, (start_x + idx * 60, 80), 20)

    # Draw empty circles for unanswered questions
    for idx in range(len(results), 7):  # assuming 7 questions max (adjust if needed)
        pygame.draw.circle(surface, CYAN, (start_x + idx * 60, 80), 20)

# Draw background circles (for style)
def draw_background(surface):
    surface.fill(YELLOW)
    for x in range(0, WIDTH, 100):
        for y in range(0, HEIGHT, 100):
            pygame.draw.circle(surface, (255, 240, 100), (x, y), 40)

# Main loop
running = True
while running:
    draw_background(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for idx, btn in enumerate(buttons):
                if btn.is_clicked(pos):
                    if questions[current_question]['options'][idx] == questions[current_question]['answer']:
                        correct_answers += 1
                        results.append(True)
                    else:
                        results.append(False)

                    current_question += 1
                    if current_question >= len(questions):
                        running = False
                    break

    if current_question < len(questions):
        # Draw Title
        title_surf = font_title.render("QUIZ WHIZ", True, WHITE)
        screen.blit(title_surf, (WIDTH//2 - title_surf.get_width()//2, 10))

        # Draw Result Icons
        draw_result_icons(screen)

        # Draw Question card
        pygame.draw.rect(screen, CYAN, (400, 150, 370, 400), border_radius=15)
        
        # Question number and text
        q_number_surf = font_small.render(f"{current_question + 1}", True, BLACK)
        screen.blit(q_number_surf, (415, 160))

        question_text = questions[current_question]['question']
        q_text_surf = font_question.render(question_text, True, BLACK)
        screen.blit(q_text_surf, (430, 200))

        # Options
        opts = questions[current_question]['options']
        for idx, btn in enumerate(buttons):
            btn.text = f"{chr(97+idx)}. {opts[idx]}"
            btn.draw(screen)

        # Dummy Image Rectangle
        pygame.draw.rect(screen, WHITE, (80, 180, 280, 280), border_radius=10)
        dummy_text = font_small.render("Image", True, BLACK)
        dummy_text_rect = dummy_text.get_rect(center=(80+140, 180+140))
        screen.blit(dummy_text, dummy_text_rect)

    pygame.display.flip()

pygame.quit()
