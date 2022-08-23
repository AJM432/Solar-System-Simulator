import pygame
import numpy as np
from constants import *
from vector_class import Vector

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

# array to keep track of path of celestial bodies
background_orbit_paths_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)
background_orbit_paths_array[0:, 0:, 0:] = BACKGROUND_COLOR

class CelestialBody:
    def __init__(self, name, mass, x, y, vx, vy, color, radius, is_influenced=True):
        self.mass = mass
        self.name = name
        self.vx = vx
        self.vy = vy
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.is_influenced = is_influenced

    def get_gravitational_velocity_vec(self, object_b): # add to initial velocity vector

        force_magnitude = object_b.mass/Vector.distance(self.get_vector(), object_b.get_vector())**2*(1/FPS) # vf_a=M_b/r^2
        force_direction = object_b.get_vector() - self.get_vector()
        return force_magnitude/force_direction.magnitude()*force_direction


    def update_orbit_velocity(self, object_b):
        gravity_vec = self.get_gravitational_velocity_vec(object_b)
        self.vx += gravity_vec.x
        self.vy += gravity_vec.y

    def get_vector(self):
        return Vector(self.x, self.y)

    def out_of_bounds(self):
        if self.x <= 0 or self.x + self.radius*2 >= WIDTH:
            return True
        if self.y <= 0 or self.y + self.radius*2 >= HEIGHT:
            return True
        return False
    
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        if not self.out_of_bounds(): # don't draw orbit pixel if object not in frame
            background_orbit_paths_array[int(self.x), int(self.y), 0:3] = self.color

    def draw(self):
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

    def handle_wall_collision(self):
        if self.x <= 0 or self.x + self.radius*2 >= WIDTH:
            self.vx*=-1
        if self.y <= 0 or self.y + self.radius*2 >= HEIGHT:
            self.vy*=-1

    # combines all methods required to draw object to screen and interact with other objects
    def next_frame(self, solar_system):
        solar_system_copy = solar_system.copy() # used to exclude current body without changing global 
        del solar_system_copy[self.name]

        if self.is_influenced: # sun is not influenced by planets
            for body in solar_system_copy.values():
                self.update_orbit_velocity(body)
            self.update_position()
        self.draw()

solar_system = {
    'sun' : CelestialBody(name='sun', mass=200000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=PALE_YELLOW, radius=10, is_influenced=False),
    'mercury' : CelestialBody(name='mercury', mass=200, x=WIDTH//2-50, y=HEIGHT//2, vx=0, vy=6, color=WHITE, radius=3),
    'venus' : CelestialBody(name='venus', mass=200, x=WIDTH//2-100, y=HEIGHT//2, vx=0.5, vy= 3, color=PINK, radius=3),
    'earth' : CelestialBody(name='earth', mass=200, x=WIDTH//2-150, y=HEIGHT//2, vx=0, vy=-4, color=BLUE, radius=7),
    'mars' : CelestialBody(name='mars', mass=200, x=WIDTH//2-200, y=HEIGHT//2, vx=0, vy=5, color=RED, radius=5),
    'jupiter' : CelestialBody(name='jupiter', mass=200, x=WIDTH//2-300, y=HEIGHT//2, vx=0, vy=-3, color=RED, radius=15),
    'saturn' : CelestialBody(name='saturn', mass=200, x=WIDTH//2-400, y=HEIGHT//2, vx=0, vy=-2, color=PALE_YELLOW, radius=13),
    'uranus' : CelestialBody(name='uranus', mass=200, x=WIDTH//2-500, y=HEIGHT//2, vx=0, vy=-2, color=BLUE, radius=11),
    'neptune' : CelestialBody(name='neptune', mass=200, x=WIDTH//2-600, y=HEIGHT//2, vx=0, vy=-1, color=BLUE, radius=11)
    }

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    WIN.fill(BACKGROUND_COLOR)
    pygame.surfarray.blit_array(WIN, background_orbit_paths_array)

    for body in solar_system.values():
        body.next_frame(solar_system)

    pygame.display.flip()
pygame.quit()
