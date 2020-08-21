"""CPU functionality."""

import sys

# instructions

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


class CPU:
    """Main CPU class."""
    # create handle methods, takes operand as a param

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256  # creates array of 256 zeros
        self.reg = [0] * 8  # Registers special variables for operations
        self.reg[7] = 0xF4
        self.pc = 0
        self.running = True
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_HLT
        self.branchtable[LDI] = self.handle_LDI
        self.branchtable[PRN] = self.handle_PRN
        self.branchtable[ADD] = self.handle_ADD
        self.branchtable[MUL] = self.handle_MUL
        self.branchtable[PUSH] = self.handle_PUSH
        self.branchtable[POP] = self.handle_POP
        self.branchtable[CALL] = self.handle_CALL
        self.branchtable[RET] = self.handle_RET
        self.branchtable[CMP] = self.handle_CMP
        self.branchtable[JMP] = self.handle_JMP
        self.branchtable[JEQ] = self.handle_JEQ
        self.branchtable[JNE] = self.handle_JNE
        self.branchtable[AND] = self.handle_AND
        self.branchtable[OR] = self.handle_OR
        self.branchtable[XOR] = self.handle_XOR
        self.branchtable[NOT] = self.handle_NOT
        self.branchtable[SHL] = self.handle_SHL
        self.branchtable[SHR] = self.handle_SHR
        self.branchtable[MOD] = self.handle_MOD

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def handle_LDI(self, a, b):
        self.reg[a] = b

    def handle_HLT(self, a, b):
        self.running = False

    def handle_PRN(self, a, b):
        # reg_num = self.ram_read(self.pc + 1)
        print(self.reg[a])

    def handle_ADD(self, a, b):
        self.alu("ADD", a, b)

    def handle_MUL(self, a, b):
        self.alu("MUL", a, b)

    def handle_PUSH(self, a, b):
        self.reg[7] -= 1
        register = self.ram_read(self.pc + 1)
        value = self.reg[register]
        sp = self.reg[7]
        self.ram[sp] = value

    def handle_POP(self, a, b):
        sp = self.reg[7]
        register = self.ram_read(self.pc + 1)
        value = self.ram[sp]
        self.reg[register] = value
        self.reg[7] += 1

    def handle_CALL(self, a, b):
        reg = self.ram_read(self.pc + 1)
        address = self.reg[reg]
        return_address = self.pc + 2
        self.reg[7] -= 1
        sp = self.reg[7]
        self.ram[sp] = return_address
        self.pc = address

    def handle_RET(self, a, b):
        sp = self.reg[7]
        return_address = self.ram[rp]
        self.reg[7] += 1
        self.pc = return_address

    def handle_CMP(self, a, b):
        self.alu("CMP", a, b)

    def handle_AND(self, a, b):
        self.alu("AND", a, b)

    def handle_OR(self, a, b):
        self.alu("OR", a, b)

    def handle_XOR(self, a, b):
        self.alu("XOR", a, b)

    def handle_NOT(self, a, b):
        self.alu("NOT", a, b)  # maybe NONE as second argument

    def handle_SHL(self, a, b):
        self.alu("SHL", a, b)

    def handle_SHR(self, a, b):
        self.alu("SHR", a, b)

    def handle_JMP(self):
        reg = self.ram_read(self.pc + 1)
        address = self.reg[reg]
        self.pc = address

    def handle_JEQ(self):
        reg = self.ram_read(self.pc + 1)
        address = self.reg[reg]
        if self.fl == 0b00000001:
            self.pc = address
        else:
            self.pc += 2

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        try:
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0].strip()
                    if split_line == "":
                        continue
                    instructions = int(split_line, 2)
                    self.ram[address] = instructions
                    address += 1
        except FileNotFoundError:
            print(f"Not Found booiii")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "PRN":
            self.handle_PRN(reg_a)

        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100

        elif op == "AND":
            result = self.reg[reg_a] & self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "OR":
            result = self.reg[reg_a] | self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "XOR":
            result = self.reg[reg_a] ^ self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "NOT":
            self.reg[reg_a] = ~self.reg[reg_a]
        elif op == "SHL":
            result = self.reg[reg_a] << self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "SHR":
            result = self.reg[reg_a] >> self.reg[reg_b]
            self.reg[reg_a] = result

        elif op == "MOD":
            if self.reg[reg_b] == 0:
                print("Error: Dividing by Zero")
                self.handle_HLT()
            else:
                result = self.reg[reg_a] % self.reg[reg_b]
                self.reg[reg_a] = result
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:
            # print("running")
            # Instruction Register #missing Operand a/b
            ir = self.ram_read(self.pc)
            ir2 = self.ram_read(self.pc + 1)
            ir3 = self.ram_read(self.pc + 2)
            # value = ir
            # op_count = value >> 6
            # ir_length = 1 + op_count
            self.branchtable[ir](ir2, ir3)
            if ir != CALL and ir != RET and ir != JMP and ir != JEQ and ir != JNE:
                self.pc += ir_length

            if ir == 0 or None:  # check instruction for print(PRN)
                print(f"Unknown Instruction: {ir}")
                # sys.exit()
