import numpy as np
from main.get_data import get_raw, get_magnitudes
import math
import csv
import matplotlib.pyplot as plt

# Shift the data to align videos and .mat files

plot_number = 17

F1_shift = [27, 9, 9, 9, 12, 6, 11, 9, 7, 9, 12, 9, 4, 12, 8, 8, 9, 10]
F2_shift = [4, 6, 9, 9, 8, 9, 10, 9, 8, 10, 9, 10, 10, 8, 8, 10, 7, 8]
F3_shift = [11, 10, 8, 8, 8, 8, 9, 8, 9, 9, 8, 11, 10, 8, 10, 10, 8, 12]

F1_foot_data, F1_size = get_raw("Foot", "F1")
F2_foot_data, F2_size = get_raw("Foot", "F2")
F3_foot_data, F3_size = get_raw("Foot", "F3")


def main_function(foot_data, file, write_file, shift, foot_size, plot_number):
    data = []
    with open(file, mode="r", newline="") as csvfile:
        read = csv.reader(csvfile)
        data = list(read)
        data = data[0]

    cur_index = 0
    written = 0
    with open(write_file, mode="w", newline="") as csvfile:
        for i in shift:
            if len(foot_data) <= written:
                break

            cur_index += 30 - abs(i)

            for k in range(100):
                # Basically just write them as long as there is one that corresponds and repeat
                for j in range(30):
                    if cur_index >= len(data):
                        break
                    if j != 0:
                        csvfile.write(" ")
                    csvfile.write(str(data[cur_index]))
                    cur_index += 1
                    if j < 29:
                        csvfile.write(",")
                written += 1
                csvfile.write("\n")

    index_num = 0
    count = 0
    for i in shift:
        index_num += 30 - abs(i)
        count += 1
        if count > plot_number:
            break
        else:
            index_num += 30 * 100

    fig, ax1 = plt.subplots()
    ax1.set_title("F1 Angle And Jointload Raw vs Time (Last Entry)")
    color = "tab:red"
    ax1.set_xlabel("Time (ms)")
    ax1.set_ylabel("Raw Value", color=color)
    ax1.plot(np.arange(0, 1000), foot_data[plot_number * 100], color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

    color = "tab:blue"
    ax2.set_ylabel(
        "Angle (Degrees)", color=color
    )  # we already handled the x-label with ax1
    ax2.plot(
        np.linspace(0, 1000, 30),
        list(map(float, data[index_num : index_num + 30])),
        color=color,
    )
    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


main_function(
    F1_foot_data,
    "./JointLoad Data/F1_Angle_Entire.csv",
    "./JointLoad Data/F1_Angle.csv",
    F1_shift,
    F1_size,
    plot_number,
)

# main_function(
#     F2_foot_data,
#     "./JointLoad Data/F2_Angle_Entire.csv",
#     "./JointLoad Data/F2_Angle.csv",
#     F2_shift,
#     F2_size,
#     plot_number,
# )

# main_function(
#     F3_foot_data,
#     "./JointLoad Data/F3_Angle_Entire.csv",
#     "./JointLoad Data/F3_Angle.csv",
#     F3_shift,
#     F3_size,
#     plot_number,
# )
