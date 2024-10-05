from pathlib import Path
from sim8086.part1.operations import mov

OPCODES = {0b100010: mov}


def decode(file: Path):
    with open(file, "rb") as f:
        data = f.read()

    output = f"; {file.name} disassembly:\n"
    output += "bits 16\n"

    for i in range(0, len(data), 2):
        opcode = data[i] >> 2
        d = (data[i] >> 1) & 0b1
        w = data[i] & 0b1
        mod = data[i + 1] >> 6
        reg = (data[i + 1] >> 3) & 0b111
        rm = data[i + 1] & 0b111

        output += OPCODES[opcode](d, w, mod, reg, rm)

    return output
