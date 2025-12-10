import sys
import dataclasses

@dataclasses.dataclass
class Range:
    start: int
    end: int

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip())

    return lines

def parse(lines: list[str]) -> tuple[list[Range], list[int]]:
    ranges: list[Range] = []
    ingredients: list[int] = []
    process_ranges = True
    for line in lines:
        if not line:
            process_ranges = False
        elif process_ranges:
            start_str, end_str = line.split('-')
            ranges.append(Range(int(start_str), int(end_str)))
        else:
            ingredients.append(int(line))

    return ranges, ingredients


def day5(file_name):
    lines = open_file(file_name)
    ranges, ingredients = parse(lines)

    fresh_ingredients_count = 0
    for ingredient in ingredients:
        is_fresh = False
        fresh_range: Range | None = None

        for curr_range in ranges:
            if curr_range.start <= ingredient and ingredient <= curr_range.end:
                is_fresh = True
                fresh_range = curr_range
                fresh_ingredients_count += 1
                break

        output = f"Ingredient ID {ingredient} is"
        if is_fresh and fresh_range:
            output += f" fresh because it falls into range {fresh_range.start}-{fresh_range.end}."
        else:
            output += " spoiled."

        print(output)

    return fresh_ingredients_count

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"{day5(curr_file)} of the ingredients are fresh")
