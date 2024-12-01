'''
Copyright (c) 2020, HUST All rights reserved

File Name: ray_tracing.py
Summary:
    This file contains a class `MultiAxisGalvanometer` that simulates a multi-axis galvanometer system used for ray tracing. The code includes methods for simulating light-ray interactions such as reflection, refraction, and movement through a series of mirrors, with the application of Rodrigues' rotation formula to rotate vectors around specified axes.

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


# Helper function to rotate a normal vector around a given axis using Rodrigues' formula
def rotate_normal_vector(normal_vector, angles):
    """
    Rotates the normal vector around the X, Y, and Z axes by the specified angles.

    Parameters:
    - normal_vector (list): The original normal vector [a, b, c].
    - angles (list): The rotation angles for X, Y, and Z axes in degrees.

    Returns:
    - list: The rotated normal vector [a', b', c'].
    """
    # Normalize the normal vector to unit length
    normal_vector = np.array(normal_vector, dtype=np.float64) / np.linalg.norm(normal_vector)  # 确保法向量为单位向量
    # Convert angles from degrees to radians
    angles_rad = np.radians(angles)
    # Define the rotation matrices for each axis (X, Y, Z)
    rotation_matrices = [
        np.array([[1, 0, 0],
                  [0, np.cos(angles_rad[0]), -np.sin(angles_rad[0])],
                  [0, np.sin(angles_rad[0]), np.cos(angles_rad[0])]]),# X-axis rotation matrix
        np.array([[np.cos(angles_rad[1]), 0, np.sin(angles_rad[1])],
                  [0, 1, 0],
                  [-np.sin(angles_rad[1]), 0, np.cos(angles_rad[1])]]),# Y-axis rotation matrix
        np.array([[np.cos(angles_rad[2]), -np.sin(angles_rad[2]), 0],
                  [np.sin(angles_rad[2]), np.cos(angles_rad[2]), 0],
                  [0, 0, 1]])# Z-axis rotation matrix
    ]
    # Initialize the new normal vector as the original normal vector
    new_normal_vector = np.array(normal_vector)
    # Apply the rotation matrices sequentially for each axis
    for rotation_matrix in rotation_matrices:
        new_normal_vector = np.dot(rotation_matrix, new_normal_vector)
    return list(new_normal_vector)


# Helper function for affine transformation (translation) of a point
def translate_position(position, translation_vector):
    """
    Translates the given position by the specified translation vector.

    Parameters:
    - position (list or numpy array): The original position [x, y, z].
    - translation_vector (list or numpy array): The translation vector [dx, dy, dz].

    Returns:
    - numpy array: The translated position [x', y', z'].
    """
    # Ensure position and translation_vector are numpy arrays for vector addition
    position = np.array(position)
    translation_vector = np.array(translation_vector)

    # Perform affine translation by adding the translation vector to the position vector
    translated_position = position + translation_vector

    return translated_position


class MultiAxisGalvanometer:
    """
    Class to simulate the multi-axis galvanometer system, including ray tracing, reflection, refraction, and scanning with rotating mirrors.
    """
    def __init__(self, focus_distance,galvo_gap):
        """
        Initializes the MultiAxisGalvanometer object with specified focus distance and galvanometer gap.

        Parameters:
        - focus_distance (float): The focus distance for the system.
        - galvo_gap (float): The gap between the galvanometer mirrors.
        """
        self.focus_distance = focus_distance  # Focus distance
        self.galvo_gap = galvo_gap  # Galvanometer gap
        self.ray = None  # Ray object, initially set to None

    def set_ray(self, ray):
        """
        Initializes the ray to be traced through the system.

        Parameters:
        - ray (Ray object): A ray object that represents the light ray in the system.
        """
        self.ray = ray

    def reflect(self, normal, point):
        """
        Reflects the ray off a mirror using its normal vector and position.

        Parameters:
        - normal (list): Normal vector of the reflecting surface.
        - point (list): A point on the reflecting surface.

        Notes:
        - The ray interacts with the mirror and then reflects off it.
        """
        self.ray.interaction(normal, point)  # Interaction with the surface
        self.ray.reflection(normal)  # Reflection based on the surface normal

    def scan(self, Px1, Px2, nx, ny, nx_rotation, ny_rotation, x_angle, y_angle):
        """
        Simulates the scanning operation of the X and Y mirrors.

        Parameters:
        - Px1 (list): Position of the first mirror.
        - Px2 (list): Position of the second mirror.
        - nx (list): Normal vector of the first mirror.
        - ny (list): Normal vector of the second mirror.
        - nx_rotation (list): Rotation axis for the first mirror.
        - ny_rotation (list): Rotation axis for the second mirror.
        - x_angle (float): Rotation angle of the first mirror (in degrees).
        - y_angle (float): Rotation angle of the second mirror (in degrees).

        Notes:
        - Rotates the normal vectors of both mirrors by the specified angles before performing the reflection.
        """
        self.ray.scan(Px1, Px2, nx, ny, nx_rotation, ny_rotation, x_angle, y_angle)

    def refract(self, normal, point, k=-1):
        """
        Simulates refraction of the ray at the field lens.

        Parameters:
        - normal (list): Normal vector of the refracting surface (field lens).
        - point (list): A point on the refracting surface.
        - k (float): Refractive index (default is -1, representing a general refraction).

        Notes:
        - The ray interacts with the surface and is refracted based on the refractive index and the surface normal.
        """
        self.ray.interaction(normal, point)  # Interaction with the field lens
        self.ray.refraction(k, normal) # Refraction based on our paper

    def trace(self, X_angle, Y_angle):
        """
        Simulates the full ray tracing process through the multi-axis galvanometer system.

        Parameters:
        - X_angle (float): Rotation angle of the X-axis mirror (in degrees).
        - Y_angle (float): Rotation angle of the Y-axis mirror (in degrees).

        Returns:
        - intersection_point (np.array): The final intersection point of the ray with the focusing plane.
        """


        # Step 1: First Mirror (Pi_1)
        # Step 1: First Mirror (Pi_1)
        n1 = [0, 1, -1]  # Normal vector for the first mirror
        # Use Rodrigues' rotation formula to rotate the normal vector, rotation variable rot=[0,0,0]
        # n1 = rotate_normal_vector(n1, [1, 0, 0])

        P1 = [0, 20, 0]  # Position of the first mirror
        # Use affine transformation for translation, translation components [1,0,0] represent movement along the X, Y, and Z axes
        # P1 = translate_position(P1, [1, 0, 0])
        self.reflect(n1, P1)  # Reflect the ray from the first mirror

        # Step 2: Second Mirror (Pi_2)
        n2 = [0, 1, -1]  # Normal vector for the second mirror
        P2 = [0, 20, 200]  # Position of the second mirror
        self.reflect(n2, P2)  # Reflect the ray from the second mirror

        # Step 3: X-Y Scanning mirrors
        Px1 = [0, 180, 200]  # Position of the first scanning mirror
        Px2 = [self.galvo_gap, 180, 200]  # Position of the second scanning mirror
        nx = [-1, 1, 0]  # Normal vector for X scanning
        ny = [1, 0, 1]  # Normal vector for Y scanning
        rx = [0, 0, 1]  # Rotation axis for X mirror
        ry = [0, 1, 0]  # Rotation axis for Y mirror
        self.scan(Px1, Px2, nx, ny, rx, ry, X_angle, Y_angle)  # Perform scanning operation

        # Step 4: Refraction at the field lens
        n5 = [0, 0, 1]  # Normal vector for the field lens
        P5 = [self.galvo_gap, 180, 170]  # Position of the field lens
        self.refract(n5, P5)  # Simulate refraction at the field lens

        # Step 5: Intersection with the focusing plane (Final output point)
        n = [0, 0, 1]  # Normal vector of the plane
        P = [self.galvo_gap, 180, 170-self.focus_distance]
        intersection_point = self.ray.interaction(n, P)

        return intersection_point



