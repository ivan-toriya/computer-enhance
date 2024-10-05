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

    return f"mov {dest}, {src}\n"
