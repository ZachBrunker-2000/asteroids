# this allows us to use code from
# the open-source pygame library
# throughout this file
import pygame
import asyncio
from constants import *
from Player import *
from asteroid import *
from asteroidfield import *
from score_api import submit_score, get_high_scores

def size_score(asteroid):
    if asteroid.radius <= ASTEROID_MIN_RADIUS:
        return SMALL_ASTEROID_POINTS
    elif asteroid.radius > ASTEROID_MIN_RADIUS and asteroid.radius < ASTEROID_MAX_RADIUS:
        return MEDIUM_ASTEROID_POINTS
    else:
        return LARGE_ASTEROID_POINTS

async def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    score = 0
    input_text = ""
    font = pygame.font.SysFont(None,50)
    title_font = pygame.font.SysFont(None, 120)
    
    state = 'MENU'
    cursor_timer = 0
    cursor_blink_interval = 500
    cursor_visible = True
    max_chars = 4
    active = True
    success = False
    
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
    
    while active:
        while state == 'MENU':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter
                        state = 'PLAYING'
                    elif event.key == pygame.K_ESCAPE:
                        active = False
                        return
                    
            screen.fill((0,0,0))
        
            title_text = "Asteroids"
            play_text = "Press Enter to Play..."
            quit_text = "Esc to Quit"
            title_surface = title_font.render(title_text, True, 'white')
            play_surface = font.render(play_text,True,'white')
            quit_surface = font.render(quit_text,True, 'white')
        
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 175))
            play_rect = play_surface.get_rect(center=(SCREEN_WIDTH // 2, 425))
            quit_rect = quit_surface.get_rect(center=(SCREEN_WIDTH//2, 500))
        
            screen.blit(title_surface,title_rect)
            screen.blit(play_surface,play_rect)
            screen.blit(quit_surface,quit_rect)
        
            pygame.display.flip()
        
        while state == 'PLAYING':            
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        state = 'GAME_OVER'
                    
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
                        state = 'GAME_OVER'
        
            for obj in asteroids:
                for bullet in shots:
                    if obj.check_collision(bullet):
                        score += size_score(obj)
                        obj.split()
                        bullet.kill()
        
            for draw in drawable:
                draw.draw(screen)
        
            screen.blit(text_surface,text_rect)
            screen.blit(lives_text_surface,lives_rect)
            clock.tick(60)
            dt = clock.tick(60)/1000
            pygame.display.flip()
            
        
        while state == 'GAME_OVER':
            ct = clock.tick(30)
            cursor_timer += ct
            
            
            if cursor_timer >= cursor_blink_interval:
                cursor_visible = not cursor_visible
                cursor_timer = 0
        
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    active = False
                    return                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and input_text:
                        success = submit_score(input_text,score)
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif len(input_text) < max_chars and event.unicode.isprintable():
                        input_text += event.unicode
                    elif event.key == pygame.K_ESCAPE:
                        state = 'MENU'
                        input_text = ''
                
            screen.fill((0,0,0))
        
            game_over_text = "Game Over!"
            score_text = f"Score: {score}"
            prompt_text = "Please enter your initials:"
            display_text = input_text.upper() + ('_' if cursor_visible else '')
            submit_text = ("Press enter to submit your score" if not success else "Score Submitted!")
            esc_text = "press esc to restart"            
        
            game_over_surface = title_font.render(game_over_text,True,'white')
            score_surface = font.render(score_text, True, 'white')
            prompt_surface = font.render(prompt_text, True, 'white')
            display_surface = title_font.render(display_text, True, 'white')
            submit_surface = font.render(submit_text, True, 'white')
            esc_surface = font.render(esc_text, True, 'white')
            
        
            game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
            score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            prompt_rect = prompt_surface.get_rect(center=(SCREEN_WIDTH // 2, 300))
            display_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, 350))
            submit_rect = submit_surface.get_rect(center=(SCREEN_WIDTH // 2, 500))
            esc_rect = esc_surface.get_rect(center=(SCREEN_WIDTH // 2, 600))
            
            
            screen.blit(game_over_surface, game_over_rect)
            screen.blit(score_surface, score_rect)
            screen.blit(prompt_surface, prompt_rect)
            screen.blit(display_surface, display_rect)
            screen.blit(submit_surface, submit_rect)
            screen.blit(esc_surface,esc_rect)
            
            pygame.display.flip()
        
            
        
        await asyncio.sleep(0)
if __name__ == "__main__":
    asyncio.run(main())