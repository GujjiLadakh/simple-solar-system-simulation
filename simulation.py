# 2D Solar System Simulation

# Libraries
from typing import Union
import matplotlib.pyplot as plt
from matplotlib import animation

# Constants
G: float           = 6.67e-11              # Constant of Gravitation
M_s: float         = 2.0e30                # Mass of Sun
M_e: float         = 5.972e24              # Mass of Earth
AU: float          = 1.5e11                # Astronomical Unit in metres

day_seconds: float = 24.0 * 60 * 60        # Number of seconds in a day
t: float           = 0.0                   # Counter
dt: float          = 1 * day_seconds       # Time step

v_e_apv: int       = 29290                 # Velocity of Earth at aphelion

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.grid()

# Classes
class Planet:
    def __init__(self, name: str, mass_of_planet: float, mass_of_host_star: float, colour: str, distance_to_sun: float, v_at_apv: int, x: Union[int, float], y: Union[int, float], z: Union[int, float]) -> None:
        # General attributes
        self.name: str = name
        self.mass: float = mass_of_planet
        self.GMm: float = G * mass_of_planet * mass_of_host_star
        self.colour: str = colour
        self.distance_to_sun: float = distance_to_sun

        # Velocity in 3D
        self.v_x: Union[int, float] = 0
        self.v_y: Union[int, float] = v_at_apv
        self.v_z: Union[int, float] = 0

        # Position in 3D
        self.x: Union[int, float] = x
        self.y: Union[int, float] = y
        self.z: Union[int, float] = z

        # List of coordinates for animation
        self.x_list: list[Union[int, float]] = []
        self.y_list: list[Union[int, float]] = []
        self.z_list: list[Union[int, float]] = []
        self.x_data: list[Union[int, float]] = []
        self.y_data: list[Union[int, float]] = []
        self.z_data: list[Union[int, float]] = []

        # Axis data
        self.line = None
        self.point = None
        self.text = None

    def get_relative_position_and_mod(self, star):
        # This data is required in a few calculations
        r_x, r_y, r_z = self.x - star.x, self.y - star.y, self.z - star.z
        mod = (r_x ** 2 + r_y ** 2 + r_z ** 2) ** 1.5
        return r_x, r_y, r_z, mod

    def get_x_position(self, star):
        # Return the force in each direction
        r_x, r_y, r_z, mod = self.get_relative_position_and_mod(star)
        fx = -self.GMm * r_x / mod
        fy = -self.GMm * r_y / mod
        fz = -self.GMm * r_z / mod
        return fx, fy, fz

    def update_velocity_and_position(self, star):
        r_x, r_y, r_z, mod = self.get_relative_position_and_mod(star)
        self.v_x += ((-self.GMm * r_x) / mod) * dt / self.mass
        self.v_y += ((-self.GMm * r_y) / mod) * dt / self.mass
        self.v_z += ((-self.GMm * r_z) / mod) * dt / self.mass
        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.z += self.v_z * dt
        self.x_list.append(self.x)
        self.y_list.append(self.y)
        self.z_list.append(self.z)

    def create_line_and_point(self):
        self.line = ax.plot([], [], lw=1)
        self.point = ax.plot([self.distance_to_sun], [0], marker='o', markersize=2, markeredgecolor=self.colour, markerfacecolor=self.colour)
        self.text = ax.text(self.distance_to_sun, 0, self.name)

    def update_line_and_point(self, i):
        self.x_data.append(self.x_list[i])
        self.y_data.append(self.y_list[i])
        self.z_data.append(self.z_list[i])

        self.line[0].set_data(self.x_data, self.y_data)
        self.point[0].set_data([self.x_list[i]], [self.y_list[i]])
        self.text.set_position((self.x_list[i], self.y_list[i]))

        return self.line[0], self.point[0], self.text

class Sun:
    def __init__(self):
        self.name: str = 'Sun'
        self.mass: float = 2.0e30
        self.colour: str = 'yellow'

        self.x: Union[int, float] = 0
        self.y: Union[int, float] = 0
        self.z: Union[int, float] = 0
        self.v_x: Union[int, float] = 0
        self.v_y: Union[int, float] = 0
        self.v_z: Union[int, float] = 0

        self.x_list: list[Union[int, float]] = []
        self.y_list: list[Union[int, float]] = []
        self.z_list: list[Union[int, float]] = []

        self.point = None
        self.text = None

    def update_velocity(self, planets: list[Planet]):
        x_total: Union[int, float] = 0
        y_total: Union[int, float] = 0
        z_total: Union[int, float] = 0
        for planet in planets:
            curr_x, curr_y, curr_z = planet.get_x_position(self)
            x_total += curr_x
            y_total += curr_y
            z_total += curr_z
        self.v_x += -x_total * dt / self.mass
        self.v_y += -y_total * dt / self.mass
        self.v_z += -z_total * dt / self.mass

        self.x += self.v_x * dt
        self.y += self.v_y * dt
        self.z += self.v_z * dt

        self.x_list.append(self.x)
        self.y_list.append(self.y)
        self.z_list.append(self.z)


    def create_point(self):
        self.point = ax.plot([0], [0], marker='o', markersize=7, markeredgecolor=self.colour, markerfacecolor=self.colour)
        self.text = ax.text(0, 0, self.name)

    def update_point(self, i):
        self.point[0].set_data([self.x_list[i]], [self.y_list[i]])
        self.text.set_position((self.x_list[i], self.y_list[i]))

        return self.point[0], self.text

# Processing

planets = []
earth = Planet('Earth', M_e, M_s, 'blue', AU, v_e_apv, 1.0167*AU, 0, 0)
planets.append(earth)
sun   = Sun()

while t < 1 * 365 * day_seconds:
    for planet in planets:
        planet.update_velocity_and_position(sun)
    sun.update_velocity(planets)
    t += dt

for planet in planets:
    planet.create_line_and_point()
sun.create_point()

def update_all(i):
    r = []
    for planet in planets:

        line, point, text = planet.update_line_and_point(i)
        r.extend([line, point, text])

    point, text = sun.update_point(i)
    r.extend([point, text])

    ax.axis('equal')
    ax.set_xlim(-3*AU, 3*AU)
    ax.set_ylim(-3*AU, 3*AU)

    return r

# Animation
anim = animation.FuncAnimation(fig, func=update_all, frames=len(planets[0].x_list), interval=1, blit=True)
plt.show()
