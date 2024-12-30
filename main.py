import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import random
import time

# Fonksiyonlar
def forward_conversion(X, moduli):
    return [X % m for m in moduli]

def modular_addition(residues_X, residues_Y, moduli):
    return [(residues_X[i] + residues_Y[i]) % moduli[i] for i in range(len(moduli))]

def modular_subtraction(residues_X, residues_Y, moduli):
    return [(residues_X[i] - residues_Y[i]) % moduli[i] for i in range(len(moduli))]

def modular_multiplication(residues_X, residues_Y, moduli):
    return [(residues_X[i] * residues_Y[i]) % moduli[i] for i in range(len(moduli))]

def modular_division(residues_X, residues_Y, moduli):
    result = []
    for i in range(len(moduli)):
        if residues_Y[i] == 0:
            raise ValueError(f"Division by zero in residue index {i}.")
        result.append((residues_X[i] * pow(residues_Y[i], -1, moduli[i])) % moduli[i])
    return result

def introduce_error(residues, error_index):
    erroneous_residues = residues.copy()
    erroneous_residues[error_index] += 1
    return erroneous_residues

def introduce_double_error(residues, error_indices):
    erroneous_residues = residues.copy()
    for idx in error_indices:
        erroneous_residues[idx] += 1
    return erroneous_residues

def detect_error_with_math(original_residues, erroneous_residues, moduli):
    for i in range(len(moduli)):
        if original_residues[i] != erroneous_residues[i]:
            return i
    return -1

def detect_and_correct_double_error(original_residues, erroneous_residues, moduli):
    detected_indices = []
    corrected_residues = erroneous_residues.copy()
    for i in range(len(moduli)):
        if original_residues[i] != erroneous_residues[i]:
            detected_indices.append(i)
            corrected_residues[i] = original_residues[i]
    return detected_indices, corrected_residues

def analyze_performance(repeat_count, moduli, X):
    single_error_times = []
    double_error_times = []
    for _ in range(repeat_count):
        original_residues = forward_conversion(X, moduli)

        # Single Error
        single_error_index = random.randint(0, len(moduli) - 1)
        erroneous_residues = introduce_error(original_residues, single_error_index)
        start_time = time.time()
        detect_error_with_math(original_residues, erroneous_residues, moduli)
        single_error_times.append(time.time() - start_time)

        # Double Error
        double_error_indices = random.sample(range(len(moduli)), 2)
        erroneous_residues = introduce_double_error(original_residues, double_error_indices)
        start_time = time.time()
        detect_and_correct_double_error(original_residues, erroneous_residues, moduli)
        double_error_times.append(time.time() - start_time)

    return single_error_times, double_error_times

