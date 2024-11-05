import sys

def hamming_distance(hex1, hex2):
    # Convert hex to binary
    bin1 = bin(int(hex1, 16))[2:].zfill(len(hex1) * 4)
    bin2 = bin(int(hex2, 16))[2:].zfill(len(hex2) * 4)
    
    # Calculate the Hamming distance
    distance = sum(b1 != b2 for b1, b2 in zip(bin1, bin2))
    return distance

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 yourname_hamming.py <hex1> <hex2>")
        sys.exit(1)

    hex1 = sys.argv[1]
    hex2 = sys.argv[2]

    distance = hamming_distance(hex1, hex2)
    print(distance)