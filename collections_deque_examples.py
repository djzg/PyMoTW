#!/usr/bin/env/python3

""" deque - Double-ended queue """

# A double-ended queue, or deque, supports adding and removing elements from either end of the queue.
# The more commonly used stacks and queues are degenerate forms of deques, where the inputs and outputs are restricted
# to a single end.

import collections

d = collections.deque("abcdefg")
print("Deque:", d)
print("Length:", len(d))
print("Left end:", d[0])
print("Right end:", d[-1])

d.remove("c")
print("remove(c):", d)

# Since deques are a type of sequence container, they support some of the same operations as list, such as examining
# the contents with __getitem__(), determining length, and removing elements from the middle of the queue by matching
# identity.

""" Populating """

# A deque can be populated from either end, termed "left" and "right" in Py implementation.

d1 = collections.deque()
# Add to the right
d1.extend("abcdefghijkl")
print("extend       :", d1)
d1.append("m")
print("append       :", d1)

d2 = collections.deque()
d2.extendleft(range(6))
print("extendleft   :", d2)
d2.appendleft(6)
print("appendleft   :", d2)


""" Consuming """

# Similarly, the elements of the deque can be consumed from both ends or either end, depending on the algorithm
# being applied.

print()
print("--- Consuming ---")
print()
print("From the right")
d = collections.deque("abcdefg")

while True:
    try:
        print(d.pop(), end="")
    except IndexError:
        break

print()

print("\nFrom the left: ")
d = collections.deque(range(6))
while True:
    try:
        print(d.popleft(), end="")
    except IndexError:
        break
print()

# Since deques are thread-safe, the contents can even be consumed from both ends at the same time from separate threads.

import threading
import time

candle = collections.deque(range(5))

def burn(direction, nextSource):
    while True:
        try:
            next = nextSource()
        except IndexError:
            break
        else:
            print("{:>8}: {}".format(direction, next))
            time.sleep(0.1)
    print("{:>8} done".format(direction))
    return

# The threads in this example alternate between each end, removing items until the deque is empty.


left = threading.Thread(target=burn,
                        args=("Left", candle.popleft))
right = threading.Thread(target=burn,
                         args=("Right", candle.pop))

left.start()
right.start()


""" Rotating """

# Another useful aspect of the deque is the ability to rotate it in either direction, so as to skip over some items.

d = collections.deque(range(10))
print("Normal           :", d)

d = collections.deque(range(10))
d.rotate(2)
print("Right rotation   :", d)

d = collections.deque(range(10))
d.rotate(-2)
print("Left rotation    :", d)


""" Constraining the queue size """

# A deque instance can be configured with a maximum length so that it never grows beyond that size. When the queue
# reaches the specified length, existing items are discarded as new items are added. This behavior is useful for
# finding the last n items in a stream of undetermined length.

import random

# Set the random seed s owe see the same output each time the script is run
random.seed(1)

d1 = collections.deque(maxlen=3)
d2 = collections.deque(maxlen=3)

for i in range(10):
    n = random.randint(0, 100)
    print("n = ", n)
    d1.append(n)
    d2.appendleft(n)
    print("D1:", d1)
    print("D2:", d2)

left.join()
right.join()