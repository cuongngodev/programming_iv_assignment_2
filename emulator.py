import sys
from typing import Callable, Optional, TextIO

# ============================================================================
# Definitions
# ============================================================================
OPERAND = int | str
OPCODE_NUMBER = int
PROGRAM_COUNTER = int
MEMORY_ADDRESS = int

# ============================================================================
# Machine
# ============================================================================
class Machine:
    def __init__(self, executable: list[OPCODE_NUMBER | OPERAND], inputs: list[int], debug_info = None):

        self.pc: PROGRAM_COUNTER = 0
        self.floor_mat: list[Optional[int]] = [None] * 24
        self.executable: list[OPCODE_NUMBER | OPERAND] = executable
        self.employee: Optional[int] = None
        self.inputs: list[int] = inputs
        self.finished: bool = False
        self.process_size: int = len(executable)

        # ------------------------------------------------------------------------
        # setup instruction table
        # ------------------------------------------------------------------------
        self.run_opcodes: list[Callable[[Machine], None]] = [
            lambda x: None,  # no operation
            self.inbox,
            self.outbox,
            self.copyto,
            self.copyto_pt,
            self.copyfrom,
            self.copyfrom_pt,
            self.add,
            self.add_pt,
            self.sub,
            self.sub_pt,
            self.bumpup,
            self.bumpup_pt,
            self.bumpdown,
            self.bumpdown_pt,
            self.jump,
            self.jumpz,
            self.jumpn,
        ]

    def process_next_instruction(self):
        if self.pc >= self.process_size:
            self.finished = True
            return
        self.run_opcodes[self.executable[self.pc]]()

    def inbox(self):
        pass

    def outbox(self):
        pass

    def copyto(self):
        pass

    def copyto_pt(self):
        pass

    def copyfrom(self):
        pass

    def copyfrom_pt(self):
        pass

    def add(self):
        pass

    def add_pt(self):
        pass

    def sub(self):
        pass

    def sub_pt(self):
        pass

    def bumpup(self):
        pass

    def bumpup_pt(self):
        pass

    def bumpdown(self):
        pass

    def bumpdown_pt(self):
        pass

    def jump(self):
        pass

    def jumpz(self):
        pass

    def jumpn(self):
        pass

    def __str__(self):
        result = f"Program Counter:  {self.pc:03d}\n"
        result += f"Employee:        {self.employee}\n"
        result += f"Memory:          {self.floor_mat}"
        return result

    def __repr__(self):
        return f"PC: {self.pc}, Walker: {self.employee}"


# ============================================================================
# emulate
# ============================================================================
def emulate(exe_file, input_file):

    # ------------------------------------------------------------------------
    # run code
    # ------------------------------------------------------------------------
    code_fh = open(exe_file, "r")
    code: list[int] = list(map(int, [line for line in code_fh.readlines() if line.strip() != ""]))
    inputs_fh = open(input_file, "r")
    inputs: list[int] = list(map(int, [line for line in inputs_fh.readlines() if line.strip() != ""]))
    code_fh.close()
    inputs_fh.close()

    machine = Machine(code, inputs)
    while not machine.finished:
        machine.process_next_instruction()


# ============================================================================
# Entry point
# ============================================================================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 filename.out machine_input.txt")
    else:
        exe_filename = sys.argv[1]
        input_filename = sys.argv[2]
        emulate(exe_filename, input_filename)
