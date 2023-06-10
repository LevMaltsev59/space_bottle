import pygame
import random
from os import path
import time


img_dir = path.join(path.dirname(__file__), 'image')
mrt_dir = path.join(path.dirname(__file__), 'meteor')
snd_dir = path.join(path.dirname(__file__), 'snd')
expl_dir = path.join(path.dirname(__file__), 'expl')
Bonus_dir = path.join(path.dirname(__file__), 'Bonus')
boss_dir = path.join(path.dirname(__file__), 'boss')
meteor_images = []

SH = 20

print(img_dir)
#переменные
WIDTH = 360
HEIGHT = 480
FPS = 50
score = 0
scorost = 4
#Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE= (0, 0, 255)

#создаем окно игры
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My game")
clock = pygame.time.Clock()

font_name = pygame.font.match_font("эria")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    if pct > 100:
        pct = 100
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100 * BAR_LENGTH)
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = (x, y,fill, BAR_HEIGHT)
    pygame.draw.rect(surf, RED, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 4 * i
        img_rect.y = y
        surf.blit(img, img_rect)

rs = ["Не поднимай красные квадраты",
      "7 ускорений = опыт",
      "Оффлайн!",
      "IdK",
      "Alt+f4 тоже сойдёт",
      "Cоветую не касаться метеоритов",
      "ORA!, 4 - плохо.",
      "Пробел - стрельба",
      "Чит-код: alt+f4",
      "Во время игры нажми windows+d",
      "Bites the dust!",
      "MUDA!",
      "Лазер рассекающий метеориты",
      "Невероятные приключения корабля",
      "Smertruss#4361",
      "Я что, похож на апельсина?",
      "Остерегайся всего!",
      "Поднимай бонусы!",
      "Нажмите ...",
      "(҂ `з´) ︻╦̵̵̿╤──"]

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Spase Bottle", 64, WIDTH / 2, HEIGHT / 12)
    draw_text(screen, "Нажми на любую клавишу", 23, WIDTH / 2, HEIGHT * 4 / 5)
    draw_text(screen, random.choice(rs), 22, WIDTH / 2, HEIGHT / 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
            if event.type == pygame.KEYUP:
               waiting = False

class Pow(pygame.sprite.Sprite):
    def __init__(self, center, type_bust):
        pygame.sprite.Sprite.__init__(self)
        self.type = type_bust
        self.type = random.choice(['shielda', 'gun', 'exp', 'hp', 'speed', 'vonuchca', 'mih'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 5

    def update(self):
        self.rect.y += self.speedy
        # убрать внизу экрана
        if self.rect.top > HEIGHT:
            self.kill()

def SHIELD(surf, x, y, SH):
    if SH < 0:
        SH = 0
    if SH > 100:
        SH = 100
    BARS_LENGTH = 100
    BARS_HEIGHT = 10
    fill = (SH / 100 * BARS_LENGTH)
    outline_rect = pygame.Rect(x, y, BARS_LENGTH, BARS_HEIGHT)
    fill_rect = (x, y,fill, BARS_HEIGHT)
    pygame.draw.rect(surf, BLUE, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_ng
        self.image = pygame.transform.scale(player_ng, (60, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2)
        self.power = 1
        self.power_time = pygame.time.get_ticks()

        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 20
        self.speed = 0
        self.shield = 100
        self.SHIELD = 20
        self.shoot_delay = 250
        self.last_shoot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
    def update(self):
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > 12000:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        self.speedx = 0
        keystate = pygame.key.get_pressed()

        if keystate[pygame.K_LEFT]:
            self.speedx = -scorost
        if keystate[pygame.K_RIGHT]:
            self.speedx = scorost
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        ##############################
        self.speedy = 0
        if keystate[pygame.K_UP]:
            self.speedy = -scorost
        if keystate[pygame.K_DOWN]:
            self.speedy = scorost
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 3500:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

    def shoot(self):
        if self.power == 1:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()
        if self.power == 2:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.right, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            bullets.add(bullet1)
            bullets.add(bullet2)
            shoot_sound.play()
        if self.power == 3:
            bullet1 = Bullet(self.rect.left +5, self.rect.centery)
            bullet2 = Bullet(self.rect.right -5, self.rect.centery)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery -10)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            shoot_sound.play()
        if self.power == 4:
            bullet1 = Bullet(self.rect.left +15, self.rect.centery -5)
            bullet2 = Bullet(self.rect.right -15, self.rect.centery -5)
            bullet3 = Bullet(self.rect.left, self.rect.centery +5)
            bullet4 = Bullet(self.rect.right, self.rect.centery +5)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            shoot_sound.play()
        if self.power == 5:
            bullet1 = Bullet(self.rect.left +15, self.rect.centery -5)
            bullet2 = Bullet(self.rect.right -15, self.rect.centery -5)
            bullet3 = Bullet(self.rect.left, self.rect.centery +5)
            bullet4 = Bullet(self.rect.right, self.rect.centery +5)
            bullet5 = Bullet(self.rect.centerx, self.rect.centery - 15)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            shoot_sound.play()
        if self.power == 6:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.left +15, self.rect.centery - 10)
            bullet3 = Bullet(self.rect.left +25, self.rect.centery -20)
            bullet4 = Bullet(self.rect.right, self.rect.centery)
            bullet5 = Bullet(self.rect.right -15, self.rect.centery - 10)
            bullet6 = Bullet(self.rect.right -25, self.rect.centery -20)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            shoot_sound.play()
        if self.power == 7:
            bullet1 = Bullet(self.rect.left, self.rect.centery)
            bullet2 = Bullet(self.rect.left +20, self.rect.centery - 15)
            bullet3 = Bullet(self.rect.left +45, self.rect.centery -50)
            bullet4 = Bullet(self.rect.right, self.rect.centery)
            bullet5 = Bullet(self.rect.right -20, self.rect.centery - 15)
            bullet6 = Bullet(self.rect.right -45, self.rect.centery -50)
            bullet7 = Bullet(self.rect.centerx, self.rect.centery)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            all_sprites.add(bullet7)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            bullets.add(bullet7)
            shoot_sound.play()
        if self.power == 8:
            bullet1 = Bullet(self.rect.centerx, self.rect.centery +110)
            bullet2 = Bullet(self.rect.centerx, self.rect.centery +95)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery +80)
            bullet4 = Bullet(self.rect.centerx, self.rect.centery +65)
            bullet5 = Bullet(self.rect.centerx, self.rect.centery +50)
            bullet6 = Bullet(self.rect.centerx, self.rect.centery +35)
            bullet7 = Bullet(self.rect.centerx, self.rect.centery +20)
            bullet8 = Bullet(self.rect.centerx, self.rect.centery +5)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            all_sprites.add(bullet7)
            all_sprites.add(bullet8)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            bullets.add(bullet7)
            bullets.add(bullet8)
            shoot_sound.play()
        if self.power == 9:
            bullet1 = Bullet(self.rect.centerx, self.rect.centery +110)
            bullet2 = Bullet(self.rect.centerx, self.rect.centery +95)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery +80)
            bullet4 = Bullet(self.rect.centerx, self.rect.centery +65)
            bullet5 = Bullet(self.rect.centerx, self.rect.centery +50)
            bullet6 = Bullet(self.rect.centerx, self.rect.centery +35)
            bullet7 = Bullet(self.rect.centerx, self.rect.centery +20)
            bullet8 = Bullet(self.rect.centerx, self.rect.centery +5)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            all_sprites.add(bullet7)
            all_sprites.add(bullet8)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            bullets.add(bullet7)
            bullets.add(bullet8)
            shoot_sound.play()
        if self.power >= 10:
            bullet1 = Bullet(self.rect.left, self.rect.centery +110)
            bullet2 = Bullet(self.rect.left, self.rect.centery +95)
            bullet3 = Bullet(self.rect.left, self.rect.centery +80)
            bullet4 = Bullet(self.rect.left, self.rect.centery +65)
            bullet5 = Bullet(self.rect.left, self.rect.centery +50)
            bullet6 = Bullet(self.rect.left, self.rect.centery +35)
            bullet7 = Bullet(self.rect.left, self.rect.centery +20)
            bullet8 = Bullet(self.rect.left, self.rect.centery +5)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            all_sprites.add(bullet7)
            all_sprites.add(bullet8)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            bullets.add(bullet7)
            bullets.add(bullet8)
            bullet9 = Bullet(self.rect.right, self.rect.centery + 95)
            bullet11 = Bullet(self.rect.right, self.rect.centery + 80)
            bullet12 = Bullet(self.rect.right, self.rect.centery + 65)
            bullet13 = Bullet(self.rect.right, self.rect.centery + 50)
            bullet14 = Bullet(self.rect.right, self.rect.centery + 20)
            bullet15 = Bullet(self.rect.right, self.rect.centery + 5)
            all_sprites.add(bullet9)
            all_sprites.add(bullet11)
            all_sprites.add(bullet12)
            all_sprites.add(bullet13)
            all_sprites.add(bullet14)
            all_sprites.add(bullet15)
            bullets.add(bullet9)
            bullets.add(bullet11)
            bullets.add(bullet12)
            bullets.add(bullet13)
            bullets.add(bullet14)
            bullets.add(bullet15)
            shoot_sound.play()
        if self.power >= 100 and player.lives == 100:
            bullet1 = Bullet(self.rect.centerx, self.rect.centery + 110)
            bullet2 = Bullet(self.rect.centerx, self.rect.centery + 95)
            bullet3 = Bullet(self.rect.centerx, self.rect.centery + 80)
            bullet4 = Bullet(self.rect.centerx, self.rect.centery + 65)
            bullet5 = Bullet(self.rect.centerx, self.rect.centery + 50)
            bullet6 = Bullet(self.rect.centerx, self.rect.centery + 35)
            bullet7 = Bullet(self.rect.centerx, self.rect.centery + 20)
            bullet8 = Bullet(self.rect.centerx, self.rect.centery + 5)
            all_sprites.add(bullet1)
            all_sprites.add(bullet2)
            all_sprites.add(bullet3)
            all_sprites.add(bullet4)
            all_sprites.add(bullet5)
            all_sprites.add(bullet6)
            all_sprites.add(bullet7)
            all_sprites.add(bullet8)
            bullets.add(bullet1)
            bullets.add(bullet2)
            bullets.add(bullet3)
            bullets.add(bullet4)
            bullets.add(bullet5)
            bullets.add(bullet6)
            bullets.add(bullet7)
            bullets.add(bullet8)
            bullet9 = Bullet(self.rect.centerx, self.rect.centery + 110)
            bullet10 = Bullet(self.rect.centerx, self.rect.centery + 95)
            bullet11 = Bullet(self.rect.centerx, self.rect.centery + 80)
            bullet12 = Bullet(self.rect.centerx, self.rect.centery + 65)
            bullet13 = Bullet(self.rect.centerx, self.rect.centery + 50)
            bullet14 = Bullet(self.rect.centerx, self.rect.centery + 35)
            bullet15 = Bullet(self.rect.centerx, self.rect.centery + 20)
            bullet16 = Bullet(self.rect.centerx, self.rect.centery + 5)
            all_sprites.add(bullet9)
            all_sprites.add(bullet10)
            all_sprites.add(bullet11)
            all_sprites.add(bullet12)
            all_sprites.add(bullet13)
            all_sprites.add(bullet14)
            all_sprites.add(bullet15)
            all_sprites.add(bullet16)
            bullets.add(bullet9)
            bullets.add(bullet10)
            bullets.add(bullet11)
            bullets.add(bullet12)
            bullets.add(bullet13)
            bullets.add(bullet14)
            bullets.add(bullet15)
            bullets.add(bullet16)

            shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hidden_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = one_boss
        self.image = pygame.transform.scale(one_boss, (100, 100))
        self.rect = self.image.get_rect()
        self.image.set_colorkey(BLACK)
        self.radius = int(self.rect.width * 0.85 / 2)
        # начальное положение
        self.rect.centerx = random.randint(60, WIDTH - 60)
        self.rect.centery = 80
        # Начальная скорость
        self.speedX = 3
        # Здоровье
        self.health = 20
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = 200

    def update(self):
        self.rect.x += self.speedX

        if self.rect.x + self.image.get_width() >= WIDTH or self.rect.x <= 0:
                self.speedX *= -1

        if self.health <= 0:
            self.rect.y = -200
            self.rect.x = -200
            self.kill()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = BulletBoss(self.rect.centerx, self.rect.bottom)
            all_sprites.add(bullet)
            bullet_boss_group.add(bullet)

class BulletBoss(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_laser
        self.image = pygame.transform.scale(boss_laser, (20, 70))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = 10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.kill()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 12)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-10, 10)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 10:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = laser
        self.image = pygame.transform.scale(laser, (10, 40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
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
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = expl_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "pew.wav"))
shoot_sound.set_volume(0.25)
expl_snd = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_snd.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
fon_Sound = pygame.mixer.Sound(path.join(snd_dir, "music.mp3"))
fon_Sound.set_volume(0.50)


#загрузике
background = pygame.image.load(path.join(img_dir, 'fon.jpg')).convert()
one_boss = pygame.image.load(path.join(boss_dir, 'one_boss.png')).convert()
two_boss = pygame.image.load(path.join(boss_dir, 'two_boss.png')).convert()
three_boss = pygame.image.load(path.join(boss_dir, 'three_boss.png')).convert()
boss_laser = pygame.image.load(path.join(boss_dir, 'boss_laser.png')).convert()

laser = pygame.image.load(path.join(img_dir, 'laser.png')).convert()
meteor = pygame.image.load(path.join(img_dir, 'meteor.png')).convert()
player_ng = pygame.image.load(path.join(img_dir, 'player.png')).convert()
player_mini_img = pygame.image.load(path.join(img_dir, 'playerLife2_red.png')).convert()
player_mini_img.set_colorkey(BLACK)

meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_big3.png', 'meteorBrown_big4.png', 'meteorBrown_med1.png', 'meteorBrown_med3.png', 'meteorBrown_small1.png', 'meteorGrey_big1.png', 'meteorGrey_big2.png', 'meteorGrey_big4.png', 'meteorGrey_med1.png', 'meteorGrey_small1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(mrt_dir, img)).convert())

