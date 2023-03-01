import pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
)
from sprites import Car, TrafficConePair

from model import Model

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
HUMAN = False

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

if not HUMAN:
    model = Model()

done = False

car = Car()
traffic_cones = pygame.sprite.Group()
for i in range(-100, SCREEN_HEIGHT, 100):
    traffic_cones.add(TrafficConePair(i))

clock = pygame.time.Clock()

last_cone = len(traffic_cones.sprites()) - 1

x = 10
y = 10


def action_to_key(action):
    if action == 0:
        return {K_LEFT: True, K_RIGHT: False}
    elif action == 1:
        return {K_LEFT: False, K_RIGHT: True}
    return {K_LEFT: False, K_RIGHT: False}


counter = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    collided_cone = pygame.sprite.spritecollideany(
        car, traffic_cones, pygame.sprite.collide_mask
    )

    if HUMAN:
        pressed = pygame.key.get_pressed()
    else:
        if counter % 10 == 0:
            car_cone1 = (
                last_cone - 1
                if last_cone > 0
                else len(traffic_cones.sprites()) - 1 + last_cone
            )
            car_cone2 = (
                last_cone - 2
                if last_cone > 1
                else len(traffic_cones.sprites()) - 2 + last_cone
            )
            car_cone3 = (
                last_cone - 3
                if last_cone > 2
                else len(traffic_cones.sprites()) - 3 + last_cone
            )
            model.update(-1 if collided_cone else 2)
            action = model.get_action(
                car.rect.left - (traffic_cones.sprites()[car_cone1].rect.left + 50),
                car.rect.left - (traffic_cones.sprites()[car_cone2].rect.left + 50),
                car.rect.left - (traffic_cones.sprites()[car_cone3].rect.left + 50),
            )
            pressed = action_to_key(action)

    restrict_left = False
    restrict_right = False
    if collided_cone:
        if car.rect.centerx < collided_cone.rect.centerx:
            restrict_left = True
        else:
            restrict_right = True

    car.update(pressed, restrict_left, restrict_right)

    screen.fill((128, 128, 128))
    for cone in traffic_cones:
        screen.blit(cone.surf, cone.rect)
    screen.blit(car.surf, car.rect)
    pygame.display.flip()
    if not collided_cone:
        for cone in traffic_cones:
            cone.update()
        if traffic_cones.sprites()[last_cone].out_of_bounds():
            first_cone = (
                last_cone + 1 if last_cone < len(traffic_cones.sprites()) - 1 else 0
            )
            traffic_cones.sprites()[last_cone].reload(
                traffic_cones.sprites()[first_cone].rect.x
            )
            last_cone = (
                last_cone - 1 if last_cone > 0 else len(traffic_cones.sprites()) - 1
            )

    clock.tick(60)
    counter += 1


if not HUMAN:
    model.save_qtable()
pygame.quit()
