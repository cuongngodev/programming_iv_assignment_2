import sys
from io import StringIO
from assembler import assemble
from emulator import emulate
import pytest

def test_in_out_assemble():
    assemble("Testing/InOut.hrm")
    obj_code = open("Testing/InOut.out").readlines()
    expected = open("Testing/InOut_good.out").readlines()
    assert obj_code == expected


def test_in_out_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/InOut_good.out", "Testing/_inputs_three_five.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [3, 5]


def test_swap_assemble():
    assemble("Testing/Swap.hrm")
    obj_code = open("Testing/Swap.out").readlines()
    expected = open("Testing/Swap_good.out").readlines()
    assert obj_code == expected


def test_swap_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/Swap_good.out", "Testing/_inputs_three_five.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [5, 3]


def test_bumpy_assemble():
    assemble("Testing/Bumpy.hrm")
    obj_code = open("Testing/Bumpy.out").readlines()
    expected = open("Testing/Bumpy_good.out").readlines()
    assert obj_code == expected


def test_bumpy_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/Bumpy_good.out", "Testing/_inputs_three_five.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [7, 1]


def test_add_subtract_assemble():
    assemble("Testing/AMinusBPlusC.hrm")
    obj_code = open("Testing/AMinusBPlusC.out").readlines()
    expected = open("Testing/AMinusBPlusC_good.out").readlines()
    assert obj_code == expected


def test_add_subtract_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/AMinusBPlusC_good.out", "Testing/_inputs_add_subtract.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [6]


def test_add_subtract_assemble_commented():
    assemble("Testing/AMinusBPlusC_commented.hrm")
    obj_code = open("Testing/AMinusBPlusC_commented.out").readlines()
    expected = open("Testing/AMinusBPlusC_good.out").readlines()
    assert obj_code == expected


def test_jump_unconditional_assemble():
    assemble("Testing/JumpUnconditional.hrm")
    obj_code = open("Testing/JumpUnconditional.out").readlines()
    expected = open("Testing/JumpUnconditional_good.out").readlines()
    assert obj_code == expected


def test_jump_unconditional_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/JumpUnconditional_good.out", "Testing/_inputs_three_five.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [3, 5]

def test_jumpz_multiply_assemble():
    assemble("Testing/JumpZMultiply.hrm")
    obj_code = open("Testing/JumpZMultiply.out").readlines()
    expected = open("Testing/JumpZMultiply_good.out").readlines()
    assert obj_code == expected


def test_jumpz_multiply_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/JumpZMultiply_good.out", "Testing/_inputs_three_five.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [15]

def test_jumpn_maximize_assemble():
    assemble("Testing/JumpNMaximization.hrm")
    obj_code = open("Testing/JumpNMaximization.out").readlines()
    expected = open("Testing/JumpNMaximization_good.out").readlines()
    assert obj_code == expected


def test_jumpn_maximize_run():
    output = StringIO()
    sys.stdout = output
    emulate("Testing/JumpNMaximization_good.out", "Testing/_inputs_maximization.txt")
    sys.stdout = sys.__stdout__
    result = output.getvalue()
    results = [int(v) for v in result.split() if v != ""]
    assert results == [9, -1, 5, 15, -3, -2]

def test_jumpz_multiply_symbolic_assemble():
    assemble("Testing/JumpZMultiply_Symbolic.hrm")
    obj_code = open("Testing/JumpZMultiply_Symbolic.out").readlines()
    expected = open("Testing/JumpZMultiply_good.out").readlines()
    assert obj_code == expected
