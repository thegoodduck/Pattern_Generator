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
    options = random.randint(0,1)
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
        
        full_output = ""  # Store the full concatenated output

        print(f"Option 1")
        print(f"Initial Sequence: {''.join(sequence)}")
        print(f"Rule: {rule}, Rule Number: {rule_num}, Digit Selected Index: {digit_selected}\n")

        # Apply the rule iteratively for the number of times equal to difficulty
        for i in range(1, difficulty + 1):
            original_value = int(sequence[digit_selected])

            if rule == "*":
                new_value = original_value * rule_num
            elif rule == "/":
                new_value = original_value // rule_num if rule_num != 0 else original_value  # Avoid division by zero
            elif rule == "+":
                new_value = original_value + rule_num
            elif rule == "-":
                new_value = max(0, original_value - rule_num)  # Ensure no negative numbers
                if new_value == 0:
                    new_value = 1  # Prevent zeros and keep updating the sequence

            # Update the selected digit in the sequence
            sequence[digit_selected] = str(new_value)[-1]  # Ensure it's still a single digit

            iteration_output = ''.join(sequence)  # Current iteration result
            full_output += iteration_output  # Append this iteration to full output
            
            print(f"Iteration {i}: {iteration_output}")  # Print each iteration
            print(f"Full Output So Far: {full_output}\n")  # Print full merged output

        # Print the final full output on a separate line
        print("Final Full Output:")
        print(full_output)

        return full_output
print(generate_pattern_num(5))