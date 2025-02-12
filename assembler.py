import re
import sys
import os

# ============================================================================
# Definitions
# ============================================================================
OPERAND = int | str
OPCODE_NUMBER = int
OPCODE_SIZE = int
OPCODE = tuple[OPCODE_NUMBER, OPCODE_SIZE]
PROGRAM_COUNTER = int
CODE_LINE = str
LABEL = str
SYMBOL_NAME = str
MEMORY_ADDRESS = int
LINE_NUMBER = int
MNEMONIC = str

DEFAULT_PATH = "./Testing/"

mnemonics: dict[MNEMONIC, OPCODE] = {
    "INBOX": (3, 1),
    "OUTBOX": (5, 1),
    "COPYTO": (3, 2),
    "COPYTO_PT": (4, 2),
    "COPYFROM": (5, 2),
    "COPYFROM_PT": (6, 2),
    "ADD": (7, 2),
    "ADD_PT": (8, 2),
    "SUB": (9, 2),
    "SUB_PT": (10, 2),
    "BUMPUP": (11, 2),
    "BUMPUP_PT": (12, 2),
    "BUMPDOWN": (13, 2),
    "BUMPDOWN_PT": (14, 2),
    "JUMP": (15, 2),
    "JUMPZ": (16, 2),
    "JUMPN": (17, 2)
}

# ============================================================================
# global variables
# ============================================================================
executable: list[OPCODE_NUMBER | OPERAND] = []
symbol_table: dict[SYMBOL_NAME, MEMORY_ADDRESS] = {}
jump_table: dict[LABEL, PROGRAM_COUNTER] = {}


# ============================================================================
# assembly
# ============================================================================
def assemble(file_name):
    executable.clear()
    symbol_table.clear()
    jump_table.clear()

    code = open(file_name, "r").readlines()
    process(code)
    file_name = os.path.basename(file_name)
    executable_file = DEFAULT_PATH + file_name[:file_name.find(".")] + ".out"
    executable_fh = open(executable_file, "w")
    for word in executable:
        print(word, file=executable_fh)
    executable_fh.close()


def process(code):
    # read source

    # create a list of instruction, it saves all instructions from the source
    instructions: list[MNEMONIC | OPERAND] = []

    # process human code.
    for line in code:
        instructions.append(line.strip())

    for instruction in instructions:
        human_code = instruction.split()
        mnemonic = human_code[0]
        executable.append(mnemonics[mnemonic][0])
        print(mnemonics[mnemonic][0])
    print(executable)




# ============================================================================
# Entry point
# ============================================================================
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python3 assembler.py filename")
    # else:
    #     filename = sys.argv[1]
    #     assemble(filename)
    filename = "Testing/InOut.hrm"
    assemble(filename)
