import sys
import typing
import dataclasses
from enum import Enum

class PointValue(str, Enum):
    NOTHING = "."
    START = "S"
    SPLITTER = "^"
    TACHYON_BEAM = "|"

@dataclasses.dataclass(frozen=True)
class Location:
    x: int
    y: int

@dataclasses.dataclass
class Point:
    value: PointValue
    loc: Location
    has_been_split: bool = False

TachyonManifold = list[list[Point]]

@dataclasses.dataclass
class Stats:
    split_count: int = 0

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    return lines

def parse(lines: list[str]) -> TachyonManifold:
    manifold: TachyonManifold = []

    for y in range(len(lines)):
        manifold.append([])
        line = lines[y]
        for x in range(len(line)):
            point_value = typing.cast(PointValue, line[x])
            manifold[y].append(Point(point_value, Location(x, y)))

    return manifold


def day(file_name):
    lines = open_file(file_name)
    manifold = parse(lines)

    return fire_beam(manifold)

def fire_beam(manifold: TachyonManifold) -> int:
    stats = Stats()
    start_point: Point | None = None
    for point in manifold[0]:
        if point.value == PointValue.START:
            start_point = point
            break

    if not start_point:
        return stats.split_count

    fire_single_beam(start_point, manifold, stats)

    print_manifold(manifold)
    return stats.split_count

def fire_single_beam(point: Point, manifold: TachyonManifold, stats: Stats):
    """
    Recursion is fun
    """
    next_point = point_from_location(Location(point.loc.x, point.loc.y+1), manifold)

    if next_point:
        if next_point.value == PointValue.NOTHING:
            next_point.value = PointValue.TACHYON_BEAM
            print_manifold(manifold)
            fire_single_beam(next_point, manifold, stats)
        elif next_point.value == PointValue.SPLITTER:
            next_point_left = point_from_location(Location(next_point.loc.x-1, point.loc.y), manifold)
            next_point_right = point_from_location(Location(next_point.loc.x+1, point.loc.y), manifold)

            if not next_point.has_been_split:
                stats.split_count += 1
                next_point.has_been_split = True

            if next_point_left and next_point_left.value == PointValue.NOTHING:
                fire_single_beam(next_point_left, manifold, stats)
            if next_point_right and next_point_right.value == PointValue.NOTHING:
                fire_single_beam(next_point_right, manifold, stats)

def point_from_location(location: Location, manifold: TachyonManifold) -> Point | None:
    if is_valid_location(location, manifold):
        return manifold[location.y][location.x]
    return None

def is_valid_location(location: Location, manifold: TachyonManifold):
    return location.x < len(manifold[0]) and location.y < len(manifold)

def print_manifold(manifold: TachyonManifold):
    output = ""
    for points in manifold:
        for point in points:
            output += point.value
        output += "\n"

    print(output)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"{day(curr_file)}")
