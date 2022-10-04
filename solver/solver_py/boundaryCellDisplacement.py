from setup import *
from index_and_direction import index, displacement
from A_matrix import A

class boundaryCellDisplacement(A):

    def __init__(self, boundaries, xy):
        
        sw_S, sw_N, sw_W, sw_E = 1, 1, 1, 1

        for boundary in boundaries:
            if boundary == "b": sw_S = 2
            if boundary == "t": sw_N = 2
            if boundary == "l": sw_W = 2
            if boundary == "r": sw_E = 2

        if transient:
            self.a_P = (rho*dx*dy/(dt**2)) + A(xy).a_N*sw_N + A(xy).a_S*sw_S + A(xy).a_E*sw_E + A(xy).a_W*sw_W
        else:
            self.a_P = A(xy).a_N*sw_N + A(xy).a_S*sw_S + A(xy).a_E*sw_E + A(xy).a_W*sw_W

        self.a_N = A(xy).a_N*sw_N
        self.a_S = A(xy).a_S*sw_S
        self.a_E = A(xy).a_E*sw_E
        self.a_W = A(xy).a_W*sw_W

    def b_temp(U_old, U_old_old, k, xy): 
        return A.b_temp(U_old, U_old_old, k, xy)
    
    def b_diff(boundaries, k, xy, U_previous):

        if xy == "x":
            uv = "v"
        if xy == "y":
            uv = "u"
            
        N_term =( 
                    + Sfy*A.coef(xy, "N", uv)*(
                    (boundaryCellDisplacement.corner(boundaries, "NE", uv, U_previous, k) - boundaryCellDisplacement.corner(boundaries, "NW", uv, U_previous, k))
                    /dx)
                )
        S_term =(
                    - Sfy*A.coef(xy, "S", uv)*(
                        (boundaryCellDisplacement.corner(boundaries, "SE", uv, U_previous, k) - boundaryCellDisplacement.corner(boundaries, "SW", uv, U_previous, k))
                        /dx)
                ) 
        E_term =(
                    + Sfx*A.coef(xy, "E", uv)*(
                        (boundaryCellDisplacement.corner(boundaries, "NE", uv, U_previous, k) - boundaryCellDisplacement.corner(boundaries, "SE", uv, U_previous, k))
                        /dy)
                ) 
        W_term =(
                    - Sfx*A.coef(xy, "W", uv)*(
                        (boundaryCellDisplacement.corner(boundaries, "NW", uv, U_previous, k) - boundaryCellDisplacement.corner(boundaries, "SW", uv, U_previous, k))
                        /dy)
                ) 

        # Add term to right hand side with no unknowns
        if boundaries[0] == "b": 
            boundaryFaceTerm = boundary_U(boundaries[0], xy).BC*boundaryCellDisplacement(boundaries, xy).a_S

        if boundaries[0] == "t": 
            boundaryFaceTerm = boundary_U(boundaries[0], xy).BC*boundaryCellDisplacement(boundaries, xy).a_N
        
        if boundaries[0] == "l": 
            boundaryFaceTerm = boundary_U(boundaries[0], xy).BC*boundaryCellDisplacement(boundaries, xy).a_W

        if boundaries[0] == "r": 
            boundaryFaceTerm = boundary_U(boundaries[0], xy).BC*boundaryCellDisplacement(boundaries, xy).a_E


        b_diffusion = (N_term + S_term + E_term + W_term) + boundaryFaceTerm

        return b_diffusion
    
    def corner(boundaries, corner_placement, uv, U_previous, k):

        if uv == "u":
            uv_i = 0
            xy = "x"
        elif uv == "v":
            uv_i = 1
            xy = "y"

        disp = displacement(k, U_previous, uv_i)

        for boundary in boundaries:
            if (boundary == "b") & (corner_placement == "SE"):
                corner =  boundary_U(boundary, xy).BC
            elif (boundary == "b") & (corner_placement == "SW"):
                corner =  boundary_U(boundary, xy).BC

            elif (boundary == "t") & (corner_placement == "NE"):
                corner =  boundary_U(boundary, xy).BC
            elif (boundary == "t") & (corner_placement == "NW"):
                corner =  boundary_U(boundary, xy).BC

            elif (boundary == "l") & (corner_placement == "NW"):
                corner =  boundary_U(boundary, xy).BC
            elif (boundary == "l") & (corner_placement == "SW"):
                corner =  boundary_U(boundary, xy).BC

            elif (boundary == "r") & (corner_placement == "NE"):
                corner =  boundary_U(boundary, xy).BC
            elif (boundary == "r") & (corner_placement == "SE"):
                corner =  boundary_U(boundary, xy).BC

            else: corner = A.corner(corner_placement, uv, U_previous, k)
        
        return corner

def displacement_cell_BCs_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous):

    A_matrix[k,k] = boundaryCellDisplacement(boundaries, xy).a_P

    if boundaries[0] != "t":
        A_matrix[k,index(k).n] = - boundaryCellDisplacement(boundaries, xy).a_N        

    if boundaries[0] != "b":
        A_matrix[k,index(k).s] = - boundaryCellDisplacement(boundaries, xy).a_S   

    if boundaries[0] != "r":
        A_matrix[k, index(k).e] = - boundaryCellDisplacement(boundaries, xy).a_E

    if boundaries[0] != "l":
        A_matrix[k, index(k).w] = - boundaryCellDisplacement(boundaries, xy).a_W

    return A_matrix

def displacement_cell_BCs_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous):

    b_matrix[k] =(
                boundaryCellDisplacement.b_temp(U_old, U_old_old, k, xy)
                +
                boundaryCellDisplacement.b_diff(boundaries, k, xy, U_previous)
            )   

    return b_matrix


def displacement_cell_BCs_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous):

    A_matrix[k,k] = boundaryCellDisplacement(boundaries, xy).a_P

    if boundaries[0] != "t":
        A_matrix[k,index(k).n] = - boundaryCellDisplacement(boundaries, xy).a_N        

    if boundaries[0] != "b":
        A_matrix[k,index(k).s] = - boundaryCellDisplacement(boundaries, xy).a_S   

    if boundaries[0] != "r":
        A_matrix[k, index(k).e] = - boundaryCellDisplacement(boundaries, xy).a_E

    if boundaries[0] != "l":
        A_matrix[k, index(k).w] = - boundaryCellDisplacement(boundaries, xy).a_W

    return A_matrix

def displacement_cell_BCs_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous):

    b_matrix[k] =(
                boundaryCellDisplacement.b_temp(U_old, U_old_old, k, xy)
                +
                boundaryCellDisplacement.b_diff(boundaries, k, xy, U_previous)
            )   

    return b_matrix
