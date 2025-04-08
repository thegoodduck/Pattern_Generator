import random
import flask
pattern = []
def generate_pattern(difficulty,char_set):
    set = (''.join(random.choice(char_set) for i in range(difficulty)))
    for i in range(difficulty):
            # generating pattern(not random) based on the char_set provided by the user.
            # We will use difficulty as the length of each iteration of the pattern. The pattern will be a list of strings.
            pattern.append(set)
    return pattern

def generate_pattern_num(difficulty):
    options = random.randint(0,2)
    if options == 0:
        print("Option 0")
        set = (''.join(random.choice("1234567890") for i in range(difficulty)))
        for i in range(difficulty):
                # generating pattern(not random) based on the char_set provided by the user.
                # We will use difficulty as the length of each iteration of the pattern. The pattern will be a list of strings.
                pattern.append(set)      
        return ''.join(pattern)
    if options == 1:
        sequence = [random.choice("1234567890") for _ in range(difficulty)]
    
        # Randomly select a rule and a number
        rule = random.choice(["*", "/", "+", "-"])
        rule_num = random.randint(2, 9) if rule in ["*", "/"] else random.randint(1, 9)  # Avoid no-op operations
        
        # Randomly select a digit index to apply the rule
        digit_selected = random.randint(0, len(sequence) - 1)
        
        full_output = ""  # Initialize full_output to store the full concatenated output

        print(f"Option 1")
        print(f"Initial Sequence: {''.join(sequence)}")
        print(f"Rule: {rule}, Rule Number: {rule_num}, Digit Selected Index: {digit_selected}\n")

        # Apply the rule iteratively for the number of times equal to difficulty
        for i in range(1, difficulty + 1):
            original_value = int(sequence[digit_selected])

            if rule == "*":
                new_value = original_value * rule_num
            elif rule == "/":
                new_value = original_value // rule_num if rule_num != 0 else original_value
            elif rule == "+":
                new_value = original_value + rule_num
            elif rule == "-":
                # Use modulo arithmetic to wrap around digits 0-9
                new_value = (original_value - rule_num) % 10

            # Update the selected digit in the sequence (keep only last digit if multi-digit)
            sequence[digit_selected] = str(new_value)[-1]
            
            iteration_output = ''.join(sequence)
            full_output += iteration_output  # Append this iteration to full output
            
            print(f"Iteration {i}: {iteration_output}")  # Print each iteration
            print(f"Full Output So Far: {full_output}\n")  # Print full merged output

        # Print the final full output on a separate line
        print("Final Full Output:")
        print(full_output)

        return full_output
    if options == 2:
        print("Option 2")
        rule = random.choice(["*", "/", "+", "-"])
        rule_num = random.randint(2, 9) if rule in ["*", "/"] else random.randint(1, 9)  # Avoid no-op operations
        # Generate a string (set) of random letters and convert it to a list so it can be iterated over
        sequence = list(''.join(random.choice("abcdefghijklmnopqrstuvwxyz") for i in range(difficulty)))
        # Will generate a pattern like if sequence = "abc" and rule == "+2" it will be abc[modified output]
        full_output = ""
        for i in range(1, difficulty + 1):
            # Apply the rule to every digit (character) in the entire sequence
            for j in range(len(sequence)):
                # Here you might want to define how to apply a rule on alphabet characters.
                # For demonstration, we'll convert 'a' to 0, 'b' to 1, etc.
                original_value = ord(sequence[j]) - ord('a')
                
                if rule == "*":
                    new_value = original_value * rule_num
                elif rule == "/":
                    new_value = original_value // rule_num if rule_num != 0 else original_value
                elif rule == "+":
                    new_value = original_value + rule_num
                elif rule == "-":
                    new_value = (original_value - rule_num) % 26  # for alphabet wrap around
                
                # Map the new value (mod 26) back to a lowercase letter
                sequence[j] = chr((new_value % 26) + ord('a'))
            
            iteration_output = ''.join(sequence)
            full_output += iteration_output  # Append this iteration to full output
            print(f"Iteration {i}: {iteration_output}")
            print(f"Full Output So Far: {full_output}\n")
        
        # Print the final full output on a separate line
        print("Final Full Output:")
        print(full_output)
        return full_output

print(generate_pattern_num(5))