from pathlib import Path
from sim8086.src.operations import mov

OPCODES = {0b100010: mov}


def decode(file: Path):
    """Decoding instruction from a binary file."""

    with open(file, "rb") as f:
        data = f.read()

    output = f"; {file.name} disassembly:\n"
    output += "bits 16\n"

    cursor = 0
    while cursor < len(data):
        print(format(data[cursor], "#010b"))
        opcode = data[cursor] >> 2
        d = (data[cursor] >> 1) & 0b1
        w = data[cursor] & 0b1
        print(format(data[cursor + 1], "#010b"))
        mod = data[cursor + 1] >> 6
        reg = (data[cursor + 1] >> 3) & 0b111
        r_m = data[cursor + 1] & 0b111

        if mod in [0b11, 0b00]:
            output += OPCODES[opcode](d, w, mod, reg, r_m)
            cursor += 2
        elif mod == 0b01:
            print(format(data[cursor + 2], "#010b"))
            disp_lo = data[cursor + 2]
            output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo)
            cursor += 3
        elif mod == 0b10:
            print(format(data[cursor + 2], "#010b"))
            disp_lo = data[cursor + 2]
            print(format(data[cursor + 3], "#010b"))
            disp_hi = data[cursor + 3]
            output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo, disp_hi)
            cursor += 4

        print("^ decoded ^")
        print("=== OUTPUT ===")
        print(output)
        print("=== EOF ===")

    return output
