from pathlib import Path

from sim8086.src.operations import imm_to_reg, imm_to_reg_mem, reg_mem_to_from_reg

OPS = {
    # MOVs
    0b100010: ("mov", reg_mem_to_from_reg),
    0b1100011: ("mov", imm_to_reg_mem),
    0b1011: ("mov", imm_to_reg),
    # ADDs
    0b000000: ("add", reg_mem_to_from_reg),
    0b1000001: ("add", imm_to_reg_mem),
}


def decode(file: Path):
    """Decoding .asm instructions from an assembled binary file."""

    with open(file, "rb") as f:
        instructions = f.read()

    output = f"; {file.name} disassembly:\n"
    output += "bits 16\n"

    p = 0
    while p < len(instructions):
        # print(format(instructions[p], "#010b"))

        if (opcode := instructions[p] >> 2) in OPS and OPS[opcode][1] == reg_mem_to_from_reg:  # reg/mem to/from reg
            op = OPS[opcode][0]
            d = (instructions[p] >> 1) & 0b1
            w = instructions[p] & 0b1
            # print(format(instructions[p + 1], "#010b"))
            mod = instructions[p + 1] >> 6
            reg = (instructions[p + 1] >> 3) & 0b111
            r_m = instructions[p + 1] & 0b111

            if mod in [0b11, 0b00]:
                output += reg_mem_to_from_reg(op, d, w, mod, reg, r_m)
                p += 2
            elif mod == 0b01:
                # print(format(instructions[p + 2], "#010b"))
                disp = instructions[p + 2]
                output += reg_mem_to_from_reg(op, d, w, mod, reg, r_m, disp)
                p += 3
            elif mod == 0b10:
                # print(format(instructions[p + 2], "#010b"))
                # print(format(instructions[p + 3], "#010b"))
                disp = (instructions[p + 3] << 8) | instructions[p + 2]
                output += reg_mem_to_from_reg(op, d, w, mod, reg, r_m, disp)
                p += 4

        elif (opcode := instructions[p] >> 4) in OPS and OPS[opcode][1] == imm_to_reg:  # immediate to register
            op = OPS[opcode][0]
            w = (instructions[p] >> 3) & 0b1
            reg = instructions[p] & 0b111

            if w == 0:
                # print(format(instructions[p + 1], "#010b"))
                data = instructions[p + 1]
                p += 2
            elif w == 1:
                # print(format(instructions[p + 1], "#010b"), format(instructions[p + 2], "#010b"))
                data = (instructions[p + 2] << 8) | instructions[p + 1]
                p += 3

            output += imm_to_reg(op, w, reg, data)

        elif (opcode := instructions[p] >> 1) in OPS and OPS[opcode][
            1
        ] == imm_to_reg_mem:  # immediate to register/memory
            op = OPS[opcode][0]
            w = instructions[p] & 0b1
            # print(format(instructions[p + 1], "#010b"))
            mod = instructions[p + 1] >> 6
            r_m = instructions[p + 1] & 0b111
            if w == 0:
                if mod == 0b00:
                    if r_m != 0b110:
                        data = instructions[p + 2]
                        output += imm_to_reg_mem(op, w, mod, r_m, data=data)
                        p += 3
                    else:
                        disp = (instructions[p + 3] << 8) | instructions[p + 2]
                        data = instructions[p + 4]
                        output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                        p += 5
                if mod == 0b01:
                    disp = instructions[p + 2]
                    data = instructions[p + 3]
                    output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                    p += 4
                if mod == 0b10:
                    disp = (instructions[p + 3] << 8) | instructions[p + 2]
                    data = instructions[p + 4]
                    output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                    p += 5
                if mod == 0b11:
                    data = instructions[p + 2]
                    output += imm_to_reg_mem(op, w, mod, r_m, data=data)
                    p += 3
            if w == 1:
                if mod == 0b00:
                    if r_m != 0b110:
                        data = (instructions[p + 3] << 8) | instructions[p + 2]
                        output += imm_to_reg_mem(op, w, mod, r_m, data=data)
                        p += 4
                    else:
                        disp = (instructions[p + 3] << 8) | instructions[p + 2]
                        data = (instructions[p + 5] << 8) | instructions[p + 4]
                        output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                        p += 6
                if mod == 0b01:
                    disp = instructions[p + 2]
                    data = (instructions[p + 4] << 8) | instructions[p + 3]
                    output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                    p += 5
                if mod == 0b10:
                    disp = (instructions[p + 3] << 8) | instructions[p + 2]
                    data = (instructions[p + 5] << 8) | instructions[p + 4]
                    output += imm_to_reg_mem(op, w, mod, r_m, disp, data=data)
                    p += 6
                if mod == 0b11:
                    data = (instructions[p + 3] << 8) | instructions[p + 2]
                    output += imm_to_reg_mem(op, w, mod, r_m, data=data)
                    p += 4
        else:
            raise NotImplementedError("Opcode not implemented")

        # print("^ decoded ^")
        # print("=== OUTPUT ===")
        # print(output)
        # print("=== END ===")

    return output
