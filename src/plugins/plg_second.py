import time

for i in range(0, 100):
    print('Hello # {} from: {}'.format(i, __file__))
    time.sleep(3)
    
print("Plugin {} complete work".format(__file__))