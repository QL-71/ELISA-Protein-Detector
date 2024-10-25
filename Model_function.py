# 学   校： 云南大学
# 学   院： 软件学院
# 谁头发少： 齐立
# 开发时间： 2024/6/18 13:53
# @File : Model_function.py
from tkinter import messagebox
from sympy import symbols, sympify, lambdify
def create_custom_function(formula_str, variable_names):
    try:
        # 使用sympy解析公式
        variables = symbols(variable_names)
        formula = sympify(formula_str)

        # 使用lambdify创建一个可执行的函数
        func = lambdify(variables, formula, 'numpy')

        return func
    except Exception as e:
        messagebox.showerror("Error", "无法解析公式: " + str(e))
        return None
