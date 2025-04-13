import random
import flask
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import requests
# Removed unused import
app = flask.Flask(__name__)
pattern = []
def generate_pattern(difficulty,char_set):
    char_sequence = ''.join(random.choice(char_set) for _ in range(difficulty))
    pattern = []
    for i in range(difficulty):
            # generating pattern(not random) based on the char_set provided by the user.
            # We will use difficulty as the length of each iteration of the pattern. The pattern will be a list of strings.
            pattern.append(char_sequence)
    return pattern

def generate_pattern_num(difficulty, char_set="0123456789"):
    options = random.randint(0, 2)
    if options == 0:
        print("Option 0")
        seq = ''.join(random.choice(char_set) for i in range(difficulty))
        pattern = []
        for i in range(difficulty):
            # generating pattern (not random) based on the char_set provided by the user.
            pattern.append(seq)
        return ''.join(pattern)
    if options == 1:
        sequence = [random.choice(char_set) for _ in range(difficulty)]
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
                new_value = (original_value - rule_num) % 10

            # Update the selected digit in the sequence (keep only last digit if multi-digit)
            sequence[digit_selected] = str(new_value)[-1]
            
            iteration_output = ''.join(sequence)
            full_output += iteration_output
            
            print(f"Iteration {i}: {iteration_output}")
            print(f"Full Output So Far: {full_output}\n")

        print("Final Full Output:")
        print(full_output)

        return full_output
    if options == 2:
        print("Option 2")
        rule = random.choice(["*", "/", "+", "-"])
        rule_num = random.randint(2, 9) if rule in ["*", "/"] else random.randint(1, 9)  # Avoid no-op operations
        sequence = list(''.join(random.choice(char_set) for i in range(difficulty)))
        full_output = ""
        for i in range(1, difficulty + 1):
            # Apply the rule to every digit in the sequence
            for j in range(len(sequence)):
                original_value = int(sequence[j])
                
                if rule == "*":
                    new_value = original_value * rule_num
                elif rule == "/":
                    new_value = original_value // rule_num if rule_num != 0 else original_value
                elif rule == "+":
                    new_value = original_value + rule_num
                elif rule == "-":
                    new_value = (original_value - rule_num) % 10  # wrap around for digits 0-9
                
                # Keep only the last digit in case of multi-digit results
                sequence[j] = str(new_value)[-1]
            
            iteration_output = ''.join(sequence)
            full_output += iteration_output
            print(f"Iteration {i}: {iteration_output}")
            print(f"Full Output So Far: {full_output}\n")
        
        print("Final Full Output:")
        print(full_output)
        return full_output

# Generate pdf with different patterns
@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        # Check for batch generation: if multiple difficulties and char_sets are provided,
        # assume form fields "difficulty" and "char_set" are lists.
        if flask.request.form.getlist('difficulty') and len(flask.request.form.getlist('difficulty')) > 1:
            difficulties = flask.request.form.getlist('difficulty')
            char_sets = flask.request.form.getlist('char_set')
            pattern_list = []
            # Process each difficulty and char_set pair
            for diff, cs in zip(difficulties, char_sets):
                diff_int = int(diff)
                if cs.isdigit():
                    p = generate_pattern_num(diff_int, cs)
                else:
                    p = generate_pattern(diff_int, cs)
                # Ensure a one-liner: join list elements without separators
                if isinstance(p, list):
                    p = "".join(p)
                pattern_list.append(p)
            # One pattern per line
            final_pattern_lines = pattern_list
        else:
            difficulty = int(flask.request.form['difficulty'])
            char_set = flask.request.form['char_set']
            if char_set.isdigit():
                pattern = generate_pattern_num(difficulty, char_set)
            else:
                pattern = generate_pattern(difficulty, char_set)
            if isinstance(pattern, list):
                pattern = "".join(pattern)
            final_pattern_lines = [pattern]

        # Generate PDF with custom styling and support for emojis
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        # Use a preinstalled font with emoji support (assumes DejaVuSans is available)
        try:
            fallback_font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            pdfmetrics.registerFont(TTFont('DejaVuSans', fallback_font_path))
            c.setFont('DejaVuSans', 14)
        except Exception as e:
            print(f"Error registering DejaVuSans font: {e}")
            c.setFont("Helvetica", 14)

        # Title, Link and Signature Settings
        title = "Pattern Generator"
        link_text = "https://github.com/thegoodduck/Pattern_Generator"
        signature = "Made with love by @thegoodduck"

        # Draw Title at top center (fixed position)
        # c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width / 2, height - 50, title)

        # Rainbow color palette (as RGB tuples normalized between 0 and 1)
        rainbow_colors = [
            (1, 0, 0),       # Red
            (1, 0.5, 0),     # Orange
            (1, 1, 0),       # Yellow
            (0, 1, 0),       # Green
            (0, 0, 1),       # Blue
            (0.29, 0, 0.51), # Indigo
            (0.93, 0.51, 0.93)  # Violet
        ]

        # Draw each pattern string at a separate random non-overlapping position
        c.setFont("Helvetica", 14)
        line_height = 20  # approximate height for text
        margin = 40
        placed_boxes = []  # To store bounding boxes for drawn texts

        for idx, line in enumerate(final_pattern_lines):
            text_width = c.stringWidth(line, "Helvetica", 14)
            color = random.choice(rainbow_colors)
            placed = False
            attempts = 0

            # Try up to 100 times to find a non-overlapping random position
            while not placed and attempts < 100:
                random_x = random.uniform(margin, width - margin - text_width)
                random_y = random.uniform(margin, height - margin - line_height)
                new_box = (random_x, random_y, random_x + text_width, random_y + line_height)

                # Check overlap with all previously placed boxes
                overlap = any(
                    not (new_box[2] < box[0] or new_box[0] > box[2] or
                         new_box[3] < box[1] or new_box[1] > box[3])
                    for box in placed_boxes
                )

                if not overlap:
                    placed_boxes.append(new_box)
                    c.setFillColorRGB(*color)
                    c.drawString(random_x, random_y, line)
                    placed = True
                attempts += 1

            # Fallback: if unable to fit without overlapping after 100 attempts
            if not placed:
                fallback_y = height - margin - idx * line_height
                c.setFillColorRGB(*color)
                c.drawString(margin, fallback_y, line)

        # Add the clickable link (centered above the signature)
        c.setFont("Helvetica-Oblique", 12)
        c.setFillColorRGB(0, 0, 1)  # Blue for the link
        c.drawCentredString(width / 2, 50, link_text)
        link_width = 200
        c.linkURL(link_text,
              (width / 2 - link_width / 2, 40, width / 2 + link_width / 2, 60),
              relative=0)

        # Add signature at the bottom-right
        c.setFillColorRGB(0, 0, 0)
        c.drawRightString(width - margin, 30, signature)

        c.showPage()
        c.save()
        pdf_buffer.seek(0)

        return flask.send_file(
            pdf_buffer,
            as_attachment=True,
            download_name='pattern.pdf',
            mimetype='application/pdf'
        )
    return flask.render_template('index.html')
app.run(debug=True)