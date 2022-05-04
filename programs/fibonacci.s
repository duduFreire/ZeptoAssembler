# addi R1, R0, R0, 0 # R1 = 0
# addi R2, R0, R0, 1 # R2 = 1
# addi R4, R0, R0, 10 # R4 = 10
# addi R5, R0, R0, 0 # R5 = 0
# bgt R5, R4, 6 # if R5 > R4 goto end
# addi R5, R5, R0, 1 # R5++
# addi R3, R2, R0, 0 # R3 = R2
# addi R2, R1, R2, 0 # R2 = R1 + R2
# addi R1, R3, R0, 0 # R1 = R3
# jal R0, -5
# beq R2, R2, 0

# maximum frequency: 6.25 MHz

addi R1, R0, R0, 0
addi R2, R0, R0, 1
addi R3, R2, R0, 0
addi R2, R1, R2, 0
addi R1, R3, R0, 0
beq R3, R3, -3

