import pygame


class YSort:
    def __init__(self, *groups):
        self.all_sprites = []
        for group in groups:
            if isinstance(group, pygame.sprite.Group):
                for sprite in group.sprites():
                    self.all_sprites.append(sprite)
            elif isinstance(group, pygame.sprite.GroupSingle):
                self.all_sprites.append(group.sprite)

    def add_group(self, group):
        if isinstance(group, pygame.sprite.Group):
            self.all_sprites.extend(group.sprites())
        elif isinstance(group, pygame.sprite.GroupSingle):
            self.all_sprites.append(group.sprite)

    def draw_groups(self, surface):
        for sprite in sorted(self.all_sprites, key=lambda s: s.rect.y):
            surface.blit(sprite.image, sprite.rect)
