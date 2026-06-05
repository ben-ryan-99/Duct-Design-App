# import modules
from dataclasses import dataclass
import math

from ductcalc.models import DuctSegment

# gloval variables
CONNECTION_TOLERANCE = 10


@dataclass
class CanvasSegment:
    id: int
    x1: float
    y1: float
    x2: float
    y2: float
    length_ft: float

# Returns the distance between two points
def point_distance(x1,y1,x2,y2):
    return math.sqrt((x2 - x1) ** 2 +(y2 - y1) ** 2)

# Returns whether two segments are connected
def segments_connected(seg1, seg2, tolerance=CONNECTION_TOLERANCE):
    endpoints1 = [(seg1.x1, seg1.y1), (seg1.x2, seg1.y2)]
    endpoints2 = [(seg2.x1, seg2.y1), (seg2.x2, seg2.y2)]

    for p1 in endpoints1:
        for p2 in endpoints2:
            if (point_distance(p1[0],p1[1],p2[0],p2[1],)<= tolerance):
                return True
    return False

# turn drawn objects intoan array of duct segment objects 
def parse_canvas_segments(objects, pixels_per_foot):
    segments = []

    for index, obj in enumerate(objects):
        if obj.get("type") != "line":
            continue

        left = obj.get("left", 0)
        top = obj.get("top", 0)

        x1 = left + obj["x1"]
        y1 = top + obj["y1"]
        x2 = left + obj["x2"]
        y2 = top + obj["y2"]

        pixel_length = point_distance(x1,y1,x2,y2)
        length_ft = pixel_length/pixels_per_foot

        segments.append(
            CanvasSegment(
                id=index,
                x1=x1,
                y1=y1,
                x2=x2,
                y2=y2,
                length_ft=length_ft,
            )
        )
    return segments

# create and return a list of duct segments
def build_canvas_duct_segments(canvas_segments, diameter_in, airflow_cfm):
    return [
        DuctSegment(
            length_ft=segment.length_ft,
            diameter_in=diameter_in,
            airflow_cfm = airflow_cfm,
        )
        for segment in canvas_segments
    ]

# determinewheter there are any connected segments in the given list of segments
def find_connections(segments,tolerance=CONNECTION_TOLERANCE):
    connections = []

    for seg1 in segments:
        for seg2 in segments:
            if seg1.id >= seg2.id:
                continue

            if segments_connected(seg1, seg2, tolerance):
                connections.append((seg1.id, seg2.id))

    return connections

# output the paths of connected segments
def group_connected_paths(connections):
    adjacency = {}

    for seg1, seg2 in connections:
        adjacency.setdefault(seg1, [])
        adjacency.setdefault(seg2, [])

        adjacency[seg1].append(seg2)
        adjacency[seg2].append(seg1)

    visited = set()
    paths = []

    for segment_id in adjacency:
        if segment_id in visited:
            continue

        current_path = []
        _dfs(segment_id, adjacency, visited, current_path)
        paths.append(current_path)

    return paths

# Depth first search function
def _dfs(segment_id, adjacency, visited, current_path):
    visited.add(segment_id)
    current_path.append(segment_id)

    for neighbor in adjacency.get(segment_id,[]):
        if neighbor not in visited:
            _dfs(neighbor,adjacency,visited,current_path)
