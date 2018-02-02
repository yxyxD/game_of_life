import numpy as np
import matplotlib.pyplot as plt

generation = np.zeros((100,100))
print(generation)

beacon = [[1,1,0,0],[1,1,0,0],[0,0,1,1],[0,0,1,1]]
generation[1:5, 1:5] = beacon

print(generation)
plt.axis('off')
plt.imshow(generation, cmap='binary', interpolation='nearest')
plt.show()