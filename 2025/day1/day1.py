import sys
import dataclasses

START = 50
MAX_NUMBER = 100

@dataclasses.dataclass(frozen=True)
class Rotation:
    isRight: bool
    amount: int

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line)

    return lines

def parse(lines: list[str]) -> list[Rotation]:
    rotations: list[Rotation] = []
    for line in lines:
        isRight = line[0] == "R"
        amount = int(line[1:])
        rotations.append(Rotation(isRight, amount))

    return rotations

def day1(file_name):
    lines = open_file(file_name)
    rotations = parse(lines)

    zero_count = 0
    passed_zero_count = 0
    current = START
    print(f"The dial starts by pointing at {current}.")
    for rotation in rotations:
        isRight = rotation.isRight
        amount = rotation.amount

        current_passed_zero_count = 0

        unmodified_new_current = current + amount if isRight else current - amount

        if unmodified_new_current == 0:
            zero_count += 1
        else:
            current_passed_zero_count = 0
            if isRight:
                current_passed_zero_count = int(unmodified_new_current / MAX_NUMBER)
            elif unmodified_new_current < 0:
                current_passed_zero_count = int((abs(unmodified_new_current) + MAX_NUMBER) / MAX_NUMBER)
                if current == 0:
                    current_passed_zero_count -= 1

            passed_zero_count += current_passed_zero_count

        current = unmodified_new_current % MAX_NUMBER

        rotate_string = "R" if isRight else "L"
        output = f"The dial is rotated {rotate_string}{amount} to point at {current}."

        if current_passed_zero_count:
            output += f" During this rotation, it points at zero {current_passed_zero_count} times."
        print(output)

    return zero_count + passed_zero_count

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"The password is {day1(curr_file)}")
