from pygame import *
import random

init()

#створи вікно гри
FPS = 60
TILE_SIZE = 50
MAP_WIDTH, MAP_HEIGHT = 20, 15
WIDTH, HEIGHT = TILE_SIZE*MAP_WIDTH, TILE_SIZE*MAP_HEIGHT
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Catch up")

clock = time.Clock()

bg = image.load('background.jpg')
bg = transform.scale(bg, (WIDTH, HEIGHT))
player_img = image.load('hero.png')
wall_img = image.load("wall.png")
enemy_img = image.load("ZPfe8ZBU7nuPiuePokAAGG5zFWHVRN19gocCLgdT.png")
treasure_img = image.load("treasure.png")

all_sprites = sprite.Group()

class BaseSprite(sprite.Sprite):
    def __init__(self, image, x,y,width, height):
        super().__init__()
        self.image = transform.scale(image, (width, height))
        self.rect = Rect(x,y,width, height)
        self.mask = mask.from_surface(self.image)
        all_sprites.add(self)
    def draw(self,window):
        window.blit(self.image, self.rect)

class Player(BaseSprite):
    def __init__(self, image,x, y, width, height):
        super().__init__(image, x, y, width, height)
        self.right_image = self.image
        self.left_image = transform.flip(self.image, True, False)
        self.speed = 5
        self.hp = 100
        self.coins_counter= 0
        self.damage_timer = time.get_ticks()

    def update(self):
        old_pos = self.rect.x, self.rect.y
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.left_image
        if keys[K_RIGHT]:
            self.rect.x += self.speed
            self.image = self.right_image
        if keys[K_UP]:
            self.rect.y -= self.speed
        if keys[K_DOWN]:
            self.rect.y += self.speed

        

        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos

        coll_list = sprite.spritecollide(self, enemys, False, sprite.collide_mask)
        if len(coll_list)>0:
            now = time.get_ticks()
            if now-self.damage_timer > 1000:
                self.damage_timer = time.get_ticks()
                self.hp -= 10
                print(self.hp)

            self.rect.x, self.rect.y = old_pos
            

class Enemy (BaseSprite):  
    def __init__(self, image, x, y, width, height):  
        super().__init__(image, x, y, width, height)  
        self.right_image = self.image  
        self.left_image = transform.flip(self.image, True, False)  
        self.speed = 4
        self.dir_list = ['left', 'right', 'up', 'down']
        self.dir = random.choice(self.dir_list)

    def update(self):
        old_pos = self.rect.x, self.rect.y

        if self.dir == 'left' and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = self.left_image
        elif self.dir == 'right' :
            self.rect.x += self.speed
            self.image = self.right_image
        elif self.dir == 'up':
            self.rect.y -= self.speed
        elif self.dir == 'down':
            self.rect.y += self.speed


        coll_list = sprite.spritecollide(self, walls, False, sprite.collide_mask)
        if len(coll_list)>0:
            self.rect.x, self.rect.y = old_pos
            self.dir = random.choice(self.dir_list)




player1 = Player(player_img, 200,300, TILE_SIZE-5, TILE_SIZE-5)
walls = sprite.Group()
enemys = sprite.Group()
with open("map.txt", "r") as file:  
    map = file.readlines()  
    x, y = 0, 0  
    for row in map:  
        for symbol in row:  
            symbol = symbol.upper()  
            if symbol == 'W':  
                walls.add(BaseSprite(wall_img, x, y, TILE_SIZE, TILE_SIZE))  
            if symbol == 'E':  
                enemys.add(Enemy(enemy_img, x, y, TILE_SIZE, TILE_SIZE))  
            if symbol == 'P':  
                player1.rect.x = x  
                player1.rect.y = y

            if symbol =='E':
                treasure = BaseSprite(treasure_img, x, y, TILE_SIZE, TILE_SIZE)

            x+=TILE_SIZE
        x = 0
        y+=TILE_SIZE
run = True
finish = False
while run:
    window.blit(bg,(0,0))
    for e in event.get():
        if e.type == QUIT:
            run=False
    if player1.hp<=0:
        finish = True

    if sprite.collide_rect(player1, treasure):
        finish=True

    if not finish:
        player1.update()
        enemys.update()
    walls.draw(window)
    all_sprites.draw(window)

    display.update()
    clock.tick(FPS)