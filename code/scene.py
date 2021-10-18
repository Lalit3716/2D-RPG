import pygame
from tiles import StaticTile
from player import Player
from utils import YSort
from settings import tile_size, scale, WINDOW_WIDTH, WINDOW_HEIGHT
from helpers import import_sprite_sheet, import_character


class Scene:
    def __init__(self, level, camera):
        # Basic
        scene_width = len(level["data"]["Floor"][0]) * tile_size
        scene_height = len(level["data"]["Floor"]) * tile_size
        self.display_surface = pygame.Surface((scene_width, scene_height))
        self.level_data = level["data"]
        self.level_resources = level["resources"]

        # Sprite Groups
        self.floor = pygame.sprite.Group()
        self.static_tiles = pygame.sprite.Group()

        # Importing and Creating Level
        self.import_level_resources()
        self.create_level()

        # Y-Sort
        self.y_sort = YSort(self.static_tiles, self.player)

        # Collisions+Camera
        self.camera = camera
        self.collidable_sprites = list(filter(lambda s: s.collideable, self.static_tiles.sprites()))
        self.collided_x = False
        self.collided_y = False

    def import_level_resources(self):
        for key, path in self.level_resources.items():
            if key != "player":
                loaded_sheet = import_sprite_sheet(path, (16, 16), scale)
                setattr(self, key, loaded_sheet)
            elif key == "player":
                self.player_sprites = import_character(path, scale=2.2)

    def create_level(self):
        for key, layout in self.level_data.items():
            for row_index, row in enumerate(layout):
                for col_index, cell in enumerate(row):
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if cell != "-1":
                        if key == "Floor":
                            surface = self.floor_tileset[int(cell)]
                            self.floor.add(StaticTile(x, y, surface))

                        elif key == "House":
                            surface = self.house_tileset[int(cell)]
                            if surface.get_at((surface.get_width()//2, surface.get_height()//2))[2] == 0:
                                self.static_tiles.add(StaticTile(x, y, surface, collideable=False))
                            else:
                                self.static_tiles.add(StaticTile(x, y, surface))

                        elif key == "CollidableNature":
                            surface = self.nature_tileset[int(cell)]
                            if surface.get_at((surface.get_width()//2, surface.get_height()//2))[2] == 0:
                                self.static_tiles.add(StaticTile(x, y, surface, collideable=False))
                            else:
                                self.static_tiles.add(StaticTile(x, y, surface))

                        elif key == "NonCollidableNature":
                            surface = self.nature_tileset[int(cell)]
                            self.static_tiles.add(StaticTile(x, y, surface, collideable=False))

                        elif key == "Character":
                            if cell == "1":
                                player_x = WINDOW_WIDTH // 2
                                player_y = WINDOW_HEIGHT // 2
                                self.player = pygame.sprite.GroupSingle(Player(player_x, player_y, self.player_sprites, self.display_surface))

    def horizontal_collisions(self):
        player = self.player.sprite
        for sprite in self.collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                print("Collided")

    def vertical_collisions(self):
        player = self.player.sprite
        for sprite in self.collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                print("Collided")

    def scroll_world(self):
        player = self.player.sprite
        if not self.collided_x:
            self.camera.x += player.direction.x * player.speed
            player.rect.x += int(player.direction.x * player.speed)
        if not self.collided_y:
            self.camera.y += player.direction.y * player.speed
            player.rect.y += int(player.direction.y * player.speed)

    # Debug
    def draw_rects(self):
        sprites = [self.player.sprite] + self.static_tiles.sprites()
        for sprite in sprites:
            pygame.draw.rect(self.display_surface, (0, 0, 0), sprite.rect, 2)

    def run(self):
        self.horizontal_collisions()
        self.vertical_collisions()
        self.scroll_world()

        # Background
        self.floor.draw(self.display_surface)

        # Player
        self.player.update()

        # Draw In Y-Sort
        self.y_sort.draw_groups(self.display_surface)

        # Debugging
        # self.draw_rects()

        return self.display_surface
