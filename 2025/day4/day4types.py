from abc import ABC, abstractmethod
import dataclasses

@dataclasses.dataclass
class Point:
    value: str
    x: int
    y: int
    neighbors_count: int = 0

PaperMap = list[list[Point]]

class Updater(ABC):
    @staticmethod
    def update(paper_map: PaperMap, curr_point: Point, update_func):
        pass

class NeighborsUpdater(Updater):
    @staticmethod
    def update(paper_map: PaperMap, curr_point: Point, update_func):
        for y in range(curr_point.y - 1, curr_point.y + 2):
            for x in range(curr_point.x - 1, curr_point.x + 2):
                if NeighborsUpdater.is_valid_location(x, y, paper_map):
                    update_func(paper_map, curr_point, paper_map[y][x])

    @staticmethod
    def is_valid_location(x: int, y: int, paper_map: PaperMap) -> bool:
        return (
            y >= 0 and y < len(paper_map)
            and
            x >= 0 and x < len(paper_map[y])
        )

class SelfUpdater(Updater):
    @staticmethod
    def update(paper_map: PaperMap, curr_point: Point, update_func):
        update_func(paper_map, curr_point)
