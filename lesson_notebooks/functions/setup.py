import numpy as np
import pandas as pd
from scipy.sparse.linalg import spsolve
from matplotlib import pyplot as plt

import sys
sys.path.append("functions/")

def printVar (varname, var):

    print(varname)
    print(var)

def saveArray (name, array): 

    pd.DataFrame(array).to_csv("Solution/" + name + ".csv", index=False, header=None)


# Set Boundary Conditions:
class BC_settings:

    left = "fixed_displacement"
    right = "traction"
    top = "traction"
    bottom = "traction"

    def __init__(self, boundary):

        if boundary == "l":
            if BC_settings.left == "traction":
                self.traction = True
                self.fixed_displacement = False
            elif BC_settings.left == "fixed_displacement":
                self.fixed_displacement = True
                self.traction = False

        if boundary == "r":
            if BC_settings.right == "traction":
                self.traction = True
                self.fixed_displacement = False
            elif BC_settings.right == "fixed_displacement":
                self.fixed_displacement = True
                self.traction = False

        if boundary == "t":
            if BC_settings.top == "traction":
                self.traction = True
                self.fixed_displacement = False
            elif BC_settings.top == "fixed_displacement":
                self.fixed_displacement = True
                self.traction = False

        if boundary == "b":
            if BC_settings.bottom == "traction":
                self.traction = True
                self.fixed_displacement = False
            elif BC_settings.bottom == "fixed_displacement":
                self.fixed_displacement = True
                self.traction = False


# Solve the 2D Navier-Cauchy equation using a segregated finite volume method

# Define mesh geometry and boundary conditions

Lx = 2 #width of domain
Ly = .1 #height of domain

fac = 1

nx = 40      #number of control volumes in the x-direction
ny = 4    #number of control volumes in the y-direction


# Cantilever Setup 

tr_right_x = 0    #u boundary condition at the right boundary
tr_right_y = - 1e6   #v boundary condition at the right boundary

tr_top_x = 0    #u boundary condition at the top boundary
tr_top_y = 0       #v boundary condition at the top boundary

tr_bottom_x = 0    #u boundary condition at the bottom boundary 
tr_bottom_y = 0  #v boundary condition at the bottom boundary

u_left = 0
v_left = 0


# my_file = open("index_and_direction.py")
# string_list = my_file.readlines()
# my_file.close()

# string_list[9] = "\tnx = " + str(nx) + "\n"
# string_list[10] = "\tny = " + str(ny) + "\n"

# my_file = open("index_and_direction.py", "w")
# my_file.writelines(string_list)
# my_file.close()

from index_and_direction import dim
from index_and_direction import index
from index_and_direction import boundary_point_index
from index_and_direction import cell_index
from index_and_direction import displacement



rho = 8050 #density of steel in kg/m^3

# Elastic Modulus (Pa) 
E = 200*1e9

# Poissons Ratio 
v = 0.3

# Shear Modulus (Pa)
mu_ = E/(2*(1+v))

# Lame Modulus (Pa)
lambda_ = (v*E)/((1+v)*(1-2*v))



## Define required variables

tf = 2           #total time in seconds
dx = Lx/nx          #length of each control volume in the x-direction
dy = Ly/ny          #length of each control volume in the y-direction
dt = tf/2          #size of time steps
Sfx = dy            #area vector x component (Area of East and West Faces)
Sfy = dx            #area vector y component (Area of North and South Faces)

transient = False



## Define  position and time vectors

t = np.array(np.arange(0,tf, dt))        #time vector (could possibly use a list)
x = np.zeros((1,nx+2))   #position vector defining the center points of the control volumes in the x-direction.
x[0,nx+1] = Lx
x[0,1:nx+1] = np.arange(dx/2,Lx,dx)

t = np.array(np.arange(0,tf, dt))        #time vector (could possibly use a list)
y = np.zeros((1,ny+2))   #position vector defining the center points of the control volumes in the y-direction.
y[0,ny+1] = Ly
y[0,1:ny+1] = np.arange(dy/2,Ly,dy)



## Define required displacement matrices and b vector

U_new = np.zeros([(ny+2)*(nx+2),2])         #unknown displacements at t + 1    (Column 1 = x, Column2 = y)
U_old = np.zeros([(ny+2)*(nx+2),2])         #displacement at time t
U_old_old = np.zeros([(ny+2)*(nx+2),2])     #displacement at time t - 1

#rhs vector
b_x = np.zeros([(ny+2)*(nx+2),1])
b_y = np.zeros([(ny+2)*(nx+2),1])



class boundary_U:

    def __init__(self, boundaries, xy):

        if xy == "x":
            if boundaries[0] == "b":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = u_bottom
            if boundaries[0] == "t":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = u_top
            if boundaries[0] == "l":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = u_left
            if boundaries[0] == "r":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = u_right

        if xy == "y":
            if boundaries[0] == "b":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = v_bottom
            if boundaries[0] == "t":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = v_top
            if boundaries[0] == "l":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = v_left
            if boundaries[0] == "r":
                if BC_settings(boundaries[0]).fixed_displacement:
                    self.BC = v_right


S_N = Sfy = dx
S_S = Sfy = dx
S_E = Sfx = dy
S_W = Sfx = dy