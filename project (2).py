import pygame
import copy
import random


class MapPeredvizenie:
    def __init__(self, width, height, char, map=[[0] * 9 for _ in range(5)]):
        self.char = char
        self.board = map
        self.risotto_coords = (1, 1)
        self.back = pygame.image.load('ECc2dTJXoAIjo7K.jpg') # как подрубать изображения:
        # self.название = pygame.image.load('название изображения')
        # чтобы использовать(использую в render()): screen.blit(self.название,
        #                                                      (координата середины фото по х,
        #                                                      координата середины фото по у))
        self.hero_image = pygame.image.load('hero.png')
        self.enermy_image = pygame.image.load('enermy.png')
        self.apple_image = pygame.image.load('apple2.png')
        self.treasures_image = pygame.image.load('treasures2.png')
        self.exit_image = pygame.image.load('exit.png')
        self.r_image = pygame.image.load('r.png')
        self.quit_game = pygame.image.load('quitgame.png')
        self.bars = pygame.image.load('bars.png')
        self.character = pygame.image.load('char.png')
        self.inventorybtn = pygame.image.load('inventorybtn.png')
        self.treasure_open = pygame.image.load('treasure_open.jpg')
        self.hardbass1 = pygame.image.load('hardbass1.png') # эти два изображения не используются,
        # т.к. я плохо шарю во времени в питон. Но когда разберусь, сделаю героя танцующего хардбасс
        self.hardbass2 = pygame.image.load('hardbass2.png')
        self.width = width
        self.height = height
        self.left = 40
        self.top = 70
        self.cell_size = 120
        self.inventory_true = False
        self.fight = False

    def render(self):
        if self.inventory_true:
            self.char.inventory.render()
        elif self.fight:
            self.char.fight.render()
        else:
            screen.blit(self.back, (0, 0))
            for x in range(self.width):
                for y in range(self.height):
                    if self.board[y][x] == 2:
                        screen.blit(self.enermy_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 3:
                        screen.blit(self.apple_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 4:
                        screen.blit(self.treasures_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 5:
                        screen.blit(self.exit_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 6:
                        screen.blit(self.bars,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                        font = pygame.font.Font(None, 25)
                        text = font.render(f"{self.char.hp}/{self.char.hp_max}", 1, (255, 255, 255))
                        screen.blit(text, (x * self.cell_size + self.left + self.cell_size // 2,
                                           y * self.cell_size + self.top + self.cell_size // 2))
                        font = pygame.font.Font(None, 25)
                        text = font.render(f"{self.char.money}", 1, (255, 255, 0))
                        screen.blit(text, (x * self.cell_size + self.left + 40,
                                           y * self.cell_size + self.top + 90))
                        font = pygame.font.Font(None, 25)
                        text = font.render(f"{self.char.dices}", 1, (255, 255, 255))
                        screen.blit(text, (x * self.cell_size + self.left + 97,
                                           y * self.cell_size + self.top + 89))
                    elif self.board[y][x] == 7:
                        screen.blit(self.character,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 9:
                        screen.blit(self.inventorybtn,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 10:
                        screen.blit(self.quit_game,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == '-':
                        screen.blit(self.r_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    if (x, y) == self.risotto_coords:
                        screen.blit(self.hero_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"Для ходьбы жмите на клетку около героя", 1, (0, 0, 0))
                    screen.blit(text, (1, 10))
                    pygame.draw.rect(screen, (0, 0, 0),
                                     (self.left + x * self.cell_size,
                                      self.top + y * self.cell_size,
                                      self.cell_size, self.cell_size), 1)

    def get_cell(self, mouse_pos):
        if (self.left <= mouse_pos[0] <= self.left + self.cell_size * self.width and
                self.top <= mouse_pos[1] <= self.top + self.cell_size * self.height):
            y = (mouse_pos[0] - self.left) // self.cell_size
            x = (mouse_pos[1] - self.top) // self.cell_size
            return x, y
        else:
            return None

    def on_click(self, cell_coords):
        y, x = cell_coords
        if self.board[y][x] == 9:
            print(self.inventory_true)
            self.inventory_true = not self.inventory_true
        elif self.board[y][x] == 10:
            pass
        ex, ey = self.risotto_coords
        well_coords = [(ey + 1, ex),
                       (ey - 1, ex),
                       (ey, ex + 1),
                       (ey, ex - 1)]
        if not cell_coords or cell_coords not in well_coords:
            return None
        if self.board[y][x] == '-':
            self.risotto_coords = (x, y)
        elif self.board[y][x] == 2:
            self.risotto_coords = (x, y)
            enemy = self.board[y][x]
            self.board[y][x] = '-'
            self.char.fight = Fight(self.char, enemy)
            self.fight = True
        elif self.board[y][x] == 3:
            self.risotto_coords = (x, y)
            if self.char.hp != self.char.hp_max:
                if self.char.hp + 10 > self.char.hp_max:
                    self.char.hp = self.char.hp_max
                else:
                    self.char.change_something(hp=10)
                self.board[y][x] = '-'
        elif self.board[y][x] == 4:
            self.risotto_coords = (x, y)
        elif self.board[y][x] == 5:
            self.risotto_coords = (x, y)
        elif self.board[y][x] == 6:
            pass  # бары хп и прочего
        elif self.board[y][x] == 7:
            pass
            # ?
        elif self.board[y][x] == 8:
            pass
            # ?

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)


class MainCharacter(MapPeredvizenie):
    def __init__(self):
        self.map_coords = (1, 1)
        self.hp_max = 24
        self.hp = 12
        self.exp = 0
        self.money = 0
        self.dices = 2
        self.dice_max = 2
        self.rage = 0
        self.inventory = Inventory(self)
        self.fight = None

    def attack(self, x):
        pass # насчёт боя я вообще без понятия шо делать... Думаю подрубить время и делать долгие анимации
        # плюс к этому сделать все заготовки атаковалок(наскриншотить, поиграв в игру :D) и атаковалок врагов
        # ну и враг представленный здесь - "Демон лицея" должен будет иметь 1 способность "Цикл while":
        # "нужно не больше 3, наносит 1 урон и возвращает кубик" что сделает его сильным противником
        # Да, как ты понял будем клепать отсылки на лицей, "Доработать!" и прочее)))

    def change_something(self, hp=0, exp=0, money=0, dices=0, rage=0, hp_max=0, dice_max=0):
        self.hp += hp
        self.exp += exp
        self.money += money
        self.dices += dices
        self.rage += rage
        self.hp_max += hp_max
        self.dice_max += dice_max

    def get_or_change_char_coords(self, x=-1, y=-1):
        if x < 0 or y < 0:
            return self.map_coords
        else:
            self.map_coords = x, y

    def inventory(self):
        pass

    def on_click(self, cell_coords):
        pass


class Inventory:
    def __init__(self, char):
        self.char = char
        self.cell_size = 120
        self.left = 40
        self.top = 70
        self.board = [[1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 0, 0, 0, 0, 0],
                      [1, 1, 1, 1, 0, 0, 1, 1, 1],
                      [1, 1, 1, 1, 0, 0, 1, 1, 1],
                      [0, 0, 7, 6, 0, 0, 9, 10, 0]]
        self.quit_game = pygame.image.load('quitgame.png')
        self.bars = pygame.image.load('bars.png')
        self.character = pygame.image.load('char.png')
        self.inventorybtn = pygame.image.load('inventorybtn.png')
        self.inventory = pygame.image.load('inventory.png')
        self.inventorycell = pygame.image.load('inventory_cell.png')

    def render(self):
        screen.blit(self.inventory, (0, 0))
        for x in range(9):
            for y in range(5):
                if self.board[y][x] == 6:
                    screen.blit(self.bars,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.char.hp}/{self.char.hp_max}", 1, (255, 255, 255))
                    screen.blit(text, (x * self.cell_size + self.left + self.cell_size // 2,
                                       y * self.cell_size + self.top + self.cell_size // 2))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.char.money}", 1, (255, 255, 0))
                    screen.blit(text, (x * self.cell_size + self.left + 40,
                                       y * self.cell_size + self.top + 90))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.char.dices}", 1, (255, 255, 255))
                    screen.blit(text, (x * self.cell_size + self.left + 97,
                                       y * self.cell_size + self.top + 89))
                elif self.board[y][x] == 7:
                    screen.blit(self.character,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                elif self.board[y][x] == 9:
                    screen.blit(self.inventorybtn,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                elif self.board[y][x] == 10:
                    screen.blit(self.quit_game,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                elif self.board[y][x] == 1:
                    screen.blit(self.inventorycell,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)


class Fight(MainCharacter):
    def __init__(self, character, enermy):
        self.character = character
        self.cell_size = 120
        self.left = 40
        self.top = 70
        self.fight_back = pygame.image.load('fight1.jpg')
        self.quit_game = pygame.image.load('quitgame.png')
        self.bars = pygame.image.load('bars.png')
        self.char = pygame.image.load('char.png')
        if enermy == 2:
            self.enermy = Luceum_demon()
            self.enermy_image = pygame.image.load('battle_enemy.png')
        self.board = [[0, 0, 0, 0, 0, 0, 2, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 7, 6, 10, 0, 0, 0, 0, 0]]

    def render(self):
        screen.blit(self.fight_back, (0, 0))
        for x in range(9):
            for y in range(5):
                if self.board[y][x] == 2:
                    screen.blit(self.enermy_image,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                elif self.board[y][x] == 6:
                    screen.blit(self.bars,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.character.hp}/{self.character.hp_max}", 1, (255, 255, 255))
                    screen.blit(text, (x * self.cell_size + self.left + self.cell_size // 2,
                                       y * self.cell_size + self.top + self.cell_size // 2))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.character.money}", 1, (255, 255, 0))
                    screen.blit(text, (x * self.cell_size + self.left + 40,
                                       y * self.cell_size + self.top + 90))
                    font = pygame.font.Font(None, 25)
                    text = font.render(f"{self.character.dices}", 1, (255, 255, 255))
                    screen.blit(text, (x * self.cell_size + self.left + 97,
                                       y * self.cell_size + self.top + 89))
                elif self.board[y][x] == 7:
                    screen.blit(self.char,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                elif self.board[y][x] == 10:
                    screen.blit(self.quit_game,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)

    def get_click(self):
        pass

    def __next__(self):
        self.character.dices = self.character.dice_max
        self.enermy


class Luceum_demon(Fight):
    def __init__(self):
        self.map_coords = (1, 1)
        self.hp = 8
        self.exp = 1
        self.money = 1
        self.dices = 1

    def change_something(self, hp=0, dices=0):
        self.hp += hp
        self.dices += dices

    def attack(self):
        pass

    def inventory(self):
        pass


pygame.init()
# 10 - инвентарь
# 1 - гг(нет, я это переработал)
# 2 - злодей
# 3 - яблоко
# 4 - сундук
# 5 - спуск
# 6 - сколько кубиков, сколько монеток, сколько жизней
# 7 - ?
# 8 - ?
# 9 - инвентарь
# 10 - выход
# "-" - дорожки
# 0 - пустота
map = [[0, 0, 2, '-', 4, 0, 0, 0, 0],
       [0, '-', '-', 0, 0, 0, 5, 0, 0],
       [0, 0, '-', 3, '-', 2, 4, 0, 0],
       [0, 0, 0, 3, 0, 0, 0, 0, 0],
       [0, 8, 7, 6, 0, 0, 9, 10, 0]]
size = width, height = 1200, 675
screen = pygame.display.set_mode(size)
character = MainCharacter()
board = MapPeredvizenie(9, 5, character, map)
running = True
MYEVENTTYPE = 10
pygame.time.set_timer(MYEVENTTYPE, 10)
clock = pygame.time.Clock()
coord = 0
peremeshenie = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            board.get_click(event.pos)
            radius = 0
            drew = True
        if event.type == MYEVENTTYPE and peremeshenie:
            coord += 1
    screen.fill((200, 0, 200))
    board.render()
    pygame.display.flip()
pygame.quit()
