import tkinter as tk
from math import sqrt, sin, cos, tan, log10, pi, exp, factorial
from tkinter import messagebox, filedialog, simpledialog
import pyperclip
import logging

# Configure logging for development mode
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AdvancedCalculator:
    VERSION = "1.5.2"  # Format: Major.Minor.Patch

    def __init__(self, root):
        self.root = root
        self.root.title(f"Modern Advanced Calculator v{self.VERSION}")
        self.root.geometry("600x900")
        self.root.resizable(True, True)
        
        # Variables
        self.expression = ""
        self.input_text = tk.StringVar()
        self.history = []
        self.memory = 0
        self.undo_stack = []
        self.redo_stack = []
        self.dark_mode = False
        self.precision = 2  # Default precision
        self.debug_mode = False  # Development mode
        self.angle_mode = "radians"  # Default angle mode (radians/degrees)
        self.scientific_mode = False  # Scientific mode toggle
        
        # Initialize UI
        self.create_widgets()
        self.setup_keyboard_bindings()

    def create_widgets(self):
        """Creates the main UI components."""
        # Title Bar
        title_frame = tk.Frame(self.root, bd=0, relief=tk.FLAT, bg=self.get_bg_color())
        title_frame.pack(fill=tk.X)

        title_label = tk.Label(title_frame, text=f"Advanced Calculator v{self.VERSION}", font=('Arial', 14, 'bold'),
                               bg=self.get_bg_color(), fg=self.get_fg_color())
        title_label.pack(pady=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bd=10, relief=tk.FLAT, bg=self.get_bg_color())
        input_frame.pack(fill=tk.BOTH, expand=True)

        self.input_field = tk.Entry(input_frame, textvariable=self.input_text, font=('Arial', 24, 'bold'), 
                                    justify=tk.RIGHT, bd=0, insertwidth=4, bg=self.get_bg_color(), fg=self.get_fg_color(),
                                    highlightthickness=0)
        self.input_field.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Buttons Frame
        buttons_frame = tk.Frame(self.root, bd=10, relief=tk.FLAT, bg=self.get_bg_color())
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
            ('Export', 9, 0), ('Precision', 9, 1), ('π', 9, 2), ('!', 9, 3),
            ('Settings', 10, 0), ('Angle Mode', 10, 1), ('Sci Mode', 10, 3)  # New Settings, Angle Mode, and Sci Mode buttons
        ]

        for (text, row, col) in buttons:
            button = tk.Button(buttons_frame, text=text, padx=20, pady=20, font=('Arial', 16, 'bold'),
                               command=lambda txt=text: self.on_button_click(txt),
                               bg=self.get_btn_color(), fg=self.get_fg_color(), relief=tk.FLAT,
                               activebackground=self.get_btn_color(), activeforeground=self.get_fg_color())
            button.grid(row=row, column=col, sticky="nsew")

        # Configure grid resizing
        for i in range(11):  # Updated for new Settings and Debug buttons
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)

        # History Log
        self.history_log = tk.Text(self.root, height=5, font=('Arial', 12), state=tk.DISABLED,
                                   bg=self.get_bg_color(), fg=self.get_fg_color(), bd=0, highlightthickness=0)
        self.history_log.pack(fill=tk.BOTH, expand=True)

    def setup_keyboard_bindings(self):
        """Binds keyboard events to the calculator."""
        self.root.bind("<Key>", self.handle_keyboard_input)

    def get_bg_color(self):
        return "#2b2b2b" if self.dark_mode else "#f0f0f0"

    def get_fg_color(self):
        return "#ffffff" if self.dark_mode else "#000000"

    def get_btn_color(self):
        return "#4a4a4a" if self.dark_mode else "#e0e0e0"

    def on_button_click(self, char):
        """Handles button clicks."""
        try:
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
            elif char == 'Debug':  # Debug Mode Toggle
                self.toggle_debug_mode()
            elif char == 'Settings':  # Open Settings Menu
                self.open_settings_menu()
            elif char == 'Angle Mode':  # Toggle Angle Mode
                self.toggle_angle_mode()
            elif char == 'Sci Mode':  # Toggle Scientific Mode
                self.toggle_scientific_mode()
            else:
                self.append_to_expression(char)
        except Exception as e:
            self.expression = "Error"
            if self.debug_mode:
                logging.error(f"Error in button click ({char}): {e}")
            messagebox.showerror("Error", str(e))
        
        self.input_text.set(self.expression)

    def append_to_expression(self, char):
        """Appends a character to the current expression."""
        if self.expression == "Error":
            self.expression = ""  # Clear error state before appending
        self.undo_stack.append(self.expression)
        self.expression += str(char)

    def clear_all(self):
        """Clears the entire expression and stacks."""
        self.expression = ""
        self.undo_stack.clear()
        self.redo_stack.clear()

    def clear_entry(self):
        """Removes the last character from the expression."""
        if self.expression:
            self.expression = self.expression[:-1]

    def evaluate_expression(self):
        """Evaluates the current expression."""
        try:
            # Handle empty expressions
            if not self.expression.strip():
                self.expression = "0"
                return

            # Evaluate the expression
            result = str(round(eval(self.expression), self.precision))
            self.history.append(f"{self.expression} = {result}")
            self.update_history_log()
            self.expression = result
        except ZeroDivisionError:
            self.expression = "Error: Division by zero"
        except SyntaxError:
            self.expression = "Error: Invalid syntax"
        except Exception as e:
            self.expression = "Error"
            if self.debug_mode:
                logging.error(f"Error evaluating expression: {e}")

    def sqrt_operation(self):
        """Calculates the square root of the current expression."""
        try:
            value = float(self.expression)
            if value < 0:
                raise ValueError("Square root of negative number")
            self.expression = str(round(sqrt(value), self.precision))
        except Exception as e:
            self.expression = "Error"
            if self.debug_mode:
                logging.error(f"Error in sqrt operation: {e}")

    def trigonometric_operations(self, operation):
        """Performs trigonometric operations."""
        try:
            value = float(self.expression)
            if self.angle_mode == "degrees":
                value = value * pi / 180  # Convert degrees to radians
            if operation == 'sin':
                self.expression = str(round(sin(value), self.precision))
            elif operation == 'cos':
                self.expression = str(round(cos(value), self.precision))
            elif operation == 'tan':
                self.expression = str(round(tan(value), self.precision))
            elif operation == 'log':
                if value <= 0:
                    raise ValueError("Logarithm of non-positive number")
                self.expression = str(round(log10(value), self.precision))
        except Exception as e:
            self.expression = "Error"
            if self.debug_mode:
                logging.error(f"Error in trigonometric operation ({operation}): {e}")

    def memory_add(self):
        """Adds the current expression to memory."""
        try:
            self.memory += float(self.expression)
        except Exception as e:
            if self.debug_mode:
                logging.error(f"Error adding to memory: {e}")

    def memory_subtract(self):
        """Subtracts the current expression from memory."""
        try:
            self.memory -= float(self.expression)
        except Exception as e:
            if self.debug_mode:
                logging.error(f"Error subtracting from memory: {e}")

    def memory_recall(self):
        """Recalls the value stored in memory."""
        self.expression = str(self.memory)

    def memory_clear(self):
        """Clears the memory."""
        self.memory = 0

    def undo(self):
        """Undoes the last action."""
        if self.undo_stack:
            self.redo_stack.append(self.expression)
            self.expression = self.undo_stack.pop()

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
        self.refresh_ui()

    def export_history(self):
        """Exports the calculation history to a file."""
        if not self.history:
            messagebox.showinfo("No History", "No history to export.")
            return

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
        if self.expression == "Error":
            self.expression = ""  # Clear error state before appending
        self.expression += str(constant)

    def factorial_operation(self):
        """Calculates the factorial of the current expression."""
        try:
            value = int(self.expression)
            if value < 0:
                raise ValueError("Factorial of negative number")
            self.expression = str(factorial(value))
        except Exception as e:
            self.expression = "Error"
            if self.debug_mode:
                logging.error(f"Error in factorial operation: {e}")

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

    def refresh_ui(self):
        """Refreshes the UI when theme changes."""
        self.root.configure(bg=self.get_bg_color())
        self.input_field.config(bg=self.get_bg_color(), fg=self.get_fg_color())
        self.history_log.config(bg=self.get_bg_color(), fg=self.get_fg_color())
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.config(bg=self.get_bg_color())
            elif isinstance(widget, tk.Button):
                widget.config(bg=self.get_btn_color(), fg=self.get_fg_color())

    def toggle_debug_mode(self):
        """Toggles debug mode."""
        self.debug_mode = not self.debug_mode
        if self.debug_mode:
            logging.info("Debug mode enabled.")
            messagebox.showinfo("Debug Mode", "Debug mode is now enabled. Logs will appear in the console.")
        else:
            logging.info("Debug mode disabled.")
            messagebox.showinfo("Debug Mode", "Debug mode is now disabled.")

    def toggle_angle_mode(self):
        """Toggles between radians and degrees for trigonometric functions."""
        self.angle_mode = "degrees" if self.angle_mode == "radians" else "radians"
        messagebox.showinfo("Angle Mode", f"Angle mode set to {self.angle_mode.capitalize()}.")

    def toggle_scientific_mode(self):
        """Toggles scientific mode."""
        self.scientific_mode = not self.scientific_mode
        if self.scientific_mode:
            messagebox.showinfo("Scientific Mode", "Scientific mode enabled.")
        else:
            messagebox.showinfo("Scientific Mode", "Scientific mode disabled.")

    def open_settings_menu(self):
        """Opens a settings menu for advanced preferences."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x500")
        settings_window.resizable(False, False)
        settings_window.configure(bg=self.get_bg_color())

        # Precision Setting
        precision_label = tk.Label(settings_window, text="Set Precision:", font=('Arial', 12),
                                   bg=self.get_bg_color(), fg=self.get_fg_color())
        precision_label.pack(pady=5)

        precision_scale = tk.Scale(settings_window, from_=0, to=10, orient=tk.HORIZONTAL, length=300,
                                   bg=self.get_bg_color(), fg=self.get_fg_color(), highlightthickness=0,
                                   command=lambda val: setattr(self, 'precision', int(val)))
        precision_scale.set(self.precision)
        precision_scale.pack(pady=5)

        # Theme Setting
        theme_label = tk.Label(settings_window, text="Toggle Theme:", font=('Arial', 12),
                               bg=self.get_bg_color(), fg=self.get_fg_color())
        theme_label.pack(pady=5)

        theme_button = tk.Button(settings_window, text="Toggle Theme", font=('Arial', 12),
                                 command=self.toggle_theme, bg=self.get_btn_color(), fg=self.get_fg_color())
        theme_button.pack(pady=5)

        # Debug Mode Setting
        debug_label = tk.Label(settings_window, text="Debug Mode:", font=('Arial', 12),
                               bg=self.get_bg_color(), fg=self.get_fg_color())
        debug_label.pack(pady=5)

        debug_button = tk.Button(settings_window, text="Toggle Debug Mode", font=('Arial', 12),
                                 command=self.toggle_debug_mode, bg=self.get_btn_color(), fg=self.get_fg_color())
        debug_button.pack(pady=5)

        # Angle Mode Setting
        angle_mode_label = tk.Label(settings_window, text="Angle Mode:", font=('Arial', 12),
                                    bg=self.get_bg_color(), fg=self.get_fg_color())
        angle_mode_label.pack(pady=5)

        angle_mode_button = tk.Button(settings_window, text=f"Toggle Angle Mode ({self.angle_mode.capitalize()})", font=('Arial', 12),
                                      command=self.toggle_angle_mode, bg=self.get_btn_color(), fg=self.get_fg_color())
        angle_mode_button.pack(pady=5)

        # Scientific Mode Setting
        sci_mode_label = tk.Label(settings_window, text="Scientific Mode:", font=('Arial', 12),
                                  bg=self.get_bg_color(), fg=self.get_fg_color())
        sci_mode_label.pack(pady=5)

        sci_mode_button = tk.Button(settings_window, text=f"Toggle Scientific Mode ({'On' if self.scientific_mode else 'Off'})", font=('Arial', 12),
                                    command=self.toggle_scientific_mode, bg=self.get_btn_color(), fg=self.get_fg_color())
        sci_mode_button.pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    calc = AdvancedCalculator(root)
    root.mainloop()