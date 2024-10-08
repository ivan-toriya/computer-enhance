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
    0b000: {0b00: "[bx + si]", 0b01: "[bx + si + {}]", 0b10: "[bx + si + {}]"},
    0b001: {0b00: "[bx + di]", 0b01: "[bx + di + {}]", 0b10: "[bx + di + {}]"},
    0b010: {0b00: "[bp + si]", 0b01: "[bp + si + {}]", 0b10: "[bp + si + {}]"},
    0b011: {0b00: "[bp + di]", 0b01: "[bp + di + {}]", 0b10: "[bp + di + {}]"},
    0b100: {0b00: "[si]", 0b01: "[si + {}]", 0b10: "[si + {}]"},
    0b101: {0b00: "[di]", 0b01: "[di + {}]", 0b10: "[di + {}]"},
    0b110: {0b00: "NotImplemented", 0b01: "[bp + {}]", 0b10: "[bp + {}]"},
    0b111: {0b00: "[bx]", 0b01: "[bx + {}]", 0b10: "[bx + {}]"},
}


def mov(d, w, mod, reg, r_m, disp_lo=None, disp_hi=None):
    """Move register/memory to/from register."""

    if mod == 0b00:
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod]
        elif d == 0:
            dest = REGMEM[r_m][mod]
            src = REG[reg][w]

    elif mod == 0b01:
        assert disp_lo is not None
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod].format(disp_lo)
        elif d == 0:
            dest = REGMEM[r_m][mod].format(disp_lo)
            src = REG[reg][w]

    elif mod == 0b10:
        assert disp_lo is not None
        assert disp_hi is not None
        # "concatenate" disp_hi and disp_lo
        disp = (disp_hi << 8) | disp_lo
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod].format(disp)

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


def imm_mov(w, reg, data):
    """Immediate to register MOV."""
    dest = REG[reg][w]
    src = data
    return f"mov {dest}, {src}\n"
