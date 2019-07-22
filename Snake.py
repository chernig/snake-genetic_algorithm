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
generation = 0
creature = 0
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
        self.number_of_moves = 0
        self.head = Block(self.x, self.y, 'right')
       
        self.body = [self.head]
        self.direction = self.head.direction
        self.genes = {
            'dist_to_food' : round(random.uniform(-3,3), 5),
            'dist_to_wall' : round(random.uniform(-3,3), 5),
            'dist_to_body' : round(random.uniform(-3,3), 5),
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
    def reset(self):
        self.x = random.randint(10,20)*30
        self.y = random.randint(10,20)*30
        self.length = 1
        self.number_of_moves = 0
        self.direction = 'right'
        self.head = Block(self.x, self.y, 'right')
        self.body = [self.head]
        self.body[0].direction = 'right'
    def move(self, direction):
        self.number_of_moves +=1
        init_x = self.body[0].x
        init_y = self.body[0].y
        self.body[0].direction = direction
        if direction == 'right':
            if self.body[0].x == 870:
                return False
            self.body[0].x += self.vel
        if direction == 'left':
            if self.body[0].x == 0:
                return False
            self.body[0].x -= self.vel
        if direction == 'up':
            if self.body[0].y == 0:
                return False
            self.body[0].y -= self.vel
        if direction == 'down':
            if self.body[0].y == 870:
                return False
            self.body[0].y += self.vel
        if self.length>1:
            if self.collision():
                return 1
            for i in range(1, self.length):
                curr_x = self.body[i].x
                curr_y = self.body[i].y
                self.body[i].x = init_x
                self.body[i].y = init_y
                init_x = curr_x
                init_y = curr_y
        self.x = self.body[0].x
        self.y = self.body[0].y
        return True
    def draw(self, win):
        for x in self.body:
            x.draw(win)
    def condition(self):
        if self.length*100 - self.number_of_moves > 0:
            return True
        return False
    def get_cords(self):
        coords = [body.get_cords() for body in self.body]
        return coords
    def best_move(self):
        ratings = {}
        init_moves = self.number_of_moves
        init_coords = self.get_cords()
        init_dir = self.body[0].direction
        rating = 0
        all_directions = ['right', 'left', 'down', 'up']
        if init_dir == 'right':
            all_directions.remove('left')
        if init_dir == 'left':
            all_directions.remove('right')
        if init_dir == 'down':
            all_directions.remove('up')
        if init_dir == 'up':
            all_directions.remove('down')
        for direction in all_directions:
            '''
            if not self.move(direction):
                ratings[direction] = -500
                for x in range(self.length):
                    self.body[x].x = init_coords[x][0]
                    self.body[x].y = init_coords[x][1]
                self.body[0].direction = init_dir
                continue
            '''
            self.move(direction)
            rating = get_dist_to_body(self)*self.genes['dist_to_body']
            rating += get_dist_to_food(self, eat) * self.genes['dist_to_food']
            rating += get_dist_to_wall(self) * self.genes['dist_to_wall']
            ratings[direction] = rating
            rating = 0
            for x in range(self.length):
                self.body[x].x = init_coords[x][0]
                self.body[x].y = init_coords[x][1]
            self.body[0].direction = init_dir
            self.direction = init_dir
            self.number_of_moves = init_moves
        return max(ratings, key=ratings.get)
    def collision(self):
        coords = [body.get_cords() for body in self.body]
        if self.head.get_cords() in coords[1:]:
            return True
        else:
            return False
def redraw(snake_obj, food_obj):
    win.fill((0, 0, 0))   
    food_obj.draw(win)
    snake_obj.draw(win)
    text = font.render("Score: " + str(snake_obj.length-1), 1, (0,255,0))
    gen_text = font.render("Current generation: " + str(generation), 1, (0,255,0))
    creature_text = font.render("Current creature: " + str(creature), 1, (0,255,0))
    genes_table = font.render("Genes of the creature: " + str(snake_obj.genes), 1 , (0,255,0))
    # win.blit(genes_table, (100, 10))
    win.blit(text, (390, 10))
    win.blit(gen_text, (390, 30))
    win.blit(creature_text, (390, 50))
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
def game(snake):
    global eat
    eat = Food()
    run = True
    available_moves = 100
    while run:
        if snake.collision():
                return 1
        if not snake.move(snake.best_move()):
            return 1
        available_moves-=1
        if available_moves<0:
            return 1
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if eat.x == snake.body[0].x and eat.y == snake.body[0].y:
            snake.add()
            eat = Food()
            available_moves+=200

        keys = pygame.key.get_pressed()
        '''
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
            print(snake.best_move())
        '''
        if keys[pygame.K_g]:
            return 1

        redraw(snake, eat)
    return 1
'''
while game(snake):
    snake = Snake(120, 120)
    eat = Food()
    game(snake)
'''
def create_population(size):
    population_snakes = []
    for _ in range(size):
        population_snakes.append(Snake(random.randint(5, 25)*30, random.randint(5, 25)*30))
    return population_snakes
def create_child(dad, mom):
    mutation_rate = 0.05
    genes = {
        'dist_to_food': random.choice([dad.genes['dist_to_food'], mom.genes['dist_to_food']]),
        'dist_to_wall': random.choice([dad.genes['dist_to_wall'], mom.genes['dist_to_wall']]),
        'dist_to_body': random.choice([dad.genes['dist_to_body'], mom.genes['dist_to_body']]),
    }
    for x in genes.keys():
        if random.random() <= mutation_rate:
            genes[x] += random.uniform(-1,1)
    child = Snake(random.randint(5, 25)*30, random.randint(5, 25)*30)
    child.update_genes(**genes)
    return child

def evolve(population):
    size = len(population)
    while (len(population) > size / 2):
        population.pop()
    while (len(population) < size):
        population.append(create_child(population[0], population[random.randint(1,9)]))
    return population
def fitness(snake_obj):
    return ((snake_obj.length-1)*1000 - snake_obj.number_of_moves)
def evolution(population):
    global generation
    global eat
    generation += 1
    global creature
    while generation < 200:
        population_by_fitness = []
        for x in range(len(population)):
            population[x].reset()
            creature = x+1
            if game(population[x]):
                population_by_fitness.append(population[x])
        population_by_fitness.sort(key=lambda x: fitness(x), reverse = True)
        population = evolve(population)
        creature = 0
        generation+=1
    return population[0].genes
evolution(create_population(20))