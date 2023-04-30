from pygame import *

init()
mixer.init()
font.init()
game = True
info = display.Info()
WIDTH = info.current_w
HEIGHT = info.current_h

FPS = 60


window = display.set_mode((WIDTH, HEIGHT))
background = transform.scale(image.load("image/background.jpg"), (WIDTH, HEIGHT))
clock = time.Clock()
mixer.music.load("Sound/jungles.ogg")
mixer.music.set_volume(0.3)
mixer.music.play()

money = mixer.Sound("Sound/jungles.ogg")
money.set_volume(0.3)

hit = mixer.Sound("Sound/kick.ogg")
hit.set_volume(0.3)

font_finish = font.Font(None, HEIGHT // 4)
win_text = font_finish.render("You WIN!", True, (208, 234, 100))
lose_text = font_finish.render("You LOSE!", True, (233, 74, 67))

class GameSprite(sprite.Sprite):
    def __init__(self, sprite_image, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(sprite_image), (HEIGHT // 8, HEIGHT // 8))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < HEIGHT - self.rect.height:
            self.rect.y += self.speed
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed


class Enemy(GameSprite):
    def __init__(self, sprite_image, x, y, speed, left_x, right_x):
        super().__init__(sprite_image, x, y, speed)
        self.right_x = right_x
        self.left_x = left_x
        self.direction = "left"

    def update(self):
        if self.rect.x > self.right_x:
            self.direction = "left"
        if self.rect.x < self.left_x:
            self.direction = "right"

        if self.direction == "left":
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed


class Wall(sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.color = (150,200,100)
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


player = Player("image/hero.png", WIDTH // 10, HEIGHT - HEIGHT // 4, HEIGHT // 80)
monster_right = Enemy("image/cyborg.png", WIDTH - WIDTH // 6, HEIGHT - HEIGHT // 2, HEIGHT // 90,
                      WIDTH - WIDTH // 3, WIDTH - WIDTH // 8)
monster_top = Enemy("image/cyborg.png", WIDTH // 3, HEIGHT // 12, HEIGHT // 90,
                    WIDTH // 5, WIDTH // 2.5)
monster_bottom = Enemy("image/cyborg.png", WIDTH // 2.5, HEIGHT - HEIGHT // 4, HEIGHT // 90,
                      WIDTH // 3, WIDTH // 1.7)
treasure = GameSprite("image/treasure.png", WIDTH - WIDTH // 6, HEIGHT - HEIGHT // 4, 0)

wall_width = HEIGHT // 50

wall_1 = Wall(WIDTH // 5, HEIGHT // 3, wall_width, int(HEIGHT // 1.5))
wall_2 = Wall(WIDTH // 2.85, 3, wall_width, int(HEIGHT // 1.5))
wall_3 = Wall(WIDTH // 2, HEIGHT // 3, wall_width, int(HEIGHT // 1.5))
wall_4 = Wall(WIDTH - WIDTH // 3, 0, wall_width, int(HEIGHT // 1.5))
wall_5 = Wall(WIDTH - WIDTH // 5, HEIGHT // 3, wall_width, int(HEIGHT // 1.5))

finish = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            if e.key == K_r:
                finish = False
                player.rect.x = WIDTH // 10
                player.rect.y = HEIGHT - HEIGHT // 4

    if not finish:
        window.blit(background, (0, 0))

        player.update()
        player.reset()

        wall_1.reset()
        wall_2.reset()
        wall_3.reset()
        wall_4.reset()
        wall_5.reset()

        monster_right.update()
        monster_right.reset()

        monster_top.update()
        monster_top.reset()

        monster_bottom.update()
        monster_bottom.reset()
        treasure.reset()

        if sprite.collide_rect(player, treasure):
            money.play()
            window.blit(win_text, (WIDTH // 3.4, HEIGHT // 2.6))
            finish = True

        if (sprite.collide_rect(player,monster_right)
                or sprite.collide_rect(player, monster_top)
                or sprite.collide_rect(player,monster_bottom)
                or sprite.collide_rect(player, wall_1)
                or sprite.collide_rect(player, wall_2)
                or sprite.collide_rect(player, wall_3)
                or sprite.collide_rect(player, wall_4)
                or sprite.collide_rect(player, wall_5)):
            hit.play()
            window.blit(lose_text, (WIDTH // 3.4, HEIGHT // 2.6))
            finish = True

    display.update()
    clock.tick(FPS)