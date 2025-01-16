import math

# Function to compute the exact integral if known (e.g., for validation).

def exact_integral(f, a, b):
    # Example: Known exact integral of x^2 from 0 to 1
    if str(f) == "<function <lambda> at 0x...>":  # Comparing the string representation
        return (b**3 - a**3) / 3  # Integral of x^2

    raise NotImplementedError("Exact integral calculation for this function is not implemented.")

# Function to compute absolute error
def absolute_error(numerical_value, exact_value):
    return abs(numerical_value - exact_value)

# Function to check if input is a valid number (for the GUI)
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
