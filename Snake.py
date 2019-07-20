'''
Usual snake game
'''
import pygame
import random
import math
# pylint: disable=no-member
pygame.init()
win = pygame.display.set_mode((900,900))
font = pygame.font.SysFont("comicsans", 30, True)
pygame.display.set_caption("Snake")
clock = pygame.time.Clock()
images = {
    'up': pygame.image.load('head_up.png'),
    'right': pygame.image.load('head_right.png'),
    'left': pygame.image.load('head_left.png'),
    'down': pygame.image.load('head_down.png'),
    'body': pygame.image.load('body.png'),
    'food': pygame.image.load('food.png')
}

class Food():
    def __init__(self):
        self.x = 30*random.randint(0,29)
        self.y = 30*random.randint(0,29)
        allow = False
        while not allow:
            if [self.x, self.y] not in snake.get_cords():
                allow = True
            else:
                self.x = 30*random.randint(0,29)
                self.y = 30*random.randint(0,29)
    def draw(self, win):
        win.blit(images['food'], (self.x, self.y))
    def get_cords(self):
        return [self.x, self.y]
class Block():
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    def get_cords(self):
        return [self.x, self.y]
    def draw(self, win):
        win.blit(images[self.direction], (self.x, self.y))

class Snake():
    def __init__(self, x, y):
        self.length = 1
        self.vel = 30
        self.x = x
        self.y = y
        self.head = Block(self.x, self.y, 'right')
        self.direction = self.head.direction
        self.body = [self.head]
        self.fitness = 0
        self.genes = {
            'dist_to_food' : round(random.uniform(-1,1), 5),
            'dist_to_wall' : round(random.uniform(-1,1), 5),
            'dist_to_body' : round(random.uniform(-1,1), 5),
            'length' : round(random.uniform(-1,1), 5)
        }
    def add(self):
        if self.length == 1:
            angle = self.body[0].direction
            if angle == 'down':
                node = Block(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y-self.vel, 'body')
            elif angle =='up':
                node = Block(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y + self.vel, 'body')
            elif angle =='left':
                node = Block(self.body[len(self.body)-1].x + self.vel, self.body[len(self.body)-1].y, 'body')
            elif angle =='right':
                node = Block(self.body[len(self.body)-1].x - self.vel, self.body[len(self.body)-1].y, 'body')
        else:
            angle_x = self.body[(self.length-1)].x - self.body[(self.length-2)].x
            angle_y = self.body[(self.length-1)].y - self.body[(self.length-2)].y
            if angle_x > 0:
                node = Block(self.body[len(self.body)-1].x + self.vel, self.body[len(self.body)-1].y, 'body')
            if angle_x < 0:
                node = Block(self.body[len(self.body)-1].x - self.vel, self.body[len(self.body)-1].y, 'body')
            if angle_y > 0:
                node = Block(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y + self.vel, 'body')
            if angle_y < 0:
                node = Block(self.body[len(self.body)-1].x, self.body[len(self.body)-1].y - self.vel, 'body')  
        self.body.append(node)
        self.length+=1
    def update_genes(self, **kwargs):
        self.genes.update(kwargs)

    def move(self, direction):
        init_x = snake.body[0].x
        init_y = snake.body[0].y
        snake.body[0].direction = direction
        if direction == 'right':
            if snake.body[0].x == 870:
                return False
            snake.body[0].x += snake.vel
        if direction == 'left':
            if snake.body[0].x == 0:
                return False
            snake.body[0].x -= snake.vel
        if direction == 'up':
            if snake.body[0].y == 0:
                return False
            snake.body[0].y -= snake.vel
        if direction == 'down':
            if snake.body[0].y == 870:
                return False
            snake.body[0].y += snake.vel
        if snake.length>1:
            if snake.collision():
                return 1
            for i in range(1, snake.length):
                curr_x = snake.body[i].x
                curr_y = snake.body[i].y
                snake.body[i].x = init_x
                snake.body[i].y = init_y
                init_x = curr_x
                init_y = curr_y
        self.x = self.body[0].x
        self.y = self.body[0].y
        return True
    def draw(self, win):
        for x in self.body:
            x.draw(win)
    def get_cords(self):
        coords = [body.get_cords() for body in self.body]
        return coords
    def best_move(self):
        ratings = {}
        init_x = self.x
        init_y = self.y
        directions = ['right', 'left', 'down', 'up']
        for direction in directions:
            self.move(direction)
            '''
            Get current values from environment
            Multiply them with genes
            Summ = rating of move
            '''
            rating += 1
            ratings[direction] = rating
            self.x = init_x
            self.y = init_y
        return max(ratings, key=ratings.get)
    def collision(self):
        coords = [body.get_cords() for body in self.body]
        if self.head.get_cords() in coords[1:]:
            return True
        else:
            return False
