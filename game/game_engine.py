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

        self.input_box = TextBox(width // 2 - 130, 210, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 + 45, 210, 95, 46)
        self.hint_btn = pygame.Rect(width // 2 + 150, 210, 85, 46)

        # Task 2: Track positions of revealed letters.
        self.revealed_indices = set()

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_word = pygame.font.SysFont(None, 52)
        self.font_msg = pygame.font.SysFont(None, 26)
        self.font_btn = pygame.font.SysFont(None, 24)

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
        self.scrambled_word = self.scramble_string(self.secret_word)

        # Task 2: Reset revealed hints for the new round.
        self.revealed_indices = set()

        self.input_box.clear()

        # Task 3: Start a fresh timer.
        self.round_start_time = pygame.time.get_ticks()
        self.remaining_time = self.round_duration

    def use_hint(self):
        # Find positions that have not been revealed yet.
        hidden_indices = [
            index
            for index in range(len(self.secret_word))
            if index not in self.revealed_indices
        ]

        # Do nothing if all letters are already revealed.
        if not hidden_indices:
            return

        # Reveal one previously hidden position.
        index = random.choice(hidden_indices)
        self.revealed_indices.add(index)

        # Task 2: Deduct 0.5 points, but never go below 0.
        self.score = max(0, self.score - 0.5)

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Compare the guess with the actual secret word.
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)

            # Correct answer starts a new round and fresh timer.
            self.next_round()

        else:
            # Wrong answer does not reset the timer.
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit_guess()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()

            elif self.hint_btn.collidepoint(event.pos):
                self.use_hint()

    def update(self):
        # Task 3: Calculate elapsed time using Pygame ticks.
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - self.round_start_time) / 1000

        self.remaining_time = max(
            0,
            self.round_duration - elapsed_time
        )

        # Time has expired.
        if self.remaining_time <= 0:
            expired_word = self.secret_word

            # Reveal the current word in the feedback message.
            self.feedback_msg = (
                f"TIME'S UP! The word was '{expired_word}'."
            )
            self.feedback_color = (240, 80, 80)

            # Automatically start the next round.
            # This also resets the timer and revealed hints.
            self.next_round()

    def render(self, screen):
        screen.fill((26, 30, 38))

        title_surf = self.font_title.render(
            "Word Scramble Arena",
            True,
            (245, 245, 245)
        )
        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                25
            )
        )

        score_surf = self.font_msg.render(
            f"Score: {self.score:g}",
            True,
            (255, 220, 80)
        )
        screen.blit(
            score_surf,
            (
                self.width // 2 - score_surf.get_width() // 2,
                70
            )
        )

        # Task 3: Display remaining time.
        timer_surf = self.font_msg.render(
            f"Time: {self.remaining_time:.1f}s",
            True,
            (255, 255, 255)
        )
        screen.blit(
            timer_surf,
            (
                self.width // 2 - timer_surf.get_width() // 2,
                100
            )
        )

        # Task 3: Horizontal timer/progress bar.
        bar_width = 400
        bar_height = 12
        bar_x = self.width // 2 - bar_width // 2
        bar_y = 125

        # Timer bar background.
        pygame.draw.rect(
            screen,
            (70, 70, 80),
            (bar_x, bar_y, bar_width, bar_height),
            border_radius=6
        )

        # Calculate remaining percentage.
        progress = self.remaining_time / self.round_duration
        progress = max(0, min(1, progress))

        current_bar_width = int(bar_width * progress)

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

        # The scrambled word remains visible.
        spaced_letters = "  ".join(self.scrambled_word)

        scramble_surf = self.font_word.render(
            spaced_letters,
            True,
            (100, 200, 255)
        )
        screen.blit(
            scramble_surf,
            (
                self.width // 2 - scramble_surf.get_width() // 2,
                145
            )
        )

        # Task 2: Display revealed letters in their correct positions.
        hint_pattern = "  ".join(
            self.secret_word[index]
            if index in self.revealed_indices
            else "_"
            for index in range(len(self.secret_word))
        )

        hint_surf = self.font_word.render(
            hint_pattern,
            True,
            (255, 200, 100)
        )
        screen.blit(
            hint_surf,
            (
                self.width // 2 - hint_surf.get_width() // 2,
                190
            )
        )

        self.input_box.render(screen)

        # Submit button.
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
                self.submit_btn.centerx - btn_text.get_width() // 2,
                self.submit_btn.centery - btn_text.get_height() // 2
            )
        )

        # HINT button.
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
                self.hint_btn.centerx - hint_btn_text.get_width() // 2,
                self.hint_btn.centery - hint_btn_text.get_height() // 2
            )
        )

        feedback_surf = self.font_msg.render(
            self.feedback_msg,
            True,
            self.feedback_color
        )
        screen.blit(
            feedback_surf,
            (
                self.width // 2 - feedback_surf.get_width() // 2,
                300
            )
        )