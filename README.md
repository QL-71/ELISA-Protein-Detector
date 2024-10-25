### Basal Insulin Elisa Curve Fitting Program 📈🔬

This program 🖥️ is designed for conducting curve fitting in Basal Insulin Enzyme-Linked Immunosorbent Assay (Basal Insulin Elisa) 🧪.

- **GUI.py**: Contains the design of the graphical user interface. This serves as the primary interface for user interaction with the program. 💻

- **Fit_Module.py**: Includes the implementation functions for curve fitting and plotting. 📊🖌️

- **Model_function.txt**: This file specifies the form of the function for curve fitting, inputted in Python code format. `f1` represents the function name, which cannot be altered. `a0-a4` denote the parameters of the function, inputted based on the number of parameters in the function. For instance, if there are 5 parameters, it will be `a0-a4`; if there are 10 parameters, it will be `a0-a9`. 📝

- **Basal.exe**: This is the executable file successfully packaged using PyInstaller. Users can directly run it, but ensure it is in the same folder as `Model_function.txt`. It can be packaged using the following command:

  ```
  pyinstaller --onefile --collect-data frozendict --icon=rock.ico GUI.py
  ```

  Users can utilize the program by running `Basal.exe`, inputting data via the graphical interface, and conducting Basal Insulin Elisa curve fitting. 🚀