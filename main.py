# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
from constants import *
from Player import *
from asteroid import *
from asteroidfield import *

def size_score(asteroid):
    if asteroid.radius <= ASTEROID_MIN_RADIUS:
        return SMALL_ASTEROID_POINTS
    elif asteroid.radius > ASTEROID_MIN_RADIUS and asteroid.radius < ASTEROID_MAX_RADIUS:
        return MEDIUM_ASTEROID_POINTS
    else:
        return LARGE_ASTEROID_POINTS

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    font = pygame.font.SysFont(None,50)
    
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    
    AsteroidField.containers = (updatable)
    Asteroid.containers = (asteroids, updatable, drawable)
    Player.containers = (updatable,drawable)
    Shot.containers = (shots,updatable,drawable)
    
    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT /2)
    
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
            
            
        screen.fill((0,0,0))
        
        score_text = f"Score: {score}"
        lives_text = f"Lives: {player.lives}"
        text_surface = font.render(score_text, True, 'white')
        lives_text_surface = font.render(lives_text,True,'white')
        
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        lives_rect = lives_text_surface.get_rect(center=(SCREEN_WIDTH // 15,50))
        
        updatable.update(dt)
        
        for object in asteroids:
            if object.check_collision(player):
                if player.lives > 0:
                    player.lives -= 1
                    player.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
                else:
                    print("Game Over!")
                    return
        
        for object in asteroids:
            for bullet in shots:
                if object.check_collision(bullet):
                    score += size_score(object)
                    object.split()
                    bullet.kill()
        
        for draw in drawable:
            draw.draw(screen)
        
        screen.blit(text_surface,text_rect)
        screen.blit(lives_text_surface,lives_rect)
        clock.tick(60)
        dt = clock.tick(60)/1000
        pygame.display.flip()
        
        
if __name__ == "__main__":
    main()