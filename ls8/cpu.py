"""CPU functionality."""

import sys
import os


# NOP = 0b00000000

HLT = 0b00000001 
LDI = 0b10000010 # 00000rrr iiiiiiii
MUL = 0b10100010 # 2 operands
PUSH = 0b01000101 # 00000rrr
POP = 0b01000110 # 00000rrr
PRN = 0b01000111 # 00000rrr
RET = 0b00010001 
CALL = 0b01010000 # 00000rrr
CMP = 0b10100111 # 00000aaa 00000bbb
JEQ = 0b01010101 # 00000rrr
JNE = 0b01010110 # 00000rrr
JMP = 0b01010100 # 00000rrr
ADD = 0b10100000 # 00000aaa 00000bbb


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [0] * 8
        self.pc =  0
        self.sp = 5
        self.fl = 0b00000000 # 00000LGE

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
            instruction = self.ram[self.pc]

            if instruction == HLT:
                halted = True 
            
            elif instruction == LDI:
                register_num = self.ram[self.pc + 1]
                self.reg[register_num] = self.ram[self.pc + 2]
                self.pc += 3

            elif instruction == PRN:
                key = self.ram[self.pc + 1]
                register_num = self.reg[key]
                print(register_num)
                self.pc += 2
            
            elif instruction == MUL:
                registerA = self.ram[self.pc + 1]
                registerB = self.ram[self.pc + 2]
                result = self.reg[registerA] * self.reg[registerB]
                self.reg[registerA] = result
                self.pc += 3

            elif instruction == PUSH:
                # 1. Decrement the `SP`.
                self.sp -= 1
                
                # 2. Copy the value in the given register to the address pointed to by `SP`.
                register_num = self.ram[self.pc + 1]
                value = self.reg[register_num]
                self.ram[self.sp] = value
                self.pc += 2


            elif instruction == POP:
                # 1. Copy the value from the address pointed to by `SP` to the given register.
                value = self.ram[self.sp]
                register_num = self.ram[self.pc + 1]
                self.reg[register_num] = value

                # 2. Increment `SP`.      
                self.sp += 1
                self.pc += 2


            elif instruction == CALL:
            # Calls a subroutine (function) at the address stored in the register.
                # 1. The address of the ***instruction*** _directly after_ `CALL` is pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
                saved_address = self.pc + 2

                # decrease sp
                self.sp -= 1

                # send saved_address to the stack in memory pointed to sp
                self.ram[self.sp] = saved_address

                # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first #instruction in the subroutine. The PC can move forward or backwards from its current location.
                register_num = self.ram[self.pc + 1]
                self.pc = self.reg[register_num]
            
            elif instruction == RET:
            # Pop the value from the top of the stack and store it in the `PC`.
                value = self.ram[self.sp]
                self.pc = value
                self.sp += 1


            elif instruction == CMP:
                """
                Compare the values in two registers.

                * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.

                * If registerA is less than registerB, set the Less-than `L` flag to 1,
                otherwise set it to 0.

                * If registerA is greater than registerB, set the Greater-than `G` flag
                to 1, otherwise set it to 0.
                """
                registerA = self.ram[self.pc + 1]
                registerB = self.ram[self.pc + 2]

                if self.reg[registerA] < self.reg[registerB]:
                    self.fl = 0b00000100
                elif self.reg[registerA] > self.reg[registerB]:
                    self.fl = 0b00000010
                elif self.reg[registerA] == self.reg[registerB]:
                    self.fl = 0b00000001
                
                self.pc += 3
            
            elif instruction == JEQ:
                """
                If `equal` flag is set (true), jump to the address stored in the given register.
                """
                if self.fl == 1:
                    register_num = self.ram[self.pc + 1]
                    self.pc = self.reg[register_num]
                else:
                    self.pc += 2
                

            elif instruction == JNE:
                """
                If `E` flag is clear (false, 0), jump to the address stored in the given
                register.
                """
                if self.fl is not 1:
                    register_num = self.ram[self.pc + 1]
                    self.pc = self.reg[register_num]
                else:
                    self.pc += 2

            elif instruction == JMP:
                """
                Jump to the address stored in the given register.

                Set the `PC` to the address stored in the given register.       
                """
                register_num = self.ram[self.pc + 1]
                self.pc = self.reg[register_num]

            elif instruction == ADD:
                # Add the value in two registers and store the result in registerA.
                registerA = self.ram[self.pc + 1]
                registerB = self.ram[self.pc + 2]
                result = self.reg[registerA] + self.reg[registerB]
                self.reg[registerA] = result

                self.pc += 3

            else:
                print(f"Uknown instruction at index {self.pc}")


