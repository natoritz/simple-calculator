import tkinter as tk
from math import sqrt, sin, cos, tan, log10, pi, exp, factorial
from tkinter import messagebox, filedialog, simpledialog
import pyperclip

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("450x700")
        self.root.resizable(False, False)
        
        # Variables
        self.expression = ""
        self.input_text = tk.StringVar()
        self.history = []
        self.memory = 0
        self.undo_stack = []
        self.redo_stack = []
        self.dark_mode = False
        self.precision = 2  # Default precision
        
        # Initialize UI
        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = tk.Frame(self.root, bd=10, relief=tk.RIDGE)
        input_frame.pack(fill=tk.BOTH, expand=True)

        input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('Arial', 24, 'bold'), 
                               justify=tk.RIGHT, bd=10, insertwidth=4)
        input_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bd=10, relief=tk.RIDGE)
        buttons_frame.pack(fill=tk.BOTH, expand=True)

        # Button Layout
        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('%', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('CE', 5, 1), ('√', 5, 2), ('=', 5, 3),
            ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('log', 6, 3),
            ('M+', 7, 0), ('M-', 7, 1), ('MR', 7, 2), ('MC', 7, 3),
            ('Undo', 8, 0), ('Redo', 8, 1), ('Copy', 8, 2), ('Theme', 8, 3),
            ('Export', 9, 0), ('Precision', 9, 1), ('π', 9, 2), ('!', 9, 3)
        ]

        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, padx=20, pady=20, font=('Arial', 16, 'bold'),
                               command=lambda txt=text: self.on_button_click(txt))
            button.grid(row=row, column=col, sticky="nsew")

        # Configure grid resizing
        for i in range(10):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)

        # History Log
        self.history_log = tk.Text(self.root, height=5, font=('Arial', 12), state=tk.DISABLED)
        self.history_log.pack(fill=tk.BOTH, expand=True)

    def on_button_click(self, char):
        if char == 'C':
            self.clear_all()
        elif char == 'CE':
            self.clear_entry()
        elif char == '=':
            self.evaluate_expression()
        elif char == '√':
            self.sqrt_operation()
        elif char in ('sin', 'cos', 'tan', 'log'):
            self.trigonometric_operations(char)
        elif char == 'M+':
            self.memory_add()
        elif char == 'M-':
            self.memory_subtract()
        elif char == 'MR':
            self.memory_recall()
        elif char == 'MC':
            self.memory_clear()
        elif char == 'Undo':
            self.undo()
        elif char == 'Redo':
            self.redo()
        elif char == 'Copy':
            self.copy_to_clipboard()
        elif char == 'Theme':
            self.toggle_theme()
        elif char == 'Export':
            self.export_history()
        elif char == 'Precision':
            self.set_precision()
        elif char == 'π':
            self.append_constant(pi)
        elif char == '!':
            self.factorial_operation()
        else:
            self.append_to_expression(char)

        self.input_text.set(self.expression)

    def append_to_expression(self, char):
        """Appends a character to the current expression."""
        self.undo_stack.append(self.expression)
        self.expression += str(char)

    def clear_all(self):
        """Clears the entire expression and stacks."""
        self.expression = ""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def clear_entry(self):
        """Removes the last character from the expression."""
        self.expression = self.expression[:-1]

    def evaluate_expression(self):
        """Evaluates the current expression."""
        try:
            result = str(round(eval(self.expression), self.precision))
            self.history.append(f"{self.expression} = {result}")
            self.update_history_log()
            self.expression = result
        except Exception:
            self.expression = "Error"

    def sqrt_operation(self):
        """Calculates the square root of the current expression."""
        try:
            self.expression = str(round(sqrt(float(self.expression)), self.precision))
        except Exception:
            self.expression = "Error"

    def trigonometric_operations(self, operation):
        """Performs trigonometric operations."""
        try:
            value = float(self.expression)
            if operation == 'sin':
                self.expression = str(round(sin(value), self.precision))
            elif operation == 'cos':
                self.expression = str(round(cos(value), self.precision))
            elif operation == 'tan':
                self.expression = str(round(tan(value), self.precision))
            elif operation == 'log':
                self.expression = str(round(log10(value), self.precision))
        except Exception:
            self.expression = "Error"

    def memory_add(self):
        """Adds the current expression to memory."""
        try:
            self.memory += float(self.expression)
        except Exception:
            pass

    def memory_subtract(self):
        """Subtracts the current expression from memory."""
        try:
            self.memory -= float(self.expression)
        except Exception:
            pass

    def memory_recall(self):
        """Recalls the value stored in memory."""
        self.expression = str(self.memory)

    def memory_clear(self):
        """Clears the memory."""
        self.memory = 0

    def undo(self):
        """Undoes the last action."""
        if self.expression:
            self.redo_stack.append(self.expression)
            self.expression = self.undo_stack.pop() if self.undo_stack else ""

    def redo(self):
        """Redoes the last undone action."""
        if self.redo_stack:
            self.undo_stack.append(self.expression)
            self.expression = self.redo_stack.pop()

    def copy_to_clipboard(self):
        """Copies the current expression to the clipboard."""
        pyperclip.copy(self.expression)
        messagebox.showinfo("Copied", "Result copied to clipboard!")

    def toggle_theme(self):
        """Toggles between light and dark themes."""
        self.dark_mode = not self.dark_mode
        bg_color = "#2b2b2b" if self.dark_mode else "#f0f0f0"
        fg_color = "#ffffff" if self.dark_mode else "#000000"
        btn_color = "#4a4a4a" if self.dark_mode else "#e0e0e0"

        self.root.configure(bg=bg_color)
        self.history_log.config(bg=bg_color, fg=fg_color)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=bg_color)
            elif isinstance(widget, tk.Button):
                widget.config(bg=btn_color, fg=fg_color)

    def export_history(self):
        """Exports the calculation history to a file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("CSV Files", "*.csv")])
        if file_path:
            with open(file_path, "w") as file:
                if file_path.endswith(".csv"):
                    file.write("Expression,Result\n")
                    for entry in self.history:
                        expr, result = entry.split("=")
                        file.write(f"{expr.strip()},{result.strip()}\n")
                else:
                    file.write("\n".join(self.history))
            messagebox.showinfo("Exported", "History exported successfully!")

    def set_precision(self):
        """Sets the number of decimal places for results."""
        precision = simpledialog.askinteger("Precision", "Enter number of decimal places:", minvalue=0, maxvalue=10)
        if precision is not None:
            self.precision = precision

    def append_constant(self, constant):
        """Appends a mathematical constant to the expression."""
        self.expression += str(constant)

    def factorial_operation(self):
        """Calculates the factorial of the current expression."""
        try:
            value = int(self.expression)
            self.expression = str(factorial(value))
        except Exception:
            self.expression = "Error"

    def update_history_log(self):
        """Updates the history log display."""
        self.history_log.config(state=tk.NORMAL)
        self.history_log.delete(1.0, tk.END)
        for entry in self.history[-5:]:
            self.history_log.insert(tk.END, entry + "\n")
        self.history_log.config(state=tk.DISABLED)

    def handle_keyboard_input(self, event):
        """Handles keyboard input."""
        key = event.char
        if key.isdigit() or key in '+-*/.%':
            self.append_to_expression(key)
        elif key == '\r':  # Enter key
            self.evaluate_expression()
        elif key == '\x08':  # Backspace key
            self.clear_entry()

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.bind("<Key>", calc.handle_keyboard_input)
    root.mainloop()