import sys
import typing
import dataclasses
from enum import Enum

class PointValue(str, Enum):
    NOTHING = "."
    START = "S"
    SPLITTER = "^"
    TACHYON_BEAM = "|"

@dataclasses.dataclass
class Point:
    value: PointValue
    x: int
    y: int
    has_been_split: bool = False

TachyonManifold = list[list[Point]]

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
            manifold[y].append(Point(point_value, x, y))

    return manifold


def day(file_name):
    lines = open_file(file_name)
    manifold = parse(lines)

    return fire_beam(manifold)

def fire_beam(manifold: TachyonManifold) -> int:
    stats: list[int] = []
    for point in manifold[0]:
        stats.append(0)

    start_point: Point | None = None
    for point in manifold[0]:
        if point.value == PointValue.START:
            start_point = point
            stats[start_point.x] += 1
            manifold[start_point.y + 1][start_point.x].value = PointValue.TACHYON_BEAM
            break

    if not start_point:
        return 0

    for points in manifold:
        for point in points:
            if point.value == PointValue.TACHYON_BEAM:
                fire_single_beam(point, manifold, stats)
                print_manifold(manifold)
                print(stats)

    print_manifold(manifold)
    print(stats)

    return sum(stats)

def fire_single_beam(point: Point, manifold: TachyonManifold, stats: list[int]):
    next_point = point_from_location(point.x, point.y+1, manifold)
    if next_point:
        if next_point.value == PointValue.SPLITTER:
            next_point_left = point_from_location(next_point.x-1, next_point.y, manifold)
            next_point_right = point_from_location(next_point.x+1, next_point.y, manifold)

            if next_point_left:
                stats[next_point_left.x] += stats[point.x]
                next_point_left.value = PointValue.TACHYON_BEAM
            if next_point_right:
                stats[next_point_right.x] += stats[point.x]
                next_point_right.value = PointValue.TACHYON_BEAM

            stats[point.x] = 0
        else:
            next_point.value = PointValue.TACHYON_BEAM

def point_from_location(x: int, y: int, manifold: TachyonManifold) -> Point | None:
    if is_valid_location(x, y, manifold):
        return manifold[y][x]
    return None

def is_valid_location(x: int, y: int, manifold: TachyonManifold):
    return x < len(manifold[0]) and y < len(manifold)

def print_manifold(manifold: TachyonManifold):
    output = ""
    for points in manifold:
        for point in points:
            output += point.value
        output += "\n"

    print(output)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"{day(curr_file)}")
