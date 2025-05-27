import sys

from grid import Grid
from blocks import *
import random
import pygame


class Game:
    def __init__(self, config):
        self.grid = Grid()
        self.block_factory = BlockFactory(config)
        self.blocks = self.block_factory.get_all_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.game_over = False
        self.score = 0
        self.config = config
        self.fall_speed = config["game_settings"]["fall_speed"]
        self.rotate_sound = pygame.mixer.Sound("../tetris_pygame_app/Sounds/rotate.ogg")
        self.clear_sound = pygame.mixer.Sound("../tetris_pygame_app/Sounds/clear.ogg")
        self.game_over_sound = pygame.mixer.Sound("../tetris_pygame_app/Sounds/GameOver.ogg")

        pygame.mixer.music.load("../tetris_pygame_app/Sounds/music.ogg")
        pygame.mixer.music.play(-1)

    def get_random_block(self):
        if len(self.blocks) == 0:
            self.blocks = self.block_factory.get_all_blocks()
        block = random.choice(self.blocks)
        self.blocks.remove(block)
        return block

    def draw_game_over(self, screen, selected_option=0):
        """Отрисовка экрана проигрыша с выделением активной опции"""
        overlay = pygame.Surface((500, 620), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        big_font = pygame.font.Font(None, 72)
        game_over_text = big_font.render("GAME OVER", True, (255, 50, 50))
        text_rect = game_over_text.get_rect(center=(250, 200))

        shadow = big_font.render("GAME OVER", True, (0, 0, 0))
        screen.blit(shadow, (text_rect.x + 2, text_rect.y + 2))
        screen.blit(game_over_text, text_rect)

        btn_font = pygame.font.Font(None, 40)

        menu_color = (255, 255, 0) if selected_option == 0 else (200, 200, 200)
        menu_text = btn_font.render("В меню", True, menu_color)
        menu_rect = menu_text.get_rect(center=(250, 350))

        restart_color = (255, 255, 0) if selected_option == 1 else (200, 200, 200)
        restart_text = btn_font.render("Играть снова", True, restart_color)
        restart_rect = restart_text.get_rect(center=(250, 400))


        screen.blit(menu_text, menu_rect)
        screen.blit(restart_text, restart_rect)

        return menu_rect, restart_rect

    def handle_game_over(self, screen):
        """Обработка экрана проигрыша с клавиатурным управлением"""
        self.game_over_sound.play()
        pygame.mixer.music.stop()

        clock = pygame.time.Clock()
        waiting = True
        result = None
        selected_option = 0
        key_delay = 0

        while waiting:
            menu_rect, restart_rect = self.draw_game_over(screen, selected_option)

            if key_delay > 0:
                key_delay -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and key_delay == 0:
                    if event.key == pygame.K_UP:
                        selected_option = 0
                        key_delay = 10
                    elif event.key == pygame.K_DOWN:
                        selected_option = 1
                        key_delay = 10
                    elif event.key == pygame.K_RETURN:
                        result = "menu" if selected_option == 0 else "restart"
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        result = "menu"
                        waiting = False

            pygame.display.update()
            clock.tick(60)

        return result

    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points

    def move_left(self):
        self.current_block.move(0, -1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, 1)

    def move_right(self):
        self.current_block.move(0, 1)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(0, -1)

    def move_down(self):
        self.current_block.move(1, 0)
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.move(-1, 0)
            self.lock_block()

    def lock_block(self):
        tiles = self.current_block.get_cell_positions()
        for position in tiles:
            self.grid.grid[position.row][position.column] = self.current_block.id
        self.current_block = self.next_block
        self.next_block = self.get_random_block()
        rows_cleared = self.grid.clear_full_rows()
        if rows_cleared > 0:
            self.clear_sound.play()
            self.update_score(rows_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True
            return True  # Возвращаем True если игра закончена
        return False

    def reset(self):
        self.grid.reset()
        self.blocks = self.block_factory.get_all_blocks()
        self.current_block = self.get_random_block()
        self.next_block = self.get_random_block()
        self.score = 0

    def block_fits(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_empty(tile.row, tile.column) == False:
                return False
        return True

    def rotate(self):
        self.current_block.rotate()
        if self.block_inside() == False or self.block_fits() == False:
            self.current_block.undo_rotation()
        else:
            self.rotate_sound.play()

    def block_inside(self):
        tiles = self.current_block.get_cell_positions()
        for tile in tiles:
            if self.grid.is_inside(tile.row, tile.column) == False:
                return False
        return True

    def draw(self, screen):
        self.grid.draw(screen)
        self.current_block.draw(screen, 11, 11)

        if self.next_block.id == 3:
            self.next_block.draw(screen, 255, 290)
        elif self.next_block.id == 4:
            self.next_block.draw(screen, 255, 280)
        else:
            self.next_block.draw(screen, 270, 270)
