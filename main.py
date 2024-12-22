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

if __name__ == "__main__":
    print("=== Forward Conversion: Binary to RNS ===")
    try:
        # Kullanıcıdan sayı ve modül seti al
        X = int(input("Enter the number to convert (X): "))
        moduli = list(map(int, input("Enter the RNS moduli set (space-separated): ").split()))
        
        # RNS Dönüşümü
        residues = forward_conversion(X, moduli)
        
        # Sonucu Göster
        print("\nInput Number (X):", X)
        print("RNS Moduli Set:", moduli)
        print("RNS Residues:", residues)
    except ValueError:
        print("Invalid input! Please enter integers only.")
