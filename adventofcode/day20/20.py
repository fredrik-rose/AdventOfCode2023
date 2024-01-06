# Day 20: Pulse Propagation
import collections as coll
import copy
import dataclasses
import os
import pathlib


from adventofcode.algorithm import algo


@dataclasses.dataclass
class Module:
    inputs: list
    outputs: list
    kind: str


def part_one(modules):
    state = create_state(modules)
    lows = 0
    highs = 0
    for _ in range(1000):
        l, h, __ = simulate(modules, state)
        lows += l
        highs += h
    answer = lows * highs
    print(f"Part one: {answer}")


def part_two(modules):
    print_graph(modules)
    broadcaster_oututs = modules["broadcaster"].outputs
    ends = modules[modules["rx"].inputs[0]].inputs
    answer = 1
    cycles = []
    for start in broadcaster_oututs:
        state = create_state(modules)
        modules["broadcaster"].outputs = [start]
        for step in range(1, 100000):
            _, __, outputs_low = simulate(modules, state, ends)
            if outputs_low:
                cycles.append(step)
                break
        else:
            assert False
        modules["broadcaster"].outputs = broadcaster_oututs
    answer = algo.lcm(cycles)
    print(f"Part two: {answer}")


def parse(file_path):
    inputs = coll.defaultdict(list)
    outputs = coll.defaultdict(list)
    kinds = {"rx": None}
    with open(file_path) as file:
        for line in file:
            line = line.strip()
            module, connections = line.split(" -> ")
            connections = connections.split(", ")
            if module == "broadcaster":
                kind = None
            else:
                kind = module[0]
                module = module[1:]
            kinds[module] = kind
            outputs[module] = connections
            for c in connections:
                inputs[c].append(module)
    modules = {
        module: Module(inputs[module], outputs[module], kind)
        for module, kind in kinds.items()
    }
    return modules


def create_state(modules):
    state = {}
    for name, module in modules.items():
        if module.kind == "%":
            state[name] = False
        elif module.kind == "&":
            state[name] = {c: False for c in module.inputs}
        else:
            assert module.kind is None
    return state


def simulate(modules, state, ends=None):
    lows = 1  # Include the low from the button press.
    highs = 0
    outputs_low = False
    queue = coll.deque(
        ("broadcaster", c, False) for c in modules["broadcaster"].outputs
    )
    while queue:
        sender, receiver, pulse = queue.popleft()
        if pulse:
            highs += 1
        else:
            lows += 1
        if ends and receiver in ends and not pulse:
            outputs_low = True
        kind = modules[receiver].kind
        if kind == "%":
            # If a flip-flop module receives a high pulse, it is ignored and nothing happens.
            # However, if a flip-flop module receives a low pulse, it flips between on and off.
            # If it was off, it turns on and sends a high pulse. If it was on, it turns off and
            # sends a low pulse.
            if not pulse:
                state[receiver] = not state[receiver]
                new_pulse = state[receiver]
                for c in modules[receiver].outputs:
                    queue.append((receiver, c, new_pulse))
        elif kind == "&":
            # When a pulse is received, the conjunction module first updates its memory for that
            # input. Then, if it remembers high pulses for all inputs, it sends a low pulse;
            # otherwise, it sends a high pulse.
            state[receiver][sender] = pulse
            new_pulse = not all(state[receiver].values())
            for c in modules[receiver].outputs:
                queue.append((receiver, c, new_pulse))
        else:
            assert kind is None
            continue
    return lows, highs, outputs_low


def print_graph(modules):
    with open("graph.dot", "w") as file:
        file.write("digraph graphname {\n")
        for name, module in modules.items():
            shape = {
                "%": "rectangle",
                "&": "diamond",
                None: "doublecircle",
            }[modules[name].kind]
            file.write(f'    {name} [label="{name}", shape={shape}];\n')
            for c in module.outputs:
                file.write(f"    {name} -> {c};\n")
        file.write("}\n")


def main():
    modules = parse(pathlib.Path(os.path.dirname(__file__)) / "input.txt")
    part_one(copy.deepcopy(modules))
    part_two(copy.deepcopy(modules))


if __name__ == "__main__":
    main()
