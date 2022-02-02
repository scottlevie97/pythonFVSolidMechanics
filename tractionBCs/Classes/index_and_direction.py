# linear indexing

import numpy as np

class dim:

    # nx = input(("Enter nx: "))
    # ny = input(("Enter ny: "))

    nx = 50
    ny = 4

class index(dim):

    def __init__(self, k):

        self.k = k
        
        n = dim().nx + 2
        s = -dim().nx -2
        e = + 1
        w = - 1
        ne =  n + e
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

        n = dim().nx + 2
        s = -dim().nx -2
        e = + 1
        w = - 1
        ne =  n + e
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


#########################################################################

class boundary_point_index(dim):

    bottom_left_corner_val = 0
    bottom_right_corner_val = dim().nx + 1
    top_left_corner_val = (dim().nx+2)*(dim().ny +1) 
    top_right_corner_val = (dim().nx+2)*(dim().ny +2) - 1

    bottom_left_bottom_val = bottom_left_corner_val + 1
    bottom_left_left_val = bottom_left_corner_val + dim().nx + 2
    bottom_right_bottom_val = bottom_right_corner_val - 1
    bottom_right_right_val = bottom_right_corner_val + dim().nx + 2
    top_left_left_val = top_left_corner_val - (dim().nx + 2)
    top_left_top_val = top_left_corner_val + 1
    top_right_right_val = top_right_corner_val - (dim().nx + 2)
    top_right_top_val = top_right_corner_val - 1

    def bottom_left_bottom(self, k): 
        if k == boundary_point_index.bottom_left_bottom_val:
            return True
        else:
            return False

    def bottom_left_left(self, k): 
        if k == boundary_point_index.bottom_left_left_val:
            return True
        else:
            return False

    def bottom_right_bottom(self, k):
        if k == boundary_point_index.bottom_right_bottom_val:
            return True
        else:
            return False

    def bottom_right_right(self, k):
        if k == boundary_point_index.bottom_right_right_val:
            return True
        else:
            return False

    def top_left_left(self, k):
        if k == boundary_point_index.top_left_left_val:
            return True
        else:
            return False

    def top_left_top(self, k):
        if k == boundary_point_index.top_left_top_val:
            return True
        else:
            return False

    def top_right_right(self, k):
        if k == boundary_point_index.top_right_right_val:
            return True
        else:
            return False
    def top_right_top(self, k):
        if k == boundary_point_index.top_right_top_val:
            return True
        else:
            return False

    def bottom_left_corner(self, k):
        if k == boundary_point_index.bottom_left_corner_val:
            return True
        else:
            return False
    
    def bottom_right_corner(self, k):
        if k == boundary_point_index.bottom_right_corner_val:
            return True
        else:
            return False
    
    def top_left_corner(self, k):
        if k == boundary_point_index.top_left_corner_val:
            return True
        else:
            return False

    def top_right_corner(self, k):
        if k == boundary_point_index.top_right_corner_val:
            return True
        else:
            return False

    def center_bottom(self, k):

        if (k > boundary_point_index.bottom_left_bottom_val)\
             & (k < boundary_point_index.bottom_right_bottom_val):
            return True
        else:
            return False

    def center_top(self, k):

        if (k > boundary_point_index.top_left_top_val)\
             & (k < boundary_point_index.top_right_top_val):
            return True
        else:
            return False

    def center_left(self, k):

        if (k < boundary_point_index.top_left_left_val)\
            & (k > boundary_point_index.bottom_left_left_val)\
                & (k%(dim().nx+2) == 0):
            return True
        else:
            return False 

    def center_right(self, k):

        if (k < boundary_point_index.top_right_right_val)\
            & (k > boundary_point_index.bottom_right_right_val)\
                & (k%(dim().nx+2) == dim().nx+1):
            return True
        else:
            return False 

##########################################################################################

class cell_index(dim):

    bottom_left_corner_val = dim().nx+3
    bottom_right_corner_val = 2*(dim().nx+2) -2
    top_left_corner_val = (dim().nx+2)*(dim().ny+2) - 2*(dim().nx+2) +1
    top_right_corner_val = (dim().nx+2)*(dim().ny+2) - (dim().nx+2) -2

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

        if (k > cell_index.bottom_left_corner_val)\
             & (k < cell_index.bottom_right_corner_val):
            return True
        else:
            return False

    def center_top(self, k):

        if (k > cell_index.top_left_corner_val)\
             & (k < cell_index.top_right_corner_val):
            return True
        else:
            return False

    def center_left(self, k):

        if (k < cell_index.top_left_corner_val)\
            & (k > cell_index.bottom_right_corner_val)\
                & (k%(dim().nx+2) == 1):
            return True
        else:
            return False 

    def center_right(self, k):

        if (k < cell_index.top_left_corner_val)\
            & (k > cell_index.bottom_right_corner_val)\
                & (k%(dim().nx+2) == dim().nx):
            return True
        else:
            return False

#######################################################################

class displacement(boundary_point_index, cell_index, dim):

    # add a statement using indexes

    def __init__(self, k, u_previous, direction): 

        self.P = u_previous[k, direction]

        if k > boundary_point_index().bottom_right_corner_val:
            self.S = u_previous[k-(dim().nx+2), direction]

        if k < boundary_point_index().top_left_corner_val:
            self.N = u_previous[k+(dim().nx+2), direction]
        
        if k > boundary_point_index().bottom_left_corner_val:
            self.W = u_previous[k-1, direction]
        
        if k < boundary_point_index().top_right_corner_val:
            self.E = u_previous[k+1, direction]

        if k >= cell_index().bottom_left_corner_val:
            self.SE = u_previous[k-(dim().nx+2)+1, direction]
        
        if k >= boundary_point_index().bottom_left_left_val:
            self.SW = u_previous[k-(dim().nx+2)-1, direction]

        if k <= cell_index().top_right_corner_val:
            self.NE = u_previous[k+(dim().nx+2)+1, direction]
        
        if k <= boundary_point_index().top_right_right_val:
            self.NW = u_previous[k+(dim().nx+2)-1, direction]  

print(dim.nx)  
