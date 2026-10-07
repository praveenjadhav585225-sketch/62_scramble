import random
import pygame
from game.text_box import TextBox


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = [
            "PYTHON",
            "PYGAME",
            "PLANET",
            "ROCKET",
            "GALAXY",
            "STREAM",
            "PUZZLE",
            "ALGORITHM"
        ]

        self.secret_word = ""
        self.scrambled_word = ""

        self.score = 0
        self.feedback_msg = "Unscramble the letters above!"
        self.feedback_color = (210, 215, 225)

        # Task 3: 15-second countdown for each round.
        self.round_duration = 15
        self.round_start_time = 0
        self.remaining_time = self.round_duration

        # Keep the existing input box for compatibility,
        # but Task 4 tiles are used as the submitted answer.
        self.input_box = TextBox(width // 2 - 130, 310, 160, 46)

        self.submit_btn = pygame.Rect(
            width // 2 + 45, 310, 95, 46
        )

        self.hint_btn = pygame.Rect(
            width // 2 + 150, 310, 85, 46
        )

        # Task 2: Track positions of revealed letters.
        self.revealed_indices = set()

        # Task 4: Interactive letter tiles.
        self.tile_width = 50
        self.tile_height = 50
        self.tile_gap = 8
        self.tile_y = 145

        self.tile_positions = []
        self.selected_tile = None

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)
        self.font_tile = pygame.font.SysFont(None, 32)

        self.next_round()

    def scramble_string(self, word):
        letters = list(word)

        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)

            if shuffled != word or len(word) <= 1:
                return shuffled

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_word = self.scramble_string(
            self.secret_word
        )

        # Task 2: Reset hints.
        self.revealed_indices = set()

        # Task 4: Reset tiles using the new scrambled word.
        self.tile_positions = list(self.scrambled_word)
        self.selected_tile = None

        self.input_box.clear()

        # Task 3: Start a fresh timer.
        self.round_start_time = pygame.time.get_ticks()
        self.remaining_time = self.round_duration

    def use_hint(self):
        hidden_indices = [
            index
            for index in range(len(self.secret_word))
            if index not in self.revealed_indices
        ]

        if not hidden_indices:
            return

        index = random.choice(hidden_indices)
        self.revealed_indices.add(index)

        # Task 2: 0.5 point penalty.
        self.score = max(0, self.score - 0.5)

    # -------------------------
    # Task 4: Letter Tiles
    # -------------------------

    def get_tile_rect(self, index):
        total_width = (
            len(self.tile_positions) * self.tile_width
            + (len(self.tile_positions) - 1) * self.tile_gap
        )

        start_x = self.width // 2 - total_width // 2

        x = start_x + index * (
            self.tile_width + self.tile_gap
        )

        return pygame.Rect(
            x,
            self.tile_y,
            self.tile_width,
            self.tile_height
        )

    def handle_tile_click(self, mouse_pos):
        clicked_index = None

        for index in range(len(self.tile_positions)):
            tile_rect = self.get_tile_rect(index)

            if tile_rect.collidepoint(mouse_pos):
                clicked_index = index
                break

        if clicked_index is None:
            return

        # First click selects a tile.
        if self.selected_tile is None:
            self.selected_tile = clicked_index
            return

        # Clicking the same tile cancels selection.
        if self.selected_tile == clicked_index:
            self.selected_tile = None
            return

        # Second click swaps the two tiles.
        first = self.selected_tile
        second = clicked_index

        self.tile_positions[first], self.tile_positions[second] = (
            self.tile_positions[second],
            self.tile_positions[first]
        )

        self.selected_tile = None

    def submit_guess(self):
        # Task 4: Tile arrangement is the submitted answer.
        guess = "".join(self.tile_positions).upper()

        if not guess:
            self.feedback_msg = "Arrange the tiles before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Validate against the actual secret word.
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1

            self.feedback_msg = (
                f"CORRECT! '{self.secret_word}' is right."
            )

            self.feedback_color = (80, 230, 110)

            # Start a new round.
            self.next_round()

        else:
            # Wrong answer does not advance the round.
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)

    def handle_event(self, event):
        # Keep the existing text box functional.
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_guess()

        elif (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):
            # Task 4: Handle tile clicks.
            self.handle_tile_click(event.pos)

            # Submit button.
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

            # Hint button.
            elif self.hint_btn.collidepoint(event.pos):
                self.use_hint()

    def update(self):
        # Task 3: Calculate elapsed time.
        current_time = pygame.time.get_ticks()

        elapsed_time = (
            current_time - self.round_start_time
        ) / 1000

        self.remaining_time = max(
            0,
            self.round_duration - elapsed_time
        )

        # Time expired.
        if self.remaining_time <= 0:
            expired_word = self.secret_word

            self.feedback_msg = (
                f"TIME'S UP! The word was '{expired_word}'."
            )

            self.feedback_color = (240, 80, 80)

            # Start the next round.
            self.next_round()

    def render(self, screen):
        screen.fill((26, 30, 38))

        # -------------------------
        # Title
        # -------------------------

        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )

        screen.blit(
            title_surf,
            (
                self.width // 2
                - title_surf.get_width() // 2,
                25
            )
        )

        # -------------------------
        # Score
        # -------------------------

        score_surf = self.font_msg.render(
            f"Score: {self.score:g}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (
                self.width // 2
                - score_surf.get_width() // 2,
                70
            )
        )

        # -------------------------
        # Timer
        # -------------------------

        timer_surf = self.font_msg.render(
            f"Time: {self.remaining_time:.1f}s",
            True,
            (255, 255, 255)
        )

        screen.blit(
            timer_surf,
            (
                self.width // 2
                - timer_surf.get_width() // 2,
                100
            )
        )

        # Timer progress bar.
        bar_width = 400
        bar_height = 12

        bar_x = (
            self.width // 2
            - bar_width // 2
        )

        bar_y = 125

        pygame.draw.rect(
            screen,
            (70, 70, 80),
            (
                bar_x,
                bar_y,
                bar_width,
                bar_height
            ),
            border_radius=6
        )

        progress = (
            self.remaining_time
            / self.round_duration
        )

        progress = max(
            0,
            min(1, progress)
        )

        current_bar_width = int(
            bar_width * progress
        )

        if current_bar_width > 0:
            pygame.draw.rect(
                screen,
                (80, 200, 110),
                (
                    bar_x,
                    bar_y,
                    current_bar_width,
                    bar_height
                ),
                border_radius=6
            )

        # -------------------------
        # Task 4: Letter Tiles
        # -------------------------

        for index, letter in enumerate(
            self.tile_positions
        ):
            tile_rect = self.get_tile_rect(index)

            if self.selected_tile == index:
                tile_color = (255, 180, 60)
            else:
                tile_color = (60, 110, 180)

            pygame.draw.rect(
                screen,
                tile_color,
                tile_rect,
                border_radius=7
            )

            pygame.draw.rect(
                screen,
                (220, 220, 220),
                tile_rect,
                width=2,
                border_radius=7
            )

            letter_surf = self.font_tile.render(
                letter,
                True,
                (255, 255, 255)
            )

            screen.blit(
                letter_surf,
                (
                    tile_rect.centerx
                    - letter_surf.get_width() // 2,
                    tile_rect.centery
                    - letter_surf.get_height() // 2
                )
            )

        # -------------------------
        # Task 2: Hint Pattern
        # -------------------------

        hint_pattern = "  ".join(
            self.secret_word[index]
            if index in self.revealed_indices
            else "_"
            for index in range(
                len(self.secret_word)
            )
        )

        hint_surf = self.font_word.render(
            hint_pattern,
            True,
            (255, 200, 100)
        )

        screen.blit(
            hint_surf,
            (
                self.width // 2
                - hint_surf.get_width() // 2,
                205
            )
        )

        # -------------------------
        # Input Box
        # -------------------------

        self.input_box.render(screen)

        # -------------------------
        # Submit Button
        # -------------------------

        pygame.draw.rect(
            screen,
            (50, 150, 85),
            self.submit_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.submit_btn,
            width=2,
            border_radius=6
        )

        btn_text = self.font_btn.render(
            "SUBMIT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            btn_text,
            (
                self.submit_btn.centerx
                - btn_text.get_width() // 2,
                self.submit_btn.centery
                - btn_text.get_height() // 2
            )
        )

        # -------------------------
        # Hint Button
        # -------------------------

        pygame.draw.rect(
            screen,
            (180, 130, 45),
            self.hint_btn,
            border_radius=6
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            self.hint_btn,
            width=2,
            border_radius=6
        )

        hint_btn_text = self.font_btn.render(
            "HINT",
            True,
            (255, 255, 255)
        )

        screen.blit(
            hint_btn_text,
            (
                self.hint_btn.centerx
                - hint_btn_text.get_width() // 2,
                self.hint_btn.centery
                - hint_btn_text.get_height() // 2
            )
        )

        # -------------------------
        # Feedback
        # -------------------------

        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )

        screen.blit(
            feedback_surf,
            (
                self.width // 2
                - feedback_surf.get_width() // 2,
                380
            )
        )