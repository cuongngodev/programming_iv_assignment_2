# Assignment Instructions

## Rubric

The weights are tentative.

| Part | Code Quality                 |
|------|------------------------------|
| --   | Comments                     |
| --   | Proper use of functions, etc |

| Part | Assemble and emulate                                                   | Worth |
|------|------------------------------------------------------------------------|-------|
| I    | I/O commands to/from `employee` register                               | 10    |
| II   | Copy data between memory and `employee` register                       | 10    |
| III  | Increment and decrement data in memory and copy to `employee` register | 10    |
| IV   | Add and subtract data in memory from `employee` register               | 10    |
| VI   | Unconditional jump                                                     | 10    |
| VII, | Jump if zero                                                           | 5     |
| VIII | Jump if negative                                                       | 5     |
| X    | Pointer Arithmetic Works                                               | 5     |
| --   | Displays appropriate error messages when assembling code               | 10    |

| Part | Documentation                           | Worth |
|------|-----------------------------------------|-------|
| V    | Allow comments in code                  | 10    |
| IX   | Create a listing file                   | 10    |
| XI   | Use variable names for memory addresses | 5     |



## Write an assembler and an emulator for Human Resource Machine

The assembler reads the source code and prints out the executable to standard out

The emulator will read in executable code and run the program.

**NOTE: Program ends when either of the following conditions occur**

* the end of code is reached
* the inbox is empty, but the program askes for new input

### Part I I/O: `INBOX`, `OUTBOX`

**Assembler**

Your assembler must be able to process and produce the machine code for the HRM program - InOut

```
INBOX
OUTBOX
INBOX
OUTBOX
```

Note: the machine code for this is: `1, 2, 1, 2`

**Emulator** 

If the inputs to this executable are: 

```
3
5
```

the outputs should be:

```
3
5
```



### Part II - Memory: `COPYFROM`, `COPYTO`

**Assembler**

Your assembler must be able to process and produce the machine code for the HRM program - Swap

```
INBOX
COPYTO 1
INBOX
OUTBOX
COPYFROM 1
OUTBOX
```

Note: The machine code for this is: `1, 3, 1, 1, 2, 5, 2`

**Emulator**

If the inputs to this executable are: 

```
3
5
```

the outputs should be:

```
5
3
```



### Part III - Increment/Decrement: `BUMPUP`, `BUMPDOWN`

**Assembler**

Your assembler must be able to process and produce the machine code for the HRM program - Bumpy

```
INBOX
COPYTO 1
INBOX
COPYTO 2
BUMPUP 2
BUMPUP 2
OUTBOX
BUMPDOWN 1
BUMPDOWN 1
OUTBOX
```

**Emulator**

If the inputs to this executable are: 

```
3
5
```

the outputs should be:

```
7
1
```



### Part IV - Addition Subtraction: `ADD`, `SUM`

**Assembler**

Your assembler must be able to process and produce the machine code for the HRM program - A_MINUS_B_PLUS_C

output `a - (b+c)`

```
INBOX
COPYTO 1
INBOX
COPYTO 2
INBOX
ADD 2
COPYTO 3
COPYFROM 1
SUB 3
OUTBOX
```

**Emulator**

If the inputs to this executable are: 

```
13
5
2
```

the outputs should be:

```
6
```



### Part V - Process Comments

The code should behave exactly as before, but we can add comments

```
INBOX	        # a = intput()
COPYTO 1        # store a in memory location 1
INBOX	        # b = input()
COPYTO 2        # store b in memory location 2
INBOX	        # c = input()
ADD 2	        # d = c + b
COPYTO 3        # store d in memory location 3
COPYFROM 1      # get a from memory
SUB 3	        # a = a - d
OUTBOX	        # print d
```



### Part VI - Unconditional Jumping: `JUMP`

**Assembler**

Your assembler must be able to process and produce the machine code for the HRM program - Jump

```
    JUMP b
a:
    OUTBOX
b:
    INBOX
    JUMP a
```

