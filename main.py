import numpy as np

def forward_conversion(X, moduli):
    """
    Forward Conversion: Converts a binary number X into its RNS residues.

    Parameters:
        X (int): Input binary number.
        moduli (list): List of RNS moduli.

    Returns:
        list: List of residues after conversion.
    """
    residues = [X % m for m in moduli]  # Calculate residues for each modulus
    return residues

# Test Example
if __name__ == "__main__":
    # Define the RNS moduli set
    moduli = [5, 3, 16, 17]  # Example moduli set: {2^n + 1, 2^n - 1, 2^(2n) + 1, 2^(2n)}

    # Input binary number
    X = 10

    # Forward Conversion
    residues = forward_conversion(X, moduli)
    print("Input Number (X):", X)
    print("RNS Residues:", residues)
