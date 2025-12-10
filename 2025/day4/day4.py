import sys
import typing
from day4types import Point, PaperMap, Updater, NeighborsUpdater, SelfUpdater

PAPER = "@"
NOTHING = "."
MOVEABLE_PAPER = "x"
MAX_MOVEABLE_NEIGHBOR_COUNT = 4

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip())

    return lines

def parse(lines: list[str]) -> PaperMap:
    paperMap: PaperMap = []

    for y in range(len(lines)):
        paperMap.append([])
        line = lines[y]
        for x in range(len(line)):
            paperMap[y].append(Point(line[x], x, y))

    return paperMap

def day4(file_name):
    lines = open_file(file_name)
    paper_map = parse(lines)

    print("Initial state:")
    print_map(paper_map, True)

    neighbors_updater = NeighborsUpdater()
    self_updater = SelfUpdater()

    update_map(paper_map, neighbors_updater, add_to_neighbors_count)

    # Loop

    moveable = 1 # dumb init value to kick things off
    moveable_total = 0
    while moveable != 0:
        # Given a point, only mark point with an x
        update_map(paper_map, self_updater, mark_as_moveable)

        moveable = count_moveable(paper_map)
        moveable_total += moveable
        print(f"Remove {moveable} rolls of paper:")
        print_map(paper_map, printValues=True)

        update_map(paper_map, neighbors_updater, remove_neighbors_count)

        update_map(paper_map, self_updater, remove_paper)


    return moveable_total

def update_map(paper_map: PaperMap, updater: Updater, update_func):
    for y in range(len(paper_map)):
        for x in range(len(paper_map[y])):
            point = paper_map[y][x]
            updater.update(paper_map, point, update_func)

def update_neighbors(paper_map: PaperMap, curr_point: Point, update_func: typing.Callable):
    for y in range(curr_point.y - 1, curr_point.y + 2):
        for x in range(curr_point.x - 1, curr_point.x + 2):
            if is_valid_location(x, y, paper_map):
                update_func(paper_map, curr_point, paper_map[y][x])

def add_to_neighbors_count(paper_map: PaperMap, curr_point: Point, neighbor_point: Point):
    is_self = neighbor_point.y == curr_point.y and neighbor_point.x == curr_point.x

    if not is_self and curr_point.value == PAPER:
        neighbor_point.neighbors_count += 1


def mark_as_moveable(paper_map: PaperMap, curr_point: Point):
    if is_moveable(curr_point):
        curr_point.value = MOVEABLE_PAPER


def is_valid_location(x: int, y: int, paper_map: PaperMap) -> bool:
    return (
        y >= 0 and y < len(paper_map)
        and
        x >= 0 and x < len(paper_map[y])
    )


def is_moveable(point: Point) -> bool:
    return point.value == PAPER and point.neighbors_count < MAX_MOVEABLE_NEIGHBOR_COUNT

def count_moveable(paper_map: PaperMap) -> int:
    moveable = 0
    for y in range(len(paper_map)):
        for x in range(len(paper_map[y])):
            if paper_map[y][x].value == MOVEABLE_PAPER:
                moveable += 1

    return moveable

def remove_neighbors_count(paper_map: PaperMap, curr_point: Point, neighbor_point: Point):
    is_self = neighbor_point.y == curr_point.y and neighbor_point.x == curr_point.x

    if curr_point.value == MOVEABLE_PAPER and not is_self:
        neighbor_point.neighbors_count -= 1

def remove_paper(paper_map: PaperMap, curr_point: Point):
    if curr_point.value == MOVEABLE_PAPER:
        curr_point.value = NOTHING

def print_map(paperMap: PaperMap, printValues: bool = False):
    output = ""
    for y in range(len(paperMap)):
        for x in range(len(paperMap[y])):
            point = paperMap[y][x]
            if printValues:
                output += point.value
            elif is_moveable(point):
                output += MOVEABLE_PAPER
            else:
                output += point.value
        output += "\n"

    print(output)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"Number rolls of paper that can be accessed by forklift: {day4(curr_file)}")
