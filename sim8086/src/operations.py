# (REG) Register Field Encoding
REG = {
    0b000: ["al", "ax"],
    0b001: ["cl", "cx"],
    0b010: ["dl", "dx"],
    0b011: ["bl", "bx"],
    0b100: ["ah", "sp"],
    0b101: ["ch", "bp"],
    0b110: ["dh", "si"],
    0b111: ["bh", "di"],
}

# R/M (Register/Memory) Field Encoding
REGMEM = {
    0b000: {0b00: "[bx + si]", 0b01: "[bx + si]"},
    0b001: {0b00: "[bx + di]", 0b01: "[bx + di]"},
    0b010: {0b00: "[bp + si]", 0b01: "[bp + si]"},
    0b011: {0b00: "[bp + di]", 0b01: "[bp + di]"},
    0b100: {0b00: "[si]", 0b01: "[si]"},
    0b101: {0b00: "[di]", 0b01: "[di]"},
    0b110: {0b00: "NotImplemented", 0b01: "[bp + {}]"},
    0b111: {0b00: "[bx]", 0b01: "[bx]"},
}


def mov(d, w, mod, reg, r_m, dist_lo=None, dist_hi=None):
    """Move register/memory to/from register."""

    if mod == 0b00:
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod]
        elif d == 0:
            dest = REGMEM[r_m][mod]
            src = REG[reg][w]
    elif mod == 0b01:
        assert dist_lo is not None
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod].format(dist_lo)
        elif d == 0:
            dest = REGMEM[r_m][mod].format(dist_lo)
            src = REG[reg][w]
    elif mod == 0b11:
        if d == 1:
            dest = REG[reg][w]
            src = REG[r_m][w]
        elif d == 0:
            dest = REG[r_m][w]
            src = REG[reg][w]
    else:
        raise NotImplementedError("The mode is not implemented.")

    return f"mov {dest}, {src}\n"
