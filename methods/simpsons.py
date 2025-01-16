def simpsons_one_third(f, a, b, n):
    if n % 2 != 0:
        raise ValueError("Number of subintervals must be even for Simpson's 1/3 Rule.")
    h = (b - a) / n
    result = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        result += 4 * f(x) if i % 2 != 0 else 2 * f(x)
    return result * h / 3

def simpsons_three_eighth(f, a, b, n):
    if n % 3 != 0:
        raise ValueError("Number of subintervals must be a multiple of 3 for Simpson's 3/8 Rule.")
    h = (b - a) / n
    result = f(a) + f(b)
    for i in range(1, n):
        x = a + i * h
        result += 3 * f(x) if i % 3 != 0 else 2 * f(x)
    return result * 3 * h / 8
