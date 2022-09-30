from setup import *
from index_and_direction import index, displacement
from A_matrix import A
from boundaryCellDisplacement import boundaryCellDisplacement

class boundaryCellTraction(boundaryCellDisplacement, A):

    def __init__(self, boundaries, xy):

        # Initialise a terms to the same as internal cell values        
        self.a_N = A(xy).a_N
        self.a_S = A(xy).a_S
        self.a_E = A(xy).a_E
        self.a_W = A(xy).a_W

        # Zero a terms if on the boundary
        for boundary in boundaries:
            if boundary == "b": self.a_S = 0
            if boundary == "t": self.a_N = 0
            if boundary == "l": self.a_W = 0
            if boundary == "r": self.a_E = 0

        if transient:
            self.a_P = (rho*dx*dy/(dt**2)) + self.a_N + self.a_S + self.a_E + self.a_W
        else:
            self.a_P = self.a_N + self.a_S + self.a_E + self.a_W


    def b_temp(U_old, U_old_old, k, xy):      
        return A.b_temp(U_old, U_old_old, k, xy)
    
    def b_diff(boundaries, k, xy, U_previous):

        if xy == "x":
            uv = "v"
        if xy == "y":
            uv = "u"

        N_term =(
                    Sfy*A.coef(xy, "N", uv)*(
                    (boundaryCellTraction.corner(boundaries, "NE", uv, U_previous, k) - boundaryCellTraction.corner(boundaries, "NW", uv, U_previous, k))
                    /dx)
                )
        S_term =(
                    Sfy*A.coef(xy, "S", uv)*(
                        (boundaryCellTraction.corner(boundaries, "SE", uv, U_previous, k) - boundaryCellTraction.corner(boundaries, "SW", uv, U_previous, k))
                        /dx)
                ) 
        E_term =(
                    Sfx*A.coef(xy, "E", uv)*(
                        (boundaryCellTraction.corner(boundaries, "NE", uv, U_previous, k) - boundaryCellTraction.corner(boundaries, "SE", uv, U_previous, k))
                        /dy)
                ) 
        W_term =(
                    Sfx*A.coef(xy, "W", uv)*(
                        (boundaryCellTraction.corner(boundaries, "NW", uv, U_previous, k) - boundaryCellTraction.corner(boundaries, "SW", uv, U_previous, k))
                        /dy)
                )

        for boundary in boundaries:

            if (boundary == "b") & (xy == "x") : S_term =  Sfy*tr_bottom_x   
            if (boundary == "b") & (xy == "y") : S_term =  Sfy*tr_bottom_y  
            if (boundary == "t") & (xy == "x") : N_term =  Sfy*tr_top_x  
            if (boundary == "t") & (xy == "y") : N_term =  Sfy*tr_top_y 
            if (boundary == "l") & (xy == "x") : W_term =  Sfx*tr_left_x  
            if (boundary == "l") & (xy == "y") : W_term =  Sfx*tr_left_y  
            if (boundary == "r") & (xy == "x") : E_term =  Sfx*tr_right_x  
            if (boundary == "r") & (xy == "y") : E_term =  Sfx*tr_right_y        

        b_diffusion = (N_term + S_term + E_term + W_term)

        return b_diffusion

    def corner(boundaries, corner_placement, uv, U_previous, k):

        # This is where the extrapolation occurs
 
        if uv == "u":
            uv_i = 0
            xy = "x"
        elif uv == "v":
            uv_i = 1
            xy = "y"

        disp = displacement(k, U_previous, uv_i)

        for boundary in boundaries:
            if (boundary == "b") & (corner_placement == "SE"):
                corner =  (1/2)*( ((3/2)*disp.E - (1/2)*disp.NE) + ((3/2)*disp.P - (1/2)*disp.N))
            elif (boundary == "b") & (corner_placement == "SW"):
                corner =  (1/2)*( ((3/2)*disp.W - (1/2)*disp.NW) + ((3/2)*disp.P - (1/2)*disp.N))            

            elif (boundary == "t") & (corner_placement == "NE"):
                corner =  (1/2)*( ((3/2)*disp.E - (1/2)*disp.SE) + ((3/2)*disp.P - (1/2)*disp.S))
            elif (boundary == "t") & (corner_placement == "NW"):
                corner =  (1/2)*( ((3/2)*disp.W - (1/2)*disp.SW) + ((3/2)*disp.P - (1/2)*disp.S))

            elif (boundary == "l") & (corner_placement == "NW"):
                corner =  (1/2)*( ((3/2)*disp.N - (1/2)*disp.NE) + ((3/2)*disp.P - (1/2)*disp.E))
            elif (boundary == "l") & (corner_placement == "SW"):
                corner =  (1/2)*( ((3/2)*disp.S - (1/2)*disp.SE) + ((3/2)*disp.P - (1/2)*disp.E))

            elif (boundary == "r") & (corner_placement == "NE"):
                corner =  (1/2)*( ((3/2)*disp.N - (1/2)*disp.NW) + ((3/2)*disp.P - (1/2)*disp.W))
            elif (boundary == "r") & (corner_placement == "SE"):
                corner =  (1/2)*( ((3/2)*disp.S - (1/2)*disp.SW) + ((3/2)*disp.P - (1/2)*disp.W))

            else: corner = A.corner(corner_placement, uv, U_previous, k)
        
        return corner


def traction_cell_BCs_A(A_matrix, k, boundaries, xy):

    A_matrix[k,k] = boundaryCellTraction(boundaries, xy).a_P
    
    if boundaries[0] != "t":
      
        A_matrix[k,index(k).n] = - boundaryCellTraction(boundaries, xy).a_N

    if boundaries[0] != "b":

        A_matrix[k,index(k).s] = - boundaryCellTraction(boundaries, xy).a_S

    if boundaries[0] != "r":

        A_matrix[k,index(k).e] = - boundaryCellTraction(boundaries, xy).a_E

    if boundaries[0] != "l":
        
        A_matrix[k,index(k).w] = - boundaryCellTraction(boundaries, xy).a_W           

    return A_matrix

def traction_cell_BCs_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous, ):

    b_matrix[k] =(
                    boundaryCellTraction.b_temp(U_old, U_old_old, k, xy)
                    +
                    boundaryCellTraction.b_diff(boundaries, k, xy, U_previous, )  
                )    

    return b_matrix