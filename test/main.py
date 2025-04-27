import pygame
import random
import asyncio
import platform

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Let's Play English")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Category-specific colors for memory game
CATEGORY_COLORS = {
    "Colours": PURPLE,
    "Animals": BLUE,
    "Food": ORANGE
}

# Fonts
font = pygame.font.SysFont("comicsans", 40)
small_font = pygame.font.SysFont("comicsans", 30)

# Game states
MAIN_MENU = 0
QUIZ_GAME = 1
MEMORY_GAME = 2
game_state = MAIN_MENU

# Quiz game variables
quiz_levels = [
    {
        "name": "Colours",
        "questions": [
            {"question": "What colour is the sky on a clear day?", "options": ["Red", "Blue", "Green"], "answer": "Blue"},
            {"question": "What colour is a banana?", "options": ["Yellow", "Purple", "Pink"], "answer": "Yellow"},
            {"question": "What colour is an apple?", "options": ["Green", "Orange", "Black"], "answer": "Green"},
            {"question": "What colour is a strawberry?", "options": ["Red", "Blue", "White"], "answer": "Red"},
            {"question": "What colour is grass?", "options": ["Purple", "Green", "Yellow"], "answer": "Green"},
            {"question": "What colour is the sun?", "options": ["Yellow", "Red", "Blue"], "answer": "Yellow"},
            {"question": "What colour is a rose?", "options": ["Pink", "Black", "Green"], "answer": "Pink"},
            {"question": "What colour is a lime?", "options": ["Green", "Red", "White"], "answer": "Green"},
            {"question": "What colour is a carrot?", "options": ["Orange", "Purple", "Blue"], "answer": "Orange"},
            {"question": "What colour is a grape?", "options": ["Purple", "Yellow", "Pink"], "answer": "Purple"},
            {"question": "What colour is a blueberry?", "options": ["Blue", "Red", "Green"], "answer": "Blue"},
            {"question": "What colour is a peach?", "options": ["Pink", "Black", "White"], "answer": "Pink"},
            {"question": "What colour is a plum?", "options": ["Purple", "Orange", "Yellow"], "answer": "Purple"},
            {"question": "What colour is a cherry?", "options": ["Red", "Blue", "Green"], "answer": "Red"},
            {"question": "What colour is a watermelon?", "options": ["Green", "Yellow", "Pink"], "answer": "Green"},
            {"question": "What colour is a pumpkin?", "options": ["Orange", "Purple", "White"], "answer": "Orange"},
            {"question": "What colour is a violet flower?", "options": ["Purple", "Red", "Blue"], "answer": "Purple"},
            {"question": "What colour is a tangerine?", "options": ["Orange", "Green", "Pink"], "answer": "Orange"},
            {"question": "What colour is a flamingo?", "options": ["Pink", "Yellow", "Black"], "answer": "Pink"},
            {"question": "What colour is a raven?", "options": ["Black", "White", "Red"], "answer": "Black"},
        ]
    },
    {
        "name": "Numbers",
        "questions": [
            {"question": "What is 2 + 3?", "options": ["4", "5", "6"], "answer": "5"},
            {"question": "What is 5 - 2?", "options": ["2", "3", "4"], "answer": "3"},
            {"question": "What is 4 x 2?", "options": ["6", "8", "10"], "answer": "8"},
            {"question": "What is 10 ÷ 2?", "options": ["5", "4", "6"], "answer": "5"},
            {"question": "What is 3 + 4?", "options": ["6", "7", "8"], "answer": "7"},
            {"question": "What is 6 - 3?", "options": ["2", "3", "4"], "answer": "3"},
            {"question": "What is 5 x 3?", "options": ["12", "15", "18"], "answer": "15"},
            {"question": "What is 12 ÷ 3?", "options": ["3", "4", "5"], "answer": "4"},
            {"question": "What is 7 + 2?", "options": ["8", "9", "10"], "answer": "9"},
            {"question": "What is 8 - 4?", "options": ["3", "4", "5"], "answer": "4"},
            {"question": "What is 6 x 2?", "options": ["10", "12", "14"], "answer": "12"},
            {"question": "What is 15 ÷ 5?", "options": ["2", "3", "4"], "answer": "3"},
            {"question": "What is 4 + 5?", "options": ["8", "9", "10"], "answer": "9"},
            {"question": "What is 9 - 3?", "options": ["5", "6", "7"], "answer": "6"},
            {"question": "What is 7 x 2?", "options": ["12", "14", "16"], "answer": "14"},
            {"question": "What is 18 ÷ 3?", "options": ["5", "6", "7"], "answer": "6"},
            {"question": "What is 5 + 6?", "options": ["10", "11", "12"], "answer": "11"},
            {"question": "What is 10 - 4?", "options": ["5", "6", "7"], "answer": "6"},
            {"question": "What is 8 x 2?", "options": ["14", "16", "18"], "answer": "16"},
            {"question": "What is 20 ÷ 4?", "options": ["4", "5", "6"], "answer": "5"},
        ]
    },
    {
        "name": "Family Members",
        "questions": [
            {"question": "Who is your mum's husband?", "options": ["Brother", "Dad", "Uncle"], "answer": "Dad"},
            {"question": "Who is your dad's wife?", "options": ["Mum", "Sister", "Aunt"], "answer": "Mum"},
            {"question": "Who is your mum's son?", "options": ["Brother", "Cousin", "Dad"], "answer": "Brother"},
            {"question": "Who is your dad's daughter?", "options": ["Sister", "Mum", "Grandma"], "answer": "Sister"},
            {"question": "Who is your mum's mum?", "options": ["Grandma", "Aunt", "Sister"], "answer": "Grandma"},
            {"question": "Who is your dad's dad?", "options": ["Grandpa", "Uncle", "Brother"], "answer": "Grandpa"},
            {"question": "Who is your brother's brother?", "options": ["Dad", "You", "Cousin"], "answer": "You"},
            {"question": "Who is your sister's sister?", "options": ["Mum", "You", "Aunt"], "answer": "You"},
            {"question": "Who is your mum's brother?", "options": ["Uncle", "Dad", "Grandpa"], "answer": "Uncle"},
            {"question": "Who is your dad's sister?", "options": ["Aunt", "Mum", "Grandma"], "answer": "Aunt"},
            {"question": "Who is your uncle's child?", "options": ["Cousin", "Brother", "Dad"], "answer": "Cousin"},
            {"question": "Who is your aunt's child?", "options": ["Cousin", "Sister", "Mum"], "answer": "Cousin"},
            {"question": "Who is your grandpa's wife?", "options": ["Grandma", "Aunt", "Mum"], "answer": "Grandma"},
            {"question": "Who is your grandma's husband?", "options": ["Grandpa", "Uncle", "Dad"], "answer": "Grandpa"},
            {"question": "Who is your cousin's dad?", "options": ["Uncle", "Brother", "Grandpa"], "answer": "Uncle"},
            {"question": "Who is your cousin's mum?", "options": ["Aunt", "Sister", "Grandma"], "answer": "Aunt"},
            {"question": "Who is your brother's mum?", "options": ["Mum", "Aunt", "Cousin"], "answer": "Mum"},
            {"question": "Who is your sister's dad?", "options": ["Dad", "Uncle", "Cousin"], "answer": "Dad"},
            {"question": "Who is your mum's dad?", "options": ["Grandpa", "Brother", "Uncle"], "answer": "Grandpa"},
            {"question": "Who is your dad's mum?", "options": ["Grandma", "Sister", "Aunt"], "answer": "Grandma"},
        ]
    },
    {
        "name": "Animals",
        "questions": [
            {"question": "Which animal is known as man's best friend?", "options": ["Cat", "Dog", "Bird"], "answer": "Dog"},
            {"question": "Which animal says 'meow'?", "options": ["Dog", "Cat", "Fish"], "answer": "Cat"},
            {"question": "Which animal lives in water?", "options": ["Bird", "Fish", "Lion"], "answer": "Fish"},
            {"question": "Which animal can fly?", "options": ["Bird", "Tiger", "Snake"], "answer": "Bird"},
            {"question": "Which animal is the king of the jungle?", "options": ["Elephant", "Lion", "Giraffe"], "answer": "Lion"},
            {"question": "Which animal has a long neck?", "options": ["Giraffe", "Zebra", "Monkey"], "answer": "Giraffe"},
            {"question": "Which animal is very big and grey?", "options": ["Elephant", "Rhino", "Hippo"], "answer": "Elephant"},
            {"question": "Which animal swings from trees?", "options": ["Monkey", "Bear", "Wolf"], "answer": "Monkey"},
            {"question": "Which animal has stripes?", "options": ["Zebra", "Cheetah", "Deer"], "answer": "Zebra"},
            {"question": "Which animal is fast and has spots?", "options": ["Cheetah", "Leopard", "Tiger"], "answer": "Cheetah"},
            {"question": "Which animal has a trunk?", "options": ["Elephant", "Rhino", "Giraffe"], "answer": "Elephant"},
            {"question": "Which animal says 'roar'?", "options": ["Lion", "Bear", "Wolf"], "answer": "Lion"},
            {"question": "Which animal is small and has wings?", "options": ["Bird", "Bat", "Butterfly"], "answer": "Bird"},
            {"question": "Which animal lives in a hive?", "options": ["Bee", "Ant", "Spider"], "answer": "Bee"},
            {"question": "Which animal has a shell?", "options": ["Turtle", "Snake", "Lizard"], "answer": "Turtle"},
            {"question": "Which animal is known for jumping?", "options": ["Kangaroo", "Rabbit", "Frog"], "answer": "Kangaroo"},
            {"question": "Which animal has eight legs?", "options": ["Spider", "Crab", "Scorpion"], "answer": "Spider"},
            {"question": "Which animal is a big cat?", "options": ["Tiger", "Wolf", "Fox"], "answer": "Tiger"},
            {"question": "Which animal lives in the Arctic?", "options": ["Polar Bear", "Grizzly Bear", "Black Bear"], "answer": "Polar Bear"},
            {"question": "Which animal is known for its black and white fur?", "options": ["Panda", "Skunk", "Dalmatian"], "answer": "Panda"},
        ]
    },
    {
        "name": "Routines",
        "questions": [
            {"question": "What do you do first in the morning?", "options": ["Eat lunch", "Wake up", "Go to bed"], "answer": "Wake up"},
            {"question": "What do you do with your teeth after eating?", "options": ["Brush teeth", "Wash face", "Comb hair"], "answer": "Brush teeth"},
            {"question": "What do you eat in the morning?", "options": ["Dinner", "Breakfast", "Lunch"], "answer": "Breakfast"},
            {"question": "What do you do at school?", "options": ["Sleep", "Learn", "Watch TV"], "answer": "Learn"},
            {"question": "What do you do after school?", "options": ["Homework", "Go to bed", "Eat breakfast"], "answer": "Homework"},
            {"question": "What do you eat at midday?", "options": ["Lunch", "Dinner", "Snack"], "answer": "Lunch"},
            {"question": "What do you do before bed?", "options": ["Eat breakfast", "Brush teeth", "Go to school"], "answer": "Brush teeth"},
            {"question": "What do you wear to bed?", "options": ["Pyjamas", "School uniform", "Swimsuit"], "answer": "Pyjamas"},
            {"question": "What do you do at night?", "options": ["Go to school", "Sleep", "Eat lunch"], "answer": "Sleep"},
            {"question": "What do you do with your hair in the morning?", "options": ["Comb hair", "Brush teeth", "Wash dishes"], "answer": "Comb hair"},
            {"question": "What do you eat in the evening?", "options": ["Breakfast", "Lunch", "Dinner"], "answer": "Dinner"},
            {"question": "What do you do to clean your face?", "options": ["Wash face", "Brush teeth", "Comb hair"], "answer": "Wash face"},
            {"question": "What do you do with dishes after eating?", "options": ["Wash dishes", "Make bed", "Read book"], "answer": "Wash dishes"},
            {"question": "What do you do to keep your room tidy?", "options": ["Make bed", "Watch TV", "Play games"], "answer": "Make bed"},
            {"question": "What do you do for fun after homework?", "options": ["Play games", "Go to school", "Sleep"], "answer": "Play games"},
            {"question": "What do you do to learn new things?", "options": ["Read book", "Eat snack", "Wash clothes"], "answer": "Read book"},
            {"question": "What do you do with dirty clothes?", "options": ["Wash clothes", "Comb hair", "Brush teeth"], "answer": "Wash clothes"},
            {"question": "What do you do to stay healthy?", "options": ["Exercise", "Sleep all day", "Watch TV"], "answer": "Exercise"},
            {"question": "What do you do to relax?", "options": ["Watch TV", "Go to school", "Wash dishes"], "answer": "Watch TV"},
            {"question": "What do you do to talk to friends?", "options": ["Call friends", "Make bed", "Eat lunch"], "answer": "Call friends"},
        ]
    }
]
current_level = 0
current_questions = []
current_question_idx = 0
quiz_score = 0
selected_answer = None
quiz_feedback = ""

