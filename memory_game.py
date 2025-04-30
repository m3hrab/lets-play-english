import pygame
import settings
import random
import json

class MemoryGame:
    def __init__(self):
        # Load memory_data.json from file
        try:
            with open('memory_data.json', 'r') as f:
                self.memory_data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError("memory_data.json file not found. Please ensure it exists in the same directory as the script.")
        except json.JSONDecodeError:
            raise ValueError("memory_data.json is not a valid JSON file.")

        # Fonts 
        self.font_large = pygame.font.Font("assets/font/PlaypenSans-Bold.ttf", 36)  
        self.font_medium = pygame.font.Font("assets/font/PlaypenSans-SemiBold.ttf", 24)  
        self.font_small = pygame.font.Font("assets/font/PlaypenSans-Bold.ttf", 14)  

        # Colors 
        self.TILE_COLOR = (255, 255, 153)        
        self.BORDER_COLOR = (255, 102, 255)      
        self.HOVER_COLOR = (153, 255, 153)       
        self.MATCH_COLOR = (102, 255, 102)       
        self.FLIP_COLOR = (153, 204, 255)       

        # Game variables
        self.current_level = 0  
        self.levels = self.memory_data["levels"]
        self.GRID_SIZE = 6  
        self.TILE_SIZE = 110  # Size of each tile
        self.GRID_X = (settings.WIDTH - self.GRID_SIZE * self.TILE_SIZE) // 2  # Center the grid
        self.GRID_Y = 80  # Start below the title
        self.initialize_game()

    def initialize_game(self):
        # Select 12 random items for pairs from the current level
        all_items = self.levels[self.current_level]["items"].copy()
        selected_items = random.sample(all_items, 12)
        # Create pairs by duplicating the selected items
        tile_items = selected_items * 2  # 12 items x 2 = 24 tiles
        random.shuffle(tile_items)

        # Initialize the 6x6 grid (36 tiles, 12 will be empty/unused)
        self.grid = []
        tile_index = 0
        for row in range(self.GRID_SIZE):
            grid_row = []
            for col in range(self.GRID_SIZE):
                if tile_index < len(tile_items):
                    item = tile_items[tile_index]
                    grid_row.append({
                        "item": {
                            "name": item["name"],
                            "color": tuple(item["color"]),
                            "image_path": item["image_path"]
                        },
                        "flipped": False,
                        "matched": False,
                        "rect": pygame.Rect(
                            self.GRID_X + col * self.TILE_SIZE,
                            self.GRID_Y + row * self.TILE_SIZE,
                            self.TILE_SIZE - 5,
                            self.TILE_SIZE - 5
                        )
                    })
                    tile_index += 1
                else:
                    # Empty tile (no item)
                    grid_row.append({
                        "item": None,
                        "flipped": False,
                        "matched": False,
                        "rect": pygame.Rect(
                            self.GRID_X + col * self.TILE_SIZE,
                            self.GRID_Y + row * self.TILE_SIZE,
                            self.TILE_SIZE - 5,
                            self.TILE_SIZE - 5
                        )
                    })
            self.grid.append(grid_row)

        # Game state
        self.flipped_tiles = []  # Track currently flipped tiles
        self.feedback = None
        self.feedback_timer = 0
        self.matches_found = 0
        self.total_pairs = 12  # 12 pairs to match
        self.game_over = False

    def draw(self, screen):
        # Draw header with level name
        header_text = self.font_large.render(f"Level: {self.levels[self.current_level]['name']}", True, settings.HEADER_COLOR)
        header_rect = header_text.get_rect(center=(settings.WIDTH // 2, 50))
        screen.blit(header_text, header_rect)

        if not self.game_over:
            # Draw the grid
            mouse_pos = pygame.mouse.get_pos()
            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    tile = self.grid[row][col]
                    rect = tile["rect"]

                    if tile["item"] is None:
                        continue  

                    # Determine tile color based on state
                    if tile["matched"]:
                        color = self.MATCH_COLOR
                    elif tile["flipped"]:
                        color = self.FLIP_COLOR
                    elif rect.collidepoint(mouse_pos):
                        color = self.HOVER_COLOR
                    else:
                        color = self.TILE_COLOR

                    # Draw the tile
                    pygame.draw.rect(screen, self.BORDER_COLOR, rect, border_radius=10)
                    pygame.draw.rect(screen, color, rect.inflate(-5, -5), border_radius=10)

                    # If flipped or matched, show the "image" (or placeholder) and subtitle
                    if tile["flipped"] or tile["matched"]:
                        # Define the image/placeholder area
                        image_rect = rect.inflate(-10, -10)
                        image_rect.height = self.TILE_SIZE // 1.2
                        image_rect.center = (rect.centerx, rect.centery)

                        # Check if there's an image path; if not, use the colored rectangle
                        if tile["item"]["image_path"] is not None:
                            try:
                                # Placeholder: Draw a colored rectangle for now
                                # When you add actual images, replace this with:
                                image = pygame.image.load(tile["item"]["image_path"]).convert_alpha()
                                image = pygame.transform.scale(image, (image_rect.width, image_rect.height))
                                screen.blit(image, image_rect)
                                # pygame.draw.rect(screen, tile["item"]["color"], image_rect, border_radius=5)
                                # Add a "Image Placeholder" label for Food and Animals
                                # if self.levels[self.current_level]["name"] != "Colors":
                                #     placeholder_text = self.font_small.render("Image Here", True, settings.BLACK)
                                #     placeholder_rect = placeholder_text.get_rect(center=image_rect.center)
                                #     screen.blit(placeholder_text, placeholder_rect)
                            except pygame.error:
                                # Fallback to colored rectangle if image loading fails
                                pygame.draw.rect(screen, tile["item"]["color"], image_rect, border_radius=5)
                        else:
                            # For Colors level, use the colored rectangle
                            pygame.draw.rect(screen, tile["item"]["color"], image_rect, border_radius=5)

                        # Draw the subtitle (name)
                        subtitle_text = self.font_small.render(tile["item"]["name"], True, settings.SUBTITLE_COLOR)
                        subtitle_rect = subtitle_text.get_rect(center=(rect.centerx, rect.centery + 27))
                        screen.blit(subtitle_text, subtitle_rect)

            # Display feedback if active
            if self.feedback:
                feedback_rect = pygame.Rect(settings.WIDTH // 2 - 150, settings.HEIGHT - 100, 300, 60)
                feedback_color = self.MATCH_COLOR if "Great job" in self.feedback else self.FLIP_COLOR
                pygame.draw.rect(screen, feedback_color, feedback_rect, border_radius=10)
                pygame.draw.rect(screen, settings.WHITE, feedback_rect.inflate(-5, -5), border_radius=10)
                feedback_text = self.font_small.render(self.feedback, True, settings.BLACK)
                feedback_text_rect = feedback_text.get_rect(center=feedback_rect.center)
                screen.blit(feedback_text, feedback_text_rect)



    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
            mouse_pos = pygame.mouse.get_pos()
            if self.feedback_timer > 0:
                return  # Don't allow new clicks while feedback is active

            for row in range(self.GRID_SIZE):
                for col in range(self.GRID_SIZE):
                    tile = self.grid[row][col]
                    if tile["item"] is None or tile["flipped"] or tile["matched"]:
                        continue

                    if tile["rect"].collidepoint(mouse_pos):
                        tile["flipped"] = True
                        self.flipped_tiles.append((row, col))

                        # If two tiles are flipped, check for a match
                        if len(self.flipped_tiles) == 2:
                            tile1_pos, tile2_pos = self.flipped_tiles
                            tile1 = self.grid[tile1_pos[0]][tile1_pos[1]]
                            tile2 = self.grid[tile2_pos[0]][tile2_pos[1]]

                            if tile1["item"]["name"] == tile2["item"]["name"]:
                                tile1["matched"] = True
                                tile2["matched"] = True
                                self.matches_found += 1
                                self.feedback = "Great job"
                                self.flipped_tiles = []  # Reset flipped tiles
                            else:
                                self.feedback = "Try again"

                            self.feedback_timer = settings.FEEDBACK_DURATION

                            if self.matches_found == self.total_pairs:
                                self.game_over = True

    def update(self):
        if self.feedback_timer > 0:
            self.feedback_timer -= 1
            if self.feedback_timer <= 0:
                self.feedback = None
                # If the last two flipped tiles didn't match, flip them back
                if self.flipped_tiles:
                    tile1_pos, tile2_pos = self.flipped_tiles
                    tile1 = self.grid[tile1_pos[0]][tile1_pos[1]]
                    tile2 = self.grid[tile2_pos[0]][tile2_pos[1]]
                    if not tile1["matched"] and not tile2["matched"]:
                        tile1["flipped"] = False
                        tile2["flipped"] = False
                    self.flipped_tiles = []

    def get_score(self):
        return self.matches_found

    def get_total_questions(self):
        return self.total_pairs

    def is_game_over(self):
        return self.game_over

    def set_level(self, level_index):
        self.current_level = level_index
        self.initialize_game()

    def reset(self):
        self.initialize_game()