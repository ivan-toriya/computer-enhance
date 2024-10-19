import subprocess
from pathlib import Path

import pytest

from sim8086.src.instruction_decode import decode
from sim8086.src.operations import reg_mem_to_from_reg


@pytest.fixture(
    scope="session",
    params=[
        "listing_0037_single_register_mov.asm",
        "listing_0038_many_register_mov.asm",
        "listing_0039_more_movs.asm",
        "listing_0040_challenge_movs.asm",
    ],
)
def assembled_instruction_path(request, tmp_path_factory):
    file: Path = tmp_path_factory.mktemp("data") / request.param
    try:
        subprocess.run(["nasm", f"tests/data/{request.param}", "-o", file], check=True)
    except FileNotFoundError:
        print("We're using `nasm` to assemble the .asm files. Have you installed it and added on PATH?")
        raise
    return file


@pytest.fixture
def mov_cx_bx():
    d = 0b0
    w = 0b1
    mod = 0b11
    reg = 0b011
    rm = 0b001
    return d, w, mod, reg, rm


@pytest.fixture
def mov_bx_cx():
    d = 0b1
    w = 0b1
    mod = 0b11
    reg = 0b011
    rm = 0b001
    return d, w, mod, reg, rm


def test_decode(assembled_instruction_path, tmp_path):
    output = decode(assembled_instruction_path)

    decoded: Path = tmp_path / (assembled_instruction_path.stem + ".asm")
    with open(decoded, "w") as f:
        f.write(output)

    reassembled: Path = tmp_path / (assembled_instruction_path.stem + ".bin")
    subprocess.run(["nasm", decoded, "-o", reassembled], check=True)

    with open(assembled_instruction_path, "rb") as f:
        original = f.read()

    with open(reassembled, "rb") as f:
        new = f.read()

    assert original == new


def test_mov_cx_bx(mov_cx_bx):
    d, w, mod, reg, rm = mov_cx_bx
    output = reg_mem_to_from_reg("mov", d, w, mod, reg, rm)
    assert output == "mov cx, bx\n"


def test_mov_bx_cx(mov_bx_cx):
    d, w, mod, reg, rm = mov_bx_cx
    output = reg_mem_to_from_reg("mov", d, w, mod, reg, rm)
    assert output == "mov bx, cx\n"
