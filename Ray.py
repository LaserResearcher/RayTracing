'''
Copyright (c) 2020, HUST All rights reserved

File Name: ray_tracing.py
Summary:
    This file contains a class `Ray` that represents a 3D ray with various methods for simulating light-ray interactions, including reflection, refraction, and movement. The code also implements the Rodrigues' rotation formula to rotate vectors around a specified axis, and provides a simulation of ray tracing with rotating mirrors.

Running Environment: Python 3.6

Modification Description:
    This file provides a basic simulation of ray tracing and vector transformations in 3D space. It includes methods to handle ray movement, reflection, refraction, and interaction with planes. The reflection and refraction methods support both simple and advanced operations like rotating mirrors and Snell's law-based refraction.

Current Version: 2.0

Modified By: Tianz

Modification Details:
    - Added ray refraction method.
    - Implemented rotating mirrors in the `scan` method.
    - Improved mathematical accuracy and vector normalization for all operations.
    - Added detailed comments and documentation.

Modification Date: [Insert Date]

Original Author: Tianz

Completion Date: 2024.06.12
'''

import numpy as np

'''
Function name: rotate_vector_around_axis
Function description: 
    Rotates a vector around a given axis by an angle theta using Rodrigues' rotation formula.

Input parameters:
    vec (np.array): The vector to be rotated.
    axis (np.array): The axis of rotation, must be a 3D vector.
    theta (float): The angle of rotation in radians.

Output parameters:
    np.array: The rotated vector.

Notes:
    The input vector and axis are normalized to unit vectors before applying the rotation formula.
'''
def rotate_vector_around_axis(vec, axis, theta):
    vec = vec / np.linalg.norm(vec)  # Normalize the vector
    axis = axis / np.linalg.norm(axis)  # Normalize the axis
    # Apply Rodrigues' rotation formula
    rotated = vec * np.cos(theta) + np.cross(axis, vec) * np.sin(theta) + axis * np.dot(axis, vec) * (1 - np.cos(theta))
    return rotated



