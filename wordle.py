"""Solve Wordle game"""

import random
import sys

# Ensure text file name is given
if len(sys.argv) != 2:
    print("Usage: python wordle.py [text_file]")
    sys.exit()

text_file = sys.argv[1]

# Word length
N = 5

# Maximum tries
T = 6

# Append words from text file into list
words = []
try:
    with open(text_file) as file:
        lines = file.readlines()
except FileNotFoundError:
    print(f"{text_file} is not found")
    sys.exit()
for word in lines:
    words.append(word.strip())

# Lists for constraints
contains = set()
not_contains = set()
not_letter = []
for i in range(N):
    not_letter.append(set())
confirm = [None] * N

# Try different words for T times
for i in range(T):
    while True:
        if not words:
            print("No solution")
            sys.exit()
        
        # Print suggested word and number of possible answers
        print(f"Guess #{i + 1}")
        print(f"Suggested word: {random.choice(words)}")
        print(f"Selected from {len(words)} possible words")
        print('―' * 80)

        # Get word and result from user
        print("- Type 'q' to exit")
        print("- Type any other key to choose another word")
        print("- Type result in format of 'hello00210' (0: grey; 1: yellow; 2: green)")
        result = input("Enter result: ")
        print()
        if len(result) == N * 2 and result[:N].isalpha() and result[N:].isdigit():
            result = result[:N].lower() + result[N:]
            break

        if result == "q":
            sys.exit()
    
    # Add knowledge to lists
    for i in range(N):
        letter = result[i]
        letter_result = int(result[i + N])

        if letter_result == 0:
            not_contains.add(letter)

        elif letter_result == 1:
            contains.add(letter)
            not_letter[i].add(letter)

        elif letter_result == 2:
            contains.add(letter)
            confirm[i] = letter

    not_contains = not_contains - contains

    # Make inference
    new_words = []
    for word in words:
        valid = True
        for i in range(N):
            if word[i] in not_contains or word[i] in not_letter[i] or (confirm[i] and confirm[i] != word[i]):
                valid = False
                break

        for letter in contains:
            if letter not in word:
                valid = False
                break        

        if valid:
            new_words.append(word)

    words = new_words
