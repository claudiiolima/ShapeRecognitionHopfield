import numpy as np

# Utils

def verify(data,predicted):
    data = [d for d in data]
    predicted = [d for d in predicted]
    for i in range(len(predicted)):
        for j in range(len(data)):
            if np.allclose(predicted[i],data[j]):
                return True

    return False

def compare(data,predicted):
    data = [d for d in data]
    for i in range(len(data)):
        if np.allclose(predicted,data[i]):
            return i

    return len(data)+1