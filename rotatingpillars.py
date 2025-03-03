import numpy as np
# By Amrit Murali on 06/10/2023

# From Sonic Frontiers: ‘A Grave Mystery’ Tombstone Puzzle on Kronos Island
# Contains Puzzle Information, Solution, Analysis, and an auto--solver

# PUZZLE INFORMATION: There are four pillars. You can rotate each pillar 45 degrees clockwise and counter clockwise. But, there are rules.

# 1. Rotating pillar one rotates pillar two the same distance
# 2. Rotating pillar two rotates pillar four the same distance
# 3. Rotating pillar three rotates pillar one and pillar two the same distance
# 4. Rotating pillar four rotates pillar three the same distance

# The goal is to rotate each pillar to a certain orientation.
# What's the most efficient way to solve this?

# SOLUTION: Rotating pillar one 45 degrees clockwise is 'a', 2 is b, 3 is c, 4 is d
#    ^
#    | if this is pillar one, then
#    | then this has a distance of
#    | 5a, since it needs to be rotated
#    O 225 degrees clockwise
#   /
#  /
# /

# Moving rules: (equaling zero means it was a valid move)
# rule 1: 1a rotates 1b: a + b = 0 (rotating pillar 1 45 degrees causes pillar 2 to rotate 45 degrees)
# rule 2: 1b rotates 1d: b + d = 0
# rule 3: 1c rotates 1a and 1b: c + a + b = 0
# rule 4: 1d rotates 1b: d + c = 0

# Method one: Brute force all possible puzzle permutations.
# Some notes so far...
# 1. Order of rotating doesn't matter.
# 2. No rule needs to be done more than 7 times for the optimal solution since a cycle is 8 rotations = 0 rotations. GREEDY decision
# 3. There are 8 valid orientations for a pillar = 8 different choices = length of 8.
# 4. There are 4 pillars = 4 different rules for rotation = 4 variables = 4-dimensional array.
# 5. Each permutation of pillar orientations has multiple solutions but only one optimal solution. That's why I don't check the previous value when storing.
# 6. There is a solution for every possible puzzle combination.
# - PROOF: rule 3 - rule 1 => c = 0
# - then rule 4 - prev. => d = 0
# - then rule 2 - prev => b = 0
# - then rule 1 - prev => a = 0
# - everything is zero, so everything has a solution!

# Program:
# Getting input: the input is 2, 5, 2, 1 for the example in the comment
pillOne = int(input("Enter how many 45-degree clockwise rotations pillar one is away from the correct direction: "))
pillTwo = int(input("Enter how many 45-degree clockwise rotations pillar two is away from the correct direction: "))
pillThree = int(input("Enter how many 45-degree clockwise rotations pillar three is away from the correct direction: "))
pillFour = int(input("Enter how many 45-degree clockwise rotations pillar four is away from the correct direction: "))
print("\nEquation: ", pillOne,  "a + ", pillTwo, "b + ", pillThree, "c + ", pillFour, "d = 0", sep='')

# 1. created a 4-d array of length 8
p = np.full((8, 8, 8, 8), -1, dtype=int)

# 2. 4 nested for loops: d is # of times rule 4 is executed, c is 3, b is 2, a is 1.
for d in range(8):
  for c in range(8):
    for b in range(8):
      for a in range(8):
        # 3. Where to store?  At the destination, which is p[(a+c)%8][(a+b+c)%8][(c+d)%8][(d+b)%8])
        # - 1st dimension is the total movement of pillar one
        # - pillar 1's own movement is accounted for in a, and the movement due to pillar 3's movement is c
        # - modulus 8 is to eliminate cycles and stay inbounds in our array

        # 4. What to store? One rule execution = one rotation
        # - so the total number of rotations, which is a + b + c + d
        # since we want the least number of rotations, we have to account for counter-clockwise rotations
        # - ex: 7 clockwise rotations equals 1 counter-clockwise rotation, 6c = 2cc, 5c = 1cc
        # - this results in a mapping of...only clockwise 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7
        #                                  both           0 | 1 | 2 | 3 | 4 | 3 | 2 | 1
        # - ternary operator is used to create this mapping
        p[(a + c) % 8][(b + a + c) % 8][(c + d) % 8][(d + b) % 8] = (a if a < 5 else 8 - a) + (b if b < 5 else 8 - b) + (c if c < 5 else 8 - c) + (d if d < 5 else 8 - d)

        # Input problem: is this the correct destination?
        if ((a + c) % 8 == pillOne and (a + b + c) % 8 == pillTwo and (c + d) % 8 == pillThree and (d + b) % 8 == pillFour):
          print("\nMethod one: (Brute Force w/exponential runtime)")
          # if so, print the rotations that must be done to each pillar to reach the desired outcome
          if a < 5:
            print("Rotate pillar one", a * 45, "degrees clockwise.")
          else: 
            print("Rotate pillar one", (8 - a) * 45, "degrees counter-clockwise.")
          if b < 5:
            print("Rotate pillar two", b * 45, "degrees clockwise.")
          else: 
            print("Rotate pillar two", (8 - b) * 45, "degrees counter-clockwise.")
          if c < 5:
            print("Rotate pillar three", c * 45, "degrees clockwise.")
          else: 
            print("Rotate pillar three", (8 - c) * 45, "degrees counter-clockwise.")
          if d < 5:
            print("Rotate pillar four", d * 45, "degrees clockwise.")
          else: 
            print("Rotate pillar four", (8 - d) * 45, "degrees counter-clockwise.")

