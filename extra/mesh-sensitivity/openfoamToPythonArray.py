import numpy as np


def openfoamToPythonArray(filepath, iteration, file, size):

    filepath = str(filepath) + "/" + str(iteration) + "/" + str(file)

    my_file = open(filepath)
    string_list = my_file.readlines()

    for i in np.arange(0, len(string_list)):
        if string_list[i] == str(size) + "\n":
            startindex = i+2
        if string_list[i] == ";\n":
            endindex = i-1
            break

    string_list = string_list[startindex:endindex]

    i = 0
    for i in range(i, len(string_list)):
        string_list[i] = string_list[i].replace("(", "")
        string_list[i] = string_list[i].replace(")", "")
        string_list[i] = string_list[i].split()
    arr = np.array(string_list)
    arr = arr.astype(np.float64)

    # x = arr[:,0]
    # y = arr[:, 1]
    # z = arr[:, 2]

    return arr


def openfoamToPythonArray(filepath, iteration, file, size):

    filepath = str(filepath) + "/" + str(iteration) + "/" + str(file)

    my_file = open(filepath)
    string_list = my_file.readlines()

    for i in np.arange(0, len(string_list)):
        if string_list[i] == str(size) + "\n":
            startindex = i+2
        if string_list[i] == ";\n":
            endindex = i-1
            break

    string_list = string_list[startindex:endindex]

    i = 0
    for i in range(i, len(string_list)):
        string_list[i] = string_list[i].replace("(", "")
        string_list[i] = string_list[i].replace(")", "")
        string_list[i] = string_list[i].split()
    arr = np.array(string_list)
    arr = arr.astype(np.float64)

    # x = arr[:,0]
    # y = arr[:, 1]
    # z = arr[:, 2]

    return arr
