# R1 = MDC(R2, R3)
# Resultado esperado: 005B

# setting R2 and R3 
addi R2, R0, R0, 182
addi R3, R0, R0, 1001

# a,b = max(a, b), min(a, b)
bgtu R2, R3, 4
addi R4, R2, R0, 0
addi R2, R3, R0, 0
addi R3, R4, R0, 0

# R1 = result = 1
addi R1, R0, R0, 1

# R8 = i = 2
addi R8, R0, R0, 2

# if i > b break
bgtu R8, R3, 12
# a % i == 0 ?
addi R6, R2, R0, 0
addi R7, R8, R0, 0
jal R14, 10
bne R5, R0, 6

# b % i == 0 ?
addi R6, R3, R0, 0
addi R7, R8, R0, 0
jal R14, 6
bne R5, R0, 2

# result = i
addi R1, R8, R0, 0

# increment i and go back to loop
addi R8, R8, R0, 1
jal R0, -11

# show R1 
beq R1, R1, 0

# R5 = R6 % R7 (unsigned integer remainder)
# R5 = 0
addi R5, R0, R0, 0

bgtu R7, R6, 4
subi R6, R6, R7, 0
addi R5, R5, R0, 1
jal R0, -3

addi R5, R6, R0, 0
jalr R0, R14, 0