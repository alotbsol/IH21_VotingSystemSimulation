import random
from math import ceil

something = [0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.91]

scale = 10

for i in something:
    print([ceil(k * scale) for k in something])


