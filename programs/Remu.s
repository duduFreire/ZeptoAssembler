# R1 = R2 % R3 (unsigned integer remainder)
# Resultado esperado: 0023

# setting R2 and R3
addi R2, R0, R0, 65535
addi R3, R0, R0, 8192

# R1 = 0
addi R1, R0, R0, 0

bgtu R3, R2, 4
subi R2, R2, R3, 0
addi R1, R1, R0, 1
jal R0, -3

addi R1, R2, R0, 0
beq R1, R1, 0