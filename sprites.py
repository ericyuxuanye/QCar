import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)
import random

class Car(pygame.sprite.Sprite):
    def __init__(self):
        super(Car, self).__init__()
        self.normal = pygame.image.load("car.png").convert_alpha()
        self.left = pygame.transform.rotate(self.normal, 30)
        self.right = pygame.transform.rotate(self.normal, -30)
        self.surf = self.normal
        self.rect = self.surf.get_rect(center=(400, 450))
        self.mask = pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys, restrict_left, restrict_right):
        if pressed_keys[K_LEFT] and not pressed_keys[K_RIGHT] and not restrict_left:
            self.rect.move_ip(-5, 0)
            self.surf = self.left
        elif pressed_keys[K_RIGHT] and not pressed_keys[K_LEFT] and not restrict_right:
            self.rect.move_ip(5, 0)
            self.surf = self.right
        else:
            self.surf = self.normal
        self.rect = self.surf.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.surf)


class TrafficConePair(pygame.sprite.Sprite):
    speed = 10
    cone_dist = 200
    width = cone_dist + 100
    def __init__(self, y):
        super(TrafficConePair, self).__init__()
        self.surf = pygame.Surface((TrafficConePair.width, 50), pygame.SRCALPHA)
        self.image = pygame.image.load("traffic_cone.png").convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        self.surf.blit(self.image, (0, 0))
        self.surf.blit(self.image, (TrafficConePair.cone_dist + 50, 0))
        self.rect = self.surf.get_rect(topleft=(400 - self.width / 2, y))
        self.mask = pygame.mask.from_surface(self.surf)

    def update(self):
        self.rect = self.rect.move(0, TrafficConePair.speed)
    
    def out_of_bounds(self):
        return self.rect.top > 600

    def reload(self, prev_x):
        new_x = prev_x + random.randint(-100, 100)
        new_x = max(new_x, 0)
        new_x = min(new_x, 800 - TrafficConePair.width)
        self.rect = pygame.Rect(new_x, -100, TrafficConePair.width, 50)