"""CPU functionality."""

import sys

# NOP = 0b00000000

HLT = 0b00000001 

LDI = 0b10000010 # 00000rrr iiiiiiii

# LD  = 0b10000011 00000aaa 00000bbb
# ST  = 0b10000100 00000aaa 00000bbb

# PUSH= 0b01000101 00000rrr
# POP = 0b01000110 00000rrr

PRN = 0b01000111 # 00000rrr
# PRA = 0b01001000 00000rrr

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.__pc =  0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read():
        pass
    
    def ram_write():
        pass

    def run(self):
        """Run the CPU."""
        halted = False
        while not halted:
            instruction = self.ram[self.__pc]

            if instruction == HLT:
                halted = True 
            
            elif instruction == LDI:
                register_num = self.ram[self.__pc + 1]
                self.reg[register_num] = self.ram[self.__pc + 2]
                self.__pc += 3

            elif instruction == PRN:
                key = self.ram[self.__pc + 1]
                register_num = self.reg[key]
                print(register_num)
                self.__pc += 2

            else:
                print(f"Uknown instruction at index {self.__pc}")


