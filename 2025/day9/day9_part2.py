import sys
import dataclasses

@dataclasses.dataclass(frozen=True)
class Point:
    x: int
    y: int

@dataclasses.dataclass(frozen=True)
class Perimeter:
    # tile1 is always more "left" and more "up" than tile1
    tile1: Point
    tile2: Point

@dataclasses.dataclass(frozen=True)
class RectangleArea:
    tile1: Point
    tile2: Point
    area: int

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
        red_tiles.append(Point(x, y))

    return red_tiles

def day(file_name):
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

        tile1 = red_tile
        tile2 = red_tiles[next_tile_index]

        if not (tile1.x <= tile2.x and tile1.y <= tile2.y):
            tile1, tile2 = tile2, tile1

        perimeters.append(Perimeter(tile1, tile2))

    return perimeters


def calculate_areas(red_tiles: list[Point]) -> list[RectangleArea]:
    areas: list[RectangleArea] = []

    for index, tile1 in enumerate(red_tiles):
        for tile2 in red_tiles[index + 1:]:
            if tile1 != tile2:
                areas.append(create_rectangle_area(tile1, tile2))

    return areas

def get_largest_area(sorted_areas: list[RectangleArea], perimeters: list[Perimeter]) -> RectangleArea | None:
    for area in sorted_areas:
        smallest_x = area.tile1.x
        largest_x = area.tile2.x
        smallest_y = area.tile1.y
        largest_y = area.tile2.y

        if smallest_x > largest_x:
            smallest_x, largest_x = largest_x, smallest_x
        if smallest_y > largest_y:
            smallest_y, largest_y = largest_y, smallest_y

        if can_create_rectangle(smallest_x, largest_x, smallest_y, largest_y, perimeters):
            return area

    return None

def can_create_rectangle(smallest_x: int, largest_x: int, smallest_y: int, largest_y: int, perimeters: list[Perimeter]) -> bool:
    top_perimeters: list[Perimeter] = []
    bottom_perimeters: list[Perimeter] = []
    left_perimeters: list[Perimeter] = []
    right_perimeters: list[Perimeter] = []
    for perimeter in perimeters:
        tile1 = perimeter.tile1
        tile2 = perimeter.tile2

        if (smallest_x <= tile2.x and tile1.x <= largest_x) and (tile1.y <= smallest_y):
            top_perimeters.append(perimeter)
        if (smallest_x <= tile2.x and tile1.x <= largest_x) and (largest_y <= tile2.y):
            bottom_perimeters.append(perimeter)
        if (tile1.x <= smallest_x) and (smallest_y <= tile2.y and tile1.y <= largest_y):
            left_perimeters.append(perimeter)
        if (largest_x <= tile2.x) and (smallest_y <= tile2.y and tile1.y <= largest_y):
            right_perimeters.append(perimeter)

    print("******")
    if not has_top_bottom(smallest_x, largest_x, top_perimeters):
        return False
    if not has_top_bottom(smallest_x, largest_x, bottom_perimeters):
        return False

    if not has_left_right(smallest_y, largest_y, left_perimeters):
        return False
    if not has_left_right(smallest_y, largest_y, right_perimeters):
        return False

    return True

def has_top_bottom(smallest_x: int, largest_x: int, perimeters: list[Perimeter]) -> bool:
    if not perimeters:
        return False

    sorted_perimeters = sorted(perimeters, key=lambda p: p.tile1.x)
    perimeter_x_start = sorted_perimeters[0].tile1.x
    perimeter_x_end = perimeter_x_start

    for perimeter in sorted_perimeters:
        if (perimeter_x_end >= perimeter.tile1.x):
            perimeter_x_end = max(perimeter_x_end, perimeter.tile2.x)

        if (perimeter_x_end >= largest_x):
            break

    print(f"top/bottom: {perimeter_x_start=} <= {smallest_x=} and {largest_x=} <= {perimeter_x_end=}")

    return perimeter_x_start <= smallest_x and largest_x <= perimeter_x_end


def has_left_right(smallest_y: int, largest_y: int, perimeters: list[Perimeter]) -> bool:
    if not perimeters:
        return False

    sorted_perimeters = sorted(perimeters, key=lambda p: p.tile1.y)
    perimeter_y_start = sorted_perimeters[0].tile1.y
    perimeter_y_end = perimeter_y_start

    for perimeter in sorted_perimeters:
        if (perimeter_y_end >= perimeter.tile1.y):
            perimeter_y_end = max(perimeter_y_end, perimeter.tile2.y)

        if (perimeter_y_end >= largest_y):
            break

    print(f"left/right: {perimeter_y_start=} <= {smallest_y=} and {largest_y=} <= {perimeter_y_end=}")

    return perimeter_y_start <= smallest_y and largest_y <= perimeter_y_end



def create_rectangle_area(tile1: Point, tile2: Point) -> RectangleArea:
    length = abs(tile1.x - tile2.x) + 1
    width = abs(tile1.y - tile2.y) + 1
    area = int(length * width)

    return RectangleArea(tile1, tile2, area)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"{day(curr_file)}")
