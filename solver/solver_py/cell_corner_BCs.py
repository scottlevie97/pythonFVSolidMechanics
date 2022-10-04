from setup import *
from index_and_direction import index, displacement
from A_matrix import A
from boundaryCellDisplacement import boundaryCellDisplacement
from boundaryCellTraction import boundaryCellTraction

# Write a function that reads each corner boundary BC (traction or displacement) and applies the correct a and b terms

#This will take in boundaries array, example: [t,l] -> this means top left corner
#It will then search BC_settings 

def cell_corner_BCs_A(A_matrix, k, boundaries, xy, U_previous, U_old, U_old_old):

    a_N = A(xy).a_N
    a_S = A(xy).a_S
    a_E = A(xy).a_E
    a_W = A(xy).a_W

    #Overrule a terms for on the boundary

    for boundary in boundaries:

        if boundary == "t":

            if BC_settings("t").traction:

                # Apply traction settings to North term
                a_N = 0        
            
            elif BC_settings("t").fixed_displacement:

                # Apply fixed boundary setings to North term
                a_N = boundaryCellDisplacement(["t"], xy).a_N        

        if boundary == "b":

            if BC_settings("b").traction:

                # Apply traction settings to South term
                a_S = 0

            elif BC_settings("b").fixed_displacement:

                # Apply fixed boundary setings to South term
                a_S = boundaryCellDisplacement(["b"], xy).a_S

        if boundary == "r":

            if BC_settings("r").traction:

                # Apply traction settings to East term
                a_E = 0

            elif BC_settings("r").fixed_displacement:

                # Apply fixed boundary setings to East term
                a_E = boundaryCellDisplacement(["r"], xy).a_E

        if boundary == "l":

            if BC_settings("l").traction:

                # Apply traction settings to West term
                a_W = 0

            elif BC_settings("l").fixed_displacement:

                # Apply fixed boundary setings to West term
                a_W = boundaryCellDisplacement([boundary], xy).a_W

    if transient:
        a_P = (rho*dx*dy/(dt**2)) + a_N + a_S + a_E + a_W

    else:
        a_P = a_N + a_S + a_E + a_W

    #Aply a terms to matrices

    A_matrix[k,k] = a_P

    for boundary in boundaries:

        if boundary == "t":
        
            A_matrix[k,index(k).s] = - a_S

        elif boundary == "b":

            A_matrix[k,index(k).n] = - a_N

        elif boundary == "l":

            A_matrix[k,index(k).e] = - a_E

        elif boundary == "r":
            
            A_matrix[k,index(k).w] = - a_W 

    return A_matrix


# Need to add face term for traction boundaries

