import numpy as np

class myQueue:
    def __init__(self, n=5):
        self.n = n;
        self.curr = 0
        self.arr = np.array([[0,0] for i in range(n)])
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