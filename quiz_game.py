import pygame
import settings
import random
import json

class QuizGame:
    def __init__(self):
        # Load quiz_data.json from file
        try:
            with open('quiz_data.json', 'r') as f:
                self.quiz_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("quiz_data.json file not found. Please ensure it exists in the same directory as the script.")
        except json.JSONDecodeError:
            raise ValueError("quiz_data.json is not a valid JSON file.")

        # Fonts (larger for kids)
        self.font_large = pygame.font.Font(None, 60)  # Bigger font for title
        self.font_medium = pygame.font.Font(None, 48)  # Bigger font for questions
        self.font_small = pygame.font.Font(None, 36)   # Bigger font for feedback

        # Colors (bright and cheerful for kids)
        self.BACKGROUND_COLOR = (255, 204, 255)  # Light pink background
        self.CARD_COLOR = (255, 255, 153)        # Light yellow card
        self.BORDER_COLOR = (255, 102, 102)      # Bright red border
        self.HOVER_COLOR = (153, 255, 153)       # Light green hover
        self.CORRECT_COLOR = (102, 255, 102)     # Bright green for correct
        self.WRONG_COLOR = (255, 102, 102)       # Bright red for wrong

        # Game variables
        self.current_level = 0  # Default level, will be set by set_level
        self.levels = self.quiz_data["levels"]
        self.initialize_level()

    def initialize_level(self):
        # Select 10 random questions for the current level
        all_questions = self.levels[self.current_level]["questions"].copy()
        self.questions = random.sample(all_questions, 10)

        # Randomize answer options for each question
        for question in self.questions:
            options = question["options"].copy()
            random.shuffle(options)
            question["shuffled_options"] = options

        # Reset game state for the level
        self.current_question = 0
        self.score = 0
        self.selected_option = None
        self.feedback = None
        self.feedback_timer = 0
        self.level_complete = False
        self.option_rects = []
        self.game_over = False  # Ensure game_over is initialized

    def wrap_text(self, text, font, max_width):
        """Wrap text to fit within a given width."""
        words = text.split(" ")
        lines = []
        current_line = []
        current_width = 0

        for word in words:
            word_surface = font.render(word, True, settings.BLACK)
            word_width = word_surface.get_width()

            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width + font.render(" ", True, settings.BLACK).get_width()
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_width = word_width + font.render(" ", True, settings.BLACK).get_width()

        if current_line:
            lines.append(" ".join(current_line))
        
        return lines

    def draw(self, screen):
        screen.fill(self.BACKGROUND_COLOR)

        # Draw header with level name
        header_text = self.font_large.render(f"Level: {self.levels[self.current_level]['name']}", True, settings.BLACK)
        header_rect = header_text.get_rect(center=(settings.WIDTH // 2, 50))
        screen.blit(header_text, header_rect)

        # Draw decorative stars across the top
        for i in range(8):
            pygame.draw.polygon(screen, settings.YELLOW, [
                (50 + i * 120, 30),
                (60 + i * 120, 50),
                (50 + i * 120, 70),
                (40 + i * 120, 50)
            ])
            pygame.draw.polygon(screen, settings.WHITE, [
                (50 + i * 120, 30),
                (60 + i * 120, 50),
                (50 + i * 120, 70),
                (40 + i * 120, 50)
            ], 2)

        if not self.level_complete:
            # Determine if the current question has an image
            has_image = self.questions[self.current_question]["image_path"] is not None

            # Adjust question box position based on whether there's an image
            if has_image:
                question_box = pygame.Rect(250, 150, 600, 300)
            else:
                # Center the question box if there's no image
                question_box = pygame.Rect(settings.WIDTH // 2 - 300, 150, 600, 300)

            # Draw question box
            pygame.draw.rect(screen, self.BORDER_COLOR, question_box, border_radius=20)
            pygame.draw.rect(screen, self.CARD_COLOR, question_box.inflate(-10, -10), border_radius=20)

            # Draw question number with a fun circle
            question_num = self.font_medium.render(str(self.current_question + 1), True, settings.ORANGE)
            num_rect = question_num.get_rect(center=(question_box.left + 40, question_box.top + 40))
            pygame.draw.circle(screen, settings.WHITE, num_rect.center, 25)
            pygame.draw.circle(screen, settings.ORANGE, num_rect.center, 23)
            screen.blit(question_num, num_rect)

            # Display wrapped question
            question_lines = self.wrap_text(self.questions[self.current_question]["question"], self.font_medium, question_box.width - 80)
            question_height = len(question_lines) * 50  # More spacing for readability
            for i, line in enumerate(question_lines):
                question_text = self.font_medium.render(line, True, settings.BLACK)
                question_rect = question_text.get_rect(topleft=(question_box.left + 40, question_box.top + 80 + i * 50))
                screen.blit(question_text, question_rect)

            # Display image placeholder if the question has an image
            if has_image:
                image_rect = pygame.Rect(50, 150, 150, 200)
                pygame.draw.rect(screen, settings.GRAY, image_rect, border_radius=10)
                image_label = self.font_small.render("Picture Here!", True, settings.BLACK)
                screen.blit(image_label, image_label.get_rect(center=image_rect.center))

            # Display options inside the question card with wrapping
            self.option_rects = []
            option_y_start = question_box.top + 80 + question_height + 20
            for i, option in enumerate(self.questions[self.current_question]["shuffled_options"]):
                # Wrap the option text
                option_text = f"{chr(97 + i)}. {option}"
                wrapped_option = self.wrap_text(option_text, self.font_medium, question_box.width - 80)
                option_height = len(wrapped_option) * 50

                # Create a rectangle for the option (based on wrapped height)
                option_rect = pygame.Rect(question_box.left + 40, option_y_start, question_box.width - 80, option_height)
                self.option_rects.append(option_rect)

                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    pygame.draw.rect(screen, self.HOVER_COLOR, option_rect, border_radius=10)
                else:
                    pygame.draw.rect(screen, self.CARD_COLOR, option_rect, border_radius=10)

                # Render wrapped option text
                for j, line in enumerate(wrapped_option):
                    option_line = self.font_medium.render(line, True, settings.BLACK)
                    screen.blit(option_line, (option_rect.left + 10, option_rect.top + j * 50))

                option_y_start += option_height + 10

            # Display feedback card if active
            if self.feedback:
                feedback_rect = pygame.Rect(settings.WIDTH // 2 - 150, settings.HEIGHT - 100, 300, 60)
                feedback_color = self.CORRECT_COLOR if "Great job" in self.feedback else self.WRONG_COLOR
                pygame.draw.rect(screen, feedback_color, feedback_rect, border_radius=10)
                pygame.draw.rect(screen, settings.WHITE, feedback_rect.inflate(-5, -5), border_radius=10)
                feedback_text = self.font_small.render(self.feedback, True, settings.BLACK)
                feedback_text_rect = feedback_text.get_rect(center=feedback_rect.center)
                screen.blit(feedback_text, feedback_text_rect)

        else:
            # Level complete message
            complete_text = self.font_large.render("Yay! Level Complete!", True, settings.BLACK)
            score_text = self.font_medium.render(f"Score: {self.score}/10", True, settings.BLACK)
            complete_rect = complete_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 - 50))
            score_rect = score_text.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
            screen.blit(complete_text, complete_rect)
            screen.blit(score_text, score_rect)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.level_complete:
            mouse_pos = pygame.mouse.get_pos()
            if self.feedback is None:
                for i, rect in enumerate(self.option_rects):
                    if rect.collidepoint(mouse_pos):
                        self.selected_option = self.questions[self.current_question]["shuffled_options"][i]
                        correct_answer = self.questions[self.current_question]["correct_answer"]
                        if self.selected_option == correct_answer:
                            self.feedback = "Great job! 🎉"
                            self.score += 1
                        else:
                            self.feedback = f"Oops! It's {correct_answer} 😊"
                        self.feedback_timer = settings.FEEDBACK_DURATION

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                self.feedback = None
                self.selected_option = None
                self.current_question += 1
                if self.current_question >= len(self.questions):
                    self.level_complete = True
                    self.game_over = True  # End the game after the selected level

    def get_score(self):
        return self.score

    def get_total_questions(self):
        return len(self.questions)

    def is_game_over(self):
        return self.game_over

    def reset(self):
        # Reset the game state but do not change current_level
        self.initialize_level()

    def set_level(self, level_index):
        self.current_level = level_index
        self.initialize_level()