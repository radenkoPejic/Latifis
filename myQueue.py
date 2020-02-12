import numpy as np
import math

class myQueue:
    def __init__(self, n=5):
        self.n = n;
        self.curr = 0
        self.reset()
    def reset(self):
        self.arr = np.array([[0,0] for i in range(self.n)])
    def put(self, obj):
        self.arr[self.curr] = obj;
        self.curr = (self.curr+1)%self.n;
    def get(self):
        new_arr = [];
        for i in range(self.n):
            index = (self.curr+i)%self.n;
            new_arr.append(self.arr[index])
        return new_arr;
    def size(self):
        return self.n;
    def calc(self):
        coef = [3,5,2,1]
        arr = self.get();
        R = 0
        for i in range(len(arr)-1):
            deltaPrev = arr[i][0]-arr[i][1]
            deltaState = arr[i+1][0]-arr[i+1][1]
            R += math.exp(coef[i]*(deltaState-deltaPrev))
        print(R)
        return R
    def calc2(self):
        arr = self.get();
        R = 0
        for i in range(len(arr)-1):
            deltaPrev = arr[i][0]-arr[i][1]
            deltaState = arr[i+1][0]-arr[i+1][1]
            R += 1.0*(deltaState-deltaPrev)/100
        print("R1: "+str(R))
        R = max(0,100*R)
        print("R2: "+str(R))
        return R