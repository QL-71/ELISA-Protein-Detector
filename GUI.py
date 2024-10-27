import os
import re
import subprocess
import warnings

from PIL import Image, ImageTk

import Model_function

warnings.filterwarnings('ignore')
import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import Fit_Module
import Back_calculation
import inspect
import datetime


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.long = 700
        self.width = 1000
        self.geometry(str(self.long) + 'x' + str(self.width))
        # self.title("Basal Insulin Elisa")
        self.title("EPD")
        # self.iconbitmap('rock.ico')
        # Model formulas
        self.formulas = [
            "(a0 - a3) / (1 + (x / a2) ** a1) ** a4 + a3",
            # "(a0 - a3) / (1 + (x / a2) ** a1) + a3",
            # "a0 * sin(x - pi) + a1 * ((x - 10) ** 2) + a2",
            # "a0 * exp(-a1 * x)",
            # "a0 * x"
        ]
        self.variable_names = "x a0 a1 a2 a3 a4"

        # Initialize the model function with a default formula
        self.f = Model_function.create_custom_function(self.formulas[0], self.variable_names)

        # model prediction
        self.model_prediction = []
        self.parameter = []
        self.residuals = []
        self.r_square = 0

        # Current formula being edited
        self.current_formula = self.formulas[0]

        # Input area
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(side=ctk.TOP, padx=10, pady=10, fill=ctk.X)

        # con_x
        self.con_x_label = ctk.CTkLabel(input_frame, text="Concentration (con_x):", font=("Arial", 12))
        self.con_x_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.con_x_entry = ctk.CTkEntry(input_frame, width=self.long - 200)
        self.con_x_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        # self.con_x_entry.insert(tk.END, "0, 0.02, 0.08, 0.15, 0.4, 1")
        # self.con_x_entry.insert(tk.END, "0.0, 0.0, 0.08, 0.15, 0.4, 1.0")
        self.con_x_entry.insert(tk.END, "0,0.02,0.08,0.15,0.4,1")

        # od_y
        self.od_y_label = ctk.CTkLabel(input_frame, text="OD Readings (od_y):", font=("Arial", 12))
        self.od_y_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.od_y_entry = ctk.CTkEntry(input_frame, width=self.long - 200)
        self.od_y_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.od_y_entry.insert(tk.END, "0.048, 0.056, 0.063, 0.099, 0.364, 1.568")
        # self.od_y_entry.insert(tk.END, "0.044, 0.044, 0.047, 0.049, 0.059, 0.103")
        # self.od_y_entry.insert(tk.END, " 0.057, 0.06, 0.07, 0.098, 0.311, 1.298")

        # Initial Parameter Guess
        self.ini_guess_label = ctk.CTkLabel(input_frame, text="Initial Function Parameter:", font=("Arial", 12))
        self.ini_guess_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.ini_guess_entry = ctk.CTkEntry(input_frame, width=self.long - 200)
        self.ini_guess_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.ini_guess_entry.insert(tk.END, "0.22, 0.75, 0.25, 0.50, 0.69")
        # self.ini_guess_entry.insert(tk.END, "0.22, 0.75, 0.25, 0.50")

        # Method options
        self.method_label = ctk.CTkLabel(input_frame, text="Method:", font=("Arial", 12))
        self.method_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        # methods = ['Nelder-Mead', 'Levenberg-Marquardt', 'SLSQP', 'COBYLA', 'TNC', 'L-BFGS-B', 'BFGS', 'CG','Nonlinear-Least-Square','ALL']
        methods = ['Nelder-Mead', 'Levenberg-Marquardt', 'SLSQP', 'COBYLA', 'L-BFGS-B', 'BFGS', 'CG',
                   'Nonlinear-Least-Square', 'ALL']
        self.method_var = tk.StringVar(self, value=methods[0])
        self.method_option = ctk.CTkOptionMenu(input_frame, values=methods, fg_color='teal', button_color='teal',
                                               variable=self.method_var, width=self.long - 200)
        self.method_option.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Function options
        self.function_label = ctk.CTkLabel(input_frame, text="Function:", font=("Arial", 12))
        self.function_label.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        self.function_var = tk.StringVar(self, value=self.formulas[0])
        self.function_option = ctk.CTkOptionMenu(input_frame, values=self.formulas, fg_color='teal',
                                                 button_color='teal', variable=self.function_var, width=self.long - 200,
                                                 command=self.update_formula)
        self.function_option.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Formula display area
        self.formula_display = ctk.CTkTextbox(input_frame, height=50, font=("Arial", 12), wrap="word", state="disabled")
        self.formula_display.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky="ew")
        self.update_formula_display(self.formulas[0])

        # Add edit, cancel, and confirm buttons for formula
        self.edit_button = ctk.CTkButton(input_frame, text="Edit", command=self.edit_formula, fg_color='teal')
        self.edit_button.grid(row=7, column=0, padx=5, pady=5, sticky="e")

        button_container = ctk.CTkFrame(input_frame)
        button_container.grid(row=7, column=1, padx=5, pady=5, sticky="e")

        self.confirm_button = ctk.CTkButton(button_container, text="Confirm", command=self.confirm_formula,
                                            state="disabled", fg_color='teal')
        self.confirm_button.pack(side=ctk.RIGHT, padx=5)

        self.cancel_button = ctk.CTkButton(button_container, text="Cancel", command=self.cancel_edit, state="disabled",
                                           fg_color='teal')
        self.cancel_button.pack(side=ctk.RIGHT, padx=5)

        # Create button container 1
        button_container = ctk.CTkFrame(input_frame)
        button_container.grid(row=8, column=1, columnspan=2)

        self.button1 = ctk.CTkButton(button_container, text="Fit Curve", command=self.button1_callback,
                                     font=("Arial", 12), fg_color='teal')
        self.button1.pack(side=ctk.LEFT, padx=5, pady=5)

        self.button3 = ctk.CTkButton(button_container, text="Clear Message", command=self.Clear_Message,
                                     font=("Arial", 12), fg_color='teal')
        self.button3.pack(side=ctk.LEFT, padx=5, pady=5)

        # Input area 2
        input_frame2 = ctk.CTkFrame(self)
        input_frame2.pack(side=ctk.TOP, padx=10, pady=10, fill=ctk.X)

        # Initial Guess
        self.initial_guess_label = ctk.CTkLabel(input_frame2, text="Initial Guess OD (Iteration):", font=("Arial", 12))
        self.initial_guess_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.initial_guess_entry = ctk.CTkEntry(input_frame2, width=self.long - 200)
        self.initial_guess_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        # self.initial_guess_entry.insert(tk.END, "0.328")

        # Given OD Readings
        self.given_od_label = ctk.CTkLabel(input_frame2, text="Given OD Readings:", font=("Arial", 12))
        self.given_od_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.given_od_entry = ctk.CTkEntry(input_frame2, width=self.long - 200)
        self.given_od_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        # self.given_od_entry.insert(tk.END, "0.044,0.048,0.050,0.054,0.059,0.065")

        # Create button container 2
        button_container2 = ctk.CTkFrame(input_frame2)
        button_container2.grid(row=3, column=1, columnspan=2)

        self.button2 = ctk.CTkButton(button_container2, text="Back Calculation", command=self.button2_callback,
                                     font=("Arial", 12), fg_color='teal')
        self.button2.pack(side=ctk.LEFT, padx=5, pady=5)

        # Create result text box
        self.result_text = ctk.CTkTextbox(self, width=80, height=100)
        self.result_text.pack(side=ctk.TOP, padx=10, pady=10, fill=ctk.BOTH, expand=True)

        # Image display area
        self.image_canvas = ctk.CTkCanvas(self, width=300, height=200, bg="white")
        self.image_canvas.pack(side=ctk.TOP, padx=10, pady=10, fill=ctk.X)
        self.display_graph(self.con_x_entry, self.od_y_entry, self.model_prediction)

        self.Clear_Message()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.destroy()
        os._exit(0)

    def Clear_Message(self):
        self.result_text.delete('1.0', tk.END)
        self.text_print(
            "🤗 Welcome🤗 \n 👣 Step 1: Remember To Fill In The Function f1 In Model_function.py File.\n 👣 Step 2: Fill in All Blanks Without Missing.",
            False)

    def update_formula(self, selected_formula):
        #Retrieve the selected formula string
        formula_str = selected_formula
        self.update_formula_display(formula_str)

        #Match parameter names using regular expressions
        param_pattern = re.compile(r'\ba\d+\b')
        params = sorted(set(param_pattern.findall(formula_str)), key=lambda x: int(x[1:]))

        #Dynamically generate variable_name
        self.variable_names = "x " + " ".join(params)

        #Create an executable custom function using Model_functional.creat_custom_function
        self.f = Model_function.create_custom_function(formula_str, self.variable_names)

        if self.f == None:
            return 0
        else:
            self.current_formula = formula_str
            return 1

    def update_formula_display(self, formula):
        self.formula_display.configure(state="normal")
        self.formula_display.delete("1.0", tk.END)
        self.formula_display.insert("1.0", formula)
        self.formula_display.configure(state="disabled")

    def edit_formula(self):
        self.formula_display.configure(state="normal")
        self.confirm_button.configure(state="normal")
        self.cancel_button.configure(state="normal")
        self.edit_button.configure(state="disabled")
        self.button1.configure(state="disabled")

    def confirm_formula(self):
        formula_str = self.formula_display.get("1.0", tk.END).strip()
        try:

            jud = self.update_formula(formula_str)
            if jud == 1:
                #Disable editing
                self.formula_display.configure(state="disabled")
                self.confirm_button.configure(state="disabled")
                self.cancel_button.configure(state="disabled")
                self.edit_button.configure(state="normal")
                self.button1.configure(state="normal")

        except Exception as e:
            self.text_print(f"Error: {str(e)}", True)

    def cancel_edit(self):
        self.update_formula_display(self.current_formula)
        self.formula_display.configure(state="disabled")
        self.confirm_button.configure(state="disabled")
        self.cancel_button.configure(state="disabled")
        self.edit_button.configure(state="normal")
        self.button1.configure(state="normal")
        self.update_formula(self.current_formula)

    import os
    import subprocess

    def show_saved_image(self, image_path):
        if os.path.exists(image_path):
            #Open an image in the Windows operating system
            if os.name == 'nt':
                os.startfile(image_path)
            #Open images in Mac OS
            elif os.name == 'posix':
                subprocess.run(['open', image_path])
            #Open an image in Linux
            else:
                subprocess.run(['xdg-open', image_path])
        else:
            self.text_print("Error: Image file does not exist.", True)

    def display_all_results(self, con_x, od_y, ini_guess1):
        methods = ['Nelder-Mead', 'Levenberg-Marquardt', 'SLSQP', 'COBYLA', 'L-BFGS-B', 'BFGS', 'CG',
                   'Nonlinear-Least-Square']
        num_methods = len(methods)

        #Set to display two charts per row
        cols = 2
        rows = (num_methods + cols - 1) // cols

        fig, axes = plt.subplots(nrows=rows, ncols=cols, figsize=(16, 6 * rows))
        axes = axes.flatten()

        for i, method in enumerate(methods):
            ax = axes[i]
            try:
                fit_params = Fit_Module.insulin_curve_fit3(con_x, od_y, self.f, method, ini_guess1)
                model_prediction = fit_params['Prediction']
                parameters = fit_params['params']
                residuals = fit_params['residuals']
                r_squared = fit_params['r_squared']

                # Plot the data
                ax.scatter(con_x, od_y, label='Data', marker='.')

                # Plot the model prediction
                if len(model_prediction) != 0:
                    ax.plot(con_x, model_prediction, 'r-', label=f'{method} Fit')

                ax.set_xlabel('Concentration (ng/mL)', fontsize=18)
                ax.set_ylabel('OD', fontsize=18)
                ax.set_title(f'Fit using {method}')
                ax.legend()
                ax.grid(True)
                ax.tick_params(axis='both', which='major', labelsize=18)

            except Exception as e:
                self.text_print(f"Error with {method}: {str(e)}", True)
                ax.set_title(f'Error with {method}')

        #Add fitting result text box
        for i, method in enumerate(methods):
            ax = axes[i]
            try:
                fit_params = Fit_Module.insulin_curve_fit3(con_x, od_y, self.f, method, ini_guess1)
                parameters = fit_params['params']
                residuals = fit_params['residuals']
                r_squared = fit_params['r_squared']

                # Display fitting results
                fit_results = f'Params: {parameters}\nResiduals: {residuals}\nR^2: {r_squared:.4f}'
                ax.text(0, -0.3, fit_results, transform=ax.transAxes, fontsize=10, ha='left', va='top', wrap=True,
                        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

            except Exception as e:
                self.text_print(f"Error with {method}: {str(e)}", True)

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        # Save and display the figure
        fig.tight_layout()
        fig.savefig("all_methods_graph.png", dpi=300, bbox_inches='tight')

        # Display on Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=self.image_canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        if hasattr(self, "canvas_widget"):
            self.canvas_widget.destroy()
        self.canvas_widget = canvas_widget
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

        #Display saved images
        self.show_saved_image("all_methods_graph.png")

    # Fit Curve
    def button1_callback(self):

        ## Check and Error Handle.
        # self.ini_guess = [0.00374, 0.965, 60.1 , 65700 , 0.0001 ]
        # self.ini_guess = [0.22, 0.75, 0.25, 0.50, 0.69]
        self.ini_guess = [0.0511, 1.99, 1.13, 3560, 0.00074]
        con_x = np.array([float(x) for x in self.con_x_entry.get().split(",")])
        od_y = np.array([float(y) for y in self.od_y_entry.get().split(",")])

        parameter_count = len(inspect.signature(self.f).parameters) - 1  # Exclude 'x'

        ini_guess1 = self.ini_guess[:parameter_count]

        if parameter_count == len(ini_guess1):

            if len(con_x) == len(od_y):
                # Get the user input for initial guess
                methods = self.method_var.get()

                if methods == 'ALL':
                    self.result_text.delete('1.0', tk.END)
                    self.display_all_results(con_x, od_y, ini_guess1)
                else:
                    fit_params = Fit_Module.insulin_curve_fit3(con_x, od_y, self.f, methods, ini_guess1)
                    self.model_prediction = fit_params['Prediction']
                    self.parameter = fit_params['params']
                    self.residuals = fit_params['residuals']
                    self.r_square = fit_params['r_squared']

                    self.result_text.delete('1.0', tk.END)
                    self.text_print(
                        "OD Predict: {}".format(self.model_prediction) + "\n" + "Parameter: {}".format(self.parameter),
                        False)
                    self.display_graph(self.con_x_entry, self.od_y_entry, self.model_prediction)
            else:
                self.text_print("Error Message: Con_x and od_y Should Have Same Length.", True)
        else:
            self.text_print("Error Message: Parameter Initial Guess Number Should Be " + str(parameter_count) + ".",
                            True)

    def text_print(self, s, is_error):

        if is_error:
            self.result_text.delete('1.0', tk.END)
        #Add current time
        self.result_text.insert(tk.END, "================================================================\n")
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.result_text.insert(tk.END, f"{current_time}\n{s}\n")
        self.result_text.insert(tk.END, "================================================================\n")

    # Back Calculation
    def button2_callback(self):

        ## Check and Error Handle.
        if len(self.model_prediction) != 0:
            params = {}
            for each in range(len(self.parameter)):
                params.update({'a' + str(each): self.parameter[each]})

            # Given OD readings
            ys = np.array([float(y) for y in self.given_od_entry.get().split(",")])

            # Initial guess for the root finding algorithm
            y0 = float(self.initial_guess_entry.get())

            conc = Back_calculation.back_calculation(ys, self.f, y0, params)
            self.text_print("Concentration: {}".format(conc), False)
        else:
            self.text_print("Error Message: Please Fit Curve First To Get The Function Parameters.", True)

    def display_graph(self, con_x_entry, od_y_entry, model_prediction):
        con_x_values = [float(x) for x in con_x_entry.get().split(",")]
        od_y_values = [float(y) for y in od_y_entry.get().split(",")]

        # Create figure and axes for plotting
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111)

        # Plot the data using the provided data
        ax.scatter(con_x_values, od_y_values, label='Data', marker='.')

        if len(model_prediction) != 0:
            ax.plot(con_x_values, model_prediction, 'r-', label='Curve Fit')

        ax.set_xlabel('Concentration (ng/mL)', fontsize=18)
        ax.set_ylabel('OD', fontsize=18)
        # ax.set_title('Insulin Concentration Curve Fit ' + str(self.method_var.get()))
        ax.legend()
        ax.grid(True)

        # Increase the font size of the ticks
        ax.tick_params(axis='both', which='major', labelsize=18)

        # Convert the Matplotlib figure into a Tkinter PhotoImage
        canvas = FigureCanvasTkAgg(fig, master=self.image_canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()

        # Check if a canvas widget already exists
        if hasattr(self, "canvas_widget"):
            # Destroy the previous canvas widget
            self.canvas_widget.destroy()

        # Save a reference to the new canvas widget
        self.canvas_widget = canvas_widget

        # Display the plotted graph on the canvas
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()

