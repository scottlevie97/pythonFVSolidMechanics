import numpy as np

#### Geometry ####
Lx = 2 
Ly = .1 


#### Mesh Grading ####
nx = 80      
ny = 8


#### Boundary Conditions ####
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

tr_right_x = 0       #u boundary condition at the right boundary
tr_right_y = -1e6   #v boundary condition at the right boundary

tr_top_x = 0    #u boundary condition at the top boundary
tr_top_y = 0       #v boundary condition at the top boundary

tr_bottom_x = 0    #u boundary condition at the bottom boundary 
tr_bottom_y = 0  #v boundary condition at the bottom boundary

u_left = 0
v_left = 0


#### Mechanical Properties #####

rho = 8050 #density of steel in kg/m^3

# Elastic Modulus (Pa) 
E = 200*1e9

# Poissons Ratio 
v = 0.3

# Shear Modulus (Pa)
mu_ = E/(2*(1+v))

# Lame Modulus (Pa)
lambda_ = (v*E)/((1+v)*(1-2*v))


#### Time controls ####

# Transient switch
transient = False

# Total time
tf = 1    

# Timestep size
dt = 0.01


# *********************************** #

#### Needs to be moved ####

# def saveDirectory(nx, ny):
#     return "Solution_rightTraction/x_" + str(nx) + "_y_" + str(ny)

# def saveArray (name, array): 

#     pd.DataFrame(array).to_csv(saveDirectory(nx, ny) + "/" + name + ".csv", index=False, header=None)


#### Write settings to another python file####

my_file = open("index_and_direction.py")
string_list = my_file.readlines()
my_file.close()

string_list[4] = "\tnx = " + str(nx) + "\n"
string_list[5] = "\tny = " + str(ny) + "\n"

my_file = open("index_and_direction.py", "w")
my_file.writelines(string_list)
my_file.close()

from index_and_direction import dim

print(dim().nx)
print(dim().ny)

#### Create position and time vectors ####

t = np.array(np.arange(0,tf, dt))

#length of each cell in the x-direction
dx = Lx/nx 
#length of each cell in the x-direction        
dy = Ly/ny          

# Position vector x
x = np.zeros((1,nx+2))  
x[0,nx+1] = Lx
x[0,1:nx+1] = np.arange(dx/2,Lx,dx)

# Position vector y
y = np.zeros((1,ny+2))  
y[0,1:ny+1] = np.arange(dy/2,Ly,dy)


#### Initialise U fields #### 

U_new = np.zeros([(ny)*(nx),2])         #unknown displacements at t + 1    (Column 1 = x, Column2 = y)
U_old = np.zeros([(ny)*(nx),2])         #displacement at time t
U_old_old = np.zeros([(ny)*(nx),2])     #displacement at time t - 1


#### Initialise b matrices ####

b_x = np.zeros([(ny)*(nx),1])
b_y = np.zeros([(ny)*(nx),1])

#### Surface area vectors ####

Sfx = dy            #area vector x component (Area of East and West Faces)
Sfy = dx            #area vector y component (Area of North and South Faces)

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
