from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

DEFAULT_EMAIL = "agarwalmudit14@gmail.com"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_password():
    password_input.delete(0, END)
    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password_gen = "".join(password_list)
    password_input.insert(END, string=password_gen)

    # This will copy the password entered to the clipboard
    pyperclip.copy(password_gen)

# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    website = website_input.get()
    email = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty")
    else:
        # is_ok = messagebox.askokcancel(title=website, message=f"The details entered are: \nEmail: {email} \n"
        #                                                       f"Password: {password} \n\nConfirm if you want to save")

        # if is_ok:
        # with open("data.txt", mode="a") as data:
        #    # data.write(f"{website} | {email} | {password}\n")
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)
        except FileNotFoundError:
            data = new_data

        with open("data.json", "w") as data_file:
            json.dump(data, data_file, indent=4)

        website_input.delete(0, END)
        password_input.delete(0, END)

# ---------------------------Searching for the website---------------------------- #


def find_password():
    website = website_input.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
            password = data[website]["password"]
            email = data[website]["email"]
            messagebox.showinfo(title=website, message=f"email: {email}\npassword:{password}")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Data file does not exist")
    except KeyError:
        messagebox.showerror(title="Error", message="No details for the website found")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=50, pady=50, bg="black")
window.title("Password Manager")


canvas = Canvas()
canvas.config(width=250, height=200, bg="black", highlightthickness=0)
image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=1, column=2)

website_label = Label(padx=5, pady=5)
website_label.config(text="Website:", bg="black", fg="white", font=("Comic Sans MS", 12))
website_label.grid(row=2, column=1)

username_label = Label(padx=5, pady=5)
username_label.config(text="Email/Username:", bg="black", fg="white", font=("Comic Sans MS", 12))
username_label.grid(row=3, column=1)

password_label = Label(padx=5, pady=5)
password_label.config(text="Password:", bg="black", fg="white", font=("Comic Sans MS", 12))
password_label.grid(row=4, column=1)

website_input = Entry(width=30, font=("Arial", 12))
website_input.grid(row=2, column=2)
website_input.focus()

username_input = Entry(width=44, font=("Arial", 12))
username_input.grid(row=3, column=2, columnspan=2)
username_input.insert(END, string=DEFAULT_EMAIL)

password_input = Entry(width=30, font=("Arial", 12))
password_input.grid(row=4, column=2)

generate_button = Button(text="Generate Password", font=("Arial", 9, "bold"), bg="skyblue",
                         command=generate_password, pady=-1)
generate_button.grid(row=4, column=3)

add_button = Button(width=49, text="Add", font=("Arial", 10, "bold"), bg="pink", command=save)
add_button.grid(row=5, column=2, columnspan=2)

search_button = Button(width=16, text="Search", font=("Arial", 9, "bold"), bg="skyblue",
                       command=find_password, pady=-1)
search_button.grid(row=2, column=3)

window.mainloop()
