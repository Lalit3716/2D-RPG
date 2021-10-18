import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, sprites, display_surface):
        super().__init__()
        # Animation And Positing
        self.display_surface = display_surface
        self.pos = pygame.math.Vector2(x, y)
        self.animations = sprites
        self.state = "Idle"
        self.facing = "Down"
        self.frame_index = 0
        self.image = self.animations[self.state][self.facing]
        self.rect = self.image.get_rect(center=self.pos)
        self.shadow = self.animations["shadow"]
        self.shadow_rect = self.rect

        # Movements
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 4

    def animate(self, speed=0.1):
        if self.state == "Walk":
            self.frame_index += speed
            if self.frame_index >= len(self.animations[self.state][self.facing]):
                self.frame_index = 0
            self.image = self.animations[self.state][self.facing][int(self.frame_index)]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            self.shadow_rect.topleft = self.rect.bottomleft + pygame.math.Vector2(5, -6)

        elif self.state == "Idle":
            self.image = self.animations["Idle"][self.facing]
            self.rect = self.image.get_rect(topleft=self.rect.topleft)
            self.shadow_rect.topleft = self.rect.bottomleft + pygame.math.Vector2(5, -6)

    def get_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.direction.y = 0
            self.state = "Walk"
        elif keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.direction.y = 0
            self.state = "Walk"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.direction.x = 0
            self.state = "Walk"
        elif keys[pygame.K_UP]:
            self.direction.y = -1
            self.direction.x = 0
            self.state = "Walk"
        else:
            self.direction = pygame.math.Vector2(0, 0)
            self.state = "Idle"

    def get_state(self):
        if self.direction.x > 0:
            self.facing = "Right"
        elif self.direction.x < 0:
            self.facing = "Left"
        elif self.direction.y > 0:
            self.facing = "Down"
        elif self.direction.y < 0:
            self.facing = "Up"

    def draw_shadow(self):
        self.display_surface.blit(self.shadow, self.shadow_rect)

    def update(self):
        # Movements and States
        self.get_input()
        self.get_state()

        # Animate+Shadow
        self.animate()
        self.draw_shadow()
