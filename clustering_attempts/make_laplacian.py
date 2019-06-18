#!/usr/bin/env python
# -*- coding: utf-8 -*-


import numpy as np

def main():
    m = np.load("./matrix.npy")
    dim = len(m[0])
    diag = np.zeros(dim)

    for row in range(dim):
        diag[row] = sum(m[row])

    d = np.diag(diag)

    laplacian = d - m

    np.save("./laplacian.npy", laplacian)


if __name__ == "__main__":
    main()