'''
Class name: Ray
Class description: 
    A class that represents a 3D ray with position and direction, supporting operations like reflection, refraction, and rotation.

'''
class Ray:
    '''
    Function name: __init__
    Function description:
        Initializes a Ray object with a given position and direction.

    Input parameters:
        position (iterable): A 3D position vector for the ray's origin.
        direction (iterable): A 3D direction vector for the ray's direction.

    Output parameters:
        None

    Notes:
        The direction vector is normalized to ensure it has unit length.
    '''
    def __init__(self, position, direction):
        self.position = np.array(position, dtype=np.float64)  # Store position as a numpy array
        self.direction = np.array(direction, dtype=np.float64) / np.linalg.norm(direction)  # Normalize direction vector



    '''
    Function name: point_at_parameter
    Function description: 
        Returns the point on the ray at parameter t.

    Input parameters:
        t (float): The parameter along the ray to evaluate.

    Output parameters:
        np.array: The point at distance t along the ray from the origin.

    Notes:
        The function calculates the point on the ray by adding t times the direction vector to the origin.
    '''
    def point_at_parameter(self, t):
        return self.position + t * self.direction



    '''
    Function name: move
    Function description: 
        Moves the ray along its direction by a distance L.

    Input parameters:
        L (float): The distance to move along the ray's direction.

    Output parameters:
        None

    Notes:
        This updates the ray's position by adding L times the direction vector.
    '''
    def move(self, L):
        self.position += L * self.direction  # Move the ray by L units along its direction
        print("New Position after move:", self.position)
        print("New direction after move:", self.direction)



    '''
    Function name: reflection
    Function description: 
        Reflects the ray's direction based on a given normal vector n.

    Input parameters:
        n (iterable): The normal vector of the reflecting surface.

    Output parameters:
        None

    Notes:
        The normal vector n is normalized before reflection. The direction vector is updated based on the reflection formula.
    '''
    def reflection(self, n):
        n = np.array(n, dtype=np.float64) / np.linalg.norm(n)  # Normalize the normal vector
        self.direction = self.direction - 2 * np.dot(self.direction, n) * n  # Reflection formula
        print("New Position after reflection:", self.position)
        print("New direction after reflection:", self.direction)



    '''
    Function name: refraction
    Function description: 
        Simulates the refraction of the ray when it passes through a surface with a given refractive index k and normal vector n.

    Input parameters:
        k (float): The refractive index (ratio of speed of light in vacuum to the speed of light in the medium).
        n (iterable): The normal vector of the refracting surface.

    Output parameters:
        None

    Notes:
        The method calculates the angle of incidence and applies Snell's law to compute the refracted direction.
        The direction vector is updated to reflect the refraction.
    '''
    def refraction(self, k, n):
        n = np.array(n, dtype=np.float64) / np.linalg.norm(n)  # Normalize the normal vector
        cos_theta = -np.dot(self.direction, n)  # Calculate the cosine of the angle of incidence
        if abs(cos_theta) >= 1:
            acos_theta = 0
        else:
            acos_theta = np.arccos(cos_theta)
        term1 = k * acos_theta / np.sqrt(1 + k ** 2 * (acos_theta) ** 2)
        # Compute the vertical and parallel components of the refracted direction
        vertical_direction = -1 * (1 / np.sqrt(1 + k ** 2 * (acos_theta) ** 2)) * n
        parallel_direction_vector = self.direction + cos_theta * n
        parallel_direction = term1 * (parallel_direction_vector / np.linalg.norm(parallel_direction_vector))
        self.direction = vertical_direction + parallel_direction  # Combine both components
        self.direction = self.direction / np.linalg.norm(self.direction)  # Normalize the resulting direction



    '''
    Function name: scan
    Function description: 
        Simulates the scanning process of the ray as it reflects off two rotating mirrors.

    Input parameters:
        Px1 (np.array): Position of the first mirror.
        Px2 (np.array): Position of the second mirror.
        nx (np.array): Normal vector of the first mirror.
        ny (np.array): Normal vector of the second mirror.
        nx_rotation (np.array): Rotation axis of the first mirror.
        ny_rotation (np.array): Rotation axis of the second mirror.
        x_angle (float): Rotation angle for the first mirror (in degrees).
        y_angle (float): Rotation angle for the second mirror (in degrees).

    Output parameters:
        None

    Notes:
        The normal vectors of the mirrors are rotated by the given angles before performing reflection. 
        The ray interacts with both mirrors and reflects accordingly.
    '''
    def scan(self, Px1, Px2, nx, ny, nx_rotation, ny_rotation, x_angle, y_angle):
        nx = np.array(nx, dtype=np.float64) / np.linalg.norm(nx)  # Normalize normal vector of the first mirror
        ny = np.array(ny, dtype=np.float64) / np.linalg.norm(ny)  # Normalize normal vector of the second mirror
        nx_rotation = np.array(nx_rotation, dtype=np.float64) / np.linalg.norm(
            nx_rotation)  # Normalize rotation axis of the first mirror
        ny_rotation = np.array(ny_rotation, dtype=np.float64) / np.linalg.norm(
            ny_rotation)  # Normalize rotation axis of the second mirror
        # Convert rotation angles from degrees to radians
        x_angle_pi = x_angle * np.pi / 180
        y_angle_pi = y_angle * np.pi / 180
        # Rotate the normal vectors of the mirrors according to the rotation angles
        nx_after = rotate_vector_around_axis(nx, nx_rotation, x_angle_pi)
        ny_after = rotate_vector_around_axis(ny, ny_rotation, y_angle_pi)
        # Compute the interaction with the first mirror and reflect the ray
        self.interaction(nx_after, Px1)
        self.reflection(nx_after)
        # Compute the interaction with the second mirror and reflect the ray again
        self.interaction(ny_after, Px2)
        self.reflection(ny_after)



    '''
    Function name: interaction
    Function description: 
        Computes the point of intersection between the ray and a plane.

    Input parameters:
        n (np.array): The normal vector of the plane.
        P (np.array): A point on the plane.

    Output parameters:
        np.array: The intersection point if there is one; None if there is no intersection.

    Notes:
        The function calculates the parameter t to find the intersection point. 
        If t is negative or the ray is parallel to the plane, no intersection occurs.
    '''
    def interaction(self, n, P):
        n = np.array(n, dtype=np.float64) / np.linalg.norm(n)  # Normalize the normal vector
        P = np.array(P, dtype=np.float64)  # Convert the point to a numpy array
        denominator = np.dot(self.direction, n)  # Calculate the denominator for the ray-plane intersection equation
        if np.abs(denominator) < 1e-10:
            return None  # If the ray is parallel to the plane, there's no intersection
        t = np.dot(P - self.position, n) / denominator  # Compute the intersection parameter t
        if t < 0:
            return None  # If the intersection point is behind the ray's origin, no valid intersection
        self.position = self.point_at_parameter(t)  # Update the ray's position to the intersection point
        return self.position
