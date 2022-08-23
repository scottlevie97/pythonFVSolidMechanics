# linear indexing

import numpy as np


class dim:

    # nx = input(("Enter nx: "))
    # ny = input(("Enter ny: "))
	nx = 6
	ny = 5


class index(dim):
    def __init__(self, k):

        self.k = k

        n = dim().nx
        s = -dim().nx
        e = +1
        w = -1
        ne = n + e
        se = s + e
        sw = s + w
        nw = n + w

        self.n = k + n
        self.s = k + s
        self.e = k + e
        self.w = k + w
        self.ne = k + ne
        self.se = k + se
        self.sw = k + sw
        self.nw = k + nw

    def dir(self, directionarray):

        n = dim().nx
        s = -dim().nx
        e = +1
        w = -1
        ne = n + e
        se = s + e
        sw = s + w
        nw = n + w

        arr1 = np.array([n, s, e, w, ne, se, sw, nw])
        arr2 = np.array(["n", "s", "e", "w", "ne", "se", "sw", "nw"])

        direction = self.k

        for i in np.arange(0, len(directionarray)):

            for j in np.arange(0, len(arr2)):

                if arr2[j] == directionarray[i]:

                    direction = direction + arr1[j]

        return direction


##########################################################################################


class cell_index(dim):

    bottom_left_corner_val = 0
    bottom_right_corner_val = dim().nx - 1
    top_left_corner_val = (dim().nx ) * (dim().ny) - dim().nx
    top_right_corner_val = (dim().nx ) * (dim().ny ) - 1

    def bottom_left_corner(self, k):
        if k == cell_index.bottom_left_corner_val:
            return True
        else:
            return False

    def bottom_right_corner(self, k):
        if k == cell_index.bottom_right_corner_val:
            return True
        else:
            return False

    def top_left_corner(self, k):
        if k == cell_index.top_left_corner_val:
            return True
        else:
            return False

    def top_right_corner(self, k):
        if k == cell_index.top_right_corner_val:
            return True
        else:
            return False

    def center_bottom(self, k):

        if (k > cell_index.bottom_left_corner_val) & (
            k < cell_index.bottom_right_corner_val
        ):
            return True
        else:
            return False

    def center_top(self, k):

        if (k > cell_index.top_left_corner_val) & (k < cell_index.top_right_corner_val):
            return True
        else:
            return False

    def center_left(self, k):

        if (
            (k < cell_index.top_left_corner_val)
            & (k > cell_index.bottom_right_corner_val)
            & (k % dim().nx == 0)
        ):
            return True
        else:
            return False

    def center_right(self, k):

        if (
            (k < cell_index.top_left_corner_val)
            & (k > cell_index.bottom_right_corner_val)
            & (k % dim().nx == dim().nx - 1)
        ):
            return True
        else:
            return False

    def no_boundary(self, k):

        if (
            (k > cell_index.bottom_right_corner_val + 1)
            & (k < cell_index.top_left_corner_val - 1)
            & (k % (dim().nx) != 0)
            & (k % (dim().nx) != (dim().nx-1))
        ):
            return True
        else:
            return False


#######################################################################

class displacement(cell_index, dim):

    # add a statement using indexes

    def __init__(self, k, U_previous, direction):

        self.P = U_previous[k, direction]

        if k > cell_index().bottom_right_corner_val:
            self.S = U_previous[k - dim().nx, direction]

        if k < cell_index().top_left_corner_val:
            self.N = U_previous[k + dim().nx, direction]

        if k > cell_index().bottom_left_corner_val:
            self.W = U_previous[k - 1, direction]

        if k < cell_index().top_right_corner_val:
            self.E = U_previous[k + 1, direction]

        if k >= cell_index().bottom_left_corner_val:
            self.SE = U_previous[k - dim().nx + 1, direction]

        if k >= (cell_index().bottom_left_corner_val + 1):
            self.SW = U_previous[k - dim().nx - 1, direction]

        if k < (cell_index().top_left_corner_val - 1):
            self.NE = U_previous[k + dim().nx + 1, direction]

        if k < (cell_index().top_left_corner_val):
            self.NW = U_previous[k + dim().nx - 1, direction]


print(dim.nx)
print(dim.ny)
