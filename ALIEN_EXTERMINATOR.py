import sys
import os
import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

Star_ship = 'SpaceShip.png'

WIDTH = 800
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000
FREEZ_TIME = 5000
HS_FILE = "highscore.txt"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ALIEN EXTERMINATOR")
clock = pygame.time.Clock()

dir = path.dirname(__file__)
with open(path.join(dir, HS_FILE), 'r') as f:
    try:
        rec_score = int(f.read())
    except:
        rec_score = 0

lvl_count = 1
boss_count = 0
lives_count = 0

def newboss():
    b = Boss()
    all_sprites.add(b)
    bosss.add(b)

def newmob():
    if boss_count < 150:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 130
    BAR_HEIGHT = 20
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('img/NNL.ttf', 36)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text2(surf, text, size, x, y):
    font = pygame.font.Font('img/NNL.ttf', 24)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_text3(surf, text, size, x, y):
    font = pygame.font.Font('img/NNL.ttf', 30)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = (x - 60) + 47 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, 'ALIEN EXTERMINATOR', 64, WIDTH / 2, HEIGHT / 8)
    draw_text3(screen, 'Press arrow keys for move, Space to fire', 22, WIDTH / 2, 350 )
    draw_text3(screen, 'Press any key to begin', 18, WIDTH / 2, 550)
    draw_text(screen, 'YOUR RECORD:', 64, WIDTH / 2,  430)
    draw_text(screen, str(rec_score), 18, WIDTH / 2, 475)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

def pause():
    screen.blit(background, background_rect)
    draw_text(screen, 'PAUSE', 64, WIDTH / 2, HEIGHT / 2)
    draw_text3(screen, 'Press any key to continue', 18, WIDTH / 2, 550)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False

