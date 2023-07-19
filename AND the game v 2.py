import numpy as np
import pygame
import datetime

screen_width = 1920
screen_height = 1080
CELL_SIZE = 64
rows = screen_height // CELL_SIZE
cols = screen_width // CELL_SIZE

# Inicializace herní plochy
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("And the game")

# Vytvoření pole součástek
components = np.zeros((3, rows, cols), dtype=int)

button_on_image = pygame.image.load("tlacitko_on.png")
button_off_image = pygame.image.load("tlacitko_off.png")
and_gate_image = pygame.image.load("and_brana.png")
nand_gate_image = pygame.image.load("nand_brana.png")
or_gate_image = pygame.image.load("or_brana.png")
xor_gate_image = pygame.image.load("xor_brana.png")
nor_gate_image = pygame.image.load("nor_brana.png")
not_gate_image = pygame.image.load("not_brana.png")
screen_on_image = pygame.image.load("obrazovka_on.png")
screen_off_image = pygame.image.load("obrazovka_off.png")

# Barva kabelu
cable_color = (30, 90, 30)
kabel_velikost = 20
background_color = (25, 26, 25)

def obnova_power():
    global vypnuti
    for x in range(0,10):
        for row in range(0, rows):
            for col in range(0, cols):
                if components[0][row][col] == 3 or components[0][row][col] == 4:
                    if components[1][row][col +1] in [2,3] or components[1][row][col-1] in [2,3] or components[1][row+1][col] in [2,3] or components[1][row-1][col] in [2,3]:
                        components[1][row][col] = 2
                        vypnuti = True
                    elif components[2][row][col] == 1:
                        components[1][row][col] = 1
                    elif components[2][row][col] == 2:
                        components[1][row][col] = 2
                    elif components[1][row][col +1] == 1 or components[1][row][col-1] == 1 or components[1][row+1][col] == 1 or components[1][row-1][col] == 1:
                        components[1][row][col] = 1
                        vypnuti = True
                    else:
                        components[1][row][col] = 0

        for row in range(rows - 1, 0, -1):
            for col in range(cols - 1, 0, -1):
                if components[0][row][col] == 3 or components[0][row][col] == 4:
                    if components[1][row][col +1] in [2,3] or components[1][row][col-1] in [2,3] or components[1][row+1][col] in [2,3] or components[1][row-1][col] in [2,3]:
                        components[1][row][col] = 2
                    elif components[2][row][col] == 1:
                        components[1][row][col] = 1
                    elif components[2][row][col] == 2:
                        components[1][row][col] = 2
                    elif components[1][row][col +1] == 1 or components[1][row][col-1] == 1 or components[1][row+1][col] == 1 or components[1][row-1][col] == 1:
                        components[1][row][col] = 1
                    else:
                        components[1][row][col] = 0

def draw_grid():
    for x in range(0, screen_width, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (x, 0), (x, screen_height))
    for y in range(0, screen_height, CELL_SIZE):
        pygame.draw.line(screen, (30, 30, 30), (0, y), (screen_width, y))

def AND_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 2:
                if components[1][row + 1][col] == 1 and components[1][row - 1][col] == 1:
                    components[2][row][col + 1] = 1
                    obnova_power()
                else:
                    components[2][row][col + 1] = 2
                    obnova_power()

def NAND_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 7:
                if components[1][row + 1][col] == 1 and components[1][row - 1][col] == 1:
                    components[2][row][col + 1] = 2
                    obnova_power()
                else:
                    components[2][row][col + 1] = 1
                    obnova_power()

def OR_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 5:
                if components[1][row + 1][col] == 1 or components[1][row - 1][col] == 1:
                    components[2][row][col + 1] = 1
                    obnova_power()
                else:
                    components[2][row][col + 1] = 2
                    obnova_power()

def XOR_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 6:
                if components[1][row + 1][col] != components[1][row - 1][col]:
                    components[2][row][col + 1] = 1
                    obnova_power()
                else:
                    components[2][row][col + 1] = 2
                    obnova_power()

