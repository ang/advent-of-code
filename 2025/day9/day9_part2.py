# Right now I iterate through all the points
# If I find a matching perimeter, I can skip through some points

import sys
import dataclasses
from enum import Enum
import functools

class PointValue(str, Enum):
    NOTHING = "."
    RED_TILE = "#"
    RECTANGLE = "O"

@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int
    value: PointValue = PointValue.NOTHING

@dataclasses.dataclass(frozen=True)
class Perimeter:
    tile1: Point
    tile2: Point

@dataclasses.dataclass(frozen=True)
class RectangleArea:
    tile1: Point
    tile2: Point
    area: int

Grid = dict[int, dict[int, PointValue]]

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    return lines

def parse(lines: list[str]) -> list[Point]:
    red_tiles: list[Point] = []

    for line in lines:
        x_str, y_str = line.split(',')
        x = int(x_str)
        y = int(y_str)
        red_tiles.append(Point(x, y, PointValue.RED_TILE))

    return red_tiles

def day(file_name, is_print_grid=False):
    lines = open_file(file_name)
    red_tiles = parse(lines)
    perimeters = build_perimeter(red_tiles)

    areas = calculate_areas(red_tiles)
    areas_sorted = sorted(areas, key=lambda a: a.area, reverse=True)
    largest_area = get_largest_area(areas_sorted, perimeters)

    if (largest_area):
        tile1 = largest_area.tile1
        tile2 = largest_area.tile2
        print(f"The largest area is {largest_area.area} with {tile1=} and {tile2=}")

def build_perimeter(red_tiles: list[Point]) -> list[Perimeter]:
    perimeters: list[Perimeter] = []

    for index, red_tile in enumerate(red_tiles):
        next_tile_index = index + 1
        if index == len(red_tiles) - 1:
            next_tile_index = 0

        perimeters.append(
            Perimeter(
                red_tile,
                red_tiles[next_tile_index]
            )
        )

    return perimeters


def calculate_areas(red_tiles: list[Point]) -> list[RectangleArea]:
    areas: list[RectangleArea] = []

    for index, tile1 in enumerate(red_tiles):
        for tile2 in red_tiles[index + 1:]:
            if tile1 != tile2:
                areas.append(create_rectangle_area(tile1, tile2))

    return areas

def get_largest_area(sorted_areas: list[RectangleArea], perimeters: list[Perimeter]) -> RectangleArea | None:
    perimeters_tuple = tuple(perimeters)
    for area in sorted_areas:
        if can_create_rectangle(area.tile1, area.tile2, perimeters_tuple):
            return area

    return None

@functools.cache
def can_create_rectangle(tile1: Point, tile2: Point, perimeters: tuple[Perimeter, ...]) -> bool:
    smallest_x = tile1.x
    largest_x = tile2.x
    smallest_y = tile1.y
    largest_y = tile2.y

    if smallest_x > largest_x:
        smallest_x, largest_x = largest_x, smallest_x
    if smallest_y > largest_y:
        smallest_y, largest_y = largest_y, smallest_y

    print(f"{tile1=}, {tile2=}")

    corners_good = (
        can_create_for_x_y(smallest_x, smallest_y, perimeters) and
        can_create_for_x_y(largest_x, largest_y, perimeters) and
        can_create_for_x_y(smallest_x, largest_y, perimeters) and
        can_create_for_x_y(largest_x, smallest_y, perimeters)
    )

    if not corners_good:
        return False

    for y in range(smallest_y + 1, largest_y + 1):
        for x in range(smallest_x + 1, largest_x + 1):
            print(f"{x=}, {y=}. {largest_x=} {largest_y=}")
            if not can_create_for_x_y(x, y, perimeters):
                return False

    test_param(smallest_x, largest_y, smallest_y, largest_y, perimeters)

    return True


def test_param(smallest_x: int, largest_x: int, smallest_y: int, largest_y: int, perimeters: tuple[Perimeter, ...]) -> bool:
    top_perimeters: list[Perimeter] = []
    for perimeter in perimeters:
        left_x = perimeter.tile1.x
        right_x = perimeter.tile2.x
        top_y = perimeter.tile1.y
        bottom_y = perimeter.tile2.y

        if left_x > right_x:
            left_x, right_x = right_x, left_x
        if top_y > bottom_y:
            top_y, bottom_y = bottom_y, top_y

        if (smallest_x <= right_x or left_x <= largest_x) and (top_y <= smallest_y):
            top_perimeters.append(perimeter)

    for perimeter in top_perimeters:
        print(perimeter)
    return False






@functools.cache
def can_create_for_x_y(x: int, y: int, perimeters: tuple[Perimeter, ...]) -> bool:
    top_perimeter: Perimeter | None = None
    bottom_perimeter: Perimeter | None = None
    left_perimeter: Perimeter | None = None
    right_perimeter: Perimeter | None = None

    for perimeter in perimeters:
        # TODO don't need to calculate this all the time
        left_x = perimeter.tile1.x
        right_x = perimeter.tile2.x
        top_y = perimeter.tile1.y
        bottom_y = perimeter.tile2.y

        if left_x > right_x:
            left_x, right_x = right_x, left_x
        if top_y > bottom_y:
            top_y, bottom_y = bottom_y, top_y

        if left_x <= x and x <= right_x and y >= top_y:
            top_perimeter = perimeter
        if left_x <= x and x <= right_x and y <= bottom_y:
            bottom_perimeter = perimeter
        if left_x <= x and top_y <= y and y <= bottom_y:
            left_perimeter = perimeter
        if x <= right_x and top_y <= y and y <= bottom_y:
            right_perimeter = perimeter

    return bool(top_perimeter and bottom_perimeter and left_perimeter and right_perimeter)


def create_rectangle_area(tile1: Point, tile2: Point) -> RectangleArea:
    length = abs(tile1.x - tile2.x) + 1
    width = abs(tile1.y - tile2.y) + 1
    area = int(length * width)

    return RectangleArea(tile1, tile2, area)

def print_grid(grid: Grid, red_tiles: list[Point]):
    largest_x = 0
    largest_y = 0
    for red_tile in red_tiles:
        if red_tile.x > largest_x:
            largest_x = red_tile.x
        if red_tile.y > largest_y:
            largest_y = red_tile.y

    output = ""
    for y in range(0, largest_y + 1):
        for x in range(0, largest_x + 1):
            output += grid.get(y, {}).get(x, PointValue.NOTHING)
        output += "\n"

    print(output)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
is_print_grid = True if len(sys.argv) > 2 and sys.argv[2] == "--print" else False
print(f"{day(curr_file, is_print_grid)}")
