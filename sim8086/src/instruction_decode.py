from pathlib import Path
from sim8086.src.operations import mov, imm_mov

OPCODES = {0b100010: mov, 0b1011: imm_mov}


def decode(file: Path):
    """Decoding .asm instructions from an assembled binary file."""

    with open(file, "rb") as f:
        instructions = f.read()

    output = f"; {file.name} disassembly:\n"
    output += "bits 16\n"

    p = 0
    while p < len(instructions):
        print(format(instructions[p], "#010b"))

        if (opcode := instructions[p] >> 4) == 0b1011:  # immediate to register
            w = (instructions[p] >> 3) & 0b1
            reg = instructions[p] & 0b111

            if w == 0:
                print(format(instructions[p + 1], "#010b"))
                data = instructions[p + 1]
                p += 2
            elif w == 1:
                print(format(instructions[p + 1], "#010b"), format(instructions[p + 2], "#010b"))
                data = (instructions[p + 2] << 8) | instructions[p + 1]
                p += 3

            output += OPCODES[opcode](w, reg, data)

        elif (opcode := instructions[p] >> 2) == 0b100010:  # reg/mem to/from reg
            d = (instructions[p] >> 1) & 0b1
            w = instructions[p] & 0b1
            print(format(instructions[p + 1], "#010b"))
            mod = instructions[p + 1] >> 6
            reg = (instructions[p + 1] >> 3) & 0b111
            r_m = instructions[p + 1] & 0b111

            if mod in [0b11, 0b00]:
                output += OPCODES[opcode](d, w, mod, reg, r_m)
                p += 2
            elif mod == 0b01:
                print(format(instructions[p + 2], "#010b"))
                disp_lo = instructions[p + 2]
                output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo)
                p += 3
            elif mod == 0b10:
                print(format(instructions[p + 2], "#010b"))
                disp_lo = instructions[p + 2]
                print(format(instructions[p + 3], "#010b"))
                disp_hi = instructions[p + 3]
                output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo, disp_hi)
                p += 4
        else:
            raise NotImplementedError("Opcode not implemented")

        print("^ decoded ^")
        print("=== OUTPUT ===")
        print(output)
        print("=== END ===")

    return output
