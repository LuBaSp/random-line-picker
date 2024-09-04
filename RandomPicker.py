import pygame
import os
import random
import tkinter as tk
from tkinter import filedialog, messagebox
import textwrap

# Initialize Pygame and create a window
pygame.init()
screen_width, screen_height = 720, 480
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("RANDOM LINE SELECTOR - by LuBaSp")

# Load the icon
icon_path = os.path.join(os.path.dirname(__file__), 'icon.png')
if os.path.exists(icon_path):
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
else:
    print("Icon file not found!")

# Colors and styles
DARK_GRAY = (50, 50, 50)
LIGHT_GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
LOAD_BUTTON_COLOR = (32, 196, 203)
PICK_BUTTON_COLOR = (203, 39, 32)
LOAD_HOVER_COLOR = (82, 246, 253)
PICK_HOVER_COLOR = (253, 89, 82)
BUTTON_CLICK_COLOR = LIGHT_GRAY
BORDER_COLOR = BLACK

# Global variables
file_path = ""
selected_line = ""

def load_file():
    """Opens a file dialog to select a text file."""
    global file_path
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=os.path.expanduser("~"), filetypes=[("Text Files", "*.txt")])
    if not file_path:
        messagebox.showwarning("No File Selected", "Please select a valid text file.")

def pick_random_line():
    """Picks a random line from the loaded text file, ignoring empty lines."""
    global selected_line
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]  # Filter out empty lines
            if lines:
                selected_line = random.choice(lines)
            else:
                selected_line = "The selected file contains only empty lines."
    else:
        selected_line = "No file loaded."

def render_text_wrapped(text, box_rect, font):
    """Renders wrapped text within a specified rectangle, ensuring it fits within the box."""
    max_width = box_rect.width - 20  # Adding a small padding inside the box
    lines = textwrap.wrap(text, width=70)
    
    # Adjust the wrapping based on actual pixel width
    wrapped_lines = []
    for line in lines:
        words = line.split()
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                wrapped_lines.append(current_line.strip())
                current_line = word + " "
        wrapped_lines.append(current_line.strip())

    # Calculate the total height of the wrapped text
    total_height = sum(font.size(line)[1] for line in wrapped_lines)
    
    # If the text is too tall, we will cut off excess lines
    available_height = box_rect.height - 20  # Adding a small padding inside the box
    y_start = box_rect.y + (box_rect.height - min(total_height, available_height)) // 2

    for line in wrapped_lines:
        if y_start + font.size(line)[1] > box_rect.y + available_height:
            break
        line_surface = font.render(line, True, BLACK)
        line_width, line_height = font.size(line)
        x = box_rect.x + (box_rect.width - line_width) // 2
        screen.blit(line_surface, (x, y_start))
        y_start += line_height

def render_centered_button_text(text, button_rect, color, font):
    """Renders text centered within a button."""
    text_surface = font.render(text, True, color)
    text_width, text_height = text_surface.get_size()
    x = button_rect.x + (button_rect.width - text_width) // 2
    y = button_rect.y + (button_rect.height - text_height) // 2
    screen.blit(text_surface, (x, y))

# Create buttons and question box
load_button = pygame.Rect(100, 400, 200, 50)
pick_button = pygame.Rect(420, 400, 200, 50)
question_box = pygame.Rect(50, 50, 620, 300)
font = pygame.font.Font(None, 36)

# Main loop
running = True
mouse_pressed = False
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pressed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pressed = False
            if load_button.collidepoint(mouse_pos):
                load_file()
            if pick_button.collidepoint(mouse_pos):
                pick_random_line()
    
    screen.fill(DARK_GRAY)
    pygame.draw.rect(screen, LIGHT_GRAY, question_box)
    pygame.draw.rect(screen, BORDER_COLOR, question_box, 3)  # 3 pixels thick border

    # Button hover and click effects
    load_button_color = LOAD_BUTTON_COLOR if not load_button.collidepoint(mouse_pos) else LOAD_HOVER_COLOR
    pick_button_color = PICK_BUTTON_COLOR if not pick_button.collidepoint(mouse_pos) else PICK_HOVER_COLOR
    if mouse_pressed and load_button.collidepoint(mouse_pos):
        load_button_color = BUTTON_CLICK_COLOR
    if mouse_pressed and pick_button.collidepoint(mouse_pos):
        pick_button_color = BUTTON_CLICK_COLOR

    pygame.draw.rect(screen, load_button_color, load_button)
    pygame.draw.rect(screen, pick_button_color, pick_button)
    pygame.draw.rect(screen, BORDER_COLOR, load_button.inflate(4, 4), 3)
    pygame.draw.rect(screen, BORDER_COLOR, pick_button.inflate(4, 4), 3)

    # Render text on buttons
    render_centered_button_text('Load File', load_button, BLACK, font)
    render_centered_button_text('Pick Line', pick_button, BLACK, font)
    
    # Display message or selected line
    if not file_path:
        message = "Please, load a file"
        msg_surface = font.render(message, True, BLACK)
        msg_width, msg_height = msg_surface.get_size()
        screen.blit(msg_surface, ((screen_width - msg_width) // 2, question_box.y + (question_box.height - msg_height) // 2))
    elif selected_line:
        render_text_wrapped(selected_line, question_box, font)
    
    pygame.display.flip()

pygame.quit()
