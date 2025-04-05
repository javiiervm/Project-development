import tkinter as tk  # Importing the tkinter module for GUI development

# Function to handle button clicks for numbers and operators
def click(number):
    """
    Appends the clicked button's value (number/operator) to the entry field.
    """
    current = entry.get()  # Get the current text in the entry field
    entry.delete(0, tk.END)  # Clear the entry field
    entry.insert(0, current + str(number))  # Insert the new text

# Function to clear the entry field
def clear():
    """
    Clears the entry field, resetting it to an empty state.
    """
    entry.delete(0, tk.END)  # Delete all content in the entry field

# Function to evaluate the expression in the entry field
def calculate():
    """
    Evaluates the mathematical expression entered in the entry field.
    If the expression is invalid, displays an error message.
    """
    try:
        result = eval(entry.get())  # Evaluate the mathematical expression
        entry.delete(0, tk.END)  # Clear the entry field
        entry.insert(0, str(result))  # Display the result in the entry field
    except:
        entry.delete(0, tk.END)  # Clear the entry field if an error occurs
        entry.insert(0, "Error")  # Display an error message

# Create the main application window
root = tk.Tk()  # Initialize the main tkinter window
root.title("Calculator")  # Set the title of the window

# Create an entry widget for displaying the input and output
entry = tk.Entry(root, width=20, font=('Arial', 18), justify='right')
entry.grid(row=0, column=0, columnspan=4)  # Place the entry widget in the grid

# Define the button layout
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),  # First row
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),  # Second row
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),  # Third row
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3),  # Fourth row
]

# Create and place the buttons
for (text, row, col) in buttons:
    if text == 'C':  # If the button is 'C', attach the clear function
        tk.Button(root, text=text, width=5, height=2, command=clear).grid(row=row, column=col)
    elif text == '=':  # If the button is '=', attach the calculate function
        tk.Button(root, text=text, width=5, height=2, command=calculate).grid(row=row, column=col)
    else:  # For other buttons, attach the click function with the button's text as an argument
        tk.Button(root, text=text, width=5, height=2,
                  command=lambda t=text: click(t)).grid(row=row, column=col)

# Run the application's event loop
root.mainloop()  # Keeps the application running and responsive