# Memory game variables
memory_items = [
    {"category": "Colours", "name": "Red"},
    {"category": "Colours", "name": "Blue"},
    {"category": "Colours", "name": "Green"},
    {"category": "Colours", "name": "Yellow"},
    {"category": "Colours", "name": "Purple"},
    {"category": "Colours", "name": "Orange"},
    {"category": "Colours", "name": "Pink"},
    {"category": "Animals", "name": "Cat"},
    {"category": "Animals", "name": "Dog"},
    {"category": "Animals", "name": "Bird"},
    {"category": "Animals", "name": "Fish"},
    {"category": "Animals", "name": "Lion"},
    {"category": "Animals", "name": "Elephant"},
    {"category": "Animals", "name": "Giraffe"},
    {"category": "Food", "name": "Apple"},
    {"category": "Food", "name": "Banana"},
    {"category": "Food", "name": "Pizza"},
    {"category": "Food", "name": "Burger"},
    {"category": "Food", "name": "Ice Cream"},
    {"category": "Food", "name": "Cake"},
    {"category": "Food", "name": "Carrot"},
]
memory_grid = []
card_size = 100
card_margin = 20
selected_cards = []
matched_pairs = []
memory_feedback = ""

def setup():
    global memory_grid, current_questions
    screen.fill(WHITE)
    pygame.display.flip()
    # Initialize quiz questions
    if game_state == QUIZ_GAME and not current_questions:
        current_questions = random.sample(quiz_levels[current_level]["questions"], 10)
    # Initialize memory game grid
    if game_state == MEMORY_GAME:
        selected_items = random.sample(memory_items, 6) * 2  # 6 pairs
        random.shuffle(selected_items)
        memory_grid = [[selected_items[i * 4 + j] for j in range(4)] for i in range(3)]

