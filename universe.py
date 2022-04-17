from turtle import back
import pygame
import math
import numpy as np

pygame.init()
# WIDTH = HEIGHT = 800
WIDTH=1400
HEIGHT = 800
FPS = 60
ZOOM_FACTOR = 1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 190, 0)

# background_orbit_paths = np.array([[x, y] for x in range(0, WIDTH) for y in range(0, HEIGHT)])

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Simulation")
clock = pygame.time.Clock()

background_orbit_paths_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def magnitude(self):
        return (self.x**2 + self.y**2)**(1/2)

    def add(vec_1, vec_2):
        return Vector(vec_1.x + vec_2.x, vec_1.y + vec_2.y)

    def subtract(vec_1, vec_2):
        return Vector.add(vec_1, Vector.multiply_scaler(vec_2, -1))

    def multiply_scaler(vec, scalar):
        return Vector(vec.x*scalar, vec.y*scalar)

    def display_components(self):
        return (self.x, self.y)

    def distance(vec_1, vec_2): # can be used for distance between points as well
        return Vector.subtract(vec_2, vec_1).magnitude()

    def angle_to_vertical(self):
        return math.atan(self.y/self.x)
        # return math.atan2(self.y, self.x)

class CelestialBody:
    def __init__(self, mass, x, y, vx, vy, color, radius):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.radius = radius
    

    def get_gravitational_velocity_vec(self, object_b): # add to initial velocity vector
        force_magnitude = object_b.mass/Vector.distance(self, object_b)**2*(1/FPS) # vf_a=M_b/r^2
        force_direction = Vector.subtract(object_b, self)
        # angle = Vector.subtract(self, object_b).angle_to_vertical()
        
        # return Vector(force_direction.x/force_direction.magnitude()*force_magnitude, force_direction.y/force_direction.magnitude()*force_magnitude)
        return Vector.multiply_scaler(force_direction, (1/force_direction.magnitude())*force_magnitude)

    def update_orbit_velocity(self, object_b):
        gravity_vec = self.get_gravitational_velocity_vec(object_b)
        self.vx += gravity_vec.x
        self.vy += gravity_vec.y

    def out_of_bounds(self):
        if self.x <= 0 or self.x + self.radius*2 >= WIDTH:
            return True
        if self.y <= 0 or self.y + self.radius*2 >= HEIGHT:
            return True
        return False
    
    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        if not self.out_of_bounds():
            background_orbit_paths_array[int(self.x), int(self.y), 0:3] = self.color

    def draw(self):
        # pygame.draw.circle(WIN, self.color, (self.x/ZOOM_FACTOR, self.y/ZOOM_FACTOR), self.radius/ZOOM_FACTOR)
        pygame.draw.circle(WIN, self.color, (self.x, self.y), self.radius)

    def handle_wall_collision(self):
        if self.x <= 0 or self.x + self.radius*2 >= WIDTH:
            self.vx*=-1
        if self.y <= 0 or self.y + self.radius*2 >= HEIGHT:
            self.vy*=-1
        



earth = CelestialBody(mass=10000, x=WIDTH//2-300, y=HEIGHT//2, vx=2, vy=2, color=BLUE, radius=7)
sun = CelestialBody(mass=300000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=YELLOW, radius=20)
moon = CelestialBody(mass=100, x=WIDTH//2-400+1, y=HEIGHT//2, vx=0, vy=2, color=WHITE, radius=3)
mars = CelestialBody(mass=5000, x=WIDTH//2+300+7, y=HEIGHT//2, vx=0, vy=-4, color=RED, radius=5)

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # if event.type == pygame.MOUSEBUTTONDOWN:
        #     if event.button == 4: # scroll down
        #         ZOOM_FACTOR -= 0.05
        #     if event.button == 5: # scroll up
        #         ZOOM_FACTOR += 0.05

    WIN.fill(BLACK)
    # earth.handle_wall_collision()
    # moon.handle_wall_collision()
    # sun.handle_wall_collision()
    pygame.surfarray.blit_array(WIN, background_orbit_paths_array)
    earth.update_orbit_velocity(sun)
    earth.update_orbit_velocity(moon)
    moon.update_orbit_velocity(sun)
    moon.update_orbit_velocity(earth)
    moon.update_orbit_velocity(mars)
    earth.update_orbit_velocity(mars)
    mars.update_orbit_velocity(sun)
    mars.update_orbit_velocity(earth)
    mars.update_orbit_velocity(moon)
    mars.update_orbit_velocity(sun)
    # sun.update_orbit_velocity(earth)
    # sun.update_orbit_velocity(moon)
    # sun.update_orbit_velocity(mars)
    earth.update_position()
    moon.update_position()
    mars.update_position()
    # sun.update_position()
    earth.draw()
    mars.draw()
    moon.draw()
    sun.draw()


    pygame.display.flip()
pygame.quit()