class Spritesheet:
        def __init__(self, filename):
            self.spritesheet = pygame.image.load(filename).convert()

        def get_image(self, x, y, width, height):
            image = pygame.Surface((width, height))
            image.blit(self.spritesheet, (0, 0), (x, y, width, height))
            image = pygame. transform.scale(image, (width // 2, height // 2))
            return image

spritesheet = Spritesheet(path.join(img_dir, Star_ship))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (75, 52))
        self.image.set_colorkey(BLACK)
        self.current_frame = 0
        self.rect = self.image.get_rect()
        self.radius = 23
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()
        self.god = 1
        self.god_time = pygame.time.get_ticks()
        self.left = False
        self.right = False

    def load_images(self):
        self.move_frame = [self.game.spritesheet.get_image(2, 3, 75, 95),
                              self.game.spritesheet.get_image(92, 4, 75, 96),
                              self.game.spritesheet.get_image(181, 4, 75, 95),
                              self.game.spritesheet.get_image(268, 4, 75, 95)]
        for frame in self.move_frame:
            frame.set_colorkey(BLACK)

    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.god >= 2 and pygame.time.get_ticks() - self.god_time > FREEZ_TIME:
            self.god -= 1
            self.god_time = pygame.time.get_ticks()

        if self.god == 1:
            self.image = pygame.transform.scale(player_img, (75, 52))
            self.image.set_colorkey(BLACK)

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.left = True
            self.right = False
            if self.power >= 1:
                self.speedx = -8
            if self.power >= 3:
                self.speedx = -16
        if keystate[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            if self.power >= 1:
                self.speedx = 8
            if self.power >= 3:
                self.speedx = 16
        if keystate[pygame.K_SPACE]:
            self.shoot()

        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        
    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()
            if boses.bosslife == 0:
                if self.power == 1:
                    bullet = DeathBullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    deadbullet.add(bullet)
                    shoot_sound.play()
                if self.power >= 2:
                    bullet1 = DeathBullet(self.rect.left, self.rect.centery)
                    bullet2 = DeathBullet(self.rect.right, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    deadbullet.add(bullet1)
                    deadbullet.add(bullet2)
                    shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 3) * lvl_count / 2
        self.speedx = random.randrange(-3, 3) 
        self.rot = 0
        self.rot_speed = random.randrange(-1, 1)
        self.last_update = pygame.time.get_ticks()

    def speed_update(self):
        if self.speedy <= 1:
            self.speedy = 2

    def rotate(self):
        now = pygame.time.get_ticks()
        if now  - self.last_update > 50:
            self.last_update = now
            self.rot =(self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):  
        self.speed_update()
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -90 or self.rect.right > WIDTH + 90:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3) * lvl_count / 2 
            self.speed_update()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(boss_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = pygame.transform.scale(self.image_orig.copy(), (363, 176 ))
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .75 / 2)
        self.rect.x = 155
        self.rect.y = -200
        self.speedy = 1 * lvl_count
        self.speedx = 1 * lvl_count
        self.bosslife = 100
        self.shoot_delay = 500
        self.shoot_delay2 = 2000
        self.last_shot = pygame.time.get_ticks()
        self.last_shot2 = pygame.time.get_ticks()
        self.last_update = pygame.time.get_ticks()
                
    def update(self):
        self.bshoot()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.speedx = -1 * lvl_count
        if self.rect.left < 0:
            self.speedx = 1 * lvl_count
        if self.rect.top > HEIGHT - 575:
            self.speedy = 0

    def bshoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet3 = Bossbullet(self.rect.left*1.15, self.rect.centery*1.85)
            bullet4 = Bossbullet(self.rect.right/1.04, self.rect.centery*1.85)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            bossbullet.add(bullet3)
            bossbullet.add(bullet4)
            shoot_sound.play()
        now2 = pygame.time.get_ticks()
        if now2 - self.last_shot2 > self.shoot_delay2:
            self.last_shot2 = now2   
            bullet5 = Bossbullet(self.rect.centerx + 6, self.rect.bottom + 25)
            all_sprites.add(bullet5)
            bossbullet.add(bullet5)
            shoot_sound.play()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        if player.power >= 2:
            self.image = bullet2_img
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class DeathBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        if player.power >= 2:
            self.image = bullet2_img
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Bossbullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bossbull_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0 :
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__ (self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'freez'])
        self.image = powerup_images [self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Fly(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = playeranim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 15
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(playeranim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = playeranim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


background = pygame.image.load(path.join(img_dir, "space.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "ship.png")).convert()
player_god_img = pygame.image.load(path.join(img_dir, "shipUP.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (50, 36))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "fire.png")).convert()
bullet2_img = pygame.image.load(path.join(img_dir, "fire02.png")).convert()
bossbull_img = pygame.image.load(path.join(img_dir, "bossbull.png")).convert()
meteor_images = []
meteor_list = [ 'ufo.png', 'ufo01.png', 'ufo02.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
boss_images = []
boss_list = [ 'boss.png', 'boss02.png', 'boss03.png']
for img in boss_list:
    boss_images.append(pygame.image.load(path.join(img_dir, img)).convert())
playeranim = {}
playeranim ['fly'] = []
for i in range(4):
    filename = 'ShipA0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_fly = pygame.transform.scale(img, (75, 52))
    playeranim['fly'].append(img_fly)
explosion_anim = {}
explosion_anim ['lg'] = []
explosion_anim ['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield01.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'gun01.png')).convert()
powerup_images['freez'] = pygame.image.load(path.join(img_dir, 'freez01.png')).convert()

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
shoot_sound.set_volume(0.5)
shield_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow4.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir, 'pow5.wav'))
expl_sounds = []
for snd in ['boom2.wav', 'boom3.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'fight.wav'))
pygame.mixer.music.set_volume(0.25)


all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bosss = pygame.sprite.Group()
bullets = pygame.sprite.Group()
bossbullet = pygame.sprite.Group()
deadbullet = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
boses = Boss ()
all_sprites.add(player)
for i in range(8):
    newmob()
score = 0
hight_score = 0
ship_count = 0
pygame.mixer.music.play(loops=-1)

game_over = True
running = True
while running:
    if game_over:
        if hight_score > rec_score:
            rec_score = hight_score
            with open(path.join(dir, HS_FILE), 'w') as f:
                f.write(str(hight_score))
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        bosss = pygame.sprite.Group()
        bossbullet = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        deadbullet = pygame.sprite.Group()
        player = Player()
        boses = Boss()
        all_sprites.add(player)
        for i in range(8):
            newmob()            
        score = 0
        ship_count = 0
        lvl_count = 1
        boss_count = 0
        lives_count = 0

        
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type ==  pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    pause()
    all_sprites.update()

    hits = pygame.sprite.groupcollide(bosss, bullets, False, True)
    for hit in hits:
        if boses.bosslife >0:
            boses.bosslife -= 2
        if boses.bosslife == 0:
            boses.bosslife -= 0

    hits = pygame.sprite.groupcollide(bosss, deadbullet, True, True)
    for hit in hits:
        if boses.bosslife == 0:
            score += 1000
            boss_count = 0
            boses.bosslife = 100
            if score > hight_score:
                hight_score = score
            random.choice(expl_sounds).play()
            expl = Explosion(hit.rect.center, 'lg')
            all_sprites.add(expl)
            for i in range(8):
                newmob()
            
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        score += 100 - hit.radius
        ship_count += 1
        boss_count += 1
        if boss_count == 150:
            newboss()
        if ship_count == 75:
            lvl_count += 1
            ship_count = 0
        if score > hight_score:
            hight_score = score
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    hits = pygame.sprite.groupcollide(mobs, deadbullet, True, True)
    for hit in hits:
        score += 100 - hit.radius
        ship_count += 1
        if ship_count == 75:
            lvl_count += 1
            ship_count = 0
        if score > hight_score:
            hight_score = score
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)


    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        if player.god == 1:
            player.shield -= hit.radius / 1.5
        if player.god >= 2:
            player.shield -= 0
        
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            random.choice(expl_sounds).play()
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, bossbullet, True, pygame.sprite.collide_circle)
    for hit in hits:
        if player.god == 1:
            player.shield -= 25
        if player.god >= 2:
            player.shield -= 0
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            random.choice(expl_sounds).play()
            player.hide()
            player.lives -= 1
            player.shield = 100

    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 50)
            lives_count += 1
            if lives_count == 20:
                player.lives += 1
                lives_count = 0
            if player.shield >= 100:
                player.shield = 100
            shield_sound.play()
        if hit.type == 'gun':
            player.powerup()
            power_sound.play()
        if hit.type == 'freez':
            player.god += 1
            player.god_time = pygame.time.get_ticks()
            player.image = pygame.transform.scale(player_god_img, (75, 52))
            player.image.set_colorkey(BLACK)
            power_sound.play()

    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text2(screen, 'SCORE', 18, 750, 10)
    draw_text(screen, str(score), 18, 750, 36)
    draw_text2(screen, 'HIGH SCORE', 18, WIDTH / 2, 10)
    draw_text(screen, str(hight_score), 18, WIDTH / 2, 36)
    #draw_text(screen, str(lvl_count), 18, WIDTH / 3, 10)
    #draw_text(screen, str(boses.bosslife), 18, WIDTH / 3, 10)
    #draw_text(screen, str(boss_count), 18, WIDTH / 5, 10)
    draw_shield_bar(screen, 10, 10, player.shield)
    draw_lives(screen, 65, 35, player.lives, player_mini_img)
    pygame.display.flip()

pygame.quit()