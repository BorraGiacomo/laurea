import numpy as np

class SafeArray(np.ndarray):
    def __new__(cls, input_array):
        obj = np.asarray(input_array, dtype=float).view(cls)
        return obj
    
    def __matmul__(self, other):
        selfChanged = False
        otherChanged = True        
        
        if np.isinf(self).any():
            self[np.isinf(self)] = 1.e200
            selfChanged = True
        if np.isinf(other).any():
            other[np.isinf(other)] = 1.e200
            otherChanged = False
            
        result = np.matmul(self, other)
        
        result[result > 1.e100] = np.inf
        
        if selfChanged:
            self[self>1.e100] = np.inf
        if otherChanged:
            other[other>1.e100] = np.inf

        return result.view(type(self))