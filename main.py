import random
import flask
import io
import os
import requests
import urllib.request
import zipfile

# Set this flag to True to use WeasyPrint (emoji-friendly) or False for ReportLab.
USE_WEASYPRINT = True

if USE_WEASYPRINT:
    from weasyprint import HTML
else:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

app = flask.Flask(__name__)

# --- Pattern Generation Functions ---
def generate_pattern(difficulty, char_set):
    """
    Generate a pattern by repeating a random sequence of characters.
    
    Args:
        difficulty (int): The length of the pattern to generate
        char_set (str): The set of characters to use for generation
        
    Returns:
        list: A list containing the generated pattern
    """
    char_sequence = ''.join(random.choice(char_set) for _ in range(difficulty))
    pattern = []
    for i in range(difficulty):
        pattern.append(char_sequence)
    return pattern

def generate_pattern_num(difficulty, char_set="0123456789"):
    """
    Generate a numeric pattern using one of three algorithms.
    
    Args:
        difficulty (int): The complexity level of the pattern
        char_set (str, optional): The set of digits to use. Defaults to "0123456789".
        
    Returns:
        str: The generated numeric pattern
    """
    # Select a random algorithm
    algorithm = random.randint(0, 2)
    
    if algorithm == 0:
        # Algorithm 0: Simple repetition of a random sequence
        sequence = ''.join(random.choice(char_set) for _ in range(difficulty))
        pattern = []
        for _ in range(difficulty):
            pattern.append(sequence)
        return ''.join(pattern)
        
    elif algorithm == 1:
        # Algorithm 1: Evolving sequence with selective digit modification
        sequence = [random.choice(char_set) for _ in range(difficulty)]
        operation = random.choice(["*", "/", "+", "-"])
        factor = random.randint(2, 9) if operation in ["*", "/"] else random.randint(1, 9)
        target_position = random.randint(0, len(sequence) - 1)
        
        result = ""
        initial_sequence = ''.join(sequence)
        
        for iteration in range(1, difficulty + 1):
            original_value = int(sequence[target_position])
            
            # Apply the selected operation to the target digit
            if operation == "*":
                new_value = original_value * factor
            elif operation == "/":
                new_value = original_value // factor if factor != 0 else original_value
            elif operation == "+":
                new_value = original_value + factor
            elif operation == "-":
                new_value = (original_value - factor) % 10
                
            # Update the sequence with the new value (last digit only)
            sequence[target_position] = str(new_value)[-1]
            current_sequence = ''.join(sequence)
            result += current_sequence
            
        return result
        
    else:  # algorithm == 2
        # Algorithm 2: Apply operation to every digit in each iteration
        sequence = list(''.join(random.choice(char_set) for _ in range(difficulty)))
        operation = random.choice(["*", "/", "+", "-"])
        factor = random.randint(2, 9) if operation in ["*", "/"] else random.randint(1, 9)
        
        result = ""
        
        for _ in range(1, difficulty + 1):
            # Apply operation to each digit
            for j in range(len(sequence)):
                original_value = int(sequence[j])
                
                if operation == "*":
                    new_value = original_value * factor
                elif operation == "/":
                    new_value = original_value // factor if factor != 0 else original_value
                elif operation == "+":
                    new_value = original_value + factor
                elif operation == "-":
                    new_value = (original_value - factor) % 10
                    
                sequence[j] = str(new_value)[-1]
                
            current_sequence = ''.join(sequence)
            result += current_sequence
            
        return result

