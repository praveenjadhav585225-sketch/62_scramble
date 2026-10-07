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

        self.input_box = TextBox(width // 2 - 130, 210, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 + 45, 210, 95, 46)
        self.hint_btn = pygame.Rect(width // 2 + 150, 210, 85, 46)

        # Stores the positions of letters that have already been revealed.
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

        # Reset all revealed hint positions for the new round.
        self.revealed_indices = set()

        self.input_box.clear()

    def use_hint(self):
        # Find positions that have not been revealed yet.
        hidden_indices = [
            index
            for index in range(len(self.secret_word))
            if index not in self.revealed_indices
        ]

        # If every letter has already been revealed, do nothing.
        if not hidden_indices:
            return

        # Select one unrevealed position.
        index = random.choice(hidden_indices)

        # Mark this position as revealed.
        self.revealed_indices.add(index)

        # Deduct 0.5 points, but never allow the score to go below 0.
        self.score = max(0, self.score - 0.5)

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()

        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1 fix: compare the guess with the actual secret word.
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 1
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)
            self.next_round()

        else:
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
        pass

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

        # The scrambled word remains visible as the puzzle.
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
                130
            )
        )

        # Display the hint pattern.
        # Revealed letters appear in their correct positions.
        # Hidden letters are represented by underscores.
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
                170
            )
        )

        self.input_box.render(screen)

        # Submit button
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

        # Hint button
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
                285
            )
        )