def analyze_sticker_model(dna_set, bit_position):
    operations = ["Combine", "Separate", "Set", "Discard"]
    times = []

    for operation in operations:
        start_time = time.time()
        if operation == "Combine":
            combine(dna_set)
        elif operation == "Separate":
            separate(dna_set, bit_position)
        elif operation == "Set":
            set_bit(dna_set, bit_position)
        elif operation == "Discard":
            discard(dna_set)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)

    # Grafik çizimi
    plt.figure(figsize=(10, 6))
    scaled_times = [t * 1000 for t in times]  # Milisaniyeye çevir
    plt.bar(operations, scaled_times, color='skyblue', width=0.5)
    plt.xlabel("Operations", fontsize=12)
    plt.ylabel("Time (milliseconds)", fontsize=12)
    plt.title("Performance Analysis of Sticker Model Operations", fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.tight_layout()
    #plt.show()
    plt.savefig("output.png")  # Grafiği 'output.png' dosyasına kaydet
    return operations, times

# DNA Sticker Model Fonksiyonları
def combine(dna_set):
    time.sleep(0.01)  # Simülasyon için bekleme
    return "".join(dna_set)

def separate(dna_strand, bit_position):
    time.sleep(0.02)  # Simülasyon için bekleme
    on = []
    off = []
    for strand in dna_strand:
        if strand[bit_position] == "1":
            on.append(strand)
        else:
            off.append(strand)
    return on, off

def set_bit(dna_strand, bit_position):
    time.sleep(0.015)  # Simülasyon için bekleme
    modified_strands = []
    for strand in dna_strand:
        strand = strand[:bit_position] + "1" + strand[bit_position + 1:]
        modified_strands.append(strand)
    return modified_strands

def discard(dna_strand):
    time.sleep(0.005)  # Simülasyon için bekleme
    return []

# Performance Analysis Function
def analyze_sticker_performance(dna_set, bit_position):
    operations = ["Combine", "Separate", "Set", "Discard"]
    times = []
    results = []

    for operation in operations:
        start_time = time.time()
        if operation == "Combine":
            result = combine(dna_set)
        elif operation == "Separate":
            result = separate(dna_set, bit_position)
        elif operation == "Set":
            result = set_bit(dna_set, bit_position)
        elif operation == "Discard":
            result = discard(dna_set)
        elapsed_time = time.time() - start_time
        times.append(elapsed_time)
        results.append(result)

    return operations, times, results

# Ana UI
def main_ui():
    root = tk.Tk()
    root.title("RNS Modular Operations and Sticker Model")
    root.geometry("1000x900")

    selection = tk.StringVar(value="Forward Conversion")

    input_frame = tk.Frame(root)
    input_frame.pack(pady=5)
    output_frame = tk.Frame(root)
    output_frame.pack(pady=5)

    def clear_frames():
        for widget in input_frame.winfo_children():
            widget.destroy()
        for widget in output_frame.winfo_children():
            widget.destroy()

    def update_ui():
        clear_frames()
        clear_output_frame()
        selected = selection.get()

        options = [
            "Forward Conversion",
            "Modular Addition",
            "Modular Subtraction",
            "Modular Multiplication",
            "Modular Division",
            "Single Error Detection",
            "Double Error Detection and Correction",
            "Analysis",
            "Sticker Model Analysis",
        ]

        for i, text in enumerate(options):
            tk.Radiobutton(root, text=text, variable=selection, value=text, command=update_ui).place(x=20, y=20 + i * 25)

        if selected == "Forward Conversion":
            tk.Label(input_frame, text="Enter a number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=1, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=1, column=1, padx=10, pady=5)

            def run_conversion():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))
                    residues = forward_conversion(X, moduli)
                    tk.Label(output_frame, text=f"RNS Residues: {residues}").pack(pady=5)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Conversion", command=run_conversion).grid(row=2, column=0, columnspan=2, pady=10)

        elif selected == "Modular Addition":
            tk.Label(input_frame, text="Enter the first number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter the second number (Y):").grid(row=1, column=0, padx=10, pady=5)
            y_entry = tk.Entry(input_frame)
            y_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=2, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=2, column=1, padx=10, pady=5)

            def run_addition():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    Y = int(y_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))

                    residues_X = forward_conversion(X, moduli)
                    residues_Y = forward_conversion(Y, moduli)
                    result = modular_addition(residues_X, residues_Y, moduli)

                    tk.Label(output_frame, text=f"RNS Residues of X: {residues_X}").pack(pady=5)
                    tk.Label(output_frame, text=f"RNS Residues of Y: {residues_Y}").pack(pady=5)
                    tk.Label(output_frame, text=f"Addition Result: {result}").pack(pady=5)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Addition", command=run_addition).grid(row=3, column=0, columnspan=2, pady=10)

        elif selected == "Modular Subtraction":
            tk.Label(input_frame, text="Enter the first number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter the second number (Y):").grid(row=1, column=0, padx=10, pady=5)
            y_entry = tk.Entry(input_frame)
            y_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=2, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=2, column=1, padx=10, pady=5)

            def run_subtraction():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    Y = int(y_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))

                    residues_X = forward_conversion(X, moduli)
                    residues_Y = forward_conversion(Y, moduli)
                    result = modular_subtraction(residues_X, residues_Y, moduli)

                    tk.Label(output_frame, text=f"RNS Residues of X: {residues_X}").pack(pady=5)
                    tk.Label(output_frame, text=f"RNS Residues of Y: {residues_Y}").pack(pady=5)
                    tk.Label(output_frame, text=f"Subtraction Result: {result}").pack(pady=5)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Subtraction", command=run_subtraction).grid(row=3, column=0, columnspan=2, pady=10)
         
        elif selected == "Modular Multiplication":
            tk.Label(input_frame, text="Enter the first number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter the second number (Y):").grid(row=1, column=0, padx=10, pady=5)
            y_entry = tk.Entry(input_frame)
            y_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=2, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=2, column=1, padx=10, pady=5)

            def run_multiplication():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    Y = int(y_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))

                    residues_X = forward_conversion(X, moduli)
                    residues_Y = forward_conversion(Y, moduli)
                    result = modular_multiplication(residues_X, residues_Y, moduli)

                    tk.Label(output_frame, text=f"RNS Residues of X: {residues_X}").pack(pady=5)
                    tk.Label(output_frame, text=f"RNS Residues of Y: {residues_Y}").pack(pady=5)
                    tk.Label(output_frame, text=f"Multiplication Result: {result}").pack(pady=5)
                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Multiplication", command=run_multiplication).grid(row=3, column=0, columnspan=2, pady=10)

        elif selected == "Modular Division":
            tk.Label(input_frame, text="Enter the first number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter the second number (Y):").grid(row=1, column=0, padx=10, pady=5)
            y_entry = tk.Entry(input_frame)
            y_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=2, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=2, column=1, padx=10, pady=5)

            def run_division():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    Y = int(y_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))

                    residues_X = forward_conversion(X, moduli)
                    residues_Y = forward_conversion(Y, moduli)
                    result = modular_division(residues_X, residues_Y, moduli)

                    tk.Label(output_frame, text=f"RNS Residues of X: {residues_X}").pack(pady=5)
                    tk.Label(output_frame, text=f"RNS Residues of Y: {residues_Y}").pack(pady=5)
                    tk.Label(output_frame, text=f"Division Result: {result}").pack(pady=5)
                except ValueError as e:
                    messagebox.showerror("Input Error", str(e))

            tk.Button(input_frame, text="Run Division", command=run_division).grid(row=3, column=0, columnspan=2, pady=10)
        
        elif selected == "Single Error Detection":
            tk.Label(input_frame, text="Enter a number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=1, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=1, column=1, padx=10, pady=5)

            def run_single_error_detection():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))
                    original_residues = forward_conversion(X, moduli)
                    error_index = random.randint(0, len(moduli) - 1)
                    erroneous_residues = introduce_error(original_residues, error_index)

                    detected_error_index = detect_error_with_math(original_residues, erroneous_residues, moduli)

                    tk.Label(output_frame, text=f"Original RNS Residues: {original_residues}").pack(pady=5)
                    tk.Label(output_frame, text=f"Erroneous RNS Residues: {erroneous_residues}").pack(pady=5)
                    if detected_error_index != -1:
                        tk.Label(output_frame, text=f"Error detected at index: {detected_error_index}").pack(pady=5)
                    else:
                        tk.Label(output_frame, text="No error detected!").pack(pady=5)

                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Detection", command=run_single_error_detection).grid(row=2, column=0, columnspan=2, pady=10)

        elif selected == "Double Error Detection and Correction":
            tk.Label(input_frame, text="Enter a number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=1, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=1, column=1, padx=10, pady=5)

            def run_double_error_detection():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))
                    original_residues = forward_conversion(X, moduli)
                    error_indices = random.sample(range(len(moduli)), 2)
                    erroneous_residues = introduce_double_error(original_residues, error_indices)

                    detected_indices, corrected_residues = detect_and_correct_double_error(original_residues, erroneous_residues, moduli)

                    tk.Label(output_frame, text=f"Original RNS Residues: {original_residues}").pack(pady=5)
                    tk.Label(output_frame, text=f"Erroneous RNS Residues: {erroneous_residues}").pack(pady=5)
                    tk.Label(output_frame, text=f"Detected Error Indices: {detected_indices}").pack(pady=5)
                    tk.Label(output_frame, text=f"Corrected RNS Residues: {corrected_residues}").pack(pady=5)

                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Detection", command=run_double_error_detection).grid(row=2, column=0, columnspan=2, pady=10)

        elif selected == "Analysis":
            tk.Label(input_frame, text="Enter a number (X):").grid(row=0, column=0, padx=10, pady=5)
            x_entry = tk.Entry(input_frame)
            x_entry.grid(row=0, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter RNS Moduli Set:").grid(row=1, column=0, padx=10, pady=5)
            moduli_entry = tk.Entry(input_frame)
            moduli_entry.grid(row=1, column=1, padx=10, pady=5)

            tk.Label(input_frame, text="Enter Number of Repeats:").grid(row=2, column=0, padx=10, pady=5)
            repeat_entry = tk.Entry(input_frame)
            repeat_entry.grid(row=2, column=1, padx=10, pady=5)

            def run_analysis():
                clear_output_frame()
                try:
                    X = int(x_entry.get())
                    moduli = list(map(int, moduli_entry.get().split()))
                    repeat_count = int(repeat_entry.get())

                    single_error_times, double_error_times = analyze_performance(repeat_count, moduli, X)

                    plt.figure(figsize=(10, 6))
                    plt.plot(range(repeat_count), single_error_times, label="Single Error Detection Time")
                    plt.plot(range(repeat_count), double_error_times, label="Double Error Detection Time")
                    plt.xlabel("Iteration")
                    plt.ylabel("Time (s)")
                    plt.title("Performance Analysis of Error Detection")
                    plt.legend()
                    #plt.show()
                    plt.savefig("output.png")  # Grafiği 'output.png' adıyla kaydeder

                except ValueError:
                    messagebox.showerror("Input Error", "Please enter valid inputs!")

            tk.Button(input_frame, text="Run Analysis", command=run_analysis).grid(row=3, column=0, columnspan=2, pady=10)
            
        elif selected == "Sticker Model Analysis":
            tk.Label(input_frame, text="Enter DNA Strands (comma-separated):").grid(row=0, column=0, padx=10, pady=10)
            dna_entry = tk.Entry(input_frame, width=50)
            dna_entry.grid(row=0, column=1, padx=10, pady=10)

            tk.Label(input_frame, text="Enter Bit Position (integer):").grid(row=1, column=0, padx=10, pady=10)
            bit_entry = tk.Entry(input_frame, width=10)
            bit_entry.grid(row=1, column=1, padx=10, pady=10)

            def run_sticker_analysis():
                clear_output_frame()
                try:
                    dna_set = dna_entry.get().split(",")
                    bit_position = int(bit_entry.get())

                    # Input validation
                    if not dna_set:
                        raise ValueError("DNA strands cannot be empty.")
                    if any(len(strand) <= bit_position for strand in dna_set):
                        raise ValueError("Bit position is out of range for the given DNA strands.")

                    operations, times, results = analyze_sticker_performance(dna_set, bit_position)

                    tk.Label(output_frame, text=f"Input DNA Strands: {dna_set}").pack(pady=5)
                    tk.Label(output_frame, text=f"Bit Position: {bit_position}").pack(pady=5)

                    for i, operation in enumerate(operations):
                        tk.Label(output_frame, text=f"{operation} Result: {results[i]}").pack(pady=5)
                        tk.Label(output_frame, text=f"{operation} Time: {times[i] * 1000:.2f} ms").pack(pady=5)

                    # Grafik çizimi
                    plt.figure(figsize=(10, 6))
                    scaled_times = [t * 1000 for t in times]  # Milisaniyeye çevir
                    plt.bar(operations, scaled_times, color='skyblue', width=0.5)
                    plt.xlabel("Operations", fontsize=12)
                    plt.ylabel("Time (milliseconds)", fontsize=12)
                    plt.title("Performance Analysis of Sticker Model Operations", fontsize=14)
                    plt.xticks(fontsize=10)
                    plt.yticks(fontsize=10)
                    plt.tight_layout()
                    #plt.show()
                    plt.savefig("output.png")  # Grafiği 'output.png' adıyla kaydeder

                except ValueError as e:
                    messagebox.showerror("Input Error", str(e))

            tk.Button(input_frame, text="Run Analysis", command=run_sticker_analysis).grid(row=2, column=0, columnspan=2, pady=20)

    def clear_output_frame():
        for widget in output_frame.winfo_children():
            widget.destroy()

    update_ui()
    root.mainloop()

if __name__ == "__main__":
    main_ui()