**Emulator**

If the inputs to this executable are: 

```
3
5
```

the outputs should be:

```
3
5
```

### Part VII - Jump if Equal to Zero: `JUMPZ`

Your assembler must be able to process and produce the machine code for the HRM program - JumpZMultiply

```
# MULTIPLY TWO NUMBERS
beginning:
    INBOX
    COPYTO   0
    INBOX
    COPYTO   1
    COPYTO   2
decrement:
    BUMPDOWN 0
    JUMPZ    result
    COPYFROM 1
    ADD      2
    COPYTO   2
    JUMP     decrement
result:
    COPYFROM 2
    OUTBOX
```

**Emulator**

If the inputs to this executable are: 

```
3
5
```

the outputs should be:

```
15
```

### Part VIII - Jump if Negative - `JUMPN`

Your assembler must be able to process and produce the machine code for the HRM program - JumpNMaximize

```
# Maximization Room

# Grab two things from the inbox,
#    and put only the bigger of the two in the outbox
# If they are equal, just pick either one.  Repeat!

beginning:
    # get both values
    INBOX                   # a = input()
    COPYTO   0              # m[0] = a
    INBOX                   # b = input()

    SUB      0              # diff = b - a

    # if its negative then ...
    JUMPN negative          # if diff<0

    # set worker back to original value
    ADD      0              # value = diff + a  (equals b)

output:
    OUTBOX                  # output value
    JUMP beginning          # all done, go for next input

negative:
    COPYFROM 0              # value = a
    JUMP output
```

Executable: `1, 3, 0, 1, 9, 0, 17, 12, 7, 0, 15, 14, 5, 0, 2, 15, 0`

### Part IX - Documentation

When assembling, create a listing file.

This file shall contain the following columns:

`address`, `opcode`,`operand`, `line number`,`code`,

where the 

* `address` is the program address,
* `opcode` is the opcode number (written in binary)
* `operand` is the value of the operand (written in binary)
* `line number` is the line number of the code
* `code` is the code

### Part X - Pointer Arithmetic

The following code sorts the input stream. 

```text
# Compiler instruction
# set memory slot 24 equal to zero before starting the execution
    ZERO     24
a:
    COPYFROM 24
    COPYTO   21
    INBOX   
    JUMP     c
b:
    COPYFROM 22
c:
    COPYTO   [21]
    COPYFROM 24
    COPYTO   20
    BUMPUP   21
    INBOX   
    JUMPZ    g
    COPYTO   22
    JUMP     f
d:
e:
    BUMPUP   20
    SUB      21
f:
    JUMPZ    b
    COPYFROM [20]
    SUB      22
    JUMPN    d
    COPYFROM [20]
    COPYTO   23
    COPYFROM 22
    COPYTO   [20]
    COPYFROM 23
    COPYTO   22
    JUMP     e
g:
    COPYTO   [21]
    COPYFROM 24
    COPYTO   20
h:
    COPYFROM [20]
    JUMPZ    a
    OUTBOX  
    BUMPUP   20
    JUMP     h
```

### Part XI - Variable Names

The following should compile to the same code as JumpZMultiply

*Note, this doesn't work if x = 0, and it it not the most efficient code*

```
# MULTIPLY TWO NUMBERS

# ------------------------------------------------------------------
# copy two inputs into x and y
# ------------------------------------------------------------------
beginning:
    INBOX               # x = input
    COPYTO   x
    INBOX               # y = input
    COPYTO   y


# ------------------------------------------------------------------
# continuously add y to z x number of times
# ------------------------------------------------------------------
    COPYTO   z          # z = y

decrement:
    BUMPDOWN x          # x--
    JUMPZ    result     # keep doing this until x is equal to zero

    COPYFROM y          # z += y
    ADD      z
    COPYTO   z
    JUMP     decrement  # end of loop

# ------------------------------------------------------------------
# finished, output z
# ------------------------------------------------------------------
result:
    COPYFROM z
    OUTBOX
```





