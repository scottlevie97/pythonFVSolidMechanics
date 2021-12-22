class boundary_point_index:

    nx =  8
    ny = 8

    bottom_left_corner_val = 0
    bottom_right_corner_val = nx + 1
    top_left_corner_val = (nx+2)*(ny +1) 
    top_right_corner_val = (nx+2)*(ny +2) - 1

    bottom_left_bottom_val = bottom_left_corner_val + 1
    bottom_left_left_val = bottom_left_corner_val + nx + 2
    bottom_right_bottom_val = bottom_right_corner_val - 1
    bottom_right_right_val = bottom_right_corner_val + nx + 2
    top_left_left_val = top_left_corner_val - (nx + 2)
    top_left_top_val = top_left_corner_val + 1
    top_right_right_val = top_right_corner_val - (nx + 2)
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
        if k == boundary_point_index.bottom_left_corner_val:
            return True
        else:
            return False
    
    def top_left_corner(self, k):
        if k == boundary_point_index.bottom_left_corner_val:
            return True
        else:
            return False

    def top_right_corner(self, k):
        if k == boundary_point_index.bottom_left_corner_val:
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
                & (k%(nx+2) == 0):
            return True
        else:
            return False 

    def center_right(self, k):

        if (k < boundary_point_index.top_right_right_val)\
            & (k > boundary_point_index.bottom_right_right_val)\
                & (k%(nx+2) == nx+1):
            return True
        else:
            return False 