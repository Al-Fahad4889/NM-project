def weddle_rule(f, a, b):
    n = 6  # Fixed for Weddle's Rule
    h = (b - a) / n
    coefficients = [1, 5, 1, 6, 1, 5, 1]
    x_values = [a + i * h for i in range(n + 1)]
    result = sum(c * f(x) for c, x in zip(coefficients, x_values))
    return result * (3 * h / 10)
