from settings import  *
from timer import Timer
from math import sin
from random import randint

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image =  surf
        self.rect = self.image.get_rect(topleft = pos)

class Bullet(Sprite):
    def __init__(self, surf, pos, direction, groups):
        super().__init__(pos, surf, groups)

        # adjustment
        self.image = pygame.transform.flip(self.image, direction == -1, False)

        # movement
        self.direction = direction
        self.speed = 850

    def update(self, dt):
        self.rect.x += self.direction * self.speed * dt

class Fire(Sprite):
    def __init__(self, surf, pos, groups, player):
        super().__init__(pos, surf, groups)
        self.player = player
        self.flip = player.flip
        self.timer = Timer(100, autostart=True, func=self.kill)
        self.y_offset = pygame.Vector2(0,8)

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect.midright = self.player.rect.midright + self.y_offset

    def update(self, dt):
        self.timer.update()

        if self.player.flip:
            self.rect.midright = self.player.rect.midleft + self.y_offset
        else:
            self.rect.midleft = self.player.rect.midright + self.y_offset

        if self.flip != self.player.flip:
            self.kill()

class AnimatedSprite(Sprite):
    def __init__(self, frames, pos, groups):
        self.frames, self.frame_index, self.animation_speed = frames, 0, 10
        super().__init__(pos, self.frames[self.frame_index], groups)

    def animate(self, dt):
        self.frame_index += self.animation_speed * dt
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

class Enemy(AnimatedSprite):
    def __init__(self, frames, pos, groups):
        super().__init__(frames, pos, groups)
        self.death_timer = Timer(200, func=self.kill)

    def destroy(self):
        self.death_timer.activate()
        self.animation_speed = 0
        self.image = pygame.mask.from_surface(self.image).to_surface()
        self.image.set_colorkey('black')

    def update(self, dt):
        self.death_timer.update()
        if not self.death_timer:
            self.move(dt)
            self.animate(dt)
        self.constraint()

class Bee(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(160,200)
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if self.rect.left < self.main_rect.left:
            self.rect.left = self.main_rect.left
            self.direction = 1
            self.frames = [pygame.transform.flip(surf, False, False) for surf in self.frames]

        if self.rect.right > self.main_rect.right:
            self.rect.right = self.main_rect.right
            self.direction = -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]

class Worm(Enemy):
    def __init__(self, frames, rect, groups):
        super().__init__(frames, rect.topleft, groups)
        self.rect.bottomleft = rect.bottomleft
        self.main_rect = rect
        self.speed = randint(160,200)
        self.direction = 1

    def move(self, dt):
        self.rect.x += self.direction * self.speed * dt

    def constraint(self):
        if self.rect.left < self.main_rect.left:
            self.rect.left = self.main_rect.left
            self.direction = 1
            self.frames = [pygame.transform.flip(surf, False, False) for surf in self.frames]

        if self.rect.right > self.main_rect.right:
            self.rect.right = self.main_rect.right
            self.direction = -1
            self.frames = [pygame.transform.flip(surf, True, False) for surf in self.frames]

class Player(AnimatedSprite):
    def __init__(self, pos, groups, collision_sprites, frames, create_bullet):
        super().__init__(frames, pos, groups)
        self.flip = False
        self.create_bullet = create_bullet

        # movement & collision
        self.direction = pygame.Vector2()
        self.collision_sprites = collision_sprites
        self.speed = 400
        self.gravity = 50
        self.on_floor = False

        # timer
        self.shoot_timer = Timer(500)

    def input(self):
        keys = pygame.key.get_pressed()
        # moving keys
        self.direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        # jumping keys
        if keys[pygame.K_w] and self.on_floor:
            self.direction.y = -20

        if keys[pygame.K_SPACE] and not self.shoot_timer:
            self.create_bullet(self.rect.center, -1 if self.flip else 1)
            self.shoot_timer.activate()

    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical
        self.direction.y += self.gravity * dt
        self.rect.y += self.direction.y
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.direction.x > 0: self.rect.right = sprite.rect.left
                    if self.direction.x < 0: self.rect.left = sprite.rect.right
                if direction == 'vertical':
                    if self.direction.y > 0: self.rect.bottom = sprite.rect.top
                    if self.direction.y < 0: self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

    def check_floor(self):
        bottom_rect = pygame.Rect(self.rect.left,
                                  self.rect.bottom,
                                  self.rect.width,
                                  2)
        self.on_floor = bottom_rect.collidelist(
            [sprite.rect for sprite in self.collision_sprites]
        ) >= 0

    def animate(self, dt):
        if self.direction.x:
            self.frame_index += self.animation_speed * dt
            self.flip = self.direction.x < 0
        else:
            self.frame_index = 0

        self.frame_index = 1 if not self.on_floor else self.frame_index
        self.image = self.frames[int(self.frame_index) % len(self.frames)]
        self.image = pygame.transform.flip(self.image, self.flip, False)

    def update(self, dt):
        self.shoot_timer.update()
        self.check_floor()
        self.input()
        self.move(dt)
        self.animate(dt)

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, value=1, *groups):
        super().__init__(*groups)
        self.image = pygame.Surface((w,h))
        self.image.fill((255,223,0))
        self.rect = pygame.Rect(x,y,w,h)
        self.value = value

class CollisionTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, removable, *groups, group_id=None):
        super().__init__(*groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.removable = removable
        self.group_id = group_id