def cell_corner_BCs_b(b_matrix, k, boundaries, xy, U_previous, U_old, U_old_old):

    def cornercorner(boundaries, corner_placement, uv, U_previous, k):

        # This is where the extrapolation occurs
 
        if uv == "u":
            uv_i = 0
            xy = "x"
        elif uv == "v":
            uv_i = 1
            xy = "y"

        disp = displacement(k, U_previous, uv_i)

        # Top left:
        if boundaries == ["t", "l"]: 
            if corner_placement == "NW":
                corner = ((3/2)*disp.P - (1/2)*disp.SE)

            elif corner_placement == "SE":
                corner = A.corner(corner_placement, uv, U_previous, k)
            
            else:
                for i in [["NE", 0], ["SW", 1]]:            
                    if corner_placement == i[0]:
                        if BC_settings(boundaries[i[1]]).traction:
                            corner = boundaryCellTraction.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)
                        elif BC_settings(boundaries[i[1]]).fixed_displacement:
                            corner = boundaryCellDisplacement.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)


        # Top Right:
        if boundaries == ["t", "r"]: 
            if corner_placement == "NE":
                corner = ((3/2)*disp.P - (1/2)*disp.SW)

            elif corner_placement == "SW":
                corner = A.corner(corner_placement, uv, U_previous, k)
            
            else:
                for i in [["NW", 0], ["SE", 1]]:
                    if corner_placement == i[0]:
                        if BC_settings(boundaries[i[1]]).traction:
                            corner = boundaryCellTraction.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)
                        elif BC_settings(boundaries[i[1]]).fixed_displacement:
                            corner = boundaryCellDisplacement.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)


        # Bottom Left:
        if boundaries == ["b", "l"]:
            if corner_placement == "SW":
                corner = ((3/2)*disp.P - (1/2)*disp.NE)

            elif corner_placement == "NE":
                corner = A.corner(corner_placement, uv, U_previous, k)
            
            else: 
                for i in [["SE", 0], ["NW", 1]]:   
                    if corner_placement == i[0]:
                        if BC_settings(boundaries[i[1]]).traction:
                            corner = boundaryCellTraction.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)
                        elif BC_settings(boundaries[i[1]]).fixed_displacement:
                            corner = boundaryCellDisplacement.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)

        # Bottom Right:
        if boundaries == ["b", "r"]: 
            if corner_placement == "SE":
                corner = ((3/2)*disp.P - (1/2)*disp.NW)

            elif corner_placement == "NW":
                corner = A.corner(corner_placement, uv, U_previous, k)
            
            else:
                for i in [["SW", 0], ["NE", 1]]:            
                    if corner_placement == i[0]:
                        if BC_settings(boundaries[i[1]]).traction:
                            corner = boundaryCellTraction.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)
                        elif BC_settings(boundaries[i[1]]).fixed_displacement:
                            corner = boundaryCellDisplacement.corner([boundaries[i[1]]], corner_placement, uv, U_previous, k)



        return corner   

    # b diff

    def b_diff(boundaries, k, xy, U_previous):

        if xy == "x":
            uv = "v"
        if xy == "y":
            uv = "u"
            
        def N_term():

            if (boundaries[0] != "t") | ((boundaries[0] == "t") & (BC_settings("t").fixed_displacement)):
                N_term = + Sfy*A.coef(xy, "N", uv)*(
                    (cornercorner(boundaries, "NE", uv, U_previous, k) - cornercorner(boundaries, "NW", uv, U_previous, k))
                    /dx)

            elif BC_settings("t").traction:   
                if (xy == "x") : N_term =  Sfy*tr_top_x  
                if (xy == "y") : N_term =  Sfy*tr_top_y            

            return N_term

        def S_term():

            if (boundaries[0] != "b") | ((boundaries[0] == "b") & (BC_settings("b").fixed_displacement)):
                S_term = - Sfy*A.coef(xy, "S", uv)*(
                    (cornercorner(boundaries, "SE", uv, U_previous, k) - cornercorner(boundaries, "SW", uv, U_previous, k))
                    /dx)

            elif BC_settings("b").traction: 
                if (xy == "x") : S_term =  Sfy*tr_bottom_x 
                if (xy == "y") : S_term =  Sfy*tr_bottom_y

            return S_term

        def E_term():

            if (boundaries[1] != "r") | ((boundaries[1] == "r") & (BC_settings("r").fixed_displacement)):
                E_term = + Sfx*A.coef(xy, "E", uv)*(
                            (cornercorner(boundaries, "NE", uv, U_previous, k) - cornercorner(boundaries, "SE", uv, U_previous, k))
                            /dy)
                
            elif BC_settings("r").traction: 
                if (xy == "x") : E_term =  Sfx*tr_right_x  
                if (xy == "y") : E_term =  Sfx*tr_right_y

            return E_term

        def W_term():

            if (boundaries[1] != "l") | ((boundaries[1] == "l") & (BC_settings("l").fixed_displacement)):
                W_term = - Sfx*A.coef(xy, "W", uv)*(
                (cornercorner(boundaries, "NW", uv, U_previous, k) - cornercorner(boundaries, "SW", uv, U_previous, k))
                /dy)

            elif BC_settings("l").traction: 
                if (xy == "x") : W_term =  Sfx*tr_left_x  
                if (xy == "y") : W_term =  Sfx*tr_left_y

            return W_term

        b_diffusion = N_term() + S_term() + E_term() + W_term()

        return b_diffusion


    b_matrix[k] =(
            A.b_temporal(U_old, U_old_old, k, xy)
            +
            b_diff(boundaries, k, xy, U_previous)
        )  

    return b_matrix    


    