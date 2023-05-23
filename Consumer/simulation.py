import pygame
import math
import pika
import json
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600  # 1 day

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.draw.circle(win, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(
                f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() /
                     2, y - distance_text.get_height()/2))

    def update_position(self, DATA, section_index, planets):

        section = DATA[section_index]
        planet_data = section.get(self.name)
        total_y = total_x = 0
        for planet in planets:
            if self == planet:
                continue
            if planet_data is not None:
                force_x = planet_data['force_x']
                force_y = planet_data['force_y']
            else:
                force_x = 0
                force_y = 0
            total_x += force_x
            total_y += force_y

        self.x_vel += total_x / self.mass * self.TIMESTEP
        self.y_vel += total_y / self.mass * self.TIMESTEP

        self.x -= self.x_vel * self.TIMESTEP
        self.y -= self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))


def load_data_from_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def apply_forces_from_data(planets, data):
    for planet in planets:
        force_data = data.get(str(planet))
        if force_data:
            force_x = force_data['force_x'] + 1e20
            force_y = force_data['force_y'] + 1e20

            planet.x_vel += force_x / planet.mass * planet.TIMESTEP
            planet.y_vel += force_y / planet.mass * planet.TIMESTEP


def main():
    # Initialize connection to RabbitMQ server
    # credentials = pika.PlainCredentials('admin1', 'admin123')
    # connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='192.168.1.24', credentials=credentials))
    # channel = connection.channel()

    # channel.queue_declare(queue='planet_simulation')

    run = True
    clock = pygame.time.Clock()

    sun = Planet('Sun', 0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet('Earth', -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet('Mars', -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet('Mercury', 0.387 * Planet.AU,
                     0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet('Venus', 0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # def callback(ch, method, properties, body):
    # 	planet_forces = json.loads(body)
    # 	for planet in planets:
    # 		force_data = planet_forces.get(str(planet))
    # 		if force_data:
    # 			force_x = force_data['force_x']
    # 			force_y = force_data['force_y']
    # 			planet.x_vel += force_x / planet.mass * planet.TIMESTEP
    # 			planet.y_vel += force_y / planet.mass * planet.TIMESTEP

    # for planet in planets:
    # 	planet.update_position(planets)
    # 	planet.draw(WIN)

    #channel.basic_consume(queue='planet_simulation', on_message_callback=callback, auto_ack=True)

    DATA = load_data_from_file('./testing.json')
    # print(DATA)
    section_index = 0
    #apply_forces_from_data(planets, DATA)

    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(DATA, section_index, planets)
            planet.draw(WIN)
        section_index += 1
        if section_index >= len(DATA):
            section_index = 0

        # 	channel.basic_publish(exchange='', routing_key='planet_simulation', body=json.dumps(planet.__dict__))
        # connection.process_data_events()
        pygame.display.update()
    pygame.quit()


main()
