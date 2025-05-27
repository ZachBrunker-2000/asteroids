# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from Player import *

def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    Player.containers = (updatable,drawable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
    
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
            
        screen.fill((0,0,0))
        
        updatable.update(dt)
        for draw in drawable:
            draw.draw(screen)
        
        clock.tick(60)
        dt = clock.tick(60)/1000
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main()