def NOR_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 8:
                if components[1][row + 1][col] == 0 and components[1][row - 1][col] == 0:
                    components[2][row][col + 1] = 1
                    obnova_power()
                else:
                    components[2][row][col + 1] = 2
                    obnova_power()

def NOT_brana():
    for row in range(1, rows):
        for col in range(1, cols):
            if components[0][row][col] == 9:
                if components[1][row][col - 1] == 1:
                    components[2][row][col + 1] = 2
                    obnova_power()
                else:
                    components[2][row][col + 1] = 1
                    obnova_power()

# Definice menu
menu_items = [
    {"label": "Reset", "value": 10},
    {"label": "Tlačítko", "value": 1},
    {"label": "Obrazovka", "value": 3},
    {"label": "Kabel", "value": 4},
    {"label": "AND brána", "value": 2},
    {"label": "NAND brána", "value": 7},
    {"label": "OR brána", "value": 5},
    {"label": "XOR brána", "value": 6},
    {"label": "NOR brána", "value": 8},
    {"label": "NOT brána", "value": 9},
    {"label": "Uložení", "value": 11},
    {"label": "Importování", "value": 12},
]
menu_width = 160
menu_padding = 5
menu_item_height = 40
menu_height = len(menu_items) * menu_item_height + menu_padding * 2
pygame.font.init()

font = pygame.font.SysFont("Monocraft", 18)

def ukladani():
    global components
    cas_ted = datetime.datetime.now()
    nazev = "save_{}.txt".format(cas_ted.strftime("%Y%m%d%H%M%S"))
    reshaped_components = np.reshape(components, (components.shape[0], -1))
    np.savetxt(nazev, reshaped_components, fmt='%d')

def ladovani():
    global components
    loaded_save = np.loadtxt('save_components.txt')
    components = np.reshape(loaded_save, (3, rows, cols))

def draw_menu():
    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, menu_width, menu_height))
    for index, item in enumerate(menu_items):
        pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(menu_padding, menu_padding + index * menu_item_height, menu_width - menu_padding * 2, menu_item_height - menu_padding))
        text = font.render(item["label"], True, (255, 255, 255))
        screen.blit(text, (menu_padding * 2, menu_padding * 2 + index * menu_item_height))

def reset():
    global components
    components = np.zeros((3, rows, cols), dtype=int)