def redraw():
    win.fill((0, 0, 0))   
    eat.draw(win)
    snake.draw(win)
    text = font.render("Score: " + str(snake.length-1), 1, (0,255,0))
    win.blit(text, (390, 10))
    pygame.display.update()

snake = Snake(120, 120)
eat = Food()
# run = True
def get_dist_to_food(snake_obj, food_obj):
    return abs(pow(((snake_obj.x - food_obj.x)**2 - (snake_obj.y - food_obj.y)**2), 0.5))
def get_dist_to_wall(snake_obj):
    if snake_obj.direction == 'up':
        return abs(0 - snake_obj.y)
    if snake_obj.direction == 'down':
        return abs(900 - snake_obj.y)
    if snake_obj.direction == 'right':
        return abs(900 - snake_obj.x)
    if snake_obj.direction == 'left':
        return abs(0 - snake_obj.x)
def get_dist_to_body(snake_obj):
    coords = []
    for x in snake_obj.body[1:]:
        coords.append([x.x, x.y])
    if snake_obj.direction == 'up':
        for x in coords:
            if snake_obj.x == x[0] and snake_obj.y > x[1]:
                return abs(snake_obj.y - x[1])
    if snake_obj.direction == 'down':
        for x in coords:
            if snake_obj.x == x[0] and snake_obj.y < x[1]:
                return abs(x[1] - snake_obj.y)
    if snake_obj.direction == 'right':
        for x in coords:
            if snake_obj.y == x[1] and snake_obj.x < x[0]:
                return abs(x[0]-snake_obj.x)
    if snake_obj.direction == 'left':
        for x in coords:
            if snake_obj.y == x[1] and snake_obj.x > x[0]:
                return abs(snake_obj.x - x[0])
    return 900
def game(player, show):
    snake = player
    draw_check = show
    global eat
    run = True
    while run:
        if snake.collision():
                return 1
        # snake.best_move()
        '''
        if not snake.move(snake.direction):
            return 1
        '''
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if eat.x == snake.body[0].x and eat.y == snake.body[0].y:
            snake.add()
            eat = Food()
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            snake.direction = 'right'
            if not snake.move(snake.direction):
                return 1
           
        if keys[pygame.K_LEFT]:
            snake.direction = 'left'
            if not snake.move(snake.direction):
                return 1

        if keys[pygame.K_DOWN]:
            snake.direction = 'down'
            if not snake.move(snake.direction):
                return 1

        if keys[pygame.K_UP]:
            snake.direction = 'up'
            if not snake.move(snake.direction):
                return 1
        if keys[pygame.K_SPACE]:
            print(get_dist_to_body(snake))
            print(get_dist_to_food(snake, eat))
            print(get_dist_to_wall(snake))
        if draw_check:
            redraw()
    return 1

while game(snake, True):
    snake = Snake(120, 120)
    eat = Food()
    game(snake, True)


def population(size):
    population_snakes = []
    for x in range(0,size):
        population_snakes[x] = Snake(random.randint(10, 20)*30, random.randint(10, 20)*30)
    return population_snakes


def evolution(population, num_generations):
    for y in range(num_generations):

        for x in population:
            game(x, True)
