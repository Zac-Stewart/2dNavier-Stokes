import numpy as np

def bresenham(pos0, pos1):
    x0 = pos0[0]
    y0 = pos0[1]
    x1 = pos1[0]
    y1 = pos1[1]

    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    return points

def winding(vertices):
    """
    vertices: (N,2) array or list of (x, y) tuples

    Returns:
        0 -> clockwise
        1 -> anticlockwise
    """
    v = np.asarray(vertices)

    x = v[:, 0]
    y = v[:, 1]

    area2 = np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)

    return 1 if area2 > 0 else 0