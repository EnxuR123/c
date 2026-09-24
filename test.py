import pygame

pygame.init()

screen = pygame.display.set_mode((1000, 800))
title=pygame.Surface((1000, 800))
pygame.display.set_caption("Cheese Chase")
my_font = pygame.font.SysFont(None, 150)
text_surface = my_font.render('Cheese Chase', True, (0, 0, 0))
clock = pygame.time.Clock()

#background
bg_image = pygame.image.load("background.png").convert_alpha()
bg_image = pygame.transform.scale(bg_image, (1000, 800))
b1 = pygame.image.load("b1.png").convert_alpha()
b1 = pygame.transform.scale(b1, (1000, 800))


#player
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(
    player_image,
    (100, 100)
)
player_x = 50
player_y = 300
JUMP_STRENGTH = -150
GRAVITY = 2
speed=5

class Player():
    def __init__(self, x, y):
        self.is_grounded = False
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.collider = self.rect.inflate(-80,-80)
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= speed
            self.collider.x = self.rect.x
        if keys[pygame.K_RIGHT]:
            self.rect.x += speed
            self.collider.x = self.rect.x
        if keys[pygame.K_UP] and self.is_grounded:
            self.rect.y += JUMP_STRENGTH
            self.collider.y = self.rect.y
            self.is_grounded = False

        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))


#buttons
exit = pygame.image.load("exit.png").convert_alpha()
exit = pygame.transform.scale(
    exit,
    (50, 50)
)
start = pygame.image.load("start.png").convert_alpha()
start = pygame.transform.scale(
    start,
    (50, 50)
)
class Button():
    def __init__(self, x,y, image, scale):
        width=image.get_width()
        height=image.get_height()
        new_size=int(width * scale*2), int(height * scale)
        self.image=pygame.transform.scale(image, new_size)
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.clicked=False

    def draw(self):
        title.blit(self.image, (self.rect.x, self.rect.y))

    def click(self):
        pos=pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                self.clicked=True
                return True

# class Enemy():

#target
cheese=pygame.image.load("cheese.png").convert_alpha()
cheese=pygame.transform.scale(
    cheese,
    (50, 50)
)
class Cheese():
    def __init__(self, x, y):
        self.image=cheese
        self.rect=self.image.get_rect()
        self.rect.topleft=(x,y)
        self.collider=pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def eat(self, player):
        if self.collider.colliderect(player.collider):
            return True
        return False

#platforms
platforms = [
    pygame.Rect(0, 550, 800, 50),     
    pygame.Rect(100, 400, 250, 20),   
    pygame.Rect(450, 300, 250, 20)    
]





button1=Button(325, 375, start, 3)
button2=Button(325, 550, exit, 3)
player=Player(player_x, player_y)
cheese=[]


running=True
page=False

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(title, (0, 0))
    if page==False:
        title.blit(bg_image, (0, 0))
        title.blit(text_surface, (175, 175))
        button1.draw()
        button2.draw()
        screen.blit(title, (0, 0))

        if(button2.click()):
            running=False
            page=True
        if(button1.click()):
            page=True
    else:
        screen.blit(b1, (0, 0))
        for platform in platforms:
            pygame.draw.rect(screen, (0, 0, 0), platform)
        # for platform in platforms:
        #     if player.collider.colliderect(platform):
                # if player.rect.bottom >= platform.top and player.rect.y > 0:
                #     player.rect.bottom = platform.top
                #     player_y = player.rect.y
                #     player.is_grounded = True
                # if player.rect.bottom <= platform.top + 20 and player.rect.bottom >= platform.top - 10:
                #     if player.rect.y > platform.top - player.rect.height:
                #         player.rect.bottom = platform.top
                #         player.collider.bottom = platform.top
                #         player.is_grounded = True

        player.move()

        if not player.is_grounded:
            player.rect.y += GRAVITY
            player.collider.y = player.rect.y
        
        player.is_grounded = False

        for platform in platforms:
            if player.rect.colliderect(platform):
                if player.rect.bottom <= platform.top+15:
                    player.rect.bottom = platform.top
                    player.collider.bottom = platform.top
                    player.is_grounded = True

    
        player.draw()

    pygame.display.flip()

    
    clock.tick(60)

pygame.quit()
