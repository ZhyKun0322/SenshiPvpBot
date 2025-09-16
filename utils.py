def distance(pos1, pos2):
    x1, y1, z1 = pos1
    x2, y2, z2 = pos2
    return ((x1-x2)**2 + (y1-y2)**2 + (z1-z2)**2)**0.5
