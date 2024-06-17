def mov(d, w, mod, reg, rm):
    if mod != 0b11:
        raise NotImplementedError("The mode is not implemented.")

    reg = REGS[reg][w]
    rm = REGS[rm][w]

    if d == 1:
        dest = reg
        src = rm
    elif d == 0:
        dest = rm
        src = reg

    print(f"mov {dest}, {src}")


OPCODES = {0b100010: mov}
REGS = {
    0b000: ["al", "ax"],
    0b001: ["cl", "cx"],
    0b010: ["dl", "dx"],
    0b011: ["bl", "bx"],
    0b100: ["ah", "sp"],
    0b101: ["ch", "bp"],
    0b110: ["dh", "si"],
    0b111: ["bh", "di"],
}


def decode(file: bytes):
    for i in range(0, len(file), 2):
        opcode = file[i] >> 2
        d = (file[i] >> 1) & 0b1
        w = file[i] & 0b1
        mod = file[i + 1] >> 6
        reg = (file[i + 1] >> 3) & 0b111
        rm = file[i + 1] & 0b111

        # for _ in [opcode, d, w, mod, reg, rm]:
        #     print(bin(_), end=" ")
        # print("")

        OPCODES[opcode](d, w, mod, reg, rm)


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "rb") as f:
        file = f.read()

    print(f"; {f.name} disassembly:")
    print("bits 16")
    decode(file)