def draw_button(text, x, y, w, h, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.rect(screen, hover_color, (x, y, w, h))
    else:
        pygame.draw.rect(screen, color, (x, y, w, h))
    text_surf = small_font.render(text, True, BLACK)
    screen.blit(text_surf, (x + (w - text_surf.get_width()) // 2, y + (h - text_surf.get_height()) // 2))

def draw_main_menu():
    screen.fill(YELLOW)
    title = font.render("Let's Play English", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))
    draw_button("Play Quiz", 300, 250, 200, 60, BLUE, GREEN)
    draw_button("Play Memory Game", 300, 350, 200, 60, BLUE, GREEN)
    draw_button("Exit", 300, 450, 200, 60, RED, PINK)

def draw_quiz_game():
    screen.fill(YELLOW)
    level_text = small_font.render(f"Level: {quiz_levels[current_level]['name']}", True, BLACK)
    screen.blit(level_text, (50, 50))
    question = current_questions[current_question_idx]
    q_text = small_font.render(question["question"], True, BLACK)
    screen.blit(q_text, (WIDTH // 2 - q_text.get_width() // 2, 150))
    
    for i, option in enumerate(question["options"]):
        draw_button(option, 300, 250 + i * 80, 200, 60, BLUE, GREEN)
    
    score_text = small_font.render(f"Score: {quiz_score}", True, BLACK)
    screen.blit(score_text, (50, 100))
    feedback_text = small_font.render(quiz_feedback, True, RED)
    screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, 500))
    draw_button("Main Menu", 50, 500, 150, 50, GRAY, GREEN)

def draw_memory_game():
    screen.fill(YELLOW)
    for i in range(3):
        for j in range(4):
            x = 200 + j * (card_size + card_margin)
            y = 100 + i * (card_size + card_margin)
            item = memory_grid[i][j]
            if (i, j) in selected_cards or item["name"] in matched_pairs:
                # Draw "image" (colored rectangle)
                pygame.draw.rect(screen, CATEGORY_COLORS[item["category"]], (x, y, card_size, card_size))
                # Draw subtitle
                text = small_font.render(item["name"], True, WHITE)
                screen.blit(text, (x + (card_size - text.get_width()) // 2, y + card_size + 5))
            else:
                pygame.draw.rect(screen, GRAY, (x, y, card_size, card_size))
    
    feedback_text = small_font.render(memory_feedback, True, RED)
    screen.blit(feedback_text, (WIDTH // 2 - feedback_text.get_width() // 2, 500))
    draw_button("Main Menu", 50, 500, 150, 50, GRAY, GREEN)

def handle_quiz_click(pos):
    global selected_answer, quiz_feedback, quiz_score, current_question_idx, current_level, game_state, current_questions
    x, y = pos
    question = current_questions[current_question_idx]
    for i, option in enumerate(question["options"]):
        if 300 < x < 500 and 250 + i * 80 < y < 310 + i * 80:
            selected_answer = option
            if selected_answer == question["answer"]:
                quiz_score += 1
                quiz_feedback = "Correct! Great job!"
            else:
                quiz_feedback = "Wrong! Try again."
            current_question_idx += 1
            if current_question_idx >= len(current_questions):
                quiz_feedback = f"Level Complete! Score: {quiz_score}"
                current_level += 1
                if current_level >= len(quiz_levels):
                    quiz_feedback = f"Game Over! Final Score: {quiz_score}"
                    current_level = 0
                    quiz_score = 0
                current_question_idx = 0
                current_questions = random.sample(quiz_levels[current_level]["questions"], 10)
            selected_answer = None
            return
    if 50 < x < 200 and 500 < y < 550:
        game_state = MAIN_MENU
        quiz_feedback = ""
        current_question_idx = 0
        current_level = 0
        quiz_score = 0
        current_questions = []

def handle_memory_click(pos):
    global selected_cards, memory_feedback, matched_pairs, game_state
    x, y = pos
    if 50 < x < 200 and 500 < y < 550:
        game_state = MAIN_MENU
        memory_feedback = ""
        selected_cards = []
        matched_pairs = []
        return
    for i in range(3):
        for j in range(4):
            card_x = 200 + j * (card_size + card_margin)
            card_y = 100 + i * (card_size + card_margin)
            if card_x < x < card_x + card_size and card_y < y < card_y + card_size:
                if (i, j) not in selected_cards and len(selected_cards) < 2:
                    selected_cards.append((i, j))
                    if len(selected_cards) == 2:
                        card1 = memory_grid[selected_cards[0][0]][selected_cards[0][1]]["name"]
                        card2 = memory_grid[selected_cards[1][0]][selected_cards[1][1]]["name"]
                        if card1 == card2:
                            matched_pairs.append(card1)
                            memory_feedback = "Match! Awesome!"
                            selected_cards = []
                            if len(matched_pairs) == 6:  # 6 pairs
                                memory_feedback = "You Win! All pairs matched!"
                                matched_pairs = []
                                setup()
                        else:
                            memory_feedback = "No match! Try again."
                            # Cards will be flipped back in update_loop

def update_loop():
    global selected_cards, memory_feedback, game_state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if game_state == MAIN_MENU:
                if 300 < x < 500 and 250 < y < 310:
                    game_state = QUIZ_GAME
                    setup()
                elif 300 < x < 500 and 350 < y < 410:
                    game_state = MEMORY_GAME
                    setup()
                elif 300 < x < 500 and 450 < y < 510:
                    pygame.quit()
                    return
            elif game_state == QUIZ_GAME:
                handle_quiz_click(event.pos)
            elif game_state == MEMORY_GAME:
                handle_memory_click(event.pos)
    
    # Clear selected cards in memory game after a short delay
    if len(selected_cards) == 2 and memory_grid[selected_cards[0][0]][selected_cards[0][1]]["name"] != memory_grid[selected_cards[1][0]][selected_cards[1][1]]["name"]:
        pygame.time.wait(1000)  # Show cards briefly
        selected_cards = []
        memory_feedback = ""
    
    # Draw current game state
    if game_state == MAIN_MENU:
        draw_main_menu()
    elif game_state == QUIZ_GAME:
        draw_quiz_game()
    elif game_state == MEMORY_GAME:
        draw_memory_game()
    
    pygame.display.flip()

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / 60)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())