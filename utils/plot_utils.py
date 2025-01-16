import matplotlib.pyplot as plt
import numpy as np

def plot_function(f, a, b):
    x = np.linspace(a, b, 1000)
    y = f(x)
    plt.plot(x, y, label="f(x)")
    plt.fill_between(x, y, alpha=0.2, color="orange", label="Integration Area")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title("Function and Integration Area")
    plt.legend()
    plt.grid()
    plt.show()
