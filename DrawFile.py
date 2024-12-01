'''
Copyright (c) 2024, HUST All rights reserved

File Name: plot_2d_points.py
Summary:
    This file contains a function `plot_2d_points` that generates a 2D scatter plot of points, visualizing their distribution in the X-Y plane. The points represent transformed 3D coordinates (after subtracting the reference plane), commonly used in ray tracing simulations to visualize the intersection points on a focus plane.

Running Environment: Python 3.6 or later

Modification Description:
    The file includes a single function `plot_2d_points` that takes a list of 3D points and extracts their X and Y coordinates for plotting in a 2D scatter plot. The plot is displayed with labels for the X and Y axes, a grid for clarity, and a title indicating that the points represent a distribution on the focus plane.

Current Version: 1.0

Modified By: Tianz

Modification Details:
    - Created a function to generate a 2D scatter plot of transformed points.
    - Extracted the X and Y coordinates from a list of 3D points for visualization.
    - Added plotting labels, grid, and title to improve clarity.
    - Used `matplotlib` for plotting.

Modification Date: [Insert Date]

Original Author: Tianz

Completion Date: 2024.06.15
'''




import matplotlib.pyplot as plt


# Assuming realresult is a list of 3D points after transformation (i.e., subtraction of plane reference)
# Let's add the function to plot the 2D scatter plot from realresult.

def plot_2d_points(realresult):
    """
    Plot the realresult points in a 2D plane (X-Y plane).

    Parameters:
    - realresult: List of transformed points after subtracting the reference plane.

    This function extracts X and Y coordinates from each point in the 3D list and plots them.
    """
    # Extracting X, Y coordinates from the 3D points
    x_coords = [point[0] for point in realresult]
    y_coords = [point[1] for point in realresult]

    # Create a scatter plot of the X, Y coordinates
    plt.figure(figsize=(8, 8))
    plt.scatter(x_coords, y_coords, c='blue', marker='o', s=50)

    # Add labels and title to the plot
    plt.xlabel('X Position (mm)')
    plt.ylabel('Y Position (mm)')
    plt.title('2D Distribution of Points on the Focus Plane')

    # Optionally, show a grid
    plt.grid(True)

    # Show the plot
    plt.show()