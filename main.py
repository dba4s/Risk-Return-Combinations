import tkinter as tk
from tkinter import ttk
import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import FuncFormatter
import mplcursors

# Function to calculate annualized return
def annualized_return(prices):
    returns = np.log(prices[-1] / prices[0])  # Calculate the logarithmic return
    num_years = len(prices) / 252  # Assuming 252 trading days in a year
    annualized_returns = np.exp(returns / num_years) - 1  # Calculate the annualized return geometrically
    return annualized_returns

# Function to calculate standard deviation
def calc_std_dev(prices):
    returns = np.diff(prices) / prices[:-1]
    std_dev = np.std(returns) * np.sqrt(252)  # Assuming 252 trading days in a year
    return std_dev

# Function to format y-axis tick labels as percentages
def percentage_formatter(x, pos):
    return '{:.2%}'.format(x)

# Function to handle button click event
def calculate():
    global canvas

    if canvas:
        canvas.get_tk_widget().destroy()

    # Retrieve ticker symbols from entry fields
    tickers = [entry.get() for entry in entry_fields]

    # Collect historical data for each stock
    stocks = []
    for ticker in tickers:
        data = yf.download(ticker, start='2022-01-01', end='2022-12-31', progress=False)
        stock_prices = data['Close'].values
        stocks.append(stock_prices)

    # Calculate annualized return and standard deviation for each stock
    returns = []
    std_devs = []
    for stock in stocks:
        returns.append(annualized_return(stock))
        std_devs.append(calc_std_dev(stock))

    # Plotting scatter plot with labels
    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(std_devs, returns, color='cyan', edgecolors='purple', alpha=0.8)
    ax.set_xlabel('Standard Deviation', fontsize=12)
    ax.set_ylabel('Annualized Return', fontsize=12)
    ax.set_title('Risk/Return Analysis', fontsize=14)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.set_xticks(np.arange(0, max(std_devs)+0.1, 0.1))
    ax.set_yticks(np.arange(min(returns), max(returns), 0.05))

    # Add labels to the data points
    for i, ticker in enumerate(tickers):
        ax.annotate(ticker, (std_devs[i], returns[i]), xytext=(10, -10), textcoords='offset points', color='black')

    # Format y-axis tick labels as percentages
    ax.yaxis.set_major_formatter(FuncFormatter(percentage_formatter))
    ax.spines['bottom'].set_color('black')
    ax.spines['left'].set_color('black')

    # Add tooltips to data points
    tooltips = mplcursors.cursor(sc).connect("add", lambda sel: sel.annotation.set_text(
        f"Mean: {returns[sel.index]:.2%}\nStd Dev: {std_devs[sel.index]:.4f}"))

    # Create Tkinter canvas and display the plot

    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    fig.tight_layout()
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Create the main Tkinter window
root = tk.Tk()
root.title('Stock Analysis')
root.geometry("800x600")

# Create frame for input fields
frame_inputs = ttk.Frame(root, padding=20)
frame_inputs.pack(side=tk.TOP)
frame_plot = ttk.Frame(root)
frame_plot.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)


# Create entry fields for ticker input
entry_fields = []
for i in range(3):
    label = ttk.Label(frame_inputs, text=f"Stock {i+1}:", font=('Helvetica', 10, 'bold'))
    label.grid(row=i, column=0, sticky='e', pady=5)
    entry = ttk.Entry(frame_inputs, font=('Helvetica', 10))
    entry.grid(row=i, column=1, padx=10, pady=5)
    entry_fields.append(entry)

# Create Calculate button
button_calculate = ttk.Button(frame_inputs, text="Calculate", command=calculate)
button_calculate.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Create frame for plot
frame_plot = ttk.Frame(root)
frame_plot.pack(fill=tk.BOTH, expand=True)

canvas = None

# Run the Tkinter event loop
root.mainloop()
