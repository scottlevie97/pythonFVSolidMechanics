from setup import *
from index_and_direction import cell_index
from A_matrix import A
from boundaryCellDisplacement import displacement_cell_BCs_A, displacement_cell_BCs_b
from boundaryCellTraction import boundaryCellTraction, traction_cell_BCs_A, traction_cell_BCs_b
from cell_corner_BCs import cell_corner_BCs_A, cell_corner_BCs_b

def cell_boundary_selection_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous):

    if BC_settings(boundaries[0]).traction:
        A_matrix = traction_cell_BCs_A(A_matrix, k, boundaries, xy)

    elif BC_settings(boundaries[0]).fixed_displacement:
        A_matrix = displacement_cell_BCs_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

    return A_matrix


def cell_boundary_selection_b(
    b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous
):

    if BC_settings(boundaries[0]).traction:
        b_matrix = traction_cell_BCs_b(
            b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous
        )

    elif BC_settings(boundaries[0]).fixed_displacement:
        b_matrix = displacement_cell_BCs_b(
            b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous
        )

    return b_matrix

def boundary_conditions_A(A_matrix, U_previous, U_old, U_old_old, xy):
    for k in np.arange(0,(nx)*(ny)):   # j is the cell number

    #    #Bottom left corner coefficients        
        if cell_index().bottom_left_corner(k):  

            boundaries = ["b", "l"]
            A_matrix = cell_corner_BCs_A(A_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)          

        #Bottom right corner coefficients            
        elif  cell_index().bottom_right_corner(k):
            
            boundaries = ["b", "r"]
            A_matrix = cell_corner_BCs_A(A_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)          

        #Top left corner coefficients            
        elif  cell_index().top_left_corner(k):
            
            boundaries = ["t", "l"]
            A_matrix = cell_corner_BCs_A(A_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)          
            
        #Top right corner coefficients            
        elif  cell_index().top_right_corner(k):

            boundaries = ["t", "r"]
            A_matrix = cell_corner_BCs_A(A_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)          
            
        # Center Bottom Boundaries
        elif  cell_index().center_bottom(k):
            
            boundaries = ["b"]
            A_matrix = cell_boundary_selection_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Top Boundaries
        elif cell_index().center_top(k):
            boundaries = ["t"]

            A_matrix = cell_boundary_selection_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Left Boundaries
        elif  cell_index().center_left(k):
            boundaries = ["l"]

            A_matrix = cell_boundary_selection_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Right Boundaries
        elif  cell_index().center_right(k):
            boundaries = ["r"]

            A_matrix = cell_boundary_selection_A(A_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)


    return A_matrix


def boundary_conditions_b(b_matrix, U_previous, U_old, U_old_old, xy):
    for k in np.arange(0,(nx)*(ny)):   # j is the cell number

    #    #Bottom left corner coefficients        
        if cell_index().bottom_left_corner(k):  

            boundaries = ["b", "l"]
            
            b_matrix = cell_corner_BCs_b(b_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)          

        #Bottom right corner coefficients            
        elif  cell_index().bottom_right_corner(k):
            boundaries = ["b", "r"]
            
            b_matrix = cell_corner_BCs_b(b_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)

        #Top left corner coefficients            
        elif  cell_index().top_left_corner(k):
            boundaries = ["t", "l"]
        
            b_matrix = cell_corner_BCs_b(b_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)

        #Top right corner coefficients            
        elif  cell_index().top_right_corner(k):  
            boundaries = ["t", "r"]
            
            b_matrix = cell_corner_BCs_b(b_matrix, k, boundaries, xy, U_previous, U_old, U_old_old)

        # Center Bottom Boundaries
        elif  cell_index().center_bottom(k):
            boundaries = ["b"]

            b_matrix = cell_boundary_selection_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Top Boundaries
        elif cell_index().center_top(k):
            boundaries = ["t"]

            b_matrix = cell_boundary_selection_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Left Boundaries
        elif  cell_index().center_left(k):
            boundaries = ["l"]

            b_matrix = cell_boundary_selection_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        # Center Right Boundaries
        elif  cell_index().center_right(k):
            boundaries = ["r"]

            b_matrix = cell_boundary_selection_b(b_matrix, k, boundaries, xy, U_old, U_old_old, U_previous)

        else:

            b_matrix[k] = (
                            A.b_temp(U_old, U_old_old, k, xy)
                            +
                            A.b_force(k, xy, U_previous)
                        )

    return b_matrix



