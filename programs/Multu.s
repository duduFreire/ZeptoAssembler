# R1 = R2 * R3 (unsigned)
# Resultado esperado: 7E81

# setting R2 and R3
addi R2, R0, R0, 10
addi R3, R0, R0, 3

beq R3, R0, 4
subi R3, R3, R0, 1
addi R1, R1, R2, 0
jal R0, -3

beq R1, R1, 0
