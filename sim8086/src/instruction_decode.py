from pathlib import Path
from sim8086.src.operations import mov, imm_mov

OPCODES = {0b100010: mov, 0b1011: imm_mov}


def decode(file: Path):
    """Decoding .asm instructions from an assembled binary file."""

    with open(file, "rb") as f:
        instuctions = f.read()

    output = f"; {file.name} disassembly:\n"
    output += "bits 16\n"

    p = 0
    while p < len(instuctions):
        print(format(instuctions[p], "#010b"))

        if (opcode := instuctions[p] >> 4) == 0b1011:  # immediate to register
            w = (instuctions[p] >> 3) & 0b1
            reg = instuctions[p] & 0b111

            if w == 0:
                print(format(instuctions[p + 1], "#010b"))
                data = instuctions[p + 1]
                p += 2
            elif w == 1:
                print(format(instuctions[p + 1], "#010b"), format(instuctions[p + 2], "#010b"))
                data = (instuctions[p + 2] << 8) | instuctions[p + 1]
                p += 3

            output += OPCODES[opcode](w, reg, data)

        elif (opcode := instuctions[p] >> 2) == 0b100010:  # reg/mem to/from reg
            d = (instuctions[p] >> 1) & 0b1
            w = instuctions[p] & 0b1
            print(format(instuctions[p + 1], "#010b"))
            mod = instuctions[p + 1] >> 6
            reg = (instuctions[p + 1] >> 3) & 0b111
            r_m = instuctions[p + 1] & 0b111

            if mod in [0b11, 0b00]:
                output += OPCODES[opcode](d, w, mod, reg, r_m)
                p += 2
            elif mod == 0b01:
                print(format(instuctions[p + 2], "#010b"))
                disp_lo = instuctions[p + 2]
                output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo)
                p += 3
            elif mod == 0b10:
                print(format(instuctions[p + 2], "#010b"))
                disp_lo = instuctions[p + 2]
                print(format(instuctions[p + 3], "#010b"))
                disp_hi = instuctions[p + 3]
                output += OPCODES[opcode](d, w, mod, reg, r_m, disp_lo, disp_hi)
                p += 4
        else:
            raise NotImplementedError("Opcode not implemented")

        print("^ decoded ^")
        print("=== OUTPUT ===")
        print(output)
        print("=== END ===")

    return output
