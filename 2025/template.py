import sys

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip())

    return lines

def parse(lines: list[str]):
    for line in lines:
        pass

def day(file_name):
    lines = open_file(file_name)
    data = parse(lines)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"{day(curr_file)}")
