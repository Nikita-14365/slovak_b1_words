import tkinter as tk
from tkinter.font import Font
from random import choice, choices


word = None
answered = False

with open("db.py", "r") as file:
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
            wordset.append(choice(tuple(filter(lambda x: x and db[x][0] and db[x][1]<10 and x not in wordset, db.keys()))))
    else:
        entry["bg"] = "red"
        right["text"] = db[word][0]
        db[word][1] = max(db[word][1]-1, 0)

def next_word():
    global word, answered
    entry["bg"]="white"
    right["text"] = ""
    text.set("")
    counter["text"] = f"{sum(1 for k, v in db.items() if k and v[0] and v[1] >= 10)} / {len(db)}"
    answered = False
    word = choice(wordset)
    label["text"] = word

def end():
    with open("db.py", "w") as file:
        file.write("{\n")
        for k, v in db.items():
            file.write(f"\t{repr(k)}: {repr(v)},\n")
        file.write("}")
    root.destroy()

root = tk.Tk()
#root.geometry("700x500")
root.title("тренажёр словацких слов")

font = Font(size=32)

label = tk.Label(root, font=font, border=32)

text = tk.StringVar(root)

entry = tk.Entry(root, font=font, textvariable=text, width=32)

right = tk.Label(root, font=font, border=32)

counter = tk.Label(root, font=font, border=32, width=10)

buttonc = tk.Button(root, command=check_word, text="проверить", font=font, width=10)
buttonn = tk.Button(root, command=next_word, text="дальше", font=font, width=10)

label.grid(row=0, column=0, columnspan=3)
entry.grid(row=1, column=0, columnspan=3)
right.grid(row=2, column=0, columnspan=3)
buttonc.grid(row=3, column=0)
counter.grid(row=3, column=1)
buttonn.grid(row=3, column=2)

root.bind("<Escape>", lambda x: end())
root.bind("<Return>", lambda x: next_word() if answered else check_word())

if __name__ == "__main__":
    next_word()
    root.mainloop()