powerup_images = {}
powerup_images['gun'] = pygame.image.load(path.join(Bonus_dir, 'gun.png')).convert()
powerup_images['exp'] = pygame.image.load(path.join(Bonus_dir, 'exp.png')).convert()
powerup_images['speed'] = pygame.image.load(path.join(Bonus_dir, 'speed.png')).convert()
powerup_images['hp'] = pygame.image.load(path.join(Bonus_dir, 'hp.png')).convert()
powerup_images['shielda'] = pygame.image.load(path.join(Bonus_dir, 'shielda.png')).convert()
powerup_images['vonuchca'] = pygame.image.load(path.join(Bonus_dir, 'vonuchca.png')).convert()
powerup_images['mih'] = pygame.image.load(path.join(Bonus_dir, 'mih.png')).convert()
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(expl_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    expl_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    expl_anim['sm'].append(img_sm)
    img_player = pygame.transform.scale(img, (100, 100))
    expl_anim['player'].append(img_player)

background_rect = background.get_rect()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#создаем мобов
mobs = pygame.sprite.Group()
#cоздаем группу пуль
bullets = pygame.sprite.Group()
bullet_boss_group = pygame.sprite.Group()
for i in range(8):
    newmob()
pows = pygame.sprite.Group()
#цикл игры
def player_win():
    screen.blit(background, background_rect)
    draw_text(screen, "Ты выпил воду из космической бутылки", 24, WIDTH/2, HEIGHT/4)
    draw_text(screen, "Хочешь ещё воды?", 37, WIDTH/2, HEIGHT/2)
    pygame. display.flip()
    waiting = True
    time.sleep(1)
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               pygame.quit()
            if event.type == pygame.KEYUP:
               waiting = False
running = True
boss_spawn = False
boss_start = True
death_diavolo = 1
game_over = True
fon_Sound.play(loops=-1)
win = False
while running:
    death_diavolo += 1
    print(f"Смерть Дьяволо №{death_diavolo}")
    if win:
        win = False
        player_win()
        all_sprites = pygame.sprite.Group()
        mobs = pygame.sprite.Group()
        pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        pows = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newmob()
        score = 0
    if game_over:

        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        # создаем мобов
        mobs = pygame.sprite.Group()
        # cоздаем группу пуль
        bullets = pygame.sprite.Group()
        for i in range(8):
            newmob()
        pows = pygame.sprite.Group()
        score = 0
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    #обновление
    all_sprites.update()
    #проверка столкновения игрока и моба
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)

    for hit in hits:
        if player.power > 1:
            player.lives - 3
        player.SHIELD -= hit.radius
        newmob()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.SHIELD <= 0:
            player.shield -= hit.radius
            if player.shield <= 0:
                death_expl = Explosion(player.rect.center, 'player')
                all_sprites.add(death_expl)
                player.hide()
                player.lives -= 1
                player.shield = 100
    if player.lives == 0 and not death_expl.alive():
        print(score)
        game_over = True
