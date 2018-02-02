from __future__ import division


def simplify(coords, first, last, sqTolerance):
    """calculate simplification data using optimized
    Douglas-Peucker algorithm"""

    maxSqDist = sqTolerance
    index = None

    ax = coords[first]
    ay = coords[first + 1]
    bx = coords[last]
    by = coords[last + 1]

    for i in range(first + 3, last, 3):
        d = getSqSegDist(coords[i], coords[i + 1], ax, ay, bx, by)
        if d > maxSqDist:
            index = i
            maxSqDist = d

    if maxSqDist > sqTolerance:
        if index - first > 3:
            simplify(coords, first, index, sqTolerance)
        coords[index + 2] = maxSqDist
        if last - index > 3:
            simplify(coords, index, last, sqTolerance)


def getSqSegDist(px, py, x, y, bx, by):
    """square distance from a point to a segment"""

    dx = bx - x
    dy = by - y

    if dx != 0 or dy != 0:
        t = ((px - x) * dx + (py - y) * dy) / (dx * dx + dy * dy)

        if t > 1:
            x = bx
            y = by

        elif t > 0:
            x += dx * t
            y += dy * t

    dx = px - x
    dy = py - y

    return dx * dx + dy * dy
