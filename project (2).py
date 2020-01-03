import pygame
import copy
import random
import os

from lvl_constructor import Load_lvl

global active_file, running, files, count, all_sprites, dice, cursor_bool, lvl_number

lvl_number = 1


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Menu:
    def __init__(self):
        self.menu_im = pygame.image.load('Главный экран.jpg')
        self.width, self.height = 1200, 675

    def render(self):
        screen.blit(self.menu_im, (0, 0))

    def on_click(self, cell_coords):
        global active_file, running, files
        if 890 <= cell_coords[0] <= 1074 and 455 <= cell_coords[1] <= 495:
            active_file = files[0]
        elif 890 <= cell_coords[0] <= 1074 and 520 <= cell_coords[1] <= 560:
            # Авторы
            print('Avtorov poka net')
        elif 890 <= cell_coords[0] <= 1074 and 580 <= cell_coords[1] <= 620:
            global running
            running = False

    def get_click(self, mouse_pos):
        self.on_click(mouse_pos)


class MapPeredvizenie:
    def __init__(self, width, height, char, map=0):
        self.width, self.height = 1200, 675
        self.char = char
        for i in range(len(map)):
            if '@' in map[i]:
                self.char.map_coords = (map[i].index('@'), i)
        self.board = map
        self.back = pygame.image.load('ECc2dTJXoAIjo7K.jpg')
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
        self.hardbass1 = pygame.image.load('hardbass1.png')  # эти два изображения не используются,
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
        screen.blit(self.back, (0, 0))
        for x in range(self.width):
            for y in range(self.height):
                if not type(self.board[y][x]) == int:
                    if self.board[y][x][:1] == '#E':
                        screen.blit(self.enermy_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == '-' or self.board[y][x] == '@':
                        screen.blit(self.r_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 'exit':
                        screen.blit(self.exit_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x][:2] == '#T':
                        screen.blit(self.treasures_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                elif self.board[y][x] == 3:
                    screen.blit(self.apple_image,
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
                elif self.board[y][x] == 2:
                    screen.blit(self.quit_game,
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

    def proverka(self, cell_coords):
        global lvl_number, active_file, files, all_sprites, map_sprites, enemy_dices, \
            character_sprite, animations, player_animation, end_hod
        y, x = cell_coords
        ex, ey = self.char.map_coords
        well_coords = [(ey + 1, ex),
                       (ey - 1, ex),
                       (ey, ex + 1),
                       (ey, ex - 1)]
        if (cell_coords not in well_coords) or (self.board[y][x] == 0):
            return False
        if self.board[y][x] == 3:
            self.char.map_coords = (x, y)
            if self.char.hp != self.char.hp_max:
                if self.char.hp + 10 > self.char.hp_max:
                    self.char.hp = self.char.hp_max
                else:
                    self.char.change_something(hp=10)
                self.board[y][x] = '-'
        elif self.board[y][x] == 4:
            self.char.map_coords = (x, y)
        elif self.board[y][x] == 5:
            self.char.map_coords = (x, y)
        elif self.board[y][x] == '-':
            self.char.map_coords = (x, y)
        elif self.board[y][x][:2] == '#T':
            self.char.map_coords = (x, y)
            treasure = self.board[y][x][2:-1].split(', ')
            self.board[y][x] = '-'
            Treasure_Chest(Weapons(*treasure))
        elif self.board[y][x][:2] == '#E':
            self.char.map_coords = (x, y)
            enemy = self.board[y][x][2:]
            self.board[y][x] = '-'
            print(f'fight! {enemy}')
            Fight(self.char, enemy, self)
        elif self.board[y][x] == 'exit':
            lvl_number += 1
            new_map = Load_lvl(f'lvl{lvl_number}.txt').load_level()
            files[0] = MapPeredvizenie(9, 5, character, new_map)
            for i in animations:
                i.kill()
            player_animation.kill()
            all_sprites = pygame.sprite.Group()
            pygame.mouse.set_visible(True)
            map_sprites = pygame.sprite.Group()
            character_sprite = pygame.sprite.Group()
            enemy_dices = pygame.sprite.Group()
            do_sprites()
            end_hod = True
            active_file = files[0]

        return True

    def on_click(self, cell_coords):
        if not cell_coords:
            return False
        global active_file
        y, x = cell_coords
        if self.board[y][x] == 9:
            active_file = files[1]
        elif self.board[y][x] == 2:
            active_file = Menu()

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
        self.exp = 0
        self.lvl_up_xp = 4
        self.rage = 0
        self.inventory = Inventory(self)
        self.fight = None

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

    def lvl_up(self, exp, money):
        self.exp += exp
        self.money += money
        if self.lvl_up_xp < self.exp:
            return False
        if self.exp > self.lvl_up_xp:
            self.exp = self.exp - self.lvl_up_xp
        elif self.exp == self.lvl_up_xp:
            self.exp = 0
        self.lvl_up_xp += 4
        self.hp_max += 4
        print(f'exp = {self.exp}, hp_max = {self.hp_max}')
        return True

    def next1(self):
        self.dices = self.dice_max


class Inventory(MapPeredvizenie):
    def __init__(self, char):
        global active_file
        self.width, self.height = 9, 5
        self.inventar = [[Weapons(lambda x: x, 'bump.png', lambda x: x + 1),
                          Weapons(lambda x: x, 'hammer.png', lambda x: x)],
                         [Weapons(lambda x: x % 2 != 0, 'snowflake.png', lambda x: x),
                          Weapons(lambda x: x <= 4, 'battle_axe.png', lambda x: x * 2)],
                         [Weapons(lambda x: x <= 5, 'cr_sword.png', lambda x: x * 3),
                          Weapons(lambda x: x <= 3, 'dagger.png', lambda x: x)]]
        # ,
        #                       [Weapons(lambda x: x, 'bump.png', lambda x: x + 1),
        #                       Weapons(lambda x: x, 'hammer.png', lambda x: x)],
        #                     [Weapons(lambda x: x <= 3 , 'dopp.png', lambda x: x * 2),
        #                      Weapons(lambda x: x, 'sword.png', lambda x: x)],
        #                      [Weapons(lambda x: x <= 5, 'cr_sword.png', lambda x: x * 3),
        #                     Weapons(lambda x: x <= 3, 'dagger.png', lambda x: x)]]
        self.backpack = [[0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0],
                         [0, 0, 0, 0]]
        self.char = char
        self.cell_size = 120
        self.left = 40
        self.top = 70
        self.waiting = False
        self.zamena_coords1 = 0
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
        if self.waiting:
            pygame.draw.circle(screen, (255, 0, 0), (600, 50), 45, 5)
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
                elif self.board[y][x] == 1:
                    screen.blit(self.inventorycell,
                                (x * self.cell_size + self.left,
                                 y * self.cell_size + self.top))
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
                pygame.draw.rect(screen, (0, 0, 0),
                                 (self.left + x * self.cell_size,
                                  self.top + y * self.cell_size,
                                  self.cell_size, self.cell_size), 1)
        for x in range(2):
            for y in range(3):
                if self.inventar[y][x] != 0:
                    screen.blit(self.inventar[y][x].image,
                                ((y + 6) * self.cell_size + self.left,
                                 (x + 2) * self.cell_size + self.top))
                elif self.board[y][x] == 1:
                    screen.blit(self.inventorycell,
                                ((y + 5) * self.cell_size + self.left,
                                 (x + 2) * self.cell_size + self.top))
        for x in range(4):
            for y in range(4):
                if self.backpack[y][x] != 0:
                    screen.blit(self.backpack[y][x].image,
                                (y * self.cell_size + self.left,
                                 x * self.cell_size + self.top))

    def on_click(self, cell_coords):
        if not cell_coords:
            self.waiting = False
            return False
        global active_file
        y, x = cell_coords
        if self.waiting:
            if (y, x) in [(3, 6), (3, 7), (3, 8), (4, 6), (3, 7), (3, 8)] \
                    and self.zamena_coords1 in [(3, 6), (3, 7), (3, 8),
                                                (4, 6), (3, 7), (3, 8)]:
                pass
            elif (y, x) in [(0, 0), (0, 1), (0, 2), (0, 3),
                            (1, 0), (1, 1), (1, 2), (1, 3),
                            (2, 0), (2, 1), (2, 2), (2, 3),
                            (3, 0), (3, 1), (3, 2), (3, 3)] \
                    and self.zamena_coords1 in [(0, 0), (0, 1), (0, 2), (0, 3),
                                                (1, 0), (1, 1), (1, 2), (1, 3),
                                                (2, 0), (2, 1), (2, 2), (2, 3),
                                                (3, 0), (3, 1), (3, 2), (3, 3)]:
                pass
            elif (y, x) in [(3, 6), (3, 7), (3, 8),
                            (4, 6), (3, 7), (3, 8)]:
                i2 = self.inventar[x - 6].pop(y - 2)
                i1 = self.backpack[self.zamena_coords1[1]].pop(self.zamena_coords1[0])
                self.inventar[x - 6].append(i1)
                self.backpack[self.zamena_coords1[1]].append(i2)
            elif (y, x) in [(0, 0), (0, 1), (0, 2), (0, 3),
                            (1, 0), (1, 1), (1, 2), (1, 3),
                            (2, 0), (2, 1), (2, 2), (2, 3),
                            (3, 0), (3, 1), (3, 2), (3, 3)]:
                i1 = self.inventar[self.zamena_coords1[1] - 6].pop(self.zamena_coords1[0] - 2)
                i2 = self.backpack[x].pop(y)
                self.inventar[self.zamena_coords1[1] - 6].append(i2)
                self.backpack[x].append(i1)
            self.waiting = False
        elif self.board[y][x] == 9:
            active_file = files[0]
        elif self.board[y][x] == 10:
            active_file = Menu()
        elif (y, x) in [(2, 6), (2, 7), (2, 8),
                        (3, 6), (3, 7), (3, 8),
                        (0, 0), (0, 1), (0, 2), (0, 3),
                        (1, 0), (1, 1), (1, 2), (1, 3),
                        (2, 0), (2, 1), (2, 2), (2, 3),
                        (3, 0), (3, 1), (3, 2), (3, 3)]:
            self.waiting = True
            self.zamena_coords1 = (y, x)

    def hranenie(self, something):
        for i in self.inventar:
            if i[0] == 0:
                i[0] = something
                break
            elif i[1] == 0:
                i[1] = something
                break
        for i in self.backpack:
            if i[0] == 0:
                i[0] = something
                break
            elif i[1] == 0:
                i[1] = something
                break


class Torgovec(MapPeredvizenie):
    def __init__(self, assortiment, cena):
        global active_file
        active_file = self
        self.assortiment = assortiment
        self.cena = cena

    def on_click(self, cell_coords):
        pass  # Я УСТАЛ


class Weapons:
    def __init__(self, attack_question, image, damage=0, size=1, dmg_type=0):
        self.attack_question, self.damage, \
        self.size, self.dmg_type = attack_question, \
                                   damage, size, dmg_type
        self.image = load_image(image)

    def attack(self, dice):
        dmg_q = list(map(self.attack_question, [dice]))
        if bool(dmg_q[0]):
            if self.damage != 0:
                return list(map(self.damage, [dice]))[0]
            return dice
        return False


class Fight(MapPeredvizenie):
    def __init__(self, character, enermy, board):
        global active_file, cursor_bool, all_sprites
        cursor_bool = True
        self.lvl_map = board
        self.lvl_map.board[character.map_coords[1]][character.map_coords[0]] = '-'
        self.first = False
        self.second = False
        self.width, self.height = 9, 5
        self.character = character
        self.bars = pygame.image.load('bars.png')
        self.perebros_counter = 3
        self.cell_size = 120
        self.left = 40
        self.top = 70
        self.win_image = pygame.image.load('win_fight.png')
        self.fight_back = pygame.image.load('fight1.jpg')
        self.hero_in_fight = pygame.image.load('hero_in_fight.png')
        self.quit_game = pygame.image.load('quitgame.png')
        self.bars = pygame.image.load('bars.png')
        self.char = pygame.image.load('char.png')
        self.perebros = pygame.image.load('perebros.png')
        self.enermy = Enemy_editor(*[int(i) for i in enermy.split(', ')[2:]])
        self.enermy_image = load_image(enermy.split(', ')[1])
        self.board = [[0, 0, 0, 0, 0, 13, 2, 0, 0],
                      [0, 0, 0, 0, 0, 3, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 7, 6, 0, 0, 0, 0, 0]]
        active_file = self
        self.enermy_hod = False
        all_sprites = pygame.sprite.Group()
        all_sprites.add(Cursor(all_sprites))

    def render(self):
        if self.enermy.hp <= 0:
            self.character.next1()
            screen.blit(self.win_image, (0, 0))
        if self.character.hp <= 0:
            screen.blit(self.win_image, (10, 0))
        else:
            screen.blit(self.fight_back, (0, 0))
            for x in range(9):
                for y in range(5):
                    if self.board[y][x] == 2:
                        screen.blit(self.enermy_image,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 13:
                        screen.blit(self.bars,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                        font = pygame.font.Font(None, 25)
                        text = font.render(f"{self.enermy.hp}/{self.enermy.hp_max}", 1, (255, 255, 255))
                        screen.blit(text, (x * self.cell_size + self.left + self.cell_size // 2,
                                           y * self.cell_size + self.top + self.cell_size // 2))
                    elif self.board[y][x] == 3:
                        screen.blit(self.perebros,
                                    (x * self.cell_size + self.left,
                                     y * self.cell_size + self.top))
                    elif self.board[y][x] == 1:
                        screen.blit(self.hero_in_fight,
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
            if not self.enermy_hod:
                for x in range(2):
                    for y in range(3):
                        if self.character.inventory.inventar[y][x] != 0:
                            screen.blit(self.character.inventory.inventar[y][x].image,
                                        ((y + 1) * self.cell_size + self.left,
                                         (x + 1) * self.cell_size + self.top))
            elif self.enermy_hod:
                for i in range(len(self.enermy.abilities)):
                    screen.blit(self.enermy.abilities[i].image,
                                ((i + 1) * self.cell_size + self.left,
                                 1 * self.cell_size + self.top))

    def on_click(self, cell_coords):
        global active_file, files, count, all_sprites, dice, cursor_bool
        if not cell_coords:
            return None
        if self.enermy.hp <= 0 and not self.first:
            self.first = True
            cursor_bool = False
            pygame.mouse.set_visible(True)
        elif self.first and not self.second:
            all_sprites = pygame.sprite.Group()
            pygame.mouse.set_visible(True)
            if self.character.lvl_up(self.enermy.exp, self.enermy.money):
                self.win_image = pygame.image.load('new_dice.png')
                self.character.dices += 1
                self.second = True
                all_sprites = pygame.sprite.Group()
            else:
                active_file = files[0]
        elif self.second:
            all_sprites = pygame.sprite.Group()
            pygame.mouse.set_visible(True)
            active_file = files[0]
        y, x = cell_coords
        if self.enermy_hod:
            if (x, y) == (8, 4):
                pass
            else:
                return None
        if (x, y) in [(1, 1), (1, 2),
                      (2, 1), (2, 2),
                      (3, 1), (3, 2)]:
            if self.character.dices > 0:
                if self.character.inventory.inventar[x - 1][y - 1] != 0:
                    if self.character.inventory.inventar[x - 1][y - 1].attack(dice):
                        self.enermy.hp -= self.character.inventory.inventar[x - 1][y - 1].attack(dice)
                        self.character.dices -= 1
                        all_sprites = pygame.sprite.Group()
                        all_sprites.add(Cursor(all_sprites))
                    print(self.enermy.hp)
            if self.character.dices <= 0:
                all_sprites = pygame.sprite.Group()
                pygame.mouse.set_visible(True)
        if (x, y) in [(5, 2), (5, 1)]:
            if self.perebros_counter > 0:
                all_sprites = pygame.sprite.Group()
                all_sprites.add(Cursor(all_sprites))
            self.perebros_counter -= 1
        if (x, y) == (8, 4):
            self.next()

    def next(self):
        self.enermy_hod = not self.enermy_hod
        self.character.next1()
        if self.enermy_hod:
            self.enermy.attack(self.character)


class Enemy_editor(Fight):
    def __init__(self, hp, hp_max, exp, money, dices, abilities=0, vibor=0):
        self.abilities = [Weapons(lambda x: x, 'bump.png', lambda x: x + 1),
                          Weapons(lambda x: x, 'hammer.png', lambda x: x),
                          Weapons(lambda x: x % 2 != 0, 'snowflake.png', lambda x: x)]
        self.vibor = '>= 3;< 2;== 6'.split(';')
        self.hp = hp
        self.hp_max = hp_max
        self.exp = exp
        self.money = money
        self.dices = dices
        self.dices_max = dices
        self.attacked = False
        self.dices_a = pygame.sprite.Group()

    def attack(self, character):
        for i in range(len(self.abilities)):
            if bool(eval(f'{i} ' + self.vibor[i])):
                a = Enemy_dices((i + 1, 1), self.dices_a)
                character.hp -= self.abilities[i].attack(a.chislo)
            else:
                Enemy_dices((6, 1), self.dices_a)


class Treasure_Chest:
    def __init__(self, treasure):
        global active_file
        active_file = self
        self.treasure = treasure  # объект Weapon
        self.base = pygame.image.load('treasure_open.jpg')

    def render(self):
        screen.blit(self.base, (0, 0))
        screen.blit(self.treasure.image, (550, 250))

    def get_click(self, coords):
        global active_file
        if 745 >= coords[0] >= 545 and coords[1] >= 500:
            files[1].hranenie(self.treasure)
            active_file = files[0]


pygame.init()
map_1 = [[0, 0, 2, '-', 4, 0, 0, 0, 0],
         [0, '@', '-', 0, 0, 0, 5, 0, 0],
         [0, 0, '-', 3, '-', 2, 4, 0, 0],
         [0, 0, 0, 3, 0, 0, 0, 0, 0],
         [0, 8, 7, 6, 0, 0, 9, 10, 0]]
size = width, height = 1200, 675
screen = pygame.display.set_mode(size)
character = MainCharacter()
a = 'lvl1.txt'
a = Load_lvl(a).load_level()
map_1lvl = MapPeredvizenie(9, 5, character, a)
inventory = Inventory(character)
files = [map_1lvl, inventory]
active_file = Menu()
dice = 6
# 10 - инвентарь
# '@' - гг
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
all_sprites = pygame.sprite.Group()
pygame.mouse.set_visible(True)
map_sprites = pygame.sprite.Group()
character_sprite = pygame.sprite.Group()
enemy_dices = pygame.sprite.Group()


class Cursor(pygame.sprite.Sprite):
    def __init__(self, group):
        global dice
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite. Это очень важно !!!
        super().__init__(group)
        dice = self.chislo = random.randint(1, 6)
        image = load_image(f"{self.chislo}.png", -1)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = -100, -100

    def get_event(self, pos):
        self.rect = self.image.get_rect()
        self.update(pos)

    def update(self, coords):
        self.rect.x, self.rect.y = coords

    def change(self):
        global dice
        dice = self.chislo = random.randint(1, 6)
        image = load_image(f"{self.chislo}.png", -1)
        self.image = image


class AnimatedMap(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(map_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def stop(self):
        self.kill()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class AnimatedCharacter(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(character_sprite)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect.x = y
        self.rect.y = x
        self.vx = 0
        self.vy = 0
        self.purpose = (0, 0)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        global end_hod
        self.rect = self.rect.move(self.vx, self.vy)
        if self.purpose == (self.rect.x, self.rect.y):
            end_hod = True
            self.vx = 0
            self.vy = 0
        if pygame.sprite.spritecollideany(self, map_sprites):
            pygame.sprite.spritecollideany(self, map_sprites).stop()
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]

    def go(self, coords):
        print(1)
        self.purpose = self.rect.x + coords[0] * 120, self.rect.y + coords[1] * 120
        if active_file.proverka((int((self.purpose[1] - 70) / 120), int((self.purpose[0] - 40) / 120))):
            print('go!')
            self.vx = 5 * coords[0]
            self.vy = 5 * coords[1]
        else:
            self.purpose = self.purpose = self.rect.x, self.rect.y


def do_sprites():
    global player_animation, animations
    for y in range(len(files[0].board)):
        for x in range(len(files[0].board[0])):
            if type(files[0].board[y][x]) == int:
                pass
            elif files[0].board[y][x][:2] == '#E':
                animations.append(
                    AnimatedMap(load_image(files[0].board[y][x][2:].split(',')[0][1:-1]), 2, 1, 40 + 120 * x,
                                70 + 120 * y))
            elif files[0].board[y][x] == 'exit':
                animations.append(AnimatedMap(load_image("exit_gif.png"), 2, 1, 40 + 120 * x, 70 + 120 * y))
            elif files[0].board[y][x] == '@':
                player_animation = AnimatedCharacter(load_image("dance_gif.png"), 2, 1, 70 + 120 * y, 40 + 120 * x)


animations = []
do_sprites()


class Enemy_dices(pygame.sprite.Sprite):
    def __init__(self, purpose, group):
        super().__init__(group)
        self.chislo = random.randint(1, 6)
        image = load_image(f"{self.chislo}.png", -1)
        self.purpose = purpose[0] * 120 + 40, purpose[1] * 120 + 70
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = 120 * 7 + 40
        self.rect.y = 120 * 1 + 70
        self.vx = -15

    def update(self):
        self.rect = self.rect.move(self.vx, 0)
        if self.purpose == (self.rect.x, self.rect.y):
            self.vx = 0

    def go(self, coords):
        self.purpose = self.rect.x + coords[0] * 120, self.rect.y + coords[1] * 120
        if active_file.proverka((int((self.purpose[1] - 70) / 120), int((self.purpose[0] - 40) / 120))):
            print('go!')
            self.vx = 5 * coords[0]
            self.vy = 5 * coords[1]
        else:
            self.purpose = self.rect.x, self.rect.y


# player_animation = AnimatedCharacter(load_image("dance_gif.png"), 2, 1, 40 + 120, 70 + 120)
# exit_animation = AnimatedMap(load_image("exit_gif.png"), 2, 1, 40 + 120 * 6, 70 + 120)
# demon_dance = AnimatedMap(load_image("demon_dance.png"), 2, 1, 40 + 120 * 2, 70)
cursor = Cursor(all_sprites)

running = True
cursor_bool = True
MYEVENTTYPE = 1
pygame.time.set_timer(MYEVENTTYPE, 10000)
clock = pygame.time.Clock()
coord = 0
peremeshenie = False
end_hod = True
while running:
    active_file.render()
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            active_file.get_click(event.pos)
            radius = 0
            drew = True
        if event.type == pygame.MOUSEMOTION and type(active_file) == Fight and cursor_bool:
            pygame.mouse.set_visible(False)
            for i in all_sprites:
                if pygame.mouse.get_focused():
                    i.get_event(event.pos)
        if type(active_file) == MapPeredvizenie and keys[pygame.K_LEFT] and end_hod:
            print(2)
            player_animation.go((-1, 0))
            end_hod = False
        elif type(active_file) == MapPeredvizenie and keys[pygame.K_RIGHT] and end_hod:
            player_animation.go((1, 0))
            end_hod = False
        elif type(active_file) == MapPeredvizenie and keys[pygame.K_UP] and end_hod:
            player_animation.go((0, -1))
            end_hod = False
        elif type(active_file) == MapPeredvizenie and keys[pygame.K_DOWN] and end_hod:
            player_animation.go((0, 1))
            end_hod = False
    if type(active_file) == MapPeredvizenie:
        map_sprites.update()
        map_sprites.draw(screen)
        character_sprite.update()
        character_sprite.draw(screen)
    if pygame.mouse.get_focused():
        all_sprites.draw(screen)
    if type(active_file) == Fight and active_file.enermy_hod:
        active_file.enermy.dices_a.draw(screen)
        active_file.enermy.dices_a.update()
    pygame.display.flip()
    clock.tick(10)
pygame.quit()
