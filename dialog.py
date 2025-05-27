import pygame
from colors import Colors


class NameDialog:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 40)
        self.big_font = pygame.font.Font(None, 60)
        self.colors = Colors()
        self.input_text = ""
        self.active = True
        self.alpha = 0
        self.blink_timer = 0
        self.sound_played = False
        self.sound = pygame.mixer.Sound("../tetris_pygame_app/Sounds/GameOver.ogg")
        self.error_sound = pygame.mixer.Sound("../tetris_pygame_app/Sounds/error.mp3")

        # Градиентный фон
        self.background = pygame.Surface((400, 200))
        self.background.fill(self.colors.dark_blue)
        self.background.set_alpha(200)

        # Позиции
        self.rect = self.background.get_rect(center=(250, 310))

    def draw(self):
        # Анимация появления
        if self.alpha < 200:
            self.alpha += 5
            self.background.set_alpha(self.alpha)

        if not self.sound_played:
            self.sound.play()
            self.sound_played = True

        # Фон с градиентом
        self.screen.blit(self.background, self.rect)
        pygame.draw.rect(self.screen, self.colors.light_blue, self.rect, 3, border_radius=10)

        # Заголовок с тенью
        text = self.big_font.render("НОВЫЙ РЕКОРД!", True, self.colors.white)
        shadow = self.big_font.render("НОВЫЙ РЕКОРД!", True, (0, 0, 0))

        # Позиционирование
        text_rect = text.get_rect(center=(250, 250))
        self.screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        self.screen.blit(text, text_rect)

        # Поле ввода
        input_rect = pygame.Rect(150, 300, 200, 40)
        pygame.draw.rect(self.screen, self.colors.light_blue, input_rect, 2, border_radius=5)

        # Мерцающий текст
        self.blink_timer = (self.blink_timer + 1) % 30
        if self.blink_timer < 20:
            prompt = self.font.render(self.input_text + "|", True, self.colors.white)
        else:
            prompt = self.font.render(self.input_text, True, self.colors.white)

        self.screen.blit(prompt, (160, 305))
        # Инструкция
        info_text = self.font.render("    Нажмите Enter", True, self.colors.white)
        self.screen.blit(info_text, (120, 370))

        pygame.display.update()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if self.input_text.strip():
                    self.active = False
                else:
                    self.error_sound.play()
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif len(self.input_text) < 15 and event.unicode.isprintable():
                self.input_text += event.unicode
