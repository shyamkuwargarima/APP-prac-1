
import numpy as np


def create_array_from_list():
    return np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


def create_array_with_arange():
    return np.arange(1, 11)


def describe_array(arr):
    print(f"Array : {arr}")
    print(f"Data type : {arr.dtype}")
    print(f"Shape : {arr.shape}")
    print(f"Number of dimensions : {arr.ndim}")
    print(f"Size : {arr.size}")


if __name__ == "__main__":
    arr1 = create_array_from_list()
    print("Array created with np.array:")
    describe_array(arr1)

    print()

    arr2 = create_array_with_arange()
    print("Array created with np.arange:")
    describe_array(arr2)

    print()
