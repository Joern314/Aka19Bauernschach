from numpy import uint64

def reverse_bits(original):
    return sum(1<<(64-1-i) for i in range(64) if original>>i&1)