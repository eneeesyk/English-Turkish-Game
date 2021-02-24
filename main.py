from tkinter import *
import pandas as pd
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# --------------------------------- WORDS DATA --------------------------------- #
try:
    data = pd.read_csv("data/words_that_learned.csv")
except FileNotFoundError:
    original_data = pd.read_csv("data/turkish_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(card_word, text=current_card["English"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(5000, func=flip_card)


# --------------------------------- FLIP CARDS  --------------------------------- #
def flip_card():
    canvas.itemconfig(card_title, text="Turkish", fill="white")
    canvas.itemconfig(card_word, text=current_card["Turkish"], fill="white")
    canvas.itemconfig(card_background, image=card_back_img)


# --------------------------------- SAVE KNOWN WORDS  --------------------------------- #
def is_known():
    to_learn.remove(current_card)
    new_data = pd.DataFrame(to_learn)
    new_data.to_csv("data/words_that_learned.csv", index=False)
    next_card()


# --------------------------------- UI SETUP  --------------------------------- #
window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(5000, func=flip_card)

# Canvas
canvas = Canvas(width=800, height=526)
card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 30, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

# Buttons
wrong_image = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, bd=0, command=next_card)
right_image = PhotoImage(file="./images/right.png")
right_button = Button(image=right_image, highlightthickness=0, bd=0, command=is_known)

wrong_button.grid(row=1, column=0)
right_button.grid(row=1, column=1)

next_card()

window.mainloop()
