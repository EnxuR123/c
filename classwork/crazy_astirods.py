import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
mass = 1

class plane:
    def __init__(self):
        self.pos = pygame.Vector2(400, 300)
        self.ship_position = self.pos.copy()
        self.ship_angle = 90
        self.forward = pygame.Vector2(1, 0)
        self.ROTATION_SPEED = 3
        self.SHIP_SPEED = 4
        self.points = [(-12, 10), (12, 0), (-12, -10)]

        # def speed(self):
        #     self.pos+=self.vect
        #     self.vect+=self.acc
        #     self.acc*=0
        #     for i in range(len(self.points)):
        #         self.points[i]=(self.points[i][0]+self.pos.x, self.points[i][1]+self.pos.y)

        # def move(self):
        #         keys = pygame.key.get_pressed()
        #         if keys[pygame.K_LEFT]:
        #             self.rect.x -= speed
        #             self.collider.x = self.rect.x
        #         if keys[pygame.K_RIGHT]:
        #             self.rect.x += speed
        #             self.collider.x = self.rect.x
        #         if keys[pygame.K_UP] and self.is_grounded:
        #             self.rect.y += JUMP_STRENGTH
        #             self.collider.y = self.rect.y
        #             self.is_grounded = False

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.ship_angle += self.ROTATION_SPEED
        if keys[pygame.K_RIGHT]:
            self.ship_angle -= self.ROTATION_SPEED

        radians = math.radians(self.ship_angle)
        self.forward = pygame.Vector2(
            math.cos(radians),
            -math.sin(radians)
        )
        if keys[pygame.K_UP]:
            self.ship_position += self.forward * self.SHIP_SPEED

        self.pos = self.ship_position.copy()
        self.pos.x = max(0, min(800, self.pos.x))
        self.pos.y = max(0, min(600, self.pos.y))
        self.ship_position = self.pos.copy()

    def collision(self, other):
        for x, y in self.points:
            px = self.pos.x + x
            py = self.pos.y + y
            if math.hypot(px - other.pos.x, py - other.pos.y) <= other.radius:
                return True
        return False

    def draw(self):
        front = self.ship_position + self.forward * 20
        left = self.forward.rotate(140)
        right = self.forward.rotate(-140)

        p1 = self.ship_position + self.forward * 22
        p2 = self.ship_position + left * 16
        p3 = self.ship_position + right * 16

        pygame.draw.polygon(
            screen,
            "black",
            [p1, p2, p3],
            2       
        )




class bullet():
    def __init__(self, pos, vect):
        self.pos = pygame.math.Vector2(pos)
        self.vect = pygame.math.Vector2(vect)
        self.radius = 5

    def speed(self):
        self.pos += self.vect

    def collision(self, other):
        x = self.pos.x - other.pos.x
        y = self.pos.y - other.pos.y
        distance = math.sqrt(x**2 + y**2)
        return distance <= self.radius + other.radius

    def draw(self):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.pos.x), int(self.pos.y)), self.radius)

class rock:
    def __init__(self, radius):
        self.radius = radius * 10
        self.pos = pygame.math.Vector2(random.randint(radius * 10, 800 - radius * 10), random.randint(radius * 10, 600 - radius * 10))
        self.vect = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))

    # def split(self):
    #     if self.radius>10:
    #         return [rock(self.radius/2), rock(self.radius/2)]
    #     else:
    #         return []

    def speed(self):
        self.pos+=self.vect
        if self.pos.x-self.radius<0 or self.pos.x+self.radius>800:
            self.vect.x*=-1
        if self.pos.y-self.radius<0 or self.pos.y+self.radius>600:
            self.vect.y*=-1

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (self.pos.x, self.pos.y), self.radius)

    def collision(self, other):
        distance = (self.pos - other.pos).length()
        if distance <= self.radius + other.radius:
            temp = self.vect.copy()
            self.vect = ((self.radius * mass - other.radius * mass) / (self.radius * mass + other.radius * mass)) * self.vect + ((2 * other.radius * mass) / (self.radius * mass + other.radius * mass)) * other.vect
            other.vect = ((2 * self.radius * mass) / (self.radius * mass + other.radius * mass)) * temp + ((other.radius * mass - self.radius * mass) / (self.radius * mass + other.radius * mass + other.radius * mass)) * other.vect

    def draw(self):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.pos.x), int(self.pos.y)), self.radius)

rocks = [rock(random.randint(1, 5)) for _ in range(10)]
player = plane()
bullets = []

running = True
while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()
    player.draw()

    if pygame.mouse.get_pressed()[0]:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction = pygame.math.Vector2(mouse_x - player.ship_position.x, mouse_y - player.ship_position.y)
        if direction.length() > 0:
            direction = direction.normalize()
        bullets.append(bullet(player.ship_position, direction * 5))

    for bullet_obj in bullets[:]:
        bullet_obj.speed()
        bullet_obj.draw()
        for i in range(len(rocks)):
            if bullet_obj.collision(rocks[i]):
                rocks.pop(i)
                bullets.remove(bullet_obj)
                break

    for i in range(len(rocks)):
        rocks[i].speed()
        for j in range(i + 1, len(rocks)):
            rocks[i].collision(rocks[j])

    for rock_obj in rocks:
        rock_obj.draw()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()