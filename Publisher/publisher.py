import pika
import json
import time
from planet import BLUE, RED, YELLOW, DARK_GREY, WHITE, Planet

# Initialize connection to RabbitMQ server
credentials = pika.PlainCredentials('admin1', 'admin123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials))

channel = connection.channel()
channel.queue_declare(queue='planet_simulation')

sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30, 'Sun')
sun.sun = True

earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24, 'Earth')
earth.y_vel = 29.783 * 1000

mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23, 'Mars')
mars.y_vel = 24.077 * 1000

mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23, 'Mercury')
mercury.y_vel = -47.4 * 1000

venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24, 'Venus')
venus.y_vel = -35.02 * 1000

planets = [sun, earth, mars, mercury, venus]

# Calculate and publish forces for each planet
while True:
    for planet in planets:
        forces = {}
        for other_planet in planets:
            if planet == other_planet:
                continue

            force_x, force_y = planet.attraction(other_planet)
            forces[other_planet.name] = {
                'force_x': force_x, 'force_y': force_y}

        channel.basic_publish(
            exchange='', routing_key='planet_simulation', body=json.dumps(forces))
        print(forces)
        time.sleep(0.1)