#    if score > 10:
#        win = false

    if score % 10000 == 0 and boss_start:
        boss = Boss()
        all_sprites.add(boss)
        boss_start = False
        boss_spawn = True
    if boss_spawn:
        boss.shoot()
        # соударение пульс и босса
        hits = pygame.sprite.spritecollide(boss, bullets, True, pygame.sprite.collide_circle)
        for hit in hits:
            boss.health -= 1
            if boss.health <= 0:
                boss_spawn = False
                score += 1000
    hits = pygame.sprite.spritecollide(player, bullet_boss_group, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= 10
        newmob()
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        if player.shield <= 0:
            player.health -= 10
            if player.health <= 0:
                death_expl = Explosion(player.rect.center, 'player')
                all_sprites.add(death_expl)
                player.hide()
                player.lives -= 1
                player.health = 100
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        sndBuz = random.choice(expl_snd)
        sndBuz.set_volume(0.5)
        sndBuz.play()
        newmob()
        score += 10
        random.choice(expl_snd).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.980:
            pow = Pow(hit.rect.center, 'shielda')
            all_sprites.add(pow)
            pows.add(pow)
        if random.random() > 0.987:
            pow = Pow(hit.rect.center, 'gun')
            all_sprites.add(pow)
            pows.add(pow)
        if random.random() > 0.980:
            pow = Pow(hit.rect.center, 'exp')
            all_sprites.add(pow)
            pows.add(pow)
        if random.random() > 0.988:
            pow = Pow(hit.rect.center, 'speed')
            all_sprites.add(pow)
            pows.add(pow)
        if random.random() > 0.988:
            pow = Pow(hit.rect.center, 'vonuchca')
            all_sprites.add(pow)
            pows.add(pow)
        if random.random() > 0.981:
            pow = Pow(hit.rect.center, 'mih')
            all_sprites.add(pow)
            pows.add(pow)

    hits = pygame.sprite.spritecollide(player, pows, True)
    for hit in hits:
        if hit.type == 'shielda':
            player.SHIELD += 40
            if player.SHIELD >= 100:
                player.SHIELD = 100
        if hit.type == 'gun':
            player.powerup()
        if hit.type == 'exp':
            score += 2000
        if hit.type == 'hp':
            player.shield += 40
        if hit.type == 'speed':
            player.lives += 1
        if hit.type == 'vonuchca':
            SHIELD == 50
            player.shield == 0
            player.powerup == 1
            if player.lives >= 3:
                player.lives = 1
            else:
                player.lives = 3
        if hit.type == 'mih':
            scorost += 1
            if scorost == 7:
              scorost = 4
              score += 2500

    #Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 35, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    SHIELD(screen, 5, 15, player.SHIELD)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    pygame.display.set_caption(f"Score: {score}, powergun: {player.power}, lives: {player.lives}, speed: {scorost}")
    #Отрисовка
    pygame.display.flip()

pygame.display.set_mode((WIDTH, HEIGHT))

pygame.quit()
























