"""Running this code will display a flashcard for the user to learn and revise on their Japanese"""
# TODO: Remove timer and allow user to flip the card manually
# TODO: User to have a choice to choose among the 8 parts of speech (noun, adjective, verb, etc.)
# TODO: Add the other parts of speech
from tkinter import Tk, Canvas, Button, PhotoImage
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
df_list = {}

try:
    df = pd.read_csv("./data/words_to_learn.csv")
    df["kanji"] = df["kanji"].fillna(df["kana"])
except FileNotFoundError:
    df = pd.read_csv("./data/nouns_jp.csv")
    df["kanji"] = df["kanji"].fillna(df["kana"])
    df_list = df.to_dict(orient="records")
else:
    df_list = df.to_dict(orient="records")


def new_card():
    """Pulls out a new card showing the Japanese word"""
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(df_list)

    canvas.itemconfig(canvas_img, image=card_front_img)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_word["kanji"], fill="black")
    canvas.itemconfig(card_romaji, text=current_word["romaji"], fill="black")

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    """Flips card to reveal the english translation"""
    canvas.itemconfig(canvas_img, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_word["english"], fill="white")
    canvas.itemconfig(card_romaji, text="", fill="white")


def correct_guess():
    """Will remove correct words guessed and update words to learn in a new CSV file"""
    df_list.remove(current_word)
    to_learn = pd.DataFrame(df_list)
    to_learn.to_csv("./data/words_to_learn.csv", index=False)

    new_card()


window = Tk()
window.title("Japanese-English Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# --------------------- Card --------------------- #
# Canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")

canvas_img = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=1, column=1, columnspan=2)

# Text
card_title = canvas.create_text(400, 150, text="", fill="black", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", fill="black", font=("Ariel", 60, "bold"))
card_romaji = canvas.create_text(400, 330, text="", fill="black", font=("Ariel", 50, "normal"))

# --------------------- Buttons --------------------- #
# 'Wrong' button
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_img, highlightbackground=BACKGROUND_COLOR, command=new_card)
wrong_btn.grid(row=2, column=1)

# 'Right' button
right_img = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_img, highlightbackground=BACKGROUND_COLOR, command=correct_guess)
right_btn.grid(row=2, column=2)

new_card()

window.mainloop()
