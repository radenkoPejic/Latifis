import  matplotlib.pyplot as plt

x = [0.9,0.8,0.7]
y = [82,66,22]
x = list(reversed(x))
y = list(reversed(y))
plt.plot(x,y,"b")
plt.show()