# RayTracing
Ray Tracing with Multi-Axis Galvanometer Simulation
Overview
This code simulates the movement and interaction of a 3D ray with various surfaces and systems, including reflection, refraction, and movement through a series of mirrors. The ray can also be rotated using Rodrigues' rotation formula for vector transformations. The system is designed to model a multi-axis galvanometer used in laser scanning systems.The MultiAxisGalvanometer class in this script simulates the behavior of light rays interacting with a multi-axis galvanometer system used in optical applications such as laser scanning and beam steering. The code includes methods for simulating light-ray interactions such as reflection, refraction, and ray tracing through multiple mirrors. Additionally, the class integrates Rodrigues' rotation formula to rotate vectors (such as mirror normal vectors) around specified axes.

Key Features:
Ray Class: Represents a 3D ray with position and direction.
Reflection and Refraction: Simulates light-ray interactions with surfaces.
Vector Rotation: Uses Rodrigues' rotation formula for rotating vectors.
Multi-Mirror Simulation: Supports rotating mirrors and interaction with the ray.
The code is useful for simulating optical systems where rays interact with surfaces (such as mirrors or lenses) in a 3D environment. It can be applied in fields like optical design, laser scanning, and ray tracing simulations.
Simulation of Multi-Axis Galvanometer: Models ray tracing through a multi-axis galvanometer system, commonly used in laser scanning and beam deflection systems.

1. Helper Functions
rotate_normal_vector(normal_vector, angles)
Rotates the normal vector around the X, Y, and Z axes by specified angles.

normal_vector: The initial normal vector to be rotated.
angles: A list of three angles (in degrees) for rotation around the X, Y, and Z axes, respectively.
Example Usage:

rotated_normal = rotate_normal_vector([1, 0, 0], [45, 0, 0])
translate_position(position, translation_vector)
Translates a position vector by a given translation vector.

position: The original position vector [x, y, z].
translation_vector: The translation vector [dx, dy, dz].
Example Usage:

new_position = translate_position([0, 0, 0], [1, 0, 0])
2. MultiAxisGalvanometer Class
The main class that simulates the multi-axis galvanometer and the ray tracing system.
Constructor:
__init__(focus_distance, galvo_gap)
focus_distance: Distance to the focus plane where the ray intersects after passing through the system.
galvo_gap: Gap between the galvanometer mirrors.
Methods:
set_ray(ray):

Initializes the ray to be traced through the system.
ray (Ray object): The light ray that will be traced through the system.
reflect(normal, point):

Reflects the ray off a mirror with a given normal vector and point on the mirror's surface.
normal (list): Normal vector of the reflecting surface.
point (list): A point on the surface of the mirror.
scan(Px1, Px2, nx, ny, nx_rotation, ny_rotation, x_angle, y_angle):

Simulates the scanning operation of the X and Y mirrors.
Px1, Px2: Positions of the first and second scanning mirrors.
nx, ny: Normal vectors of the X and Y mirrors.
nx_rotation, ny_rotation: Rotation axes for the X and Y mirrors.
x_angle, y_angle: Rotation angles for the X and Y mirrors (in degrees).
refract(normal, point, k=-1):

Simulates refraction at the field lens, where the light ray changes direction based on the refractive index and surface normal.
normal (list): Normal vector of the refracting surface.
point (list): A point on the refracting surface.
k (float): Refractive index (default is -1, representing general refraction).
trace(X_angle, Y_angle):

Simulates the full ray tracing process, including reflection from two mirrors, scanning of X-Y mirrors, and refraction at the field lens.
X_angle, Y_angle: Rotation angles of the X and Y mirrors.
Returns the final intersection point of the ray with the focusing plane.

Example Usage:
1. Creating the Multi-Axis Galvanometer and Ray Object:
# Define the focus distance and galvanometer gap
focus_distance = 100
galvo_gap = 10

# Initialize the Multi-Axis Galvanometer
galvo = MultiAxisGalvanometer(focus_distance, galvo_gap)

# Create a Ray object (assuming you have a Ray class defined elsewhere)
ray = Ray([0, 0, 0], [1, 0, 0])

# Set the ray for tracing
galvo.set_ray(ray)
2. Performing Ray Tracing with Mirror Scanning:
# Define rotation angles for the mirrors
X_angle = 30  # Rotation angle for the X-axis mirror (in degrees)
Y_angle = 45  # Rotation angle for the Y-axis mirror (in degrees)

# Trace the ray through the system
intersection_point = galvo.trace(X_angle, Y_angle)

# Output the intersection point with the focusing plane
print(f"The final intersection point of the ray is: {intersection_point}")
Application
This simulation can be applied in several fields:

Laser Scanning Systems: Model and optimize multi-axis galvanometer systems for beam deflection and laser scanning.
Optical Design: Simulate ray interactions in complex optical systems involving multiple reflective and refractive surfaces.
Beam Steering: Design systems for controlling laser or light beams through rotating mirrors in scanning or projection systems.