# --- PDF Generation Functions ---
def generate_pdf_weasyprint(final_pattern_lines):
    """
    Generate a PDF document with the provided pattern lines using WeasyPrint.
    
    Args:
        final_pattern_lines (list): List of pattern strings to include in the PDF
        
    Returns:
        BytesIO: A buffer containing the generated PDF
    """
    # Page settings (letter size)
    PAGE_WIDTH, PAGE_HEIGHT = 612, 792
    margin = 40
    line_height = 20
    placed_boxes = []  # Track absolute positions to avoid overlapping

    # Start building the HTML string with styles
    html_lines = [f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body {{
            position: relative;
            width: {PAGE_WIDTH}px;
            height: {PAGE_HEIGHT}px;
            margin: 0;
            padding: 0;
            background: white;
            font: 14px Helvetica, Arial, sans-serif;
        }}
        .title {{
            position: absolute;
            top: 20px;
            width: 100%;
            text-align: center;
            font-weight: bold;
            font-size: 24px;
            color: black;
        }}
        .link {{
            position: absolute;
            bottom: 60px;
            width: 100%;
            text-align: center;
            font-style: italic;
            font-size: 12px;
            color: blue;
        }}
        .signature {{
            position: absolute;
            bottom: 30px;
            right: {margin}px;
            color: black;
        }}
        .line {{
            position: absolute;
            white-space: nowrap;
        }}
    </style>
</head>
<body>
    <div class="title">Pattern Generator</div>
    <div class="link"><a href="https://github.com/thegoodduck/Pattern_Generator">https://github.com/thegoodduck/Pattern_Generator</a></div>
    <div class="signature">Made with love by @thegoodduck</div>
"""]

    # Rainbow colors (in hex)
    rainbow_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#4B0082", "#9400D3"]

    # Place each pattern line on the page
    for idx, line in enumerate(final_pattern_lines):
        # Approximate text width
        text_width = len(line) * 8  
        placed = False
        attempts = 0
        max_attempts = 100

        # Try to place text without overlapping other elements
        while not placed and attempts < max_attempts:
            # Generate random position
            random_x = random.uniform(margin, PAGE_WIDTH - margin - text_width)
            random_y = random.uniform(margin + 50, PAGE_HEIGHT - margin - line_height - 60)
            new_box = (random_x, random_y, random_x + text_width, random_y + line_height)
            
            # Check for overlap with existing elements
            overlap = any(
                not (new_box[2] < box[0] or new_box[0] > box[2] or
                     new_box[3] < box[1] or new_box[1] > box[3])
                for box in placed_boxes
            )
            
            if not overlap:
                placed_boxes.append(new_box)
                color = random.choice(rainbow_colors)
                html_lines.append(f"""<div class="line" style="left:{random_x}px; top:{random_y}px; color:{color};">{line}</div>""")
                placed = True
            attempts += 1

        # Fallback positioning if random placement fails
        if not placed:
            fallback_y = PAGE_HEIGHT - margin - idx * line_height - 60
            color = random.choice(rainbow_colors)
            html_lines.append(f"""<div class="line" style="left:{margin}px; top:{fallback_y}px; color:{color};">{line}</div>""")
    
    # Finalize HTML and generate PDF
    html_lines.append("</body></html>")
    html_str = "\n".join(html_lines)
    pdf_bytes = HTML(string=html_str).write_pdf()
    return io.BytesIO(pdf_bytes)

def generate_pdf_reportlab(final_pattern_lines):
    """
    Generate a PDF document with the provided pattern lines using ReportLab.
    
    Args:
        final_pattern_lines (list): List of pattern strings to include in the PDF
        
    Returns:
        BytesIO: A buffer containing the generated PDF
    """
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter
    margin = 40
    line_height = 20

    # Document metadata
    title = "Pattern Generator"
    link_text = "https://github.com/thegoodduck/Pattern_Generator"
    signature = "Made with love by @thegoodduck"

    # Add document title
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 50, title)

    # Rainbow colors (in RGB format)
    rainbow_colors = [
        (1, 0, 0),      # Red
        (1, 0.5, 0),    # Orange
        (1, 1, 0),      # Yellow
        (0, 1, 0),      # Green
        (0, 0, 1),      # Blue
        (0.29, 0, 0.51), # Indigo
        (0.93, 0.51, 0.93) # Violet
    ]

    # Place pattern lines on the page
    placed_boxes = []
    c.setFont("Helvetica", 14)
    for idx, line in enumerate(final_pattern_lines):
        text_width = c.stringWidth(line, "Helvetica", 14)
        color = random.choice(rainbow_colors)
        placed = False
        attempts = 0
        max_attempts = 100

        # Try to place text without overlapping other elements
        while not placed and attempts < max_attempts:
            # Generate random position
            random_x = random.uniform(margin, width - margin - text_width)
            random_y = random.uniform(margin + 50, height - margin - line_height - 60)
            new_box = (random_x, random_y, random_x + text_width, random_y + line_height)
            
            # Check for overlap with existing elements
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
            
        # Fallback positioning if random placement fails
        if not placed:
            fallback_y = height - margin - idx * line_height - 60
            c.setFillColorRGB(*color)
            c.drawString(margin, fallback_y, line)

    # Add link and signature
    c.setFont("Helvetica-Oblique", 12)
    c.setFillColorRGB(0, 0, 1)
    c.drawCentredString(width / 2, 50, link_text)
    link_width = 200
    c.linkURL(link_text,
              (width / 2 - link_width / 2, 40, width / 2 + link_width / 2, 60),
              relative=0)
    c.setFillColorRGB(0, 0, 0)
    c.drawRightString(width - margin, 30, signature)
    
    # Finalize the PDF
    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# --- Flask Routes ---
@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Main route handler for the Pattern Generator web application.
    
    GET: Displays the pattern generation form
    POST: Processes form submission and returns a generated PDF
    
    Returns:
        Response: HTML template or PDF file download
    """
    if flask.request.method == 'POST':
        try:
            # Process batch or single pattern generation
            if flask.request.form.getlist('difficulty') and len(flask.request.form.getlist('difficulty')) > 1:
                # Batch pattern generation
                difficulties = flask.request.form.getlist('difficulty')
                char_sets = flask.request.form.getlist('char_set')
                pattern_list = []
                
                # Generate each requested pattern
                for diff, char_set in zip(difficulties, char_sets):
                    difficulty = int(diff)
                    # Choose appropriate generator based on character set
                    if char_set.isdigit():
                        pattern = generate_pattern_num(difficulty, char_set)
                    else:
                        pattern = generate_pattern(difficulty, char_set)
                    
                    # Convert list patterns to strings if needed
                    if isinstance(pattern, list):
                        pattern = "".join(pattern)
                    pattern_list.append(pattern)
                    
                final_pattern_lines = pattern_list
            else:
                # Single pattern generation
                try:
                    difficulty = int(flask.request.form['difficulty'])
                    char_set = flask.request.form['char_set']
                    
                    # Choose appropriate generator based on character set
                    if char_set.isdigit():
                        pattern = generate_pattern_num(difficulty, char_set)
                    else:
                        pattern = generate_pattern(difficulty, char_set)
                        
                    # Convert list patterns to strings if needed
                    if isinstance(pattern, list):
                        pattern = "".join(pattern)
                    final_pattern_lines = [pattern]
                except ValueError:
                    # Handle invalid difficulty value
                    return flask.render_template('index.html', 
                                               error="Please enter a valid number for difficulty.")
                except KeyError:
                    # Handle missing form fields
                    return flask.render_template('index.html', 
                                               error="Please fill in all required fields.")
            
            # Generate PDF using selected backend
            if USE_WEASYPRINT:
                pdf_buffer = generate_pdf_weasyprint(final_pattern_lines)
            else:
                pdf_buffer = generate_pdf_reportlab(final_pattern_lines)
                
            # Return PDF file for download
            return flask.send_file(
                pdf_buffer,
                as_attachment=True,
                download_name='pattern.pdf',
                mimetype='application/pdf'
            )
            
        except Exception as e:
            # Log exception and return error page
            app.logger.error(f"Error generating pattern: {str(e)}")
            return flask.render_template('index.html', 
                                       error="An error occurred while generating the pattern.")
    
    # Display pattern generation form
    return flask.render_template('index.html')


if __name__ == '__main__':
    # Run the Flask application in debug mode (disable in production)
    app.run(debug=True)