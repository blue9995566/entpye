import random

positions=[]
def newposition():
    a=(random.randint(-3,0)*150,random.randint(0,9)*60)
    while a in positions:
        a=(random.randint(-3,0)*150,random.randint(0,9)*60)
    positions.append(a)
    return a

print int(round(1.9))