import sys
import re

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    return lines

def parse(lines: list[str]) -> tuple[list[list[int]], list[str]]:
    list_of_list_of_numbers: list[list[int]] = []

    operations: list[str] = lines[-1].split()

    # TODO: I assumed the lines were all equal

    x = 0
    while x < len(lines[0]):
        starting_x = x
        number_width = get_number_width(x, lines[-1])

        # Get all numbers for a given operator
        curr_list: list[int] = []
        list_of_list_of_numbers.append(curr_list)
        while x < starting_x + number_width:
            number_str = ""
            for y in range(len(lines) - 1):
                number_str += lines[y][x]
                
            clean_number_str = re.sub(r"\s+", "", number_str)
            number = int(clean_number_str) if clean_number_str else 0
            curr_list.append(number)

            x += 1

        x += 1 # One more move because of the separator
        print(f"{number_width=}, {curr_list=}")

    return list_of_list_of_numbers, operations

def get_number_width(x: int, operator_line: str) -> int:
    width = 1
    curr_index = x + width
    while curr_index < len(operator_line) and operator_line[curr_index] not in ["*", "+"]:
        width += 1
        curr_index = x + width

    # Hit the next operator, so minus a width. 
    # But if we hit the very end of the line, don't do this, we're not hitting another operator
    if curr_index != len(operator_line):
        width -= 1

    return width

def day6(file_name):
    lines = open_file(file_name)
    list_of_list_of_numbers, operations = parse(lines)

    answer = 0
    for index, numbers in enumerate(list_of_list_of_numbers):
        operation = operations[index]

        answer += calculate_numbers_list(numbers, operation)

    return answer

def calculate_numbers_list(numbers: list[int], operation: str) -> int:
    # If multiplication then start with 1
    curr_value = 0 if operation == "+" else 1

    for number in numbers:
        if operation == "+":
            curr_value += number
        else: # *
            curr_value *= number

    print(f"{numbers=} {operation=} = {curr_value}")
    return curr_value


curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"The answer is {day6(curr_file)}")
