'''
Copyright (c) 2024, HUST All rights reserved

File Name: test_mechanical_error_distribution.py
Summary:
    This file contains a simulation of point distribution in a multi-axis galvanometer system, with mechanical errors taken into account. The code generates a 2D distribution map of intersection points for rays passing through the system, taking into account mechanical errors that affect the positioning of the ray. The results are saved to a CSV file for further analysis and visualization.

Running Environment: Python 3.6

Modification Description:
    This file simulates the behavior of a ray passing through a multi-axis galvanometer system and calculates the points of intersection. The test accounts for mechanical errors, generating a point distribution map that is stored in a CSV file. The results can be visualized in a 2D plot.

Current Version: 1.0

Modified By: Tianz

Modification Details:
    - Implemented ray tracing simulation using multi-axis galvanometer.
    - Added point distribution generation based on mechanical error simulation.
    - Stored the results in CSV format for easier analysis and visualization.
    - Visualized the results using 2D plotting.

Modification Date: [Insert Date]

Original Author: Tianz

Completion Date: 2024.06.21
'''


# This test file is used to generate a distribution map of points under mechanical error conditions.

import GalvoGeo.MutiAxisParam as MA  # Import multi-axis galvanometer parameter module
import RayData.Ray as ry  # Import Ray class for ray-tracing simulations
import numpy as np  # Import numpy for numerical operations
import Draw.DrawFile as df  # Import draw module to visualize the points
import csv  # Import csv module to save data in CSV format


def test(num):
    intersection_point_list = []  # List to store the intersection points of the ray with the system

    # Initialize a ray with an initial position and direction
    initial_position = [0, 0, 0]  # Starting position of the ray (origin)
    initial_direction = [0, 1, 0]  # Direction of the ray (in the positive Y-axis direction)
    ray = ry.Ray(initial_position, initial_direction)  # Create the Ray object with the given initial conditions

    # Initialize the multi-axis galvanometer with focus distance and gap between mirrors
    focus_distance = 165  # The focus distance (example value)
    galvo_gap = 13.05  # The gap between the galvanometer mirrors (example value)
    mag = MA.MultiAxisGalvanometer(focus_distance, galvo_gap)  # Create a MultiAxisGalvanometer object

    # Set the ray for the galvanometer system
    mag.set_ray(ray)

    # Generate a grid of X and Y values using linspace for a range of values, equally spaced
    valuex = np.linspace(-11, 11, num)  # Create an array of X values from -11 to 11, with `num` points
    valuey = np.linspace(-11, 11, num)  # Create an array of Y values from -11 to 11, with `num` points

    # Iterate over each point in the generated grid (valuex, valuey)
    for i in valuex:
        for j in valuey:
            ray = ry.Ray(initial_position, initial_direction)  # Re-initialize the ray for each point in the grid
            mag = MA.MultiAxisGalvanometer(focus_distance, galvo_gap)  # Re-initialize the multi-axis galvanometer
            mag.set_ray(ray)  # Set the new ray for the system

            # Trace the ray through the system for the given X and Y angles (i, j)
            intersection_point = mag.trace(i, j)
            intersection_point_list.append(intersection_point)  # Store the intersection points

    P1 = [galvo_gap, 180, 5]  # A point on the plane (arbitrary chosen for reference)
    A = np.array(P1)  # Convert the point to a numpy array for easy vector operations

    # Subtract the reference point (A) from each intersection point to calculate the relative position
    realresult = [point - A for point in intersection_point_list]  # Perform element-wise subtraction

    # Save the results to a CSV file
    # Specify the path for the CSV file where the results will be saved
    csv_file_path = "realpoint_draw.csv"  # File name for storing the result data

    # Write the data to the CSV file
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)  # Create a CSV writer object
        # Write the header row, with column names: X, Y, Z
        writer.writerow(['X', 'Y', 'Z'])
        # Write the actual data points
        for point in realresult:
            writer.writerow(point)

    print("CSV file has been created:", csv_file_path)  # Print a message indicating the CSV file creation

    # Visualize the result by plotting the 2D points (X, Y positions)
    df.plot_2d_points(realresult)  # Plot the points using the drawing module
