import tkinter as tk
from math import sqrt

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator")
        
        self.expression = ""
        self.input_text = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        input_frame = tk.Frame(self.root)
        input_frame.pack()

        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('arial', 18, 'bold'), bd=10, insertwidth=4, width=14, borderwidth=4)
        input_field.grid(row=0, column=0, columnspan=4)
        input_field.pack()

        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack()

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('√', 5, 1), ('^', 5, 2), ('=', 5, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, padx=20, pady=20, font=('arial', 18, 'bold'),
                               command=lambda txt=text: self.on_button_click(txt))
            button.grid(row=row, column=col)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                self.expression = str(eval(self.expression))
            except Exception as e:
                self.expression = "Error"
        elif char == '√':
            try:
                self.expression = str(sqrt(float(self.expression)))
            except Exception as e:
                self.expression = "Error"
        elif char == '^':
            self.expression += '**'
        else:
            self.expression += str(char)
        
        self.input_text.set(self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
