# R1 = R2 / R3 (signed integer division)
# Resultado esperado: FEF6

# setando R2
addi R2, R0, R0, -30767
# setando R3
addi R3, R0, R0, 7672

addi R15, R0, R0, 32768 # bitmask for MSB
andi R4, R2, R15, -1 # R4 = sign(R2)
andi R5, R3, R15, -1 # R5 = sign(R3)

# R2 = |R2|
beq R4, R0, 2
subi R2, R0, R2, 0 
# R3 = |R3|
beq R5, R0, 2
subi R3, R0, R3, 0

# R1 = |R2| / |R3|, com R14 = return address
jal R14, 5

xori R4, R4, R5, 0 # R4 = resultado é negativo ? 1:0
beq R4, R0, 2 # se resultado é pra ser negativo R1 = -R1
subi R1, R0, R1, 0
beq R1, R1, 0

# Unsigned division function. R1 = R2 / R3 (unsigned)
# R1 = 0
addi R1, R0, R0, 0

bgtu R3, R2, 4
subi R2, R2, R3, 0
addi R1, R1, R0, 1 
jal R0, -3

jalr R0, R14, 0 # return to R14
