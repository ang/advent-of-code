import dataclasses
import sys

@dataclasses.dataclass(frozen=True)
class ProductIdRange:
    start: int
    end: int

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line)

    return lines

def parse(lines: list[str]) -> list[ProductIdRange]:
    productIdRanges: list[ProductIdRange] = []
    for line in lines:
        ranges = line.split(',')
        for curr_range in ranges:
            start, end = curr_range.split('-')
            productIdRanges.append(ProductIdRange(int(start), int(end)))

    return productIdRanges

def day2(file_name):
    lines = open_file(file_name)
    product_id_ranges = parse(lines)

    invalid_ids = []
    for product_id_range in product_id_ranges:
        num_invalid_ids = 0
        curr_invalid_ids = []

        for i in range(product_id_range.start, product_id_range.end + 1):
            if is_invalid_id(i):
                curr_invalid_ids.append(i)

        invalid_ids.extend(curr_invalid_ids)

        print(f"{product_id_range.start}-{product_id_range.end} has {num_invalid_ids} invalid IDs: {curr_invalid_ids}")

    return sum(invalid_ids)

def is_invalid_id(id: int) -> bool:
    str_id = str(id)
    part_size = 1
    while part_size <= len(str_id) / 2:
        parts = []
        curr_index = 0
        while curr_index < len(str_id):
            parts.append(str_id[curr_index:curr_index + part_size])
            curr_index += part_size

        parts_match = len(set(parts)) == 1
        if parts_match:
            return True

        part_size += 1

    return False




curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"Adding up all the invalid ids: {day2(curr_file)}")
