from ast import Num
from io import TextIOWrapper
import sys

class Instruction:
	def __init__(self, instruction : str) -> None:
		instruction = instruction.split()
		self.name = instruction[0]
		instruction = ("".join(instruction[1:])).split(",")

		if self.name[0] == "b":
			self.rd = "R0"
			self.ra = instruction[0]
			self.rb = instruction[1]
			self.imm = instruction[2]
		elif self.name == "jal":
			self.rd = instruction[0]
			self.ra = "R0"
			self.rb = "R0"
			self.imm = instruction[1]
		elif self.name == "jalr":
			self.rd = instruction[0]
			self.ra = instruction[1]
			self.rb = "R0"
			self.imm = instruction[2]
		else:
			self.rd = instruction[0]
			self.ra = instruction[1]
			self.rb = instruction[2]
			self.imm = instruction[3]

	def __repr__(self) -> str:
		return str([self.name, self.rd, self.ra, self.rb, self.imm])

class Program:
	def __init__(self, file : TextIOWrapper) -> None:
		self.instructions = []
		self.get_instructions(file)
		self.filename = file.name.split(".")[0]
	
	def get_instructions(self, file : TextIOWrapper):
		for line in file:
			line = " ".join(line.split())
			line = line.split("#")[0]
			line = line.strip()
			if line == "": continue

			self.instructions.append(Instruction(line))

	def assemble_bin(self):
		file1 = open(f"programs/{self.filename}_1.drs", "w")
		file2 = open(f"programs/{self.filename}_2.drs", "w")

		self.opcodes = {"addi":"0000", "subi":"0001", "andi":"0010", 
		"ori":"0011", "xori":"0100", "beq":"0101", "bne":"0110", "ble":"0111",
		"bleu":"1000", "bgt":"1001", "bgtu":"1010", "jal":"1011", "jalr":"1100"}

		file1.write("#H\n")
		file2.write("#H\n")

		for instruction in self.instructions:
			opcode = self.opcodes[instruction.name]
			rd = dec_to_bin(instruction.rd[1:], 4)
			ra = dec_to_bin(instruction.ra[1:], 4)
			rb = dec_to_bin(instruction.rb[1:], 4)
			imm = dec_to_bin(instruction.imm, 16)
			imm = ".".join([imm[i:i+4] for i in range(0, len(imm), 4)])

			assembled1 =  f"{rb}.{ra}.{rd}.{opcode}\n"
			assembled2 = imm + "\n"

			file1.write(assembled1)
			file2.write(assembled2)

	def assemble_hex(self):
		file1 = open(f"{self.filename}_1.drs", "w")
		file2 = open(f"{self.filename}_2.drs", "w")

		self.opcodes = {"addi":"0", "subi":"1", "andi":"2", 
		"ori":"3", "xori":"4", "beq":"5", "bne":"6", "ble":"7",
		"bleu":"8", "bgt":"9", "bgtu":"A", "jal":"B", "jalr":"C"}

		file1.write("#H\n")
		file2.write("#H\n")

		for instruction in self.instructions:
			opcode = self.opcodes[instruction.name]
			rd = bin_to_hex(dec_to_bin(instruction.rd[1:], 4))
			ra = bin_to_hex(dec_to_bin(instruction.ra[1:], 4))
			rb = bin_to_hex(dec_to_bin(instruction.rb[1:], 4))
			imm = dec_to_bin(instruction.imm, 16)
			imm = "".join([bin_to_hex(imm[i:i+4]) for i in range(0, len(imm), 4)])

			assembled1 =  f"{rb}{ra}{rd}{opcode}\n"
			assembled2 = imm + "\n"

			file1.write(assembled1)
			file2.write(assembled2)

