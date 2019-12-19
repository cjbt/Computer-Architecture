"""CPU functionality."""

import sys
import os


# NOP = 0b00000000

HLT = 0b00000001 
LDI = 0b10000010 # 00000rrr iiiiiiii
MUL = 0b10100010 # 2 operands
# LD  = 0b10000011 00000aaa 00000bbb
# ST  = 0b10000100 00000aaa 00000bbb
PUSH = 0b01000101 # 00000rrr
POP = 0b01000110 # 00000rrr
PRN = 0b01000111 # 00000rrr
# PRA = 0b01001000 00000rrr

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.__pc =  0
        self.__sp = 5

    def load(self, filename):
        """Load a program into memory."""
        cur_path = os.path.dirname(__file__)
        new_path = os.path.join(cur_path, f'examples/{filename}')
        address = 0

        with open(new_path) as f:
            for line in f:
                n = line.split("#")
                n[0] = n[0].strip()

                if n[0] == '':
                    continue

                value = int(n[0], 2)
                self.ram[address] = value
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
        # instruction = self.ram[0]
        # print(instruction, LDI)

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
            
            elif instruction == MUL:
                registerA = self.ram[self.__pc + 1]
                registerB = self.ram[self.__pc + 2]
                result = self.reg[registerA] * self.reg[registerB]
                self.reg[registerA] = result
                self.__pc += 3

            elif instruction == PUSH:
                # 1. Decrement the `SP`.
                self.reg[self.__sp] -= 1

                # 2. Copy the value in the given register to the address pointed to by
                #   `SP`.
                register_num = self.ram[self.__pc + 1]
                value = self.reg[register_num]
                self.ram[self.reg[self.__sp]] = value
                self.__pc += 2

            elif instruction == POP:
                # 1. Copy the value from the address pointed to by `SP` to the given register.
                register_num = self.ram[self.__pc + 1]
                value = self.ram[self.reg[self.__sp]]
                self.reg[register_num] = value

                # 2. Increment `SP`.
                self.reg[self.__sp] += 1
                self.__pc += 2

                

            else:
                print(f"Uknown instruction at index {self.__pc}")


