import numpy as np
from functions.dim import dim
from matplotlib import pyplot as plt
import pandas as pd


def writeDimensions(nx, ny, Lx, Ly):

    my_file = open("functions/dim.py")
    string_list = my_file.readlines()
    my_file.close()

    string_list[2] = "\tnx = " + str(nx) + "\n"
    string_list[3] = "\tny = " + str(ny) + "\n"
    string_list[4] = "\tLx = " + str(Lx) + "\n"
    string_list[5] = "\tLy = " + str(Ly) + "\n"

    my_file = open("functions/dim.py", "w")
    my_file.writelines(string_list)
    my_file.close()


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

        self.dx = dim().dx
        self.dy = dim().dy

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


class cell_index(dim):

    bottom_left_corner_val = 0
    bottom_right_corner_val = dim().nx - 1
    top_left_corner_val = (dim().nx) * (dim().ny) - dim().nx
    top_right_corner_val = (dim().nx) * (dim().ny) - 1

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


class displacement(cell_index, dim):

    # add a statement using indexes

    def __init__(self, k, U_previous, direction):

        self.P = U_previous[k, direction]

        if k > cell_index().bottom_right_corner_val:
            self.S = U_previous[k - dim().nx, direction]

        if k < cell_index().top_left_corner_val:
            self.N = U_previous[k + dim().nx, direction]

        if (k % dim().nx != 0):
            self.W = U_previous[k - 1, direction]

        if (k % dim().nx != dim().nx - 1):
            self.E = U_previous[k + 1, direction]

        if (k > cell_index().bottom_left_corner_val) & (k % dim().nx != dim().nx - 1):
            self.SE = U_previous[k - dim().nx + 1, direction]

        if (k > cell_index().bottom_left_corner_val) & (k % dim().nx != 0):
            self.SW = U_previous[k - dim().nx - 1, direction]

        if (k < cell_index().top_left_corner_val) & (k % dim().nx != dim().nx - 1):
            self.NE = U_previous[k + dim().nx + 1, direction]

        if (k < cell_index().top_left_corner_val) & (k % dim().nx != 0):
            self.NW = U_previous[k + dim().nx - 1, direction]


def visualise_mesh(Lx, Ly, nx, ny):

    dy = Ly/ny
    dx = Lx/nx
    # position vector defining the center points of the control volumes in the $x$-direction.
    x = np.zeros((1, nx+2))
    x[0, nx+1] = Lx
    x[0, 1:nx+1] = np.arange(dx/2, Lx, dx)

    # position vector defining the center points of the control volumes in the $y$-direction.
    y = np.zeros((1, ny+2))
    y[0, ny+1] = Ly
    y[0, 1:ny+1] = np.arange(dy/2, Ly, dy)

    dispx, dispy = np.meshgrid(x, y)

    x_cells = x[0, 1:len(x[0, :])-1]
    y_cells = y[0, 1:len(y[0, :])-1]

    dispx_cells, dispy_cells = np.meshgrid(x_cells, y_cells)

    labels = np.arange(0, nx*ny, 1)

    fig = plt.figure(figsize=(10*(Lx/Ly), 10))
    ax = fig.add_subplot(111)
    ax.set_facecolor('lightgrey')

    f1 = 20
    f2 = 15

    plt.xticks(np.arange(0, Lx+1, Lx/nx), fontsize=f2)
    plt.yticks(np.arange(0, Ly+1, Ly/ny), fontsize=f2)
    plt.xlim(0, Lx)
    plt.ylim(0, Ly)
    plt.xlabel("x (m)", fontsize=f2)
    plt.ylabel("y (m)", fontsize=f2)

    plt.grid(linestyle="-", color="black", linewidth=2)

    for axis in ['top', 'bottom', 'left', 'right']:
        ax.axes.spines[axis].set_linewidth(3)

    plt.scatter(dispx_cells, dispy_cells, s=30, color="red", clip_on=False)

    dispx_cells_new = dispx_cells.reshape(
        len(dispx_cells[0, :])*len(dispy_cells), 1)
    dispy_cells_new = dispy_cells.reshape(
        len(dispx_cells[0, :])*len(dispy_cells), 1)

    for i in labels:
        plt.annotate(str(i), xy=(dispx_cells_new[i][0], dispy_cells_new[i][0]), size=f1,
                     horizontalalignment='left', verticalalignment='bottom',  textcoords='offset points', xytext=(2, 2))

    # plt.annotate(str(0), xy=(dispx_new[0][0],dispy_new[0][0]))

    plt.show()


def visualiseInternalCells(Lx, Ly, NX, NY):

    print("Make sure you write dimesnions using writeDimensions(nx, ny)")

    no_boundary_index = np.array([])

    print(Lx, Ly, NX, NY)

    for k in np.arange(0, (NX+2)*(NY+2)):
        if cell_index().no_boundary(k):
            no_boundary_index = np.append(no_boundary_index, k)

    dy = Ly/NY
    dx = Lx/NX
    # position vector defining the center points of the control volumes in the $x$-direction.
    x = np.zeros((1, NX+2))
    x[0, NX+1] = Lx
    x[0, 1:NX+1] = np.arange(dx/2, Lx, dx)

    # position vector defining the center points of the control volumes in the $y$-direction.
    y = np.zeros((1, NY+2))
    y[0, NY+1] = Ly
    y[0, 1:NY+1] = np.arange(dy/2, Ly, dy)

    dispx, dispy = np.meshgrid(x, y)

    labels = np.arange(0, (NX+2)*(NY+2), 1)

    plt.figure(figsize=(10, 10*(Ly/Lx)))
    plt.xticks(np.arange(0, Lx+1, Lx/NX))
    plt.yticks(np.arange(0, Ly+1, Ly/NY))
    plt.xlabel("x (m)")
    plt.ylabel("y (m)")
    plt.xlim(0, Lx)
    plt.ylim(0, Ly)

    plt.rc('grid', linestyle="--", color='black')
    plt.grid(True)
    plt.rc('grid', linestyle="--", color='black')
    plt.scatter(dispx, dispy, s=10)

    # print((dispx))
    # print((dispy))

    dispx_new = dispx.reshape(len(dispx)*len(dispy[0, :]), 1)
    dispy_new = dispy.reshape(len(dispx)*len(dispy[0, :]), 1)

    for i in no_boundary_index:
        plt.scatter(dispx_new[int(i)], dispy_new[int(i)], s=60,  c="red")

    for i in labels:
        plt.annotate(str(i), xy=(dispx_new[i][0], dispy_new[i][0]), size=12)

    plt.title("Visualising Cells with no Boundaries\n", size=25)
    plt.show()


def printVar(var):

    print(str(var) + ":")
    print(var)


def saveArray(name, array):

    pd.DataFrame(array).to_csv("Solution/" + name +
                               ".csv", index=False, header=None)


def initialise_U_field(nx, ny):

    # Create an zero array for the u and v values for each point
    U = np.zeros([nx*ny, 2])

    return U
