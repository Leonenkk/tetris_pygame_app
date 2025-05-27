import pygame
from colors import Colors

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.colors = Colors()  # Создаем экземпляр
        self.buttons = [
            {"text": "Начать игру", "pos": (250, 200)},
            {"text": "Таблица рекордов", "pos": (250, 300)},
            {"text": "Справка", "pos": (250, 400)},
            {"text": "Выход", "pos": (250, 500)}
        ]
        self.font = pygame.font.Font(None, 40)
        self.selected = 0

    def draw(self):
        self.screen.fill(self.colors.dark_blue)  # Используем экземпляр
        for idx, btn in enumerate(self.buttons):
            color = self.colors.white if idx == self.selected else self.colors.grey
            text_surface = self.font.render(btn["text"], True, color)
            rect = text_surface.get_rect(center=btn["pos"])
            self.screen.blit(text_surface, rect)
        pygame.display.update()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.buttons)
            elif event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.buttons)
            elif event.key == pygame.K_RETURN:
                return self.selected
        return -1