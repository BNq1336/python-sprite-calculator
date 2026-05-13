import pygame
import re

pygame.init()

screen = pygame.display.set_mode((480,700))
pygame.display.set_caption("Helluva calculator")

RED = (216,41,50)
BLACK = (0,0,0)
WHITE = (254,255,250)

calculation = ""
operators = ".+/*-"

font = pygame.font.SysFont("bahnschrift", 50)

class Button:
   
    def __init__(self, screen, color, x, y, width, height, text):
        self.color = color
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
    
    def button_draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=15)
        
        button_inside = font.render(self.text, True, (254,255,250))
        button_inside_rect = button_inside.get_rect(center=self.rect.center)

        screen.blit(button_inside, button_inside_rect)

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.color = (44,42,54)
        else:
            self.color = (0,0,0)

    def click(self, event, calculation, operators):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                try:

                    if self.text == "C" or calculation == "Can't divide by 0":
                        calculation = ""

                    elif self.text == "=":
                        if len(calculation) == 0 or calculation[-1] in operators:
                            return calculation
                        calculation = str(eval(calculation))[:13]

                    elif len(calculation) == 0 and self.text in operators and self.text != "-":
                        return calculation

                    elif self.text == ".":
                        last_number = re.split(r"[+-/*]", calculation)[-1]
                        if "." in last_number:
                            return calculation
                        calculation += self.text

                    elif len(calculation) > 0 and calculation[-1] in operators and self.text in operators:
                        return calculation

                    elif len(calculation) > 13:
                        calculation = calculation[:13]

                    else:
                        calculation += self.text

                except ZeroDivisionError:
                    calculation = "Can't divide by 0"

        return calculation
                
button_data = [
    ("1", 50, 500, 80, 80),
    ("2", 150, 500, 80, 80),
    ("3", 250, 500, 80, 80),
    ("4", 50, 400, 80, 80),
    ("5", 150, 400, 80, 80),
    ("6", 250, 400, 80, 80),
    ("7", 50, 300, 80, 80),
    ("8", 150, 300, 80, 80),
    ("9", 250, 300, 80, 80),
    ("0", 150, 600, 80, 80),
    ("+", 350, 500, 80, 80),
    ("-", 350, 400, 80, 80),
    ("/", 350, 300, 80, 80),
    ("*", 350, 200, 80, 80),
    ("=", 250, 600, 180, 80),
    ("C", 50, 200, 180, 80),
    (".", 50, 600, 80, 80)
]

buttons = []

for text, x, y, width, height in button_data:
    button = Button(screen, BLACK, x, y, width, height, text)
    buttons.append(button)

running = True

while running:

    for button in buttons:
        button.hover()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        for button in buttons:
            calculation = button.click(event, calculation, operators)

    screen.fill(RED)

    pygame.draw.rect(screen, WHITE,(50, 50, 380, 100), border_radius=10)
    calculation_surface = font.render(calculation, True, BLACK)
    screen.blit(calculation_surface, (50, 80))

    for button in buttons:
        button.button_draw()

    pygame.display.update()

pygame.quit()