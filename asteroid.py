from circleshape import *
from constants import *
import random


class Asteroid(CircleShape):
    
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
        
        
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255),self.position, self.radius,2)
        
    def update(self, dt):
        self.position += self.velocity *dt
        
    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        
        rand_ang = random.uniform(20,50)
        
        vel1 = self.velocity.rotate(rand_ang)
        vel2 = self.velocity.rotate(-rand_ang)
        
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        
        asteroid1 = Asteroid(self.position[0],self.position[1],new_radius)
        asteroid2 = Asteroid(self.position[0],self.position[1],new_radius)
        
        asteroid1.velocity = vel1 * 1.2
        asteroid2.velocity = vel2 * 1.2
        
        
        