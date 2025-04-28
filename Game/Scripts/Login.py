import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json  # Import JSON module
from Game import open_room1  # Import the function to open Room1

# File to store user credentials
CREDENTIALS_FILE = "user_credentials.json"

# Load user credentials from file
def load_credentials():
    try:
        with open(CREDENTIALS_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save user credentials to file
def save_credentials():
    with open(CREDENTIALS_FILE, "w") as file:
        json.dump(user_credentials, file)

user_credentials = load_credentials()

def sign_up():
    username = username_entry.get()
    password = password_entry.get()
    if username in user_credentials:
        messagebox.showerror("Error", "Username already exists!")
    else:
        user_credentials[username] = password
        save_credentials()  # Save updated credentials
        messagebox.showinfo("Success", "Sign-up successful!")

def open_difficulty_selection():
    root.destroy()  # Close the login/sign-up window
    year_window = tk.Tk()  # Create a new main window for year selection
    year_window.title("Year Selection")
    
    # Set window dimensions
    window_width = 400
    window_height = 300
    screen_width = year_window.winfo_screenwidth()
    screen_height = year_window.winfo_screenheight()
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)
    year_window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    # Define a callback to close the year selection window
    def on_button_click():
        year_window.destroy()

    tk.Button(year_window, text="Years 9-10", font=("Arial", 14), command=lambda: [on_button_click(), open_room1()]).pack(pady=10)
    tk.Button(year_window, text="Year 11", font=("Arial", 14), command=on_button_click).pack(pady=10)
    tk.Button(year_window, text="Year 12", font=("Arial", 14), command=on_button_click).pack(pady=10)
    tk.Button(year_window, text="Year 13", font=("Arial", 14), command=on_button_click).pack(pady=10)

    year_window.mainloop()

def login():
    username = username_entry.get()
    password = password_entry.get()
    if username in user_credentials and user_credentials[username] == password:
        messagebox.showinfo("Success", "Login successful!")
        open_difficulty_selection()  # Open year selection window
    else:
        messagebox.showerror("Error", "Invalid username or password!")

def clear_username_placeholder(event):
    if username_entry.get() == "USERNAME":
        username_entry.delete(0, tk.END)
        username_entry.config(fg="black")

def add_username_placeholder(event):
    if username_entry.get() == "":
        username_entry.insert(0, "USERNAME")
        username_entry.config(fg="grey")

def clear_password_placeholder(event):
    if password_entry.get() == "PASSWORD":
        password_entry.delete(0, tk.END)
        password_entry.config(fg="black", show="*")

def add_password_placeholder(event):
    if password_entry.get() == "":
        password_entry.insert(0, "PASSWORD")
        password_entry.config(fg="grey", show="")

root = tk.Tk()
root.title("Game Login/Sign-Up")

# Center the window on the screen
window_width = 1280
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width // 2) - (window_width // 2)
y_coordinate = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

background_image = Image.open("Graphics\Backgrounds\Title\Title.png")
background_image = background_image.resize((1280, 720), Image.Resampling.LANCZOS)
background_photo = ImageTk.PhotoImage(background_image)

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_photo, anchor="nw")

username_entry = tk.Entry(root, font=("Arial", 24), fg="grey")
username_entry.insert(0, "USERNAME")
username_entry.bind("<FocusIn>", clear_username_placeholder)
username_entry.bind("<FocusOut>", add_username_placeholder)
username_entry.place(x=640, y=300)

password_entry = tk.Entry(root, font=("Arial", 24), fg="grey")
password_entry.insert(0, "PASSWORD")
password_entry.bind("<FocusIn>", clear_password_placeholder)
password_entry.bind("<FocusOut>", add_password_placeholder)
password_entry.place(x=640, y=360)

sign_up_button = tk.Button(root, text="Sign Up", command=sign_up, font=("Arial", 12))
sign_up_button.place(x=580, y=450)

login_button = tk.Button(root, text="Login", command=login, font=("Arial", 12))
login_button.place(x=700, y=450)

root.mainloop()
