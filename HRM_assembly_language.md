# Human Resource Machine (HRM) Assembly Language

## Reference Manual

> This is just a subset of what is required for JAC Programming 4 class



### Registers

There is only one general purpose register: `employee`

Program counter `pc` which indicates the address of the next instruction to be executed

### Memory (`floormat`)

The memory has a maximum of 64 values

### Notes

##### `employee` opcodes

Any opcode that uses the `worker` register will ***FAIL*** if the `employee` register does not contain a value 

```python
if employee is None:
  raise TypeError("Employee is not holding anything!")
```

##### program termination

The program will terminate if an `INBOX` instruction is given, and the input stream is empty

```python
def inbox():
  try:
    employee = next(input_stream)
  exception StopIteration:
    exit()
```



### Opcodes

| Mnemonic | Opcode        | Operand   | Description                                                                                                    |
|----------|---------------|-----------|----------------------------------------------------------------------------------------------------------------|
| NOP      | `00 000` (0)  |           | no operation                                                                                                   |
| INBOX    | `00 001` (1)  |           | `employee = next(input_stream)`                                                                                |
| OUTBOX   | `00 010` (2)  |           | `print(employee)`, employee is then set to None                                                                |
| &nbsp;   |               |           |                                                                                                                |
| COPYTO   | `00 011` (3)  | address   | `floormat[address] = employee`                                                                                 |
| COPYTO   | `00 100` (4)  | [address] | `floormat[ floormat[adress] ] = employee`    *pointer arithmetic*                                              |
| COPYFROM | `00 101` (5)  | address   | `employee = floormat[address]`                                                                                 |
| COPYFROM | `00 110` (6)  | [address] | `employee = floormat[ floormat[address] ]`   *pointer arithmetic*                                              |
| ADD      | `00 111` (7)  | address   | `employee += floormat[address]`                                                                                |
| ADD      | `01 000` (8)  | [address] | `employee += floormat[ floormat[address] ]`    *pointer arithmetic*                                            |
| SUB      | `01 001` (9)  | address   | `employee -= floormat[address]`                                                                                |
| SUB      | `01 010` (10) | [address] | `employee -= floormat[ floormat[address] ]`    *pointer arithmetic*                                            |
| BUMPUP   | `01 011` (11) | address   | `floormat[address]++`                                                                                          |
| BUMPUP   | `01 100` (12) | [address] | `floormat[ floormat[address] ]++`    *pointer arithmetic*                                                      |
| BUMPDOWN | `01 101` (13) | address   | `floormat[address]--`, `employee = floormat[address]`                                                          |
| BUMPDOWN | `01 110` (14) | [address] | `floormat[ floormat[address] ]--`, `employee = floormat[address]`    *pointer arithmetic*                      |
|          |               |           |                                                                                                                |
| JUMP     | `01 111` (15) | LABEL     | Set the program counter register (`pc`) to the program address of *LABEL*                                      |
| JUMPZ    | `10 000` (16) | LABEL     | Jump if zero                                                                                                   |
| JUMPN    | `10 001` (17) | LABEL     | Jump if less than zero                                                                                         |
| ZERO     | `10 010` (18) | address   | Sets the floormat address to zero. <br>***Not part of the instruction set that the HRM machine understands.*** |



## Assembly

Each opcode takes up one `word`

Each operand takes up one `word`

***Example***

```
Address  Opcode  Operand   Code      
                          # Maximization Room
                          
                          # Grab two things from the inbox, and put only the bigger of the two in the outbox
                          # If they are equal, just pick either one.  Repeat!
                          
                          beginning:
                              # get both values
   0     000001               INBOX                   # a = input()
   1     000011 000000        COPYTO   0              # m[0] = a
   3     000001               INBOX                   # b = input()
                          
   4     001001 000000        SUB      0              # diff = b - a
                          
                              # if its negative then ...
   6     010001 001101        JUMPN negative          # if diff<0 goto negative
                          
                              # set worker back to original value
   8     000111 000000        ADD      0              # value = diff + a  (equals b)
                          
                          output:
  10     000010               OUTBOX                  # output value
  11     001111 000000        JUMP beginning          # all done, go for next input
                          
                          negative:
  13     000101 000000        COPYFROM 0              # value = a
  15     001111 001010        JUMP output

```