def addBoundaryDisplacements(U_field):

    # Add boundaries to displacement fields:
    U_with_boundaries = np.zeros((ny+2, nx+2)) 
    U_reshape = U_field[:, 0].reshape(ny, nx)
    U_reshape = np.flip(U_reshape, 0)
    U_with_boundaries[1:ny+1, 1:nx +1] =  U_reshape

    V_with_boundaries = np.zeros((ny+2, nx+2)) 
    V_reshape = U_field[:, 1].reshape(ny, nx)
    V_reshape = np.flip(V_reshape, 0)
    V_with_boundaries[1:ny+1, 1:nx +1] =  V_reshape

    linearExtrapolate = boundaryCellTraction.linearExtrapolate

    # Traction

    # Bottom boundary:
    if BC_settings("b").traction:

        for i in np.arange(1, nx + 1):
            ycoord = ny+1
            U_with_boundaries[ycoord, i] = linearExtrapolate(U_with_boundaries[(ycoord-1), i], U_with_boundaries[(ycoord-2), i])
            V_with_boundaries[ycoord, i] = linearExtrapolate(V_with_boundaries[(ycoord-1), i], V_with_boundaries[(ycoord-2), i])

    # Top boundary:
    if BC_settings("t").traction:

        for i in np.arange(1, nx + 1):
            ycoord = 0
            U_with_boundaries[ycoord, i] = linearExtrapolate(U_with_boundaries[(ycoord+1), i], U_with_boundaries[(ycoord+2), i])
            V_with_boundaries[ycoord, i] = linearExtrapolate(V_with_boundaries[(ycoord+1), i], V_with_boundaries[(ycoord+2), i])


    # Right boundary:
    if BC_settings("r").traction:

        for i in np.arange(1, ny + 1):
            xcoord = nx+1
            U_with_boundaries[i, xcoord] = linearExtrapolate(U_with_boundaries[i, (xcoord-1)], U_with_boundaries[i, (xcoord-2)]) 
            V_with_boundaries[i, xcoord] = linearExtrapolate(V_with_boundaries[i, (xcoord-1)], V_with_boundaries[i, (xcoord-2)]) 

    # Left boundary:
    if BC_settings("l").traction:

        for i in np.arange(1, ny + 1):
            xcoord = 0
            U_with_boundaries[i, xcoord] = linearExtrapolate(U_with_boundaries[i, (xcoord+1)], U_with_boundaries[i, (xcoord+2)])
            V_with_boundaries[i, xcoord] = linearExtrapolate(V_with_boundaries[i, (xcoord+1)], V_with_boundaries[i, (xcoord+2)])

    # Fixed Displacement:

    # Bottom boundary:
    if BC_settings("b").fixed_displacement:

        for i in np.arange(1, nx + 1):
            ycoord = ny+1
            U_with_boundaries[ycoord, i] = boundary_U("b", "x").BC
            V_with_boundaries[ycoord, i] = boundary_U("b", "y").BC

    # Top boundary:
    if BC_settings("t").fixed_displacement:

        for i in np.arange(1, nx + 1):
            ycoord = 0
            U_with_boundaries[ycoord, i] = boundary_U("t", "x").BC
            V_with_boundaries[ycoord, i] = boundary_U("t", "y").BC


    # Right boundary:
    if BC_settings("r").fixed_displacement:

        for i in np.arange(1, ny + 1):
            xcoord = nx+1
            U_with_boundaries[i, xcoord] = boundary_U("r", "x").BC
            V_with_boundaries[i, xcoord] =  boundary_U("r", "y").BC

    # Left boundary:
    if BC_settings("l").fixed_displacement:

        for i in np.arange(1, ny + 1):
            xcoord = 0
            U_with_boundaries[i, xcoord] = boundary_U("l", "x").BC
            V_with_boundaries[i, xcoord] = boundary_U("l", "y").BC

    # Corners:

    # Bottom Left:
    xcoord = 0
    ycoord = ny+1
    U_with_boundaries[ycoord, xcoord] = linearExtrapolate(U_with_boundaries[ycoord -1, xcoord +1], (1/2)*U_with_boundaries[ycoord -2, xcoord +2]) 
    V_with_boundaries[ycoord, xcoord] = linearExtrapolate(V_with_boundaries[ycoord -1, xcoord +1], (1/2)*V_with_boundaries[ycoord -2, xcoord +2]) 

    # Bottom Right:
    xcoord = nx+1
    ycoord = ny+1
    U_with_boundaries[ycoord, xcoord] = linearExtrapolate(U_with_boundaries[ycoord -1, xcoord -1], (1/2)*U_with_boundaries[ycoord -2, xcoord -2]) 
    V_with_boundaries[ycoord, xcoord] = linearExtrapolate(V_with_boundaries[ycoord -1, xcoord -1], (1/2)*V_with_boundaries[ycoord -2, xcoord -2]) 

    # Top Left:
    xcoord = 0
    ycoord = 0
    U_with_boundaries[ycoord, xcoord] = linearExtrapolate(U_with_boundaries[ycoord +1, xcoord +1], (1/2)*U_with_boundaries[ycoord +2, xcoord +2]) 
    V_with_boundaries[ycoord, xcoord] = linearExtrapolate(V_with_boundaries[ycoord +1, xcoord +1], (1/2)*V_with_boundaries[ycoord +2, xcoord +2]) 

    # Top Right:
    xcoord = nx+1
    ycoord = 0
    U_with_boundaries[ycoord, xcoord] = linearExtrapolate(U_with_boundaries[ycoord +1, xcoord -1], (1/2)*U_with_boundaries[ycoord +2, xcoord -2]) 
    V_with_boundaries[ycoord, xcoord] = linearExtrapolate(V_with_boundaries[ycoord +1, xcoord -1], (1/2)*V_with_boundaries[ycoord +2, xcoord -2]) 

    return U_with_boundaries, V_with_boundaries