print("At least", p[pillOne][pillTwo][pillThree][pillFour], "45-degree rotations to reach the desired orientations.\n")

# Analysis: this solving algorithm has a runtime of c x 8^4
# - which is O((# of orientations)^(# of pillars))

# Method two: Find a single, efficient solution for the puzzle
# So...we found out that if you know how many times each rule WAS executed, then you can find the destination.
# - the difference b/w the current and correct direction is how many total rotations a pillar did mod 8
# - we can back track and figure out how many times each rule was executed
# - how many 45 degree rotations away is pillar one from its desired orientation = # of times rule one and rule three were executed mod 8
# finding the solution is now an O(1) operation

# Continuing the previous example: (from the if statements)
# (a + c) % 8 = 1 -> the actions of moving pillar one happened once
# (a + b + c) % 8 = 5 -> the actions of moving pillar two happened five times
# (c + d) % 8 = 2
# (d + b) % 8 = 1

# b % 8 = 5 - 1 => b % 8 = 4 second statement minus the first statement
# then d % 8 = 1 - 4 => d % 8 = -3 using fourth statement minus previous statement
# then c % 8 = 2 - (-3) => c % 8 = 5 using third statement minus previous statement
# lastly, a % 8 = 1 - 5 => a % 8 = -4 using first statement minus previous

# a mod 8 = -4 mod 8 = 4
# b mod 8 = 4
# c mod 8 = 5 = 3 cc rotations
# d mod 8 = -3 mod 8 = 5 = 3 cc rotations
# 14 total rotations, which is the same as method one!

input = [pillOne, pillTwo, pillThree, pillFour]

rota = -input[2] + input[3] - input[1] + 2 * input[0]
rotb = input[1] - input[0]
rotc = input[2] - input[3] + input[1] - input[0]
rotd = input[3] - input[1] + input[0]

# accounting for mod...
rota = rota % 8
rotb = rotb % 8
rotc = rotc % 8
rotd = rotd % 8

# and counter-clockwise rotations...
print("Method two: (Single, efficient solution in constant runtime")
if rota < 5:
  print("Rotate pillar one", rota, "times clockwise.")
else: 
  print("Rotate pillar one", (8 - rota), "times counter-clockwise.")
if rotb < 5:
  print("Rotate pillar two", rotb, "times clockwise.")
else: 
  print("Rotate pillar two", (8 - rotb), "times counter-clockwise.")
if rotc < 5:
  print("Rotate pillar three", rotc, "times clockwise.")
else: 
  print("Rotate pillar three", (8 - rotc), "times counter-clockwise.")
if rotd < 5:
  print("Rotate pillar four", rotd, "times clockwise.")
else: 
  print("Rotate pillar four", (8 - rotd), "times counter-clockwise.")

# Method 3: checking if method one and two give the same output
right = 0  # right prediction
wrong = 0  # wrong prediction

# making a table for using the second method...a lot of copypasta
p2 = np.full((8, 8, 8, 8), 999, dtype=int)

for d in range(8):
  for c in range(8):
    for b in range(8):
      for a in range(8):
        input[0] = a
        input[1] = b
        input[2] = c
        input[3] = d
        
        rota = -input[2] + input[3] - input[1] + 2 * input[0]
        rotb = input[1] - input[0]
        rotc = input[2] - input[3] + input[1] - input[0]
        rotd = input[3] - input[1] + input[0]

        rota = rota % 8
        rotb = rotb % 8
        rotc = rotc % 8
        rotd = rotd % 8

        rota = rota if rota < 5 else (8 - rota)
        rotb = rotb if rotb < 5 else (8 - rotb)
        rotc = rotc if rotc < 5 else (8 - rotc)
        rotd = rotd if rotd < 5 else (8 - rotd)

        p2[a][b][c][d] = rota + rotb + rotc + rotd

        if (p[a][b][c][d] - p2[a][b][c][d] == 0):
          right = right + 1
        else:
          wrong = wrong + 1
print("\nMethod three: (Do method one and method two yield the same results?)")   
print(right-wrong,"out of", right+wrong)
