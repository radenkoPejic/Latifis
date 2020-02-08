from myQueue import myQueue

red = myQueue(3)
red.put(3)
red.put(2)
red.put(4)
red.put(1)
red.put(7)
elems = red.get();
for elem in elems:
    print(elem)

