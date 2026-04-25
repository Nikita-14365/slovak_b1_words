import tkinter as tk
from tkinter.font import Font
from random import choice, choices


word = None
answered = False

with open("словацкий_словарь.db4.py", "r") as file:
    db = eval(file.read())

wordset = choices(tuple(filter(lambda x: x and db[x][0] and db[x][1]<10, db.keys())), k=10)

def check_word():
    global answered
    answered = True
    if text.get() == db[word][0]:
        entry["bg"] = "green"
        db[word][1] += 1
        if db[word][1] >= 10:
            wordset.remove(word)
            wordset.append(choice(tuple(filter(lambda x: x and db[x][0] and db[x][1]<10, db.keys()))))
    else:
        entry["bg"] = "red"
        right["text"] = db[word][0]
        db[word][1] = max(db[word][1]-1, 0)

def next_word():
    global word, answered
    entry["bg"]="white"
    right["text"] = ""
    text.set("")
    answered = False
    word = choice(wordset)
    label["text"] = word

def end():
    with open("словацкий_словарь.db4.py", "w") as file:
        file.write("{\n")
        for k, v in db.items():
            file.write(f"\t'{k}': {v},\n")
        file.write("}")
    root.destroy()

root = tk.Tk()
root.geometry("700x500")

font = Font(size=32)

frame = tk.Frame(root, width=500, height=700)

label = tk.Label(frame, font=font, border=32)

text = tk.StringVar(root)

entry = tk.Entry(frame, font=font, textvariable=text)

right = tk.Label(frame, font=font, border=32)

buttonc = tk.Button(frame, command=check_word, text="check", font=font)
buttonn = tk.Button(frame, command=next_word, text="next", font=font)

frame.pack()
label.pack()
entry.pack()
right.pack()
buttonc.pack()
buttonn.pack()

root.bind("<Escape>", lambda x: end())
root.bind("<Return>", lambda x: next_word() if answered else check_word())

if __name__ == "__main__":
    next_word()
    root.mainloop()
