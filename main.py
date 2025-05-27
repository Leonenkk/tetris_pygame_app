import pygame
import sys
import json
from game import Game
from colors import Colors
from menu import Menu
from highscores import Highscores
from dialog import NameDialog

pygame.init()

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Настройки экрана
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 620
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Python Tetris")


title_font = pygame.font.Font(None, 40)
help_font = pygame.font.Font(None, 30)

colors = Colors()
highscores = Highscores()


def draw_help_screen():
    screen.fill(colors.dark_blue)
    help_text = config["help_text"].split("\n")
    y_offset = 50
    for line in help_text:
        text_surface = help_font.render(line, True, colors.white)
        screen.blit(text_surface, (50, y_offset))
        y_offset += 40
    pygame.display.update()


def draw_highscores_screen():
    screen.fill(colors.dark_blue)
    scores = highscores.load()
    text_surface = title_font.render("Таблица рекордов", True, colors.white)
    screen.blit(text_surface, (150, 50))

    y_offset = 120
    for idx, score in enumerate(scores[:10]):
        entry = f"{idx + 1}. {score['name']}: {score['score']}"
        text_surface = help_font.render(entry, True, colors.white)
        screen.blit(text_surface, (150, y_offset))
        y_offset += 40

    back_text = help_font.render("Нажмите ESC для возврата", True, colors.white)
    screen.blit(back_text, (150, 500))
    pygame.display.update()


def main():
    clock = pygame.time.Clock()
    menu = Menu(screen)
    current_screen = "menu"
    game = None
    colors = Colors()

    GAME_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(GAME_UPDATE, config["game_settings"]["fall_speed"])

    while True:
        if current_screen == "menu":
            menu.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        menu.selected = (menu.selected + 1) % 4
                    elif event.key == pygame.K_UP:
                        menu.selected = (menu.selected - 1) % 4
                    elif event.key == pygame.K_RETURN:
                        if menu.selected == 0:
                            game = Game(config)
                            current_screen = "game"
                        elif menu.selected == 1:
                            current_screen = "highscores"
                        elif menu.selected == 2:
                            current_screen = "help"
                        elif menu.selected == 3:
                            pygame.quit()
                            sys.exit()

        elif current_screen == "game":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if game.game_over:
                        continue
                    if event.key == pygame.K_LEFT:
                        game.move_left()
                    elif event.key == pygame.K_RIGHT:
                        game.move_right()
                    elif event.key == pygame.K_DOWN:
                        game.move_down()
                        game.update_score(0, 1)
                    elif event.key == pygame.K_UP:
                        game.rotate()
                if event.type == GAME_UPDATE and not game.game_over:
                    game.move_down()

            screen.fill(colors.dark_blue)
            game.draw(screen)
            score_text = title_font.render(f"Счет: {game.score}", True, colors.white)
            screen.blit(score_text, (320, 20))
            if game.game_over:
                top_scores = highscores.load()
                if not top_scores or game.score > top_scores[0]["score"]:
                    dialog = NameDialog(screen)
                    while dialog.active:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            dialog.handle_input(event)
                        screen.fill(colors.dark_blue)
                        game.draw(screen)
                        score_text = title_font.render(
                            f"Счет: {game.score}", True, colors.white
                        )
                        screen.blit(score_text, (320, 20))
                        dialog.draw()
                        pygame.display.update()
                        clock.tick(60)
                    if dialog.input_text.strip():
                        highscores.add_score(dialog.input_text.strip(), game.score)
                    current_screen = "menu"
                    game.reset()
                else:
                    game.game_over_sound.play()
                    choice = game.handle_game_over(screen)
                    if choice == "menu":
                        current_screen = "menu"
                        game.reset()
                    elif choice == "restart":
                        game = Game(config)
                        current_screen = "game"
                        continue
            pygame.display.update()
            clock.tick(60)

        elif current_screen == "highscores":
            draw_highscores_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_screen = "menu"

        elif current_screen == "help":
            draw_help_screen()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_screen = "menu"


if __name__ == "__main__":
    main()
