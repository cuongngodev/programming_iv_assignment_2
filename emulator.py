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
        self.employee: Optional[int] = None # hold current temporary values
        self.inputs: list[int] = inputs
        self.finished: bool = False
        self.process_size: int = len(executable)
        self.input_index: int = 0
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
        # run code until reaching the end of code
        if self.pc >= self.process_size:
            self.finished = True
            return

        self.run_opcodes[self.executable[self.pc]]()
        self.pc += 1

    def inbox(self):
        # keep reading input when the input stream is not empty
        if self.input_index < len(self.inputs):
            # Read the next input value
            self.employee = self.inputs[self.input_index]
            self.input_index += 1  # Move to the next input
        else:
            # terminate the program
            self.finished = True

    def outbox(self):
        if self.employee is not None:
            print(self.employee) # print value
            self.employee = None  # clears the employee register
        else:
            # error raised when trying to output with nothing in my hand
            self.finished = True
            raise TypeError("Employee is not holding anything!")

    def copyto(self):
        # move to the operand
        self.pc += 1

        address = self.executable[self.pc]
        # Question: do we need to check if the address is out of bound?
        if self.employee is None:
            raise TypeError("Employee is not holding anything!")
        if address >= len(self.floor_mat):
            raise IndexError("Address out of range!")
        self.floor_mat[address] = self.employee

    def copyto_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]
        self.floor_mat[address] = self.employee

    # checked
    def copyfrom(self):
        self.pc += 1
        address = self.executable[self.pc]

        if address >= len(self.floor_mat):
            raise IndexError("Address out of range!")

        # copy value from memory to employee
        if self.floor_mat[address] is None: # value at the address is none
            raise ValueError("Address is not holding anything to copy from!")
        self.employee = self.floor_mat[address]

    def copyfrom_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]
        self.employee = self.floor_mat[address]

    def add(self):
        # check if employee holds something
        if self.employee is None:
            raise TypeError("Employee is not holding anything!")
        self.pc += 1

        # if there is nothing in the address to add to, raise exception
        address = self.executable[self.pc]
        if address >= len(self.floor_mat):
            raise IndexError("Address out of range!")

        # if nothing in the address
        if self.floor_mat[address] is None:
            raise ValueError("Address is not holding anything to add!")
        self.employee += self.floor_mat[address]

    def add_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]

        self.employee += self.floor_mat[address]  # Add memory value to employee (pointer)

    def sub(self):
        # check if employee holds something
        if self.employee is None:
            raise TypeError("Employee is not holding anything!")
        self.pc += 1

        # if there is nothing in the address to subtract, raise exception
        address = self.executable[self.pc]
        if address >= len(self.floor_mat):
            raise IndexError("Address out of range!")

        # if nothing in the address
        if self.floor_mat[address] is None:
            raise ValueError("Address is not holding anything to subtract!")

        self.employee -= self.floor_mat[address]

    def sub_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]
        self.employee -= self.floor_mat[address]

    def bumpup(self):
        self.pc += 1
        address = self.executable[self.pc]

        if self.floor_mat[address] is None:
            raise ValueError("Address is not holding anything to bump up!")

        # bump the current value up
        self.floor_mat[address] += 1
        self.employee = self.floor_mat[address]

    def bumpup_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]
        self.floor_mat[address] += 1

    def bumpdown(self):
        self.pc += 1
        address = self.executable[self.pc]

        if self.floor_mat[address] is None:
            raise ValueError("Address is not holding anything to bump down!")
        # self.employee -= 1
        self.floor_mat[address] -= 1
        self.employee = self.floor_mat[address]   # Update employee register

    def bumpdown_pt(self):
        self.pc += 1
        address = self.floor_mat[self.executable[self.pc]]
        self.floor_mat[address] -= 1  # Decrement memory value (pointer)
        self.employee = self.floor_mat[address]  # Update employee register

    def jump(self):
        # check if employee holds something

        self.pc += 1
        self.pc = self.executable[self.pc]  # Set PC to the jump address

        # if the address where jump to is out of floor mat
        if self.pc >= len(self.floor_mat):
            raise IndexError("Address out of range!")

        # jump to address and continue
        self.run_opcodes[self.executable[self.pc]]()

    def jumpz(self):
        if self.employee == 0:
            self.pc += 1
            self.pc = self.executable[self.pc]  # Jump if employee is zero

            # if the address where jump to is out of floor mat
            if self.pc >= len(self.floor_mat):
                raise IndexError("Address out of range!")

            # start jumping
            self.run_opcodes[self.executable[self.pc]]()
        else:
            self.pc +=1


    def jumpn(self):
        if self.employee < 0:
            self.pc += 1
            self.pc = self.executable[self.pc]

            # if the address where jump to is out of floor mat
            if self.pc >= len(self.floor_mat):
                raise IndexError("Address out of range!")
            # start jumping
            self.run_opcodes[self.executable[self.pc]]()
        else:
            self.pc +=1


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
