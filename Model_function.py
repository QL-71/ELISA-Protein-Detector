from tkinter import messagebox
from sympy import symbols, sympify, lambdify
def create_custom_function(formula_str, variable_names):
    try:
        #Using Sympy to parse formulas
        variables = symbols(variable_names)
        formula = sympify(formula_str)

        #Create an executable function using lambda
        func = lambdify(variables, formula, 'numpy')

        return func
    except Exception as e:
        messagebox.showerror("Error", "Unable to parse formula: " + str(e))
        return None