running = True
pokladano = 0
vypnuti = False
menu_active = True
while running:
    screen.fill(background_color)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_o:
                pokladano = 3
            elif event.key == pygame.K_t:
                pokladano = 1
            elif event.key == pygame.K_a:
                pokladano = 2
            elif event.key == pygame.K_k:
                pokladano = 4
            elif event.key == pygame.K_r:
                pokladano = 5
            elif event.key == pygame.K_x:
                pokladano = 6
            elif event.key == pygame.K_n:
                pokladano = 7
            elif event.key == pygame.K_d:
                pokladano = 8
            elif event.key == pygame.K_e:
                pokladano = 9
            elif event.key == pygame.K_m:
                menu_active = not menu_active

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if menu_active and event.button == 1:
                mouse_x, mouse_y = event.pos
                if mouse_x < menu_width and mouse_y < menu_height:
                    clicked_item_index = (mouse_y - menu_padding) // menu_item_height
                    pokladano = menu_items[clicked_item_index]["value"]
                    if pokladano == 10:
                        reset()
                    elif pokladano == 11:
                        ukladani()
                    elif pokladano == 12:
                        ladovani()

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Získání pozice myši v herním okně
            x, y = pygame.mouse.get_pos()

            # Výpočet indexu buňky v poli součástek
            cell_col = x // CELL_SIZE
            cell_row = y // CELL_SIZE

            # Přidání nebo změna součástky na kliknutém místě
            if event.button == 1:  # Levé tlačítko myši
                if menu_active and x < menu_width and y < menu_height:
                    clicked_item_index = (y - menu_padding) // menu_item_height
                    pokladano = menu_items[clicked_item_index]["value"]
                elif components[0][cell_row][cell_col] == 0:
                    components[0][cell_row][cell_col] = pokladano
                elif components[0][cell_row][cell_col] == 1:
                    if components[1][cell_row][cell_col] in [0,3]:
                        components[1][cell_row][cell_col] = 1
                        obnova_power()
                    elif components[1][cell_row][cell_col] == 1:
                        components[1][cell_row][cell_col] = 3
                        obnova_power()
            if event.button == 3:  # Pravé tlačítko myši
                if components[0][cell_row][cell_col] != 0:
                    components[0][cell_row][cell_col] = 0
    obnova_power()
    # brany
    AND_brana()
    OR_brana()
    XOR_brana()
    NAND_brana()
    NOR_brana()
    NOT_brana()

    draw_grid()

    if menu_active:
        draw_menu()
    
    

    if vypnuti:
        for row in range(1, rows):
            for col in range(1, cols):
                if components[1][row][col] == 2:
                    components[1][row][col] = 0
        vypnuti = False

    # Vykreslení součástek a kabelů na herní plochu
    for row in range(rows):
        for col in range(cols):
            component_type = components[0][row][col]
            voltage = components[1][row][col]
            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if component_type == 1:  # Tlačítko
                if voltage == 1:
                    screen.blit(button_on_image, (x, y))
                else:
                    screen.blit(button_off_image, (x, y))
            elif component_type == 2:  # AND brána
                screen.blit(and_gate_image, (x, y))
            elif component_type == 3:  # Obrazovka
                if (voltage == 1 or components[1][row + 1][col] == 1 or components[1][row - 1][col] == 1 or components[1][row][col + 1] == 1 or components[1][row][col - 1] == 1):
                    screen.blit(screen_on_image, (x, y))
                else:
                    screen.blit(screen_off_image, (x, y))
            elif component_type == 4:
                # Vykreslení kabelů
                if voltage == 1:
                    cable_color = (255, 165, 0)
                else:
                    cable_color = (30, 90, 30)
                pygame.draw.rect(screen,cable_color,((x + CELL_SIZE // 2 - kabel_velikost // 2),(y + CELL_SIZE // 2 - kabel_velikost // 2), kabel_velikost, kabel_velikost,),)
                if components[0][row - 1][col] in range(1, 10):
                    pygame.draw.rect(screen, cable_color,((x + CELL_SIZE // 2 - kabel_velikost // 2),y,kabel_velikost,CELL_SIZE // 2,),)
                if components[0][row + 1][col] in range(1, 10):
                    pygame.draw.rect(screen, cable_color,((x + CELL_SIZE // 2 - kabel_velikost // 2),(y + CELL_SIZE // 2),kabel_velikost,CELL_SIZE // 2,),)
                if components[0][row][col - 1] in range(1, 10):
                    pygame.draw.rect( screen,cable_color,(x,(y + CELL_SIZE // 2 - kabel_velikost // 2),CELL_SIZE // 2,kabel_velikost,),)
                if components[0][row][col + 1] in range(1, 10):
                    pygame.draw.rect( screen,cable_color,((x + CELL_SIZE // 2),(y + CELL_SIZE // 2 - kabel_velikost // 2),CELL_SIZE // 2, kabel_velikost,),)
            elif component_type == 5:  # OR brána
                screen.blit(or_gate_image, (x, y))
            elif component_type == 6:  # XOR brána
                screen.blit(xor_gate_image, (x, y))
            elif component_type == 7:  # NAND brána
                screen.blit(nand_gate_image, (x, y))
            elif component_type == 8:  # NOR brána
                screen.blit(nor_gate_image, (x, y))
            elif component_type == 9:  # NOT brána
                screen.blit(not_gate_image, (x, y))

    pygame.display.flip()

pygame.quit()