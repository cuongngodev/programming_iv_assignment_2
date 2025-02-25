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
    "INBOX": (1, 1),
    "OUTBOX": (2, 1),
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
    """
    Assembles the human-readable assembly code from the specified file into machine code.
    :param file_name: The name of file to assemble.
    """
    executable.clear()
    symbol_table.clear()
    jump_table.clear()

    code = open(file_name, "r").readlines()
    listing: [str] = process(code)
    file_name = os.path.basename(file_name)
    executable_file = DEFAULT_PATH + file_name[:file_name.find(".")] + ".out"
    listing_file = DEFAULT_PATH + file_name[:file_name.find(".")] + ".listing"

    with open(listing_file, "w") as listing_file:
        listing_file.writelines("Address  Opcode  Operand   Code\n")
        listing_file.writelines(listing)
    executable_fh = open(executable_file, "w")
    for word in executable:
        print(word, file=executable_fh)
    executable_fh.close()

def identify_labels(code):
    """
    Identifies labels in the assembly code and stores their program counter values in the jump_table.
    :param code: The assembly code as a list of strings.
    """
    pc: PROGRAM_COUNTER = 0
    for line in code:
        line = line.strip()

        # ignore empty lines and comments
        if not line or line.startswith("#"):
            continue

        # lines contain label
        if ":" in line:
            # extract the label name
            label = line.split(":")[0].strip()
            # store the label and its PC
            jump_table[label] = pc
        else:
            mnemonic: MNEMONIC = line.split()[0]
            # increment the PC by the size of the instruction
            pc += mnemonics[mnemonic][1]
def convert_hrm_to_code(code) -> [str]:
    """
    Converts the HRM assembly code to machine code.
    :param code: The assembly code as a list of strings.
    """
    pc: PROGRAM_COUNTER = 0
    memory_address: MEMORY_ADDRESS = 0
    listing: [str] = []
    operand_str: str = ""

    for line in code:
        line = line.strip()

        if not line or line.startswith("#"):
            listing.append(' ' * 27 + line + "\n")
            continue
        if ':' in line:  # when encounter label
            listing.append(' ' * 27 + line + "\n")
            continue

        # parts -> (mnemonic and operand)
        parts = line.split()
        mnemonic: MNEMONIC = parts[0]

        opcode, size = mnemonics[mnemonic]
        executable.append(opcode)

        # if opcode requires operand, then process
        if size == 2:
            operand = parts[1]

            # If the operand is a label (for jump instructions)
            if operand in jump_table:
                # replace it with the corresponding PC value from the jump_table.
                operand = jump_table[operand]

            # check if operand is a variable name (x, y, z, ...)
            elif operand.isidentifier():
                if operand not in symbol_table:
                    # allocate a new memory address for the variable
                    symbol_table[operand] = memory_address
                    memory_address += 1
                # replace operand with its memory address
                operand = symbol_table[operand]
            else:
                # if operand is a number.
                operand = int(operand)

            # add operand to the executable list
            executable.append(int(operand))
            operand_str = f"{operand:06d}"
        else:
            operand_str = " " * 6
        listing_line: str = f"{pc}        {opcode:06d}  {operand_str}    {line} \n"
        listing.append(listing_line)
        # update the pc by the size
        pc += size
    return listing

def process(code) -> [str]:
    """
    Processes the assembly code to generate machine codes.
    :param code: The assembly code as a list of strings.
    """

    # 1st: identify labels and their addresses
    identify_labels(code)

    # 2nd: convert hrm to machine code
    return convert_hrm_to_code(code)

# ============================================================================
# Entry point
# ============================================================================
if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("Usage: python3 assembler.py filename")
    # else:
    #     filename = sys.argv[1]
    #     assemble(filename)
    filename = "Testing/JumpZMultiply.hrm"
    assemble(filename)
