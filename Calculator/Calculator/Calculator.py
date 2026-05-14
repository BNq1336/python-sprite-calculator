import pygame
import re

pygame.init()

screen = pygame.display.set_mode((800,1100))
pygame.display.set_caption("Helluva calculator")

BLACK = (0,0,0)
WHITE = (254,255,250)

calculation = ""
operators = ".+/*-"

font = pygame.font.Font("PressStart2P-Regular.ttf", 40)

background = pygame.image.load("background.png").convert_alpha()
background = pygame.transform.scale(background, (800,1100))

button_img = pygame.image.load("button.png").convert_alpha()
button_img = pygame.transform.scale(button_img, (100,100))

button_hov_img = pygame.image.load("button_hov.png").convert_alpha()
button_hov_img = pygame.transform.scale(button_hov_img, (100,100))

class Button:
   
    def __init__(self, x, y, width, height, text):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)

        self.image = button_img 
        self.hover_image = button_hov_img

        self.current_image = self.image

    def button_draw(self):
        if self.text == "C":
            self.current_image = pygame.transform.scale(self.current_image, (230,100))

        screen.blit(self.current_image, self.rect)
        
        button_inside = font.render(self.text, False, (255,240,195))
        button_inside_rect = button_inside.get_rect(center=self.rect.center)

        screen.blit(button_inside, button_inside_rect)

    def hover(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.current_image = self.hover_image
        else:
            self.current_image = self.image

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
                    
                    elif len(calculation) >= 13:
                        return calculation

                    else:
                        calculation += self.text

                except ZeroDivisionError:
                    calculation = "Can't divide by 0"

        return calculation
                
button_data = [
    ("1", 170, 750, 110,105),
    ("2", 300, 750, 110,105),
    ("3", 430, 750, 110,105),
    ("4", 170, 650, 110,105),
    ("5", 300, 650, 110,105),
    ("6", 430, 650, 110,105),
    ("7", 170, 550, 110,105),
    ("8", 300, 550, 110,105),
    ("9", 430, 550, 110,105),
    ("0", 300, 850, 110,105),
    ("+", 560, 750, 110,105),
    ("-", 560, 550, 110,105),
    ("/", 560, 650, 110,105),
    ("*", 560, 450, 110,105),
    ("=", 430, 850, 110,105),
    ("C", 300, 450, 240,105),
    (".", 170, 850, 110,105)
]

buttons = []

for text, x, y, width, height in button_data:
    buttons.append(Button(x, y, width, height, text))

running = True

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        for button in buttons:
            calculation = button.click(event, calculation, operators)

    screen.blit(background,(0,0))

    calculation_surface = font.render(calculation, False, BLACK)
    screen.blit(calculation_surface, (130, 270))

    for button in buttons:
        button.hover()
        button.button_draw()

    pygame.display.update()

pygame.quit()