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
    0b000: {0b00: "[bx + si]", 0b01: "[bx + si {0} {1}]", 0b10: "[bx + si {0} {1}]"},
    0b001: {0b00: "[bx + di]", 0b01: "[bx + di {0} {1}]", 0b10: "[bx + di {0} {1}]"},
    0b010: {0b00: "[bp + si]", 0b01: "[bp + si {0} {1}]", 0b10: "[bp + si {0} {1}]"},
    0b011: {0b00: "[bp + di]", 0b01: "[bp + di {0} {1}]", 0b10: "[bp + di {0} {1}]"},
    0b100: {0b00: "[si]", 0b01: "[si + {0} {1}]", 0b10: "[si {0} {1}]"},
    0b101: {0b00: "[di]", 0b01: "[di + {0} {1}]", 0b10: "[di {0} {1}]"},
    0b110: {0b00: "NotImplemented", 0b01: "[bp {0} {1}]", 0b10: "[bp {0} {1}]"},
    0b111: {0b00: "[bx]", 0b01: "[bx {0} {1}]", 0b10: "[bx {0} {1}]"},
}


def reg_mem_to_from_reg(op: str, d: int, w: int, mod: int, reg: int, r_m: int, disp: int | None = None):
    """Register/memory to/from register."""

    if mod == 0b00:
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod]
        elif d == 0:
            dest = REGMEM[r_m][mod]
            src = REG[reg][w]

    elif mod == 0b01:
        assert disp is not None
        sign = "+"
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod].format(sign, disp)
        elif d == 0:
            dest = REGMEM[r_m][mod].format(sign, disp)
            src = REG[reg][w]

    elif mod == 0b10:
        assert disp is not None
        sign = "+"
        if d == 1:
            dest = REG[reg][w]
            src = REGMEM[r_m][mod].format(sign, disp)

    elif mod == 0b11:
        if d == 1:
            dest = REG[reg][w]
            src = REG[r_m][w]
        elif d == 0:
            dest = REG[r_m][w]
            src = REG[reg][w]

    return f"{op} {dest}, {src}\n"


def imm_to_reg(op: str, w: int, reg: int, data: int):
    """Immediate to register."""
    dest = REG[reg][w]
    src = data
    return f"{op} {dest}, {src}\n"


def imm_to_reg_mem(op: str, w, mod, r_m, disp=None, *, data):
    """Immediate to register/memory."""
    dest = REGMEM[r_m][mod]
    if mod in [0b01, 0b10]:
        sign = "+"
        dest = REGMEM[r_m][mod].format(sign, disp)
    if w == 0b0:
        src = f"byte {data}"
    elif w == 0b1:
        src = f"word {data}"

    return f"{op} {dest}, {src}\n"
