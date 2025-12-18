import sys
import dataclasses
from enum import Enum

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

    grid = make_grid(red_tiles)

    if is_print_grid:
        print_grid(grid, red_tiles)

    areas = calculate_areas(red_tiles)
    areas_sorted = sorted(areas, key=lambda a: a.area, reverse=True)

    if is_print_grid:
        add_rectangle(grid, areas_sorted[0])
        print_grid(grid, red_tiles)

    largest_area = areas_sorted[0]
    tile1 = largest_area.tile1
    tile2 = largest_area.tile2
    print(f"The largest area is {largest_area.area} with {tile1=} and {tile2=}")


def make_grid(red_tiles: list[Point]) -> Grid:
    grid: Grid = {}

    for red_tile in red_tiles:
        if red_tile.y not in grid:
            grid[red_tile.y] = {}
        grid[red_tile.y][red_tile.x] = PointValue.RED_TILE

    return grid

def calculate_areas(red_tiles: list[Point]) -> list[RectangleArea]:
    areas: list[RectangleArea] = []

    for index, tile1 in enumerate(red_tiles):
        for tile2 in red_tiles[index + 1:]:
            if tile1 != tile2:
                areas.append(create_rectangle_area(tile1, tile2))

    return areas

def create_rectangle_area(tile1: Point, tile2: Point) -> RectangleArea:
    length = abs(tile1.x - tile2.x) + 1
    width = abs(tile1.y - tile2.y) + 1
    area = int(length * width)

    return RectangleArea(tile1, tile2, area)

def add_rectangle(grid: Grid, rectangle: RectangleArea):
    smallest_x = sorted([rectangle.tile1.x, rectangle.tile2.x])[0]
    largest_x = sorted([rectangle.tile1.x, rectangle.tile2.x], reverse=True)[0]

    smallest_y = sorted([rectangle.tile1.y, rectangle.tile2.y])[0]
    largest_y = sorted([rectangle.tile1.y, rectangle.tile2.y], reverse=True)[0]

    for y in range(smallest_y, largest_y + 1):
        for x in range(smallest_x, largest_x + 1):
            if y not in grid:
                grid[y] = {}

            grid[y][x] = PointValue.RECTANGLE

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
