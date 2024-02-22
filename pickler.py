import binascii
import sys

for line in sys.stdin:
    pickled = (binascii.unhexlify(line))
filename = './token.pickle'
with open(filename, 'wb') as f:
    f.write(pickled)
