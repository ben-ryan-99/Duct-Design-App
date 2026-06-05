import math

CONNECTION_TOLERANCE = 10


# Returns the distance between two points
def point_distance(x1,y1,x2,y2):
    return math.sqrt(
        (x2 - x1) ** 2 +
        (y2 - y1) ** 2
    )

# Returns whether two segments are connected
def segments_connected(seg1, seg2):
    endpoints1 = [
        (seg1["x1"], seg1["y1"]),
        (seg1["x2"], seg1["y2"]),
    ]

    endpoints2 = [
        (seg2["x1"], seg2["y1"]),
        (seg2["x2"], seg2["y2"]),
    ]

    for p1 in endpoints1:
        for p2 in endpoints2:
            if (
                point_distance(
                    p1[0],
                    p1[1],
                    p2[0],
                    p2[1],
                )
                <= CONNECTION_TOLERANCE
            ):
                return True
    return False

# Depth first search function
def dfs(segment_id, adjacency, visited, current_path):
    
    visited.add(segment_id)

    current_path.append(segment_id)

    for neighbor in adjacency.get(segment_id,[]):
        if neighbor not in visited:
            dfs(
                neighbor,
                adjacency,
                visited,
                current_path
            )