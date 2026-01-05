import tkinter as tk
from functools import partial

def load_questions(filename):
    with open(filename, "r") as file:
        lines = file.read().strip().split("\n\n")  # Each question block

    questions = []

    for block in lines:
        parts = block.strip().split("\n")
        question_text = parts[0][3:]  # Remove "Q: "
        options = [(p[0], p[3:]) for p in parts[1:5]]
        answer = parts[5].split(": ")[1]
        questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })

    return questions

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title("Quiz App")
        self.questions = questions
        self.current = 0
        self.score = 0

        self.question_label = tk.Label(master, text="", wraplength=400, font=("Arial", 14))
        self.question_label.pack(pady=20)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(master, text="", width=30, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=5)
            self.buttons.append(btn)

        self.display_question()

    def display_question(self):
        q = self.questions[self.current]
        self.question_label.config(text=q["question"])

        for idx, (letter, option) in enumerate(q["options"]):
            self.buttons[idx].config(text=f"{letter}) {option}")

    def check_answer(self, idx):
        selected_letter, _ = self.questions[self.current]["options"][idx]
        correct_letter = self.questions[self.current]["answer"]

        if selected_letter == correct_letter:
            self.score += 1

        self.current += 1
        if self.current >= len(self.questions):
            self.show_result()
        else:
            self.display_question()

    def show_result(self):
        for btn in self.buttons:
            btn.pack_forget()
        self.question_label.config(text=f"Quiz finished! Your score: {self.score}/{len(self.questions)}")

if __name__ == "__main__":
    root = tk.Tk()
    questions = load_questions("questions.txt")  
    app = QuizApp(root, questions)
    root.mainloop()
