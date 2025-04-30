import pygame
import settings
import random
import json

class QuizGame:
    
    def __init__(self):
        # Load quiz_data.json 
        try:
            with open('quiz_data.json', 'r') as f:
                self.quiz_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("quiz_data.json file not found. Please ensure it exists in the same directory as the script.")
        except json.JSONDecodeError:
            raise ValueError("quiz_data.json is not a valid JSON file.")

        # Custom Fonts 
        self.font_large = pygame.font.Font("assets/font/PlaypenSans-Bold.ttf", settings.FONT_LARGE_SIZE)
        self.font_medium = pygame.font.Font("assets/font/PlaypenSans-SemiBold.ttf", settings.FONT_MEDIUM_SIZE)
        self.font_small = pygame.font.Font("assets/font/PlaypenSans-Regular.ttf", settings.FONT_SMALL_SIZE)

        # Load background image
        self.bg = pygame.image.load("assets/4.png").convert()
        self.bg = pygame.transform.scale(self.bg, (settings.WIDTH, settings.HEIGHT))

        # Game variables
        self.current_level = 0 
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
        self.game_over = False  

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
        screen.blit(self.bg, (0, 0))  

        # Draw header with level name
        header_text = self.font_large.render(f"Level: {self.levels[self.current_level]['name']}", True, settings.HEADER_COLOR)
        header_rect = header_text.get_rect(center=(settings.WIDTH // 2, 50))
        screen.blit(header_text, header_rect)


        if not self.level_complete:
            # Determine if the current question has an image
            has_image = self.questions[self.current_question]["image_path"] is not None
            question_box = pygame.Rect(340, 120, 600, 300)


        
            # Draw question number 
            question_num = self.font_medium.render(str(self.current_question + 1)+".", True, settings.QUESTION_COLOR)
            # top left corner of the question box
            num_rect = question_num.get_rect(topleft=(question_box.left + 10, question_box.top + 40))
            # Draw a circle around the number
            screen.blit(question_num, num_rect)

            # Display wrapped question
            question_lines = self.wrap_text(self.questions[self.current_question]["question"], self.font_medium, question_box.width - 80)
            question_height = len(question_lines) * 30  
            for i, line in enumerate(question_lines):
                question_text = self.font_medium.render(line, True, settings.QUESTION_COLOR)
                question_rect = question_text.get_rect(topleft=(question_box.left + 40, question_box.top + 40 + i * 30))
                screen.blit(question_text, question_rect)

            if has_image:
                image_rect = pygame.Rect(65, 187, 205, 205)
                
                try:
                    image = pygame.image.load(self.questions[self.current_question]["image_path"]).convert_alpha()
                    image = pygame.transform.scale(image, (image_rect.width, image_rect.height))
                    screen.blit(image, image_rect)
                except FileNotFoundError:
                    pygame.draw.rect(screen, settings.GRAY, image_rect, border_radius=10)
                    image_label = self.font_small.render("Image Not Found", True, settings.BLACK)
                    screen.blit(image_label, image_label.get_rect(center=image_rect.center))
                    print(f"Image not found: {self.questions[self.current_question]['image_path']}")
                # image_rect = pygame.Rect(65, 187, 205, 205)
                # pygame.draw.rect(screen, settings.GRAY, image_rect, border_radius=10)
                # image_label = self.font_small.render("Refference Picture", True, settings.BLACK)
                # screen.blit(image_label, image_label.get_rect(center=image_rect.center))

            self.option_rects = []
            option_y_start = question_box.top + 40 + question_height + 20
            for i, option in enumerate(self.questions[self.current_question]["shuffled_options"]):
                # Wrap the option text
                option_text = f"{chr(97 + i)}. {option}"
                wrapped_option = self.wrap_text(option_text, self.font_medium, question_box.width - 80)
                option_height = len(wrapped_option) * 50

                # Create a rectangle for the option
                option_rect = pygame.Rect(question_box.left + 40, option_y_start, question_box.width - 80, option_height)
                self.option_rects.append(option_rect)

                # Hover effect
                mouse_pos = pygame.mouse.get_pos()
                if option_rect.collidepoint(mouse_pos):
                    # Draw hover effect
                    option_rect_hovered = option_rect.copy()
                    option_rect_hovered.y -= 5
                    pygame.draw.rect(screen, settings.HOVER_COLOR, option_rect_hovered, border_radius=10)
                # else:
                #     pygame.draw.rect(screen, self.CARD_COLOR, option_rect, border_radius=10)

                # Render wrapped option text
                for j, line in enumerate(wrapped_option):
                    option_line = self.font_medium.render(line, True, settings.QUESTION_COLOR)
                    screen.blit(option_line, (option_rect.left + 10, option_rect.top + j * 50))

                option_y_start += option_height + 10

            # Display feedback card if active
            if self.feedback:
                # play sound based on feedback
                if "Great job" in self.feedback and settings.SOUND_ON:
                    # play only one time 
                    if not self.feedback_timer == settings.FEEDBACK_DURATION:
                        settings.CORRECT_SOUND.play()
                elif "Oops" in self.feedback and settings.SOUND_ON:
                    # play only one time 
                    if not self.feedback_timer == settings.FEEDBACK_DURATION:
                        settings.WRONG_SOUND.play()
                    
                # Draw feedback card
                feedback_rect = pygame.Rect(settings.WIDTH // 2 - 200, settings.HEIGHT // 2 - 80 , 400, 160)
                feedback_color = settings.CORRECT_COLOR if "Great job" in self.feedback else settings.WRONG_COLOR
                pygame.draw.rect(screen, feedback_color, feedback_rect, border_radius=10)
                pygame.draw.rect(screen, settings.WHITE, feedback_rect.inflate(-10, -10), border_radius=10)
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
                            self.feedback = "Great job"
                            self.score += 1
                        else:
                            self.feedback = f"Oops! It's {correct_answer}"
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
                    self.game_over = True  

    def get_score(self):
        return self.score

    def get_total_questions(self):
        return len(self.questions)

    def is_game_over(self):
        return self.game_over

    def reset(self):
        self.initialize_level()

    def set_level(self, level_index):
        self.current_level = level_index
        self.initialize_level()