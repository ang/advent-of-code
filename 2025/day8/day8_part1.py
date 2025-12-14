# Note: This one I changed it two take in two required arguments, because we
# need an additional argument for the sample vs the input.
#
# In the instructions the sample only wants 10 connection
# `python day8_part1.py sample.txt 10`
# For the normal input, we want 1000 connections
# `python day8_part1.py input.txt 1000`


import sys
import dataclasses
import math

TOP_NUMBER_OF_CIRCUITS = 3

@dataclasses.dataclass(frozen=True)
class JunctionBox:
    id: int
    x: int
    y: int
    z: int

@dataclasses.dataclass(frozen=True)
class BoxDistance:
    box1: JunctionBox
    box2: JunctionBox
    distance: float

@dataclasses.dataclass(frozen=True)
class Circuit:
    boxes: set[JunctionBox]

    def __eq__(self, other):
        return self.boxes == other.boxes

    def __hash__(self):
        hash_str = ""
        for box in self.boxes:
            hash_str += str(box.id) + "_"
        return hash(hash_str)

    def __str__(self):
        output = ""
        for box in sorted(self.boxes, key=lambda b: b.id):
            output += str(box.id) + "_"
        return output[0:-1]



def open_file(file_name: str) -> list[str]:
    lines: list[str] = []
    with open(file_name, 'r') as file:
        for line in file:
            lines.append(line.rstrip('\n'))

    return lines

def parse(lines: list[str]) -> list[JunctionBox]:
    junction_boxes: list[JunctionBox] = []
    for index, line in enumerate(lines):
        x, y, z = line.split(',')
        junction_boxes.append(JunctionBox(index, int(x), int(y), int(z)))

    return junction_boxes

def day(file_name: str, num_connections: int):
    lines = open_file(file_name)
    junction_boxes = parse(lines)

    box_distances = calculate_distances(junction_boxes)
    box_distances.sort(key=lambda box_distance: box_distance.distance)

    box_to_circuit = connect_boxes(junction_boxes, box_distances, num_connections)

    print("")

    circuits = set(box_to_circuit.values())
    top_circuits = sorted(circuits, key=lambda c: len(c.boxes), reverse=True)[0:TOP_NUMBER_OF_CIRCUITS]
    circuit_multiplied = 1
    for circuit in top_circuits:
        print(f"Circuit {circuit} len: {len(circuit.boxes)}")
        circuit_multiplied *= len(circuit.boxes)

    return circuit_multiplied

def calculate_distances(junction_boxes: list[JunctionBox]) -> list[BoxDistance]:
    box_distances: list[BoxDistance] = []

    for index, box1 in enumerate(junction_boxes):
        for box2 in junction_boxes[index + 1:]:
            if box1 != box2:
                box_distances.append(get_box_distance(box1, box2))

    return box_distances

def connect_boxes(junction_boxes: list[JunctionBox], box_distances: list[BoxDistance], num_connections: int):
    box_to_circuit: dict[JunctionBox, Circuit] = {
        box: Circuit(set([box]))
        for box in junction_boxes
    }

    for i in range(num_connections):
        box_distance = box_distances[i]
        box1 = box_distance.box1
        box2 = box_distance.box2

        box1_circuit: Circuit = box_to_circuit[box1]
        box2_circuit: Circuit = box_to_circuit[box2]

        combined_circuit = Circuit(boxes=box1_circuit.boxes | box2_circuit.boxes)

        for box in combined_circuit.boxes:
            box_to_circuit[box] = combined_circuit

        print(f"Connecting {box1=} {box2=} to make circuit: {combined_circuit}. Len: {len(combined_circuit.boxes)}")

    return box_to_circuit


def get_box_distance(box1: JunctionBox, box2: JunctionBox) -> BoxDistance:
    # https://en.wikipedia.org/wiki/Euclidean_distance
    distance = math.sqrt(
        (box1.x - box2.x) ** 2 +
        (box1.y - box2.y) ** 2 +
        (box1.z - box2.z) ** 2
    )

    return BoxDistance(box1, box2, distance)

file_name = sys.argv[1]
num_connections = int(sys.argv[2])
print(f"{day(file_name, num_connections)}")
