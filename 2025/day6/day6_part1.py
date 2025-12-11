import sys

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip())

    return lines

def parse(lines: list[str]):
    num_cols = len(lines[0].split())
    list_of_list_of_numbers: list[list[int]] = [[] for _i in range(num_cols)]

    operations: list[str] = []
    for i in range(len(lines)):
        if i == len(lines) - 1:
            operations.extend(lines[i].split())
        else:
            for index, number in enumerate(lines[i].split()):
                list_of_list_of_numbers[index].append(int(number))

    return list_of_list_of_numbers, operations

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

    return curr_value


curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"The answer is {day6(curr_file)}")
