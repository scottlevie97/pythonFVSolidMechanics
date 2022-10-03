from setup import *
from index_and_direction import index, cell_index, displacement

class A(index, displacement):

    val = "value that stays in class without changning with instance"

    def __init__(self, xy):

        if xy == "x":
            uv = "u"

        if xy == "y":
            uv = "v"

        self.a_N = + A.coef(xy, "N", uv)*(Sfy)/dy
        self.a_S = - A.coef(xy, "S", uv)*(Sfy)/dy
        self.a_E = + A.coef(xy, "E", uv)*(Sfx)/dx
        self.a_W = - A.coef(xy, "W", uv)*(Sfx)/dx

        if transient:
            self.a_P = (rho*dx*dy/(dt**2)) + self.a_N + self.a_S + self.a_E + self.a_W
        else:
            self.a_P = self.a_N + self.a_S + self.a_E + self.a_W

    def createMatrix(self):

        A_no_boundary = np.zeros([ny*nx, ny*nx])

        # I think this is the only for loop?

        for k in range(0, ny*nx):
            if cell_index().no_boundary(k):      
                    A_no_boundary[k, k] = self.a_P
                    A_no_boundary[k, index(k).n] = -self.a_N
                    A_no_boundary[k, index(k).s] = -self.a_S
                    A_no_boundary[k, index(k).e] = -self.a_E
                    A_no_boundary[k, index(k).w] = -self.a_W

        return A_no_boundary

    # b temporal term
    def b_temp(U_old, U_old_old, k, xy):

        if xy == "x":
            if transient:
                b_temporal_term = (rho/(dt**2))*( 2*(U_old[k,0])*dx*dy - U_old_old[k,0]*dx*dy)
            else:
                b_temporal_term = 0

        if xy == "y":
            if transient:
                b_temporal_term = (rho/(dt**2))*( 2*(U_old[k,1])*dx*dy - U_old_old[k,1]*dx*dy)
            else:
                b_temporal_term = 0
        
        return b_temporal_term
    
    def b_force(k, xy, U_previous):

        if xy == "x":
            uv = "v"
        if xy == "y":
            uv = "u"

        b_diffusion = (
                                Sfy*A.coef(xy, "N", uv)*(
                                    (A.corner("NE", uv, U_previous, k) - A.corner("NW", uv, U_previous, k))
                                    /dx)
                                + 
                                Sfy*A.coef(xy, "S", uv)*(
                                    (A.corner("SE", uv, U_previous, k) - A.corner("SW", uv, U_previous, k))
                                    /dx)
                                +
                                Sfx*A.coef(xy, "E", uv)*(
                                    (A.corner("NE", uv, U_previous, k) - A.corner("SE", uv, U_previous, k))
                                    /dy)
                                +
                                Sfx*A.coef(xy, "W", uv)*(
                                    (A.corner("NW", uv, U_previous, k) - A.corner("SW", uv, U_previous, k))
                                    /dy)
        )

        return b_diffusion
    
    def corner(corner_placement, uv, U_previous, k):
        if uv == "u":
            uv_i = 0
        elif uv == "v":
            uv_i = 1

        disp = displacement(k, U_previous, uv_i)

        if corner_placement == "NE":
            return (1/4)*(disp.P + disp.NE + disp.N + disp.E)
        if corner_placement == "SE":
            return (1/4)*(disp.P + disp.SE + disp.S + disp.E)
        if corner_placement == "SW":
            return (1/4)*(disp.P + disp.SW + disp.S + disp.W)
        if corner_placement == "NW":
            return (1/4)*(disp.P + disp.NW + disp.N + disp.W)


    
    def coef(xy, face, uv):
        # could have and statements
        if xy == "x":
            if face == "N":
                if uv == "u":
                    return mu_
                if uv == "v":
                    return mu_
            if face == "S":
                if uv == "u":
                    return - mu_
                if uv == "v":
                    return - mu_
            if face == "E":
                if uv == "u":
                    return 2*mu_ + lambda_
                if uv == "v":
                    return lambda_
            if face == "W":
                if uv == "u":
                    return - (2*mu_ + lambda_)
                if uv == "v":
                    return - lambda_

        elif xy == "y":
            if face == "N":
                if uv == "u":
                    return lambda_
                if uv == "v":
                    return 2*mu_ + lambda_
            if face == "S":
                if uv == "u":
                    return - lambda_
                if uv == "v":
                    return - (2*mu_ + lambda_)
            if face == "E":
                if uv == "u":
                    return mu_
                if uv == "v":
                    return mu_
            if face == "W":
                if uv == "u":
                    return - mu_
                if uv == "v":
                    return - mu_