class Num16:
	def __init__(self, num:str) -> None:
		num = "0" * (4-len(num)) + num
		self.num = num
	
	def __repr__(self) -> str:
		return self.num

	def __getitem__(self, num):
		return self.num[num]

	def __add__(self, other):
		num1 = int(self.num, 16)
		num2 = int(other.num, 16)
		return Num16(hex((num1 + num2) % (2 ** 16))[2:].upper())

	def __invert__(self):
		result = []
		for i in range(4):
			result.append(hex(15 - int(self.num[i], 16))[2:].upper())
		return Num16("".join(result))

	def __neg__(self):
		return ~self + Num16("0001")

	def __sub__(self, other):
		return self + (-other)

	def __and__(self, other):
		num1 = int(self.num, 16)
		num2 = int(other.num, 16)
		return Num16(hex((num1 & num2) % (2 ** 16))[2:].upper())

	def __or__(self, other):
		num1 = int(self.num, 16)
		num2 = int(other.num, 16)
		return Num16(hex((num1 | num2) % (2 ** 16))[2:].upper())

	def __xor__(self, other):
		num1 = int(self.num, 16)
		num2 = int(other.num, 16)
		return Num16(hex((num1 ^ num2) % (2 ** 16))[2:].upper())

	def le(self, other):
		return self.signed() <= other.signed()
	
	def leu(self, other):
		return self.unsigned() <= other.unsigned()

	def gt(self, other):
		return self.signed() > other.signed()
	
	def gtu(self, other):
		return self.unsigned() > other.unsigned()

	def __eq__(self, __o: object) -> bool:
		return self.num == __o.num
	
	def unsigned(self):
		return int(self.num, 16)
	
	def signed(self):
		if self.num[0] == "F":
			return - (2**16 - self.unsigned())
		return self.unsigned()

	def to_hex(self):
		return "0x" + self.num 

	def from_decimal(num):
		if num >= 0: return Num16(hex(int(num))[2:].upper())
		return -Num16(hex(int(-num))[2:].upper())
	

class Processor:
	def __init__(self, instructions) -> None:
		self.instructions = instructions 
		self.registers = [Num16("0000") for i in range(16)]
		self.program_counter = Num16("0000")
		self.cycles = 0

		self.stopped = False
	

	def set_reg(self, addr, val):
		if addr != 0:
			self.registers[addr] = val

	def exec(self):
		cmd = self.instructions[self.program_counter.unsigned()]
		rd = int(cmd.rd[1:])
		ra = self.registers[int(cmd.ra[1:])]
		rb = self.registers[int(cmd.rb[1:])]
		imm = Num16.from_decimal(int(cmd.imm))
		
		if not self.stopped:
			self.cycles += 1

		if cmd.name == "addi":
			self.set_reg(rd, ra + rb + imm)
			self.program_counter += Num16("0001")
		elif cmd.name == "subi":
			self.set_reg(rd, ra - rb - imm) 
			self.program_counter += Num16("0001")
		elif cmd.name == "andi":
			self.set_reg(rd, ra & rb & imm) 
			self.program_counter += Num16("0001")
		elif cmd.name == "ori":
			self.set_reg(rd, ra | rb | imm) 
			self.program_counter += Num16("0001")
		elif cmd.name == "xori":
			self.set_reg(rd, ra ^ rb ^ imm) 
			self.program_counter += Num16("0001")
		elif cmd.name == "beq":
			if cmd.ra == cmd.rb: self.stopped = True
			self.program_counter += imm if ra == rb else Num16("0001")
		elif cmd.name == "bne":
			self.program_counter += imm if ra != rb else Num16("0001")
		elif cmd.name == "ble":
			self.program_counter += imm if ra.le(rb) else Num16("0001")
		elif cmd.name == "bleu":
			self.program_counter += imm if ra.leu(rb) else Num16("0001")
		elif cmd.name == "bgt":
			self.program_counter += imm if ra.gt(rb) else  Num16("0001")
		elif cmd.name == "bgtu":
			self.program_counter += imm if ra.gtu(rb) else Num16("0001")
		elif cmd.name == "jal":
			self.set_reg(rd, self.program_counter +  Num16("0001"))
			self.program_counter += imm
		else:
			self.set_reg(rd, self.program_counter + Num16("0001"))
			self.program_counter = ra + imm

	def exec_n(self, n):
		for _ in range(n):
			self.exec()
			if self.stopped: break
		print(self.registers, self.cycles)

def dec_to_bin(num, bits):
	num = int(num)
	leading = "0"
	if num < 0:
		num = 2 ** bits + num
		leading = "1"
	
	num = bin(num)[2:]
	num = leading * (bits-len(num)) + num 
	return num

def bin_to_hex(num):
	return hex(int(num, 2))[2:].upper()

file = open(sys.argv[1], "r")


prog = Program(file)
prog.assemble_hex()

if len(sys.argv) > 2:
	processor = Processor(prog.instructions)
	processor.exec_n(int(sys.argv[2]))

file.close()
