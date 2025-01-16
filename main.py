import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from methods.simpsons import simpsons_one_third, simpsons_three_eighth
from methods.trapezoidal import trapezoidal_rule
from methods.weddle import weddle_rule
from utils.plot_utils import plot_function
from utils.math_utils import exact_integral, absolute_error, is_number


class NumericalIntegrationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Numerical Integration Tool")
        self.root.geometry("400x700")  # Adjust window size

        # Input fields
        self.function_label = tk.Label(root, text="Function (e.g., x**2 + 3):")
        self.function_label.pack()
        self.function_entry = tk.Entry(root, width=40)
        self.function_entry.pack()

        self.lower_limit_label = tk.Label(root, text="Lower Limit:")
        self.lower_limit_label.pack()
        self.lower_limit_entry = tk.Entry(root, width=20)
        self.lower_limit_entry.pack()

        self.upper_limit_label = tk.Label(root, text="Upper Limit:")
        self.upper_limit_label.pack()
        self.upper_limit_entry = tk.Entry(root, width=20)
        self.upper_limit_entry.pack()

        self.subintervals_label = tk.Label(root, text="Number of Subintervals:")
        self.subintervals_label.pack()
        self.subintervals_entry = tk.Entry(root, width=20)
        self.subintervals_entry.pack()

        # Significant digits input
        self.sig_digits_label = tk.Label(root, text="Significant Digits:")
        self.sig_digits_label.pack()
        self.sig_digits_entry = tk.Entry(root, width=20)
        self.sig_digits_entry.pack()
        self.sig_digits_entry.insert(0, "6")  # Default value

        # Method selection
        self.method_label = tk.Label(root, text="Select Method:")
        self.method_label.pack()
        self.method_combobox = ttk.Combobox(root, values=["Simpson's 1/3", "Simpson's 3/8", "Trapezoidal", "Weddle's"])
        self.method_combobox.pack()

        # Buttons
        self.calculate_button = tk.Button(root, text="Calculate", command=self.calculate_integral)
        self.calculate_button.pack()

        self.plot_button = tk.Button(root, text="Plot Function", command=self.plot_function)
        self.plot_button.pack()

        self.compare_button = tk.Button(root, text="Compare Methods", command=self.compare_methods)
        self.compare_button.pack()

        # Output
        self.result_label = tk.Label(root, text="Result:")
        self.result_label.pack()
        self.result_output = tk.Label(root, text="", fg="blue")
        self.result_output.pack()

    def calculate_integral(self):
        try:
            # Parse inputs
            func = self.function_entry.get()
            lower_limit = self.lower_limit_entry.get()
            upper_limit = self.upper_limit_entry.get()
            subintervals = self.subintervals_entry.get()
            sig_digits = self.sig_digits_entry.get()

            # Validate input fields
            if not func or not lower_limit or not upper_limit or not subintervals or not sig_digits:
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return

            if not is_number(lower_limit) or not is_number(upper_limit) or not is_number(subintervals) or not sig_digits.isdigit():
                messagebox.showerror("Input Error", "Please enter valid numbers for all fields.")
                return

            lower_limit = float(lower_limit)
            upper_limit = float(upper_limit)
            subintervals = int(subintervals)
            sig_digits = int(sig_digits)

            method = self.method_combobox.get()

            # Convert function to callable
            f = lambda x: eval(func)

            # Perform selected method
            if method == "Simpson's 1/3":
                result = simpsons_one_third(f, lower_limit, upper_limit, subintervals)
            elif method == "Simpson's 3/8":
                result = simpsons_three_eighth(f, lower_limit, upper_limit, subintervals)
            elif method == "Trapezoidal":
                result = trapezoidal_rule(f, lower_limit, upper_limit, subintervals)
            elif method == "Weddle's":
                result = weddle_rule(f, lower_limit, upper_limit)
            else:
                messagebox.showerror("Error", "Select a valid method.")
                return

            # If exact integral is known, calculate the absolute error
            try:
                exact_value = exact_integral(f, lower_limit, upper_limit)
                error = absolute_error(result, exact_value)
                self.result_output.config(
                    text=f"Result: {round(result, sig_digits)}\n"
                         f"Error: {round(error, sig_digits)}"
                )
            except NotImplementedError:
                self.result_output.config(
                    text=f"Result: {round(result, sig_digits)}\nExact integral not available."
                )

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def plot_function(self):
        try:
            func = self.function_entry.get()
            lower_limit = float(self.lower_limit_entry.get())
            upper_limit = float(self.upper_limit_entry.get())
            f = lambda x: eval(func)
            plot_function(f, lower_limit, upper_limit)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def compare_methods(self):
        try:
            # Parse inputs
            func = self.function_entry.get()
            lower_limit = float(self.lower_limit_entry.get())
            upper_limit = float(self.upper_limit_entry.get())
            subintervals = int(self.subintervals_entry.get())

            if not func:
                messagebox.showerror("Input Error", "Function cannot be empty.")
                return

            # Convert function to callable
            f = lambda x: eval(func)

            # Generate x values
            x = np.linspace(lower_limit, upper_limit, 1000)
            y = [f(val) for val in x]

            # Plot original function
            plt.figure(figsize=(10, 6))
            plt.plot(x, y, label="Original Function", color="black", linewidth=2)

            # Simpson's 1/3 rule
            result_13 = simpsons_one_third(f, lower_limit, upper_limit, subintervals)
            plt.fill_between(x, y, where=((x >= lower_limit) & (x <= upper_limit)), color='blue', alpha=0.2, label="Simpson's 1/3")

            # Simpson's 3/8 rule
            result_38 = simpsons_three_eighth(f, lower_limit, upper_limit, subintervals)
            plt.fill_between(x, y, where=((x >= lower_limit) & (x <= upper_limit)), color='green', alpha=0.2, label="Simpson's 3/8")

            # Trapezoidal rule
            result_trap = trapezoidal_rule(f, lower_limit, upper_limit, subintervals)
            plt.fill_between(x, y, where=((x >= lower_limit) & (x <= upper_limit)), color='red', alpha=0.2, label="Trapezoidal")

            # Weddle's rule
            result_weddle = weddle_rule(f, lower_limit, upper_limit)
            plt.fill_between(x, y, where=((x >= lower_limit) & (x <= upper_limit)), color='purple', alpha=0.2, label="Weddle's")

            # Labels and legend
            plt.title("Comparison of Numerical Integration Methods")
            plt.xlabel("x")
            plt.ylabel("f(x)")
            plt.legend()
            plt.grid()

            # Show the plot
            plt.show()

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = NumericalIntegrationApp(root)
    root.mainloop()
