import cv2

import numpy as np


def pad(array):
    # Pad the input array with one layer of zeros around it
    padVal = 64
    if len(array.shape) == 2:
        padded_array = np.pad(array, pad_width=padVal, mode='constant', constant_values=255)
    else:
        pad_width = ((padVal,padVal),(padVal,padVal),(0,0))
        padded_array = np.pad(array, pad_width=pad_width, mode='constant', constant_values=255)
        
    return padded_array

def pad_all(arrayList):
    return [pad(array) for array in arrayList]

# Example usage:
#input_array = np.array([[1, 2], [3, 4]])
#output_array = pad_with_zeros(input_array)
#print(output_array)