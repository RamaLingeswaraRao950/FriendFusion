import tkinter as tk
from tkinter import messagebox
import random
from playsound import playsound
import threading


def friendship_score(name1, name2):
    name1, name2 = name1.lower(), name2.lower()
    score = 0

    shared_letters = set(name1) & set(name2)
    vowels = set('aeiou')
    score += len(shared_letters) * 5
    score += len(vowels & shared_letters) * 10

    min_length = min(len(name1), len(name2))
    position_score = sum(1 for i in range(min_length) if name1[i] == name2[i])
    score += position_score * 3

    length_diff = abs(len(name1) - len(name2))
    score += max(0, 10 - length_diff * 2)

    return min(score, 100)


fun_pairs = [
    "Chai & Samosa", "Peanut Butter & Jelly", "Coffee & Cookies",
    "Batman & Robin", "Salt & Pepper", "Burger & Fries"
]


def get_themed_message(score):
    pair = random.choice(fun_pairs)
    if score == 80:
        return f"🎉 Perfect match! Like {pair} forever! 💯🔥"
    elif score > 60:
        return f"🔥 You're like {pair} — made for each other! 🔥"
    elif score > 40:
        return f"😊 Great vibes! Like {pair}! 🍪☕"
    elif score > 20:
        return "🤔 Hmm... maybe a bit of effort needed. 🤝"
    else:
        return "😅 Well... opposites attract, maybe? 💫"


def get_advice(score):
    if score == 80:
        return "Unbreakable bond! Treasure this friendship forever! 💖✨"
    elif score > 60:
        return "Keep nurturing this awesome bond! 💖"
    elif score > 40:
        return "Hang out more and discover new fun things together! 🎉"
    elif score > 20:
        return "Try to understand each other better. 🤗"
    else:
        return "Give it time, friendship grows slowly. 🌱"


# --- GUI Animations ---
falling_objects = []


def spawn_hearts():
    """Background falling hearts animation."""
    if len(falling_objects) < 20:
        x = random.randint(20, 430)
        obj = tk.Label(root, text="💖", font=("Helvetica", 12), bg="#FFF0F5")
        obj.place(x=x, y=0)
        falling_objects.append((obj, random.randint(1, 3)))
    root.after(500, spawn_hearts)


def move_objects():
    """Move all falling objects downwards."""
    for obj, speed in list(falling_objects):
        y = obj.winfo_y()
        if y < 430:
            obj.place(y=y+speed)
        else:
            obj.place_forget()
            falling_objects.remove((obj, speed))
    root.after(50, move_objects)


def confetti_explosion():
    """Confetti effect when score = 80."""
    for _ in range(30):
        x = random.randint(20, 430)
        y = random.randint(20, 200)
        confetti = tk.Label(root, text=random.choice(
            ["🎉", "✨", "🌟", "💫", "🎊"]), font=("Helvetica", 14), bg="#FFF0F5")
        confetti.place(x=x, y=y)
        root.after(1000, confetti.destroy)


def update_score_bar(score):
    if score > 80:
        color = "#4CAF50"  # green
    elif score > 60:
        color = "#FFEB3B"  # yellow
    elif score > 40:
        color = "#FF9800"  # orange
    else:
        color = "#F44336"  # red

    score_bar.config(width=int(score*3), bg=color)


def play_sound(file):
    """Play sound in a separate thread to avoid freezing UI."""
    threading.Thread(target=playsound, args=(file,), daemon=True).start()


def calculate():
    name1 = entry_name1.get().strip()
    name2 = entry_name2.get().strip()

    if not name1 or not name2:
        messagebox.showwarning("Input Error", "Please enter both names!")
        return

    score = friendship_score(name1, name2)
    message = get_themed_message(score)
    advice = get_advice(score)

    result_text.set(f"Friendship Score: {score}%\n{message}\n{advice}")
    update_score_bar(score)

    # Play sounds
    play_sound("ding.mp3")
    if score == 80:
        confetti_explosion()
        play_sound("cheer.mp3")


# --- Tkinter Window ---
root = tk.Tk()
root.title("💕 Measure the magic of friendship 💕")
root.geometry("555x555")
root.resizable(False, False)
root.configure(bg="#FFF0F5")

# --- Widgets ---
tk.Label(root, text="🔗 FriendFusion 🔗",
         font=("Helvetica", 16, "bold"), bg="#FFF0F5").pack(pady=10)

frame = tk.Frame(root, bg="#FFF0F5")
frame.pack(pady=10)

tk.Label(frame, text="Enter First Name:", font=("Helvetica", 12),
         bg="#FFF0F5").grid(row=0, column=0, padx=5, pady=5, sticky='e')
entry_name1 = tk.Entry(frame, font=("Helvetica", 12))
entry_name1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Enter Second Name:", font=("Helvetica", 12),
         bg="#FFF0F5").grid(row=1, column=0, padx=5, pady=5, sticky='e')
entry_name2 = tk.Entry(frame, font=("Helvetica", 12))
entry_name2.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Calculate Score 💖", font=("Helvetica", 12, "bold"),
          bg="#FF69B4", fg="white", command=calculate).pack(pady=15)

score_bar_frame = tk.Frame(root, bg="#DDD", width=300, height=20)
score_bar_frame.pack(pady=10)
score_bar = tk.Frame(score_bar_frame, bg="#4CAF50", width=0, height=20)
score_bar.pack(side="left")

result_text = tk.StringVar()
tk.Label(root, textvariable=result_text, font=("Helvetica", 12),
         bg="#FFF0F5", justify="center").pack(pady=10)

# Start background animations
spawn_hearts()
move_objects()

root.mainloop()
