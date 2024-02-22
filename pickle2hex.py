import binascii
filename = 'C:/Users/Tom/.credentials/token.pickle'
with open(filename, 'rb') as f:
    content = f.read()
filename = 'C:/Users/Tom/.credentials/token.pickled'
with open(filename, 'w') as f:
    f.write(str(binascii.hexlify(content)))
