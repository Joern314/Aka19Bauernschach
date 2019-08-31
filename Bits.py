import math

def get_x(pawn):
    return int(math.log2(pawn) / 8)

def get_y(pawn):
     return int(math.log2(pawn))%8


def popcount_32(i): #32 bit
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    return (((i + (i >> 4)) & 0x0F0F0F0F) * 0x01010101) >> 24

def popcount(i):
    return popcount_32(i >> 32) + popcount_32(i & 0xFFFFFFFF)