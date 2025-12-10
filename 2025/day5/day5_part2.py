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

def parse(lines: list[str]) -> list[Range]:
    ranges: list[Range] = []
    process_ranges = True
    for line in lines:
        if not line:
            process_ranges = False
            break
        elif process_ranges:
            start_str, end_str = line.split('-')
            ranges.append(Range(int(start_str), int(end_str)))
        else:
            ingredients.append(int(line))

    return ranges


def day5(file_name):
    lines = open_file(file_name)
    ranges = parse(lines)

    # Sort the ranges first, by start, and then ends
    sorted_ranges = sorted(ranges, key=lambda curr_range: [curr_range.start, curr_range.end])

    print(sorted_ranges)
    combined_ranges = merge_ranges(sorted_ranges)
    print(combined_ranges)

    fresh_ingredients_count = 0
    for curr_range in combined_ranges:
        fresh_ingredients_count += curr_range.end - curr_range.start + 1

    return fresh_ingredients_count

def merge_ranges(ranges: list[Range]) -> list[Range]:
    combined_ranges: list[Range] = []

    combined_ranges.append(ranges[0])

    combined_range_index = 0
    iterating_range_index = 1
    while iterating_range_index < len(ranges):
        curr_range = combined_ranges[combined_range_index]
        next_range = ranges[iterating_range_index]

        if curr_range.end >= next_range.start:
            new_range = Range(curr_range.start, max(curr_range.end, next_range.end))
            print(f"{new_range=}")
            combined_ranges[combined_range_index] = new_range
        else:
            combined_ranges.append(next_range)
            combined_range_index += 1

        iterating_range_index += 1

    return combined_ranges

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"There are {day5(curr_file)} fresh ingredient ids")
