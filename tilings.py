import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d


def apothem(s, n):
    """Finds apothem (distance from polygon center to side midpoint) for n-gon with side length s."""
    return s*0.5/np.tan(np.pi/n)

def radius(s, n):
    """Finds radius (distance from polygon center to vertex) for n-gon with side length s."""
    return s*0.5/np.sin(np.pi/n)

def rectangular_tiling():
    return np.array([[0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2],
                     [2, 0], [2, 1], [2, 2]])

def hexagonal_tiling():
    """Hexaonal tiling with spacing of 1 between voronoi centers.

    Returns:
        [type]: [description]
    """
    size = 5
    base_hline = np.arange(size)
    vline = np.zeros(size)
    points = np.concatenate([[base_hline], [vline]]).T
    shift_right = True
    for i in range(size):
        vline = vline + np.cos(30*np.pi/180)
        if shift_right:
            hline = base_hline + 0.5
            shift_right = False
        else:
            hline = base_hline
            shift_right = True

        p = np.concatenate([[hline], [vline]]).T
        points = np.concatenate([points, p])

    return points

def altair_tiling():
    # https://krazydad.com/slitherlink/altair.png
    s = 1 # side length
    size = 4  # number of octagons in a major row

    # Octagonal center to pentagonal center
    oct2pent = apothem(s, 8) + apothem(s, 5)
    pent2square = s*0.8 + radius(s, 5)
    oct2hex = apothem(s, 8) + apothem(s, 6)  # this is at a pi/4 angle
    oct2hex_proj = oct2hex*np.sqrt(2)  # prjection to horizontal axis

    square2hept = apothem(s, 4) + apothem(s, 7)  #  I don't think the heptagon is regular, so this might fail
    sqaure2hept_proj = square2hept*np.sqrt(2)

    # Octagons
    oct_spacing_maj = (oct2pent + pent2square)*2
    base_hline = np.arange(size) * oct_spacing_maj
    vline = np.zeros(size)
    oct_points = alternate_grid_pattern(size, vline, oct_spacing_maj, base_hline)

    # Squares
    base_hline = np.arange(size) * oct_spacing_maj - oct_spacing_maj/2
    vline = np.zeros(size)
    square_points = alternate_grid_pattern(size, vline, oct_spacing_maj, base_hline)

    # Pentagons
    pent_points = []
    for p in oct_points:
        # add one on each orthogonal direction
        perturbations = np.array([[0, oct2pent], [0, -oct2pent], [oct2pent, 0], [-oct2pent, 0]])
        for pent in perturbations:
            pent_points.append(pent + p)
    pent_points = np.array(pent_points)

    # Hexagons
    hex_points = []
    for p in oct_points:
        # add one on each orthogonal direction
        perturbations = np.array([[oct2hex_proj, oct2hex_proj], [-oct2hex_proj, oct2hex_proj], [oct2hex_proj, -oct2hex_proj], [-oct2hex_proj, -oct2hex_proj]])
        for pent in perturbations:
            hex_points.append(pent + p)
    hex_points = np.array(hex_points)

    # Heptagons
    hept_points = []
    for p in square_points:
        # add one on each orthogonal direction
        perturbations = np.array([[sqaure2hept_proj, sqaure2hept_proj], [-sqaure2hept_proj, sqaure2hept_proj], [sqaure2hept_proj, -sqaure2hept_proj], [-sqaure2hept_proj, -sqaure2hept_proj]])
        for pent in perturbations:
            hept_points.append(pent + p)
    hept_points = np.array(hept_points)

    points = np.concatenate([square_points, oct_points, hex_points, pent_points, hept_points])
    return points

def alternate_grid_pattern(size, vline, spacing, base_hline):
    points = np.concatenate([[base_hline], [vline]]).T
    shift_right = True
    for i in range(size):
        vline = vline + spacing/2
        if shift_right:
            hline = base_hline + spacing/2
            shift_right = False
        else:
            hline = base_hline
            shift_right = True

        p = np.concatenate([[hline], [vline]]).T
        points = np.concatenate([points, p])
    return points


def main():
    points = rectangular_tiling()
    points = hexagonal_tiling()
    points = altair_tiling()
    vor = Voronoi(points)
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    ax.axis('equal')
    voronoi_plot_2d(vor, ax=ax)
    plt.show()


if __name__ == '__main__':
    main()

