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
ORANGE = (255, 215, 0)
GREY = (125, 125, 125)
PALE_YELLOW = (240, 240, 0)
# background_orbit_paths = np.array([[x, y] for x in range(0, WIDTH) for y in range(0, HEIGHT)])

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation")
clock = pygame.time.Clock()

background_orbit_paths_array = np.zeros((WIDTH, HEIGHT, 3), dtype=np.uint8)


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def magnitude(self):
        return (self.x**2 + self.y**2)**(1/2)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + -1*other

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __rmul__(self, scalar): # scalar must be on left side (scalar*Vector)
        return Vector(self.x*scalar, self.y*scalar)

    def distance(vec_1, vec_2): # can be used for distance between points as well
        return (vec_2 - vec_1).magnitude()

    def angle_to_vertical(self):
        return math.atan(self.y/self.x)
        # return math.atan2(self.y, self.x)

a= Vector(1, 2)
print(5*a)
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

        # # Integral method
        # #__________________
        # current_distance = Vector.distance(self, object_b)
        # self.x -= self.vx
        # self.y -= self.vy
        # last_distance = Vector.distance(self, object_b)
        # self.x += self.vx
        # self.y += self.vy
        # # force_magnitude = (-object_b.mass/(2*current_distance) - (-object_b.mass/(2*last_distance)))*(1/FPS)
        # #__________________

        force_magnitude = object_b.mass/Vector.distance(self.get_vector(), object_b.get_vector())**2*(1/FPS) # vf_a=M_b/r^2



        force_direction = object_b.get_vector() - self.get_vector()
        
        return ((1/force_direction.magnitude())*force_magnitude)*force_direction

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

    def update_all(self, solar_system):
        solar_system_copy = solar_system.copy() # used to exclude current body without changing global 
        del solar_system_copy[self.name]

        if self.is_influenced: # sun is not influenced by planets
            for body in solar_system_copy.values():
                self.update_orbit_velocity(body)
            self.update_position()
        self.draw()


# solar_system = {
#     'sun' : CelestialBody(name='sun', mass=300000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=YELLOW, radius=40, is_influenced=False),
#     'mercury' : CelestialBody(name='mercury', mass=100, x=WIDTH//2-50, y=HEIGHT//2, vx=0, vy=-10, color=WHITE, radius=3),
#     'venus' : CelestialBody(name='venus', mass=1000, x=WIDTH//2-100, y=HEIGHT//2-3, vx=0, vy=-8, color=ORANGE, radius=7),
#     'earth' : CelestialBody(name='earth', mass=1000, x=WIDTH//2-150, y=HEIGHT//2, vx=0, vy=-7, color=BLUE, radius=7),
#     'mars' : CelestialBody(name='mars', mass=500, x=WIDTH//2-200, y=HEIGHT//2, vx=0, vy=-5, color=RED, radius=5),
#     'jupiter' : CelestialBody(name='jupiter', mass=3000, x=WIDTH//2-300, y=HEIGHT//2, vx=0, vy=-4, color=RED, radius=20),
#     'saturn' : CelestialBody(name='saturn', mass=2000, x=WIDTH//2-400, y=HEIGHT//2, vx=0, vy=-3, color=GREY, radius=16),
#     'uranus' : CelestialBody(name='uranus', mass=1500, x=WIDTH//2-500, y=HEIGHT//2, vx=0, vy=-2, color=BLUE, radius=12),
#     'neptune' : CelestialBody(name='neptune', mass=1500, x=WIDTH//2-600, y=HEIGHT//2, vx=0, vy=-1, color=BLUE, radius=12),
#     }

# solar_system = {
#     'sun' : CelestialBody(name='sun', mass=500000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=YELLOW, radius=30, is_influenced=True),
#     'sun2' : CelestialBody(name='sun2', mass=50000, x=WIDTH//2-201, y=HEIGHT//2, vx=0, vy=5, color=YELLOW, radius=30),
#     'mercury' : CelestialBody(name='mercury', mass=10, x=WIDTH//2-50, y=HEIGHT//2, vx=0, vy=-12, color=WHITE, radius=3),
#     'venus' : CelestialBody(name='venus', mass=10, x=WIDTH//2-100, y=HEIGHT//2-3, vx=0, vy= 8, color=ORANGE, radius=7),
#     'earth' : CelestialBody(name='earth', mass=10, x=WIDTH//2-150, y=HEIGHT//2, vx=0, vy=-6, color=BLUE, radius=7),
#     'mars' : CelestialBody(name='mars', mass=10, x=WIDTH//2-200, y=HEIGHT//2, vx=0, vy=-5, color=RED, radius=5),
#     'jupiter' : CelestialBody(name='jupiter', mass=10, x=WIDTH//2-300, y=HEIGHT//2, vx=0, vy=-4, color=RED, radius=15),
#     'saturn' : CelestialBody(name='saturn', mass=10, x=WIDTH//2-400, y=HEIGHT//2, vx=0, vy=-3.5, color=PALE_YELLOW, radius=13),
#     'uranus' : CelestialBody(name='uranus', mass=10, x=WIDTH//2-500, y=HEIGHT//2, vx=0, vy=-3, color=BLUE, radius=11),
#     'neptune' : CelestialBody(name='neptune', mass=10, x=WIDTH//2-600, y=HEIGHT//2, vx=0, vy=-2.5, color=BLUE, radius=11),
#     }



# x1 = WIDTH//2
# y1 = HEIGHT//2
# x2 = WIDTH//2-100
# y2 = y=HEIGHT//2-3
# mb = 2000000
# b=0
# t=1
# r = Vector.distance(Vector(x1, y1), Vector(x2, y2))

# c= ((x1-x2)*((mb*t)/(r**3)+1))
# d= ((y1-y2)*((mb*t)/(r**3)+1))
# v_1 = (-2*c + math.sqrt((2*c)**2 -4*(-r**2 + c**2 + d**2 + 2*b*d+b**2)))/2
# v_2 = (-2*c + math.sqrt((2*c)**2 -4*(-r**2 + c**2 + d**2 + 2*b*d+b**2)))/2




solar_system = {
    'sun' : CelestialBody(name='sun', mass=200000, x=WIDTH//2, y=HEIGHT//2, vx=0, vy=0, color=YELLOW, radius=10, is_influenced=False),
    'mercury' : CelestialBody(name='mercury', mass=200, x=WIDTH//2-50, y=HEIGHT//2, vx=0, vy=6, color=WHITE, radius=3),
    'venus' : CelestialBody(name='venus', mass=200, x=WIDTH//2-100, y=HEIGHT//2-3, vx=0, vy= 4, color=ORANGE, radius=3),
    'earth' : CelestialBody(name='earth', mass=200, x=WIDTH//2-150, y=HEIGHT//2, vx=0, vy=-4, color=BLUE, radius=7),
    'mars' : CelestialBody(name='mars', mass=200, x=WIDTH//2-200, y=HEIGHT//2, vx=0, vy=-3, color=RED, radius=5),
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

    for body in solar_system.values():
        body.update_all(solar_system)


    pygame.display.flip()
pygame.quit()
