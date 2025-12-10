import dataclasses
from collections import defaultdict
import sys

MAX_JOLTAGE = 9

@dataclasses.dataclass(frozen=True)
class ProductIdRange:
    start: int
    end: int

@dataclasses.dataclass(frozen=True)
class BatteryIndex:
    joltage: int
    index: int

type Bank = list[int]

def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line)

    return lines

def parse(lines: list[str]) -> list[Bank]:
    banks: list[Bank] = []
    for line in lines:
        batteries = list(line)
        bank = []
        for battery in batteries:
            if not battery == "\n":
                bank.append(int(battery))

        banks.append(bank)

    return banks

def day3(file_name):
    lines = open_file(file_name)
    banks = parse(lines)

    total_joltage = 0
    for bank in banks:
        highest_joltage = get_highest_joltage(bank)
        total_joltage += highest_joltage

        bank_str = "".join([str(i) for i in bank])

        print(f"In {bank_str}, the largest joltage possible: {highest_joltage}")

    return total_joltage

def get_highest_joltage(bank: Bank, num_batteries: int = 12) -> int:
    # Create hash of value -> list[index]
    # Then go from 9 to 0
    # Check how many numbers there are behind it by looking at the index, if there are enough, add it to the battery list
    joltage_to_indicies: dict[int, list[int]] = defaultdict(list)

    for i in range(0, len(bank)):
        joltage_to_indicies[bank[i]].append(i)

    for indicies in joltage_to_indicies.values():
        indicies.sort()

    joltages: list[int] = []
    joltage_indicies: set[int] = set()
    curr_index = 0
    curr_joltage = MAX_JOLTAGE

    while len(joltages) < num_batteries and curr_joltage >= 0:
        found_joltage = False
        if indicies := joltage_to_indicies.get(curr_joltage):
            for index in indicies:
                is_before_current_index = index >= curr_index
                spaces_behind_index_count = len(bank) - index
                batteries_to_fill_count = num_batteries - len(joltages)
                is_enough_batteries = spaces_behind_index_count >= batteries_to_fill_count
                is_already_used_battery = index in joltage_indicies


                if is_before_current_index and is_enough_batteries and not is_already_used_battery:
                    found_joltage = True
                    joltages.append(curr_joltage)
                    joltage_indicies.add(index)
                    curr_index = index
                    break

        if found_joltage:
            curr_joltage = MAX_JOLTAGE
        else:
            curr_joltage -= 1


    highest_joltage_strs = "".join([str(joltage) for joltage in joltages])
    return int(highest_joltage_strs)

curr_file = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"
print(f"Total output joltage: {day3(curr_file)}")
