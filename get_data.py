import os
import scipy.io
import numpy as np


def get_raw(kind: str, test: str):

    # Ensure proper input
    if kind != "Jointload" and kind != "Foot":
        raise ValueError(f"Expected Jointload or Foot for kind instead got {kind}")
    if test != "F1" and test != "F2" and test != "F3":
        raise ValueError(f"Expected F1, F2 or F3 for test, instead got {test}")

    # Set path
    path = "./JointLoad Data/20240624-" + test + "_" + kind

    # Get data
    data = []
    data_size = []

    # Get what the data is called
    if kind == "Foot":
        arr_name = "A"
    else:
        arr_name = "D"

    for i in range(1, 19):
        loaded_data = scipy.io.loadmat(
            path + "/20240624-" + test + "_" + kind + "_" + str(i).zfill(2) + ".mat"
        )
        # Reshape data from 100000, 1 to 100000,
        pending_data = loaded_data[arr_name]
        pending_data = np.array(pending_data).reshape(len(pending_data))
        data_size.append(loaded_data["Length"][0][0])

        # Group data by 1 second intervals of 1000 samples discarding extra
        num_groups = data_size[i - 1] // 1000
        for j in range(num_groups):
            data.append(pending_data[j * 1000 : (j + 1) * 1000])

    # Get rid of the single element array
    return data, data_size


def get_magnitudes(kind: str, test: str, dataset=None):
    if dataset == None:
        # Ensure proper input
        if kind != "Jointload" and kind != "Foot":
            raise ValueError(f"Expected Jointload or Foot for kind instead got {kind}")
        if test != "F1" and test != "F2" and test != "F3":
            raise ValueError(f"Expected F1, F2 or F3 for test, instead got {test}")

    # Get raw data
    if dataset == None:
        data, data_size = get_raw(kind, test)
    else:
        # Should probably make sure dataset is 3d
        data = dataset

    # Get magnitude
    magnitudes = []
    for i in data:
        magnitudes.append((max(i) - min(i)))

    return magnitudes


def get_features(kind: str, test: str):
    # Ensure proper input
    if kind != "Jointload" and kind != "Foot":
        raise ValueError(f"Expected Jointload or Foot for kind instead got {kind}")
    if test != "F1" and test != "F2" and test != "F3":
        raise ValueError(f"Expected F1, F2 or F3 for test, instead got {test}")

    # Get raw data
    data, data_size = get_raw(kind, test)
    for i in data:
        for j in i:
            pass


# raw, size = get_raw("Foot", "F3")
# print(len(raw[0][0]))
# print(size)
# joint_mags = get_magnitudes("Jointload", "F3")
# print(len(joint_mags))
# foot_mags = get_magnitudes("Foot", "F2")


# print((joint_mags[0][0] + 0.7367) / 63.981)
# print(foot_mags[0][0] * 112.41)
# print(foot_mags[0][0])
# get_features("Jointload", "F1")
