import matplotlib.pyplot as plt
import json
import pandas as pd
with open('./data/sciERC.json','r') as f:
    data = json.load(f)

steps = [d["step"] for d in data]
losses = [d["loss"] for d in data]

plt.plot(steps, losses, marker='o')
plt.xlabel('Step')
plt.ylabel('Loss')
plt.title('Loss vs Step')
plt.grid(True)
plt.savefig('img/sciLoss.png')
plt.show()
