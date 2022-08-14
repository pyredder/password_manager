import json
from random import randint, choice, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip

FILE = 'Enter File Path: *.json'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_pwd():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # e.g. 4 letter, 2 symbol, 2 number = JduE&!91
    pwd_letter = [choice(letters) for _ in range(randint(8, 10))]
    pwd_number = [choice(numbers) for _ in range(randint(2, 4))]
    pwd_symbol = [choice(symbols) for _ in range(randint(2, 4))]

    pwd_string = pwd_letter + pwd_number + pwd_symbol
    shuffle(pwd_string)
    pwd = "".join(pwd_string)
    password_t.delete(0, END)
    password_t.insert(0, pwd)
    pyperclip.copy(pwd)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_to_memory():
    website = website_t.get()
    username = username_t.get()
    password = password_t.get()

    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title='Error', message="All fields are mandatory!\nPlease enter all details")
    else:
        confirm = messagebox.askokcancel(title=website, message=f"Please verify your details: \nUsername: {username}\n"
                                                                f"Password: {password}")
        if confirm:
            data_format = {
                website: {
                    'email': username,
                    'password': password
                }
            }

            try:
                with open(FILE, mode='r') as datafile:
                    # Read
                    data = json.load(datafile)
            except FileNotFoundError:
                with open(FILE, mode='w') as datafile:
                    json.dump(data_format, datafile, indent=4)
            else:
                # Update
                data.update(data_format)
                with open(FILE, mode='w') as datafile:
                    # Update
                    json.dump(data, datafile, indent=4)
            finally:
                website_t.delete(0, END)
                password_t.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search_password():
    website = website_t.get()
    try:
        with open(FILE, mode='r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title=website, message=f"No Database file found!")
    else:
        if website in data:
            username = data[website]['email']
            password = data[website]['password']
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f'Username: {username}\nPassword: {password}\n copied')
        else:
            messagebox.showinfo(title=website, message=f"This data does not exist")


# ---------------------------- UI SETUP ------------------------------- #
# Window
root = Tk()
root.title('Password Manager')
root.config(pady=50, padx=50)

# Canvas with Logo
canvas = Canvas(width=200, height=300)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 150, image=lock)
canvas.grid(row=0, column=1)

# 3 Labels: Website, Username , Password + Text box for input
website_l = Label(text='Website: ')
website_t = Entry(width=23)
website_t.focus()
search = Button(text='Search', command=search_password)

username_l = Label(text='Email/Username: ')
username_t = Entry(width=35)
username_t.insert(0, 'Default Email')

password_l = Label(text='Password: ')
password_t = Entry(width=24)
generate = Button(text='Generate', command=generate_pwd)

add_b = Button(text='Add', width=33, command=add_to_memory)

# Geometry
website_l.grid(row=1, column=0)
website_t.grid(row=1, column=1)
search.grid(row=1, column=2)
username_l.grid(row=2, column=0)
username_t.grid(row=2, column=1, columnspan=2)
password_l.grid(row=3, column=0)
password_t.grid(row=3, column=1)
generate.grid(row=3, column=2)
add_b.grid(row=4, column=1, columnspan=2)

root.mainloop()
