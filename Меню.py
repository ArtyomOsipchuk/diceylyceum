import pygame


class Menu:
    def __init__(self):
        self.menu_im = pygame.image.load('Главный экран.jpg')
        self.width = width
        self.height = height

    def render(self):
        screen.blit(self.menu_im, (0, 0))

    def on_click(self, cell_coords):
        if 890 <= cell_coords[0] <= 1074 and 455 <= cell_coords[1] <= 495:
            # MapPeredvizenie()
            #Запуск игры
            print(1)
        elif 890 <= cell_coords[0] <= 1074 and 520 <= cell_coords[1] <= 560:
            #Авторы
            print(2)
        elif 890 <= cell_coords[0] <= 1074 and 580 <= cell_coords[1] <= 620:
            #Выход из игры
            print(3)

    def get_click(self, mouse_pos):
        self.on_click(mouse_pos)


size = width, height = 1200, 675
screen = pygame.display.set_mode(size)
menu = Menu()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            menu.get_click(event.pos)
    menu.render()
    pygame.display.flip()
pygame.quit()
