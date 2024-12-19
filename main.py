import os
import re
import random as rn
import tkinter as tk
from tkinter import messagebox as mg
from PIL import ImageTk, Image, ImageDraw, ImageFont, ImageFilter

# General settings
main_dir = os.path.dirname(os.path.abspath(__file__))
app_font = ('times', 17)
hint_font = ('times', 14)
header_font = ('times', 30)
colors = ['blue', 'black', 'red', 'green', 'darkorange', 'darkorchid', 'darkblue', 'darkmagenta', 'darkred', 'olivedrab', 'crimson', 'dodgerblue', 'goldenrod']

# Main window settings
window = tk.Tk()
window.geometry('500x250')
window.title('Math Captcha')
window.resizable(False, False)
window.iconbitmap(os.path.join(main_dir, 'app icon.ico'))

# Title and description
tk.Label(window, text='Math Captcha', font=header_font, fg='black').pack()
tk.Label(window, text='Please enter the answer to the math expression in the box below', font=hint_font, fg='black').pack()

# Functions
def generate_captcha_image(text, width=150, height=50):
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("arial.ttf", 45)
    color = rn.choice(colors)
    
    bbox = draw.textbbox((0, 0), text, font=font)
    x = (width - (bbox[2] - bbox[0]) + 10) / 2
    y = (height - (bbox[3] - bbox[1]) - 15) / 3
    draw.text((x, y), text, font=font, fill=color)
    
    for _ in range(220):
        x = rn.randint(0, width)
        y = rn.randint(0, height)
        draw.line(((x, y), (x + rn.randint(-10, 10), y + rn.randint(-10, 10))), fill=color, width=1)
    
    return image.filter(ImageFilter.GaussianBlur(0.4))

def generate_captcha():
    num1, num2 = rn.randint(1, 9), rn.randint(1, 9)
    
    # Selecting an operator based on conditions
    if num1 == num2 * 2 or num1 == num2 * 3 or num1 == num2 * 4 or num1 == num2 * 5:
        operator = '÷'
    elif num1 < 5 or num2 < 5:
        operator = '×'
    elif num1 > num2:
        operator = '-'
    elif num1 < num2:
        operator = '+'
    else:
        operator = '×'
    
    # Creating CAPTCHA text
    captcha_text = f"{num1} {operator} {num2} ="
    return captcha_text, num1, num2, operator

captcha_text, num1, num2, operator = generate_captcha()
captcha_image_path = os.path.join(main_dir, 'captcha.png')
generate_captcha_image(captcha_text).save(captcha_image_path)
captcha_image = ImageTk.PhotoImage(Image.open(captcha_image_path))

# Show captcha and input box
captcha_label = tk.Label(window, image=captcha_image, fg='white', bg='black')
captcha_label.place(x=55, y=90)
captcha_entry = tk.Entry(window, font=app_font)
captcha_entry.place(x=225, y=100)
captcha_entry.focus()

# Captcha update function
def update_captcha():
    global captcha_image, captcha_text, num1, num2, operator
    captcha_text, num1, num2, operator = generate_captcha()
    generate_captcha_image(captcha_text).save(captcha_image_path)
    captcha_image = ImageTk.PhotoImage(Image.open(captcha_image_path))
    captcha_label.config(image=captcha_image)

# CAPTCHA verification function
def verify_captcha():
    answer = captcha_entry.get()
    if re.fullmatch(r'\d+', answer):
        result = {'+': num1 + num2, '-': num1 - num2, '×': num1 * num2, '÷': num1 // num2}.get(operator)
        if int(answer) == result:
            mg.showinfo('Success', 'The captcha answer is correct')
        else:
            mg.showerror('Failed', 'The captcha answer is incorrect')
    else:
        mg.showerror('Error', 'Please enter a valid number')
    captcha_entry.delete(0, tk.END)
    update_captcha()

# Icons and buttons
change_icon = ImageTk.PhotoImage(Image.open(os.path.join(main_dir, 'change icon.png')).resize((50, 50), Image.LANCZOS))
confirm_icon = ImageTk.PhotoImage(Image.open(os.path.join(main_dir, 'confirm icon.png')).resize((50, 50), Image.LANCZOS))

tk.Button(window, image=change_icon, command=update_captcha).place(x=275, y=150)
tk.Button(window, image=confirm_icon, command=verify_captcha).place(x=340, y=150)

window.mainloop()
