from settings import *
from sprites import *
from groups import AllSprites
from support import *
from timer import Timer
from random import randint
from pytmx import load_pygame
from os.path import join

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Jumper's Odyssey")
        self.clock = pygame.time.Clock()
        self.running = True
        PLAY_IMPACT_SOUND = pygame.USEREVENT + 1

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.bullet_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.item_sprites = pygame.sprite.Group()
        self.drzwi1_sprites = pygame.sprite.Group()
        self.drzwi2_sprites = pygame.sprite.Group()
        self.drzwi3_sprites = pygame.sprite.Group()
        self.drzwi4_sprites = pygame.sprite.Group()
        self.drzwi5_sprites = pygame.sprite.Group()

        # load game
        self.load_assets()
        self.setup()

    def create_bullet(self, pos, direction):
        x = pos[0] + direction * 34 if direction == 1 else pos[0] + direction * 34 - self.bullet_surf.get_width()
        Bullet(self.bullet_surf, (x, pos[1]), direction, (self.all_sprites, self.bullet_sprites))
        Fire(self.fire_surf, pos, self.all_sprites, self.player)
        self.audio['shoot'].play().set_volume(0.2)

    def load_assets(self):
        # graphics
        self.player_frames = import_folder('..', 'images', 'player')
        self.bullet_surf = import_image('..', 'images', 'gun', 'bullet')
        self.fire_surf = import_image('..', 'images', 'gun', 'fire')
        self.bee_frames = import_folder('..', 'images', 'enemies', 'bee')
        self.worm_frames = import_folder('..', 'images', 'enemies', 'worm')

        # sounds
        self.audio = audio_importer('..', 'audio')
        print("Wczytane dźwięki:", list(self.audio.keys()))

    def setup(self):
        self.audio['music'].play(loops = -1).set_volume(0.2)

        base_dir = dirname(__file__)
        tmx_path = join(base_dir, '..', 'data', 'maps', 'mapa.tmx')
        tmx_map = load_pygame(tmx_path)
        self.level_width = tmx_map.width * TILE_SIZE
        self.level_height = tmx_map.height * TILE_SIZE

        try:
            drzwi_layer1 = tmx_map.get_layer_by_name('drzwi1')
        except Exception:
            drzwi_layer1 = None

        if drzwi_layer1:
            for x, y, image in drzwi_layer1.tiles():
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE

                CollisionTile((pixel_x, pixel_y), image, True,
                              self.all_sprites, self.collision_sprites,
                              group_id='drzwi1'
                              )

        try:
            drzwi_layer2 = tmx_map.get_layer_by_name('drzwi2')
        except Exception:
            drzwi_layer2 = None

        if drzwi_layer2:
            for x, y, image in drzwi_layer2.tiles():
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE

                CollisionTile((pixel_x, pixel_y), image, True,
                              self.all_sprites, self.collision_sprites,
                              group_id='drzwi2'
                              )

        try:
            drzwi_layer3 = tmx_map.get_layer_by_name('drzwi3')
        except Exception:
            drzwi_layer3 = None

        if drzwi_layer3:
            for x, y, image in drzwi_layer3.tiles():
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE

                CollisionTile((pixel_x, pixel_y), image, True,
                              self.all_sprites, self.collision_sprites,
                              group_id='drzwi3'
                              )

        try:
            drzwi_layer4 = tmx_map.get_layer_by_name('drzwi4')
        except Exception:
            drzwi_layer4 = None

        if drzwi_layer4:
            for x, y, image in drzwi_layer4.tiles():
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE

                CollisionTile((pixel_x, pixel_y), image, True,
                              self.all_sprites, self.collision_sprites,
                              group_id='drzwi4'
                              )

        try:
            drzwi_layer5 = tmx_map.get_layer_by_name('drzwi5')
        except Exception:
            drzwi_layer5 = None

        if drzwi_layer5:
            for x, y, image in drzwi_layer5.tiles():
                pixel_x = x * TILE_SIZE
                pixel_y = y * TILE_SIZE

                CollisionTile((pixel_x, pixel_y), image, True,
                              self.all_sprites, self.collision_sprites,
                              group_id='drzwi5'
                              )

        try:
            items_layer = tmx_map.get_layer_by_name('itemy')
        except Exception:
            items_layer = None

        if items_layer:
            for obj in items_layer:
                if obj.properties.get('item', False):
                    x, y = int(obj.x), int(obj.y)
                    w, h = int(obj.width), int(obj.height)
                    value = obj.properties.get('value', 1)
                    Item(x, y, w, h, value,
                         self.all_sprites, self.item_sprites)

        for x, y, image in tmx_map.get_layer_by_name('baza').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites, self.collision_sprites))

        for x, y, image in tmx_map.get_layer_by_name('dekoracja').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image, (self.all_sprites))

        for x, y, image in tmx_map.get_layer_by_name('drzwi1').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
                   (self.all_sprites, self.drzwi1_sprites))

        for x, y, image in tmx_map.get_layer_by_name('drzwi2').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
                   (self.all_sprites, self.drzwi2_sprites))

        for x, y, image in tmx_map.get_layer_by_name('drzwi3').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
                   (self.all_sprites, self.drzwi3_sprites))

        for x, y, image in tmx_map.get_layer_by_name('drzwi4').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
                   (self.all_sprites, self.drzwi4_sprites))

        for x, y, image in tmx_map.get_layer_by_name('drzwi5').tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), image,
                   (self.all_sprites, self.drzwi5_sprites))

        for obj in tmx_map.get_layer_by_name('przeciwnicy'):
            if obj.name == 'gracz':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites, self.player_frames, self.create_bullet)

            if obj.name == 'robak':
                Worm(self.worm_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

            if obj.name == 'pszczola':
                Bee(self.bee_frames, pygame.FRect(obj.x, obj.y, obj.width, obj.height), (self.all_sprites, self.enemy_sprites))

        self.collected_count = 0

    def collision(self):
        # bullet -> enemies
        for bullet in self.bullet_sprites:
            sprite_collisions = pygame.sprite.spritecollide(bullet, self.enemy_sprites, False, pygame.sprite.collide_mask)
            if sprite_collisions:
                self.audio['impact'].play()
                bullet.kill()
                for sprite in sprite_collisions:
                    sprite.destroy()

        # bullet -> surface
        for bullet in self.bullet_sprites:
            sprite_collisions_surface = pygame.sprite.spritecollide(bullet, self.collision_sprites, False)
            if sprite_collisions_surface:
                self.audio['impact'].play()
                bullet.kill()


        # enemies -> player
        if pygame.sprite.spritecollide(self.player, self.enemy_sprites, False, pygame.sprite.collide_mask):
            self.running = False

        item_hits = pygame.sprite.spritecollide(
            self.player, self.item_sprites, dokill=True
        )
        if item_hits:
            for item in item_hits:
                self.collected_count += item.value
                self.audio['impact'].play().set_volume(0.2)
                print("Collected:", self.collected_count)

            if self.collected_count >= 1:
                for col in self.collision_sprites:
                    if getattr(col, 'removable', False) and getattr(col, 'group_id', None) == 'drzwi1':
                        col.kill()
                for door in self.drzwi1_sprites.sprites():
                    door.kill()

            if self.collected_count >= 5:
                for col in self.collision_sprites:
                    if getattr(col, 'removable', False) and getattr(col, 'group_id', None) == 'drzwi2':
                        col.kill()
                for door in self.drzwi2_sprites.sprites():
                    door.kill()

            if self.collected_count >= 7:
                for col in self.collision_sprites:
                    if getattr(col, 'removable', False) and getattr(col, 'group_id', None) == 'drzwi3':
                        col.kill()
                for door in self.drzwi3_sprites.sprites():
                    door.kill()

            if self.collected_count >= 9:
                for col in self.collision_sprites:
                    if getattr(col, 'removable', False) and getattr(col, 'group_id', None) == 'drzwi4':
                        col.kill()
                for door in self.drzwi4_sprites.sprites():
                    door.kill()

            if self.collected_count >= 15:
                for col in self.collision_sprites:
                    if getattr(col, 'removable', False) and getattr(col, 'group_id', None) == 'drzwi5':
                        col.kill()
                for door in self.drzwi5_sprites.sprites():
                    door.kill()


    def run(self):
        while self.running:
            dt = self.clock.tick(FRAMERATE) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False

            # update
            self.all_sprites.update(dt)
            self.collision()

            #draw
            self.display_surface.fill(BG_COLOR)
            self.all_sprites.draw(self.player.rect.center)

            offset_x = self.player.rect.centerx - WINDOW_WIDTH // 2
            offset_y = self.player.rect.centery - WINDOW_HEIGHT // 2

            for item in self.item_sprites:
                screen_x = item.rect.x - offset_x
                screen_y = item.rect.y - offset_y
                self.display_surface.blit(item.image, (screen_x, screen_y))



            pygame.display.update()

        pygame.quit()

if __name__ == '__main__':
    game = Game()
    game.run()
