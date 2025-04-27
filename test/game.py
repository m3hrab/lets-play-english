import pygame
import json

# Simulated quiz data (since local file I/O isn't used)
QUIZ_DATA = {
    "questions": [
        {
            "question": "Which of these people was the first to set foot on the moon?",
            "options": ["Neil Armstrong", "Jim Lovell", "Luke Skywalker", "Orville Wright"],
            "correct_answer": "Neil Armstrong",
            "image_path": "moon_landing.jpg"
        },
        {
            "question": "What is the capital of France?",
            "options": ["Berlin", "Madrid", "Paris", "Rome"],
            "correct_answer": "Paris",
            "image_path": "france_flag.jpg"
        }
    ]
}

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 960, 540
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quiz Whiz")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (200, 200, 200)
HOVER_COLOR = (150, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Game variables
questions = QUIZ_DATA["questions"]
current_question = 0
score = 0
selected_option = None
feedback = None
feedback_timer = 0
game_over = False
option_rects = []
restart_rect = None

def wrap_text(text, font, max_width):
    """Wrap text to fit within a given width."""
    words = text.split(" ")
    lines = []
    current_line = []
    current_width = 0

    for word in words:
        word_surface = font.render(word, True, BLACK)
        word_width = word_surface.get_width()

        if current_width + word_width <= max_width:
            current_line.append(word)
            current_width += word_width + font.render(" ", True, BLACK).get_width()
        else:
            lines.append(" ".join(current_line))
            current_line = [word]
            current_width = word_width + font.render(" ", True, BLACK).get_width()

    if current_line:
        lines.append(" ".join(current_line))
    
    return lines

def draw_game():
    global option_rects, restart_rect
    screen.fill(YELLOW)

    # Draw header
    header_text = font_large.render("QUIZ WHIZ", True, BLACK)
    header_rect = header_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(header_text, header_rect)

    # Draw dots across the top
    for i in range(10):
        pygame.draw.circle(screen, CYAN, (50 + i * 95, 50), 20)
        pygame.draw.circle(screen, WHITE, (50 + i * 95, 50), 18)

    if not game_over:
        # Draw question box
        question_box = pygame.Rect(250, 150, 600, 300)
        pygame.draw.rect(screen, CYAN, question_box, border_radius=20)
        pygame.draw.rect(screen, WHITE, question_box.inflate(-10, -10), border_radius=20)

        # Draw question number
        question_num = font_medium.render(str(current_question + 1), True, ORANGE)
        num_rect = question_num.get_rect(center=(question_box.left + 30, question_box.top + 30))
        pygame.draw.circle(screen, WHITE, num_rect.center, 20)
        screen.blit(question_num, num_rect)

        # Display wrapped question
        question_lines = wrap_text(questions[current_question]["question"], font_medium, question_box.width - 80)
        question_height = len(question_lines) * 40
        for i, line in enumerate(question_lines):
            question_text = font_medium.render(line, True, BLACK)
            question_rect = question_text.get_rect(topleft=(question_box.left + 40, question_box.top + 60 + i * 40))
            screen.blit(question_text, question_rect)

        # Simulate reference image (placeholder, outside the question card)
        image_rect = pygame.Rect(50, 150, 150, 200)
        pygame.draw.rect(screen, GRAY, image_rect)
        image_label = font_small.render("Image Placeholder", True, BLACK)
        screen.blit(image_label, image_label.get_rect(center=image_rect.center))

        # Display options inside the question card with wrapping
        option_rects = []
        option_y_start = question_box.top + 60 + question_height + 20  # Start below the question text
        for i, option in enumerate(questions[current_question]["options"]):
            # Wrap the option text
            option_text = f"{chr(97 + i)}. {option}"
            wrapped_option = wrap_text(option_text, font_medium, question_box.width - 80)
            option_height = len(wrapped_option) * 40

            # Create a rectangle for the option (based on wrapped height)
            option_rect = pygame.Rect(question_box.left + 40, option_y_start, question_box.width - 80, option_height)
            option_rects.append(option_rect)

            # Hover effect
            mouse_pos = pygame.mouse.get_pos()
            if option_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, HOVER_COLOR, option_rect, border_radius=10)
            else:
                pygame.draw.rect(screen, WHITE, option_rect, border_radius=10)

            # Render wrapped option text
            for j, line in enumerate(wrapped_option):
                option_line = font_medium.render(line, True, BLACK)
                screen.blit(option_line, (option_rect.left + 10, option_rect.top + j * 40))

            option_y_start += option_height + 10  # Space between options

        # Display feedback card if active
        if feedback:
            feedback_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT - 100, 300, 60)
            feedback_color = GREEN if "Correct" in feedback else RED
            pygame.draw.rect(screen, feedback_color, feedback_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, feedback_rect.inflate(-5, -5), border_radius=10)
            feedback_text = font_small.render(feedback, True, BLACK)
            feedback_text_rect = feedback_text.get_rect(center=feedback_rect.center)
            screen.blit(feedback_text, feedback_text_rect)

    else:
        # Game over screen
        game_over_text = font_large.render("Game Over!", True, BLACK)
        score_text = font_medium.render(f"Your Score: {score}/{len(questions)}", True, BLACK)
        restart_text = font_medium.render("Restart", True, BLACK)

        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
        restart_button = pygame.Rect(restart_rect.left - 20, restart_rect.top - 10, restart_rect.width + 40, restart_rect.height + 20)

        pygame.draw.rect(screen, CYAN, restart_button, border_radius=10)
        pygame.draw.rect(screen, WHITE, restart_button.inflate(-5, -5), border_radius=10)

        screen.blit(game_over_text, game_over_rect)
        screen.blit(score_text, score_rect)
        screen.blit(restart_text, restart_rect)

def main():
    global current_question, score, selected_option, feedback, feedback_timer, game_over, option_rects, restart_rect
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if game_over:
                    if restart_rect and restart_rect.collidepoint(mouse_pos):
                        # Reset game
                        current_question = 0
                        score = 0
                        game_over = False
                        feedback = None
                        feedback_timer = 0
                        selected_option = None
                elif feedback is None:
                    for i, rect in enumerate(option_rects):
                        if rect.collidepoint(mouse_pos):
                            selected_option = questions[current_question]["options"][i]
                            correct_answer = questions[current_question]["correct_answer"]
                            if selected_option == correct_answer:
                                feedback = "Correct!"
                                score += 1
                            else:
                                feedback = f"Wrong! Correct: {correct_answer}"
                            feedback_timer = 120  # 2 seconds at 60 FPS

        # Update feedback timer
        if feedback_timer > 0:
            feedback_timer -= 1
            if feedback_timer <= 0:
                feedback = None
                selected_option = None
                current_question += 1
                if current_question >= len(questions):
                    game_over = True

        # Draw everything
        draw_game()
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()