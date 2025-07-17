import cv2
import numpy as np
from main.get_data import get_raw, get_magnitudes
import math

# Video is at 30 fps


# Feed image in to find the x and y coordinates of the red dots
# Code used from https://stackoverflow.com/questions/61769416/red-dot-coordinates-detection
def locate_dots(frame, crop):

    cropped_frame = frame[crop[2] : crop[3], crop[0] : crop[1]]

    # Apply median blur
    blur = cv2.medianBlur(cropped_frame, 9)

    # Convert to hsv
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # Mask code from https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
    # lower mask (0-10)
    lower_red = np.array([0, 100, 100])
    upper_red = np.array([10, 200, 200])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)

    # upper mask (170-180)
    lower_red = np.array([170, 100, 100])
    upper_red = np.array([180, 200, 200])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)

    # join my masks
    mask = mask0 + mask1

    connectivity = 8
    # Perform the operation
    output = cv2.connectedComponentsWithStats(
        mask, connectivity=connectivity, ltype=cv2.CV_32S
    )
    # Get the results

    num_labels = output[0] - 1
    centroids = output[3][1:]

    # # print results
    # print("number of dots, should be 3:", num_labels)
    # print("array of dot center coordinates:", centroids)
    # for center in centroids:
    #     cv2.circle(
    #         frame,
    #         (int(center[0] + crop[0]), int(center[1] + crop[2])),
    #         5,
    #         (0, 255, 0),
    #         -1,
    #     )
    # cv2.rectangle(frame, (crop[0], crop[2]), (crop[1], crop[3]), (255, 0, 0), 2)
    # cv2.imshow("Frame", frame)
    # cv2.waitKey()

    return centroids, num_labels


def find_average_min(data):
    if len(data) == 0:
        return 0
    total = 0
    for i in data:
        minimum = np.where(i == min(i))[0]
        total += minimum[len(minimum) // 2]
    return total / len(data)
    # total = 0
    # total_count = 0
    # for i in data:
    #     sort = np.argsort(i)
    #     total += sum(sort[: math.floor(len(sort) / 15)])
    #     total_count += math.floor(len(sort) / 15)
    # return total / total_count


def find_average_max(data):
    if len(data) == 0:
        print("Here")
        return 0
    total = 0
    # total_count = 0
    for i in range(min(len(data) // 100, 100)):
        total += np.argmax(data[i * 30 : min((i + 1) * 30, len(data))])
        # sort = np.argsort(data[i * 30 : min((i + 1) * 30, len(data))])
        # total += sum(sort[-1 * math.floor(len(sort) / 15) :])
        # total_count += math.floor(len(sort) / 15)
    # return total / total_count
    return total / math.ceil(len(data) / 100)


def main_function(video, cropped_location, write_file, foot_data, shift):
    less_than = 0
    more_than = 0

    angle_list = []

    file = open(write_file, mode="w", newline="")

    prev_centroids = [[0, 0], [0, 0], [0, 0]]
    while video.isOpened():
        ret, frame = video.read()
        # Ret is if it was successful or not
        if not ret:
            break

        centroids, amount = locate_dots(frame, cropped_location)

        # Since sometimes there are not three dots located we will just take previous value
        if amount != 3:
            centroids = prev_centroids
        else:
            prev_centroids = centroids

        # Centroids are sorted by Y coordinate and are labeled inside our crop
        # Get angle

        v1 = [centroids[0][0] - centroids[1][0], centroids[0][1] - centroids[1][1]]
        v2 = [centroids[2][0] - centroids[1][0], centroids[2][1] - centroids[1][1]]

        angle = np.degrees(
            np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)))
        )

        file.write(str(angle))
        file.write(",")
        # angle_list.append(angle)

        if amount > 3:
            more_than += 1
        elif amount < 3:
            less_than += 1

    # print(len(angle_list))
    count = 0
    written = 0

    # for sh in shift:
    #     if len(foot_data) <= written:
    #         break
    #     # foot_min_avg = find_average_min(
    #     #     foot_data[written : min(written + 100, len(foot_data))]
    #     # )
    #     # angle_max_avg = find_average_max(
    #     #     angle_list[count : min(count + 3000, len(angle_list))]
    #     # )
    #     # foot_min_avg = math.floor(foot_min_avg / 1000 * 30)

    #     # shift = foot_min_avg - math.floor(angle_max_avg)
    #     print("Hi")
    #     # print(angle_max_avg)
    #     print(sh)
    #     # print(foot_min_avg)
    #     print(count)

    #     # if shift < 0:
    #     #     count += abs(shift)
    #     # elif shift > 0:
    #     count += 30 - abs(sh)

    #     for i in range(100):
    #         # Basically just write them as long as there is one that corresponds and repeat
    #         for j in range(30):
    #             if count >= len(angle_list):
    #                 break
    #             if j != 0:
    #                 file.write(" ")
    #             file.write(str(angle_list[count]))
    #             count += 1
    #             if j < 29:
    #                 file.write(",")
    #         written += 1
    #         file.write("\n")
    #     # break

    file.close()
    print(more_than)
    print(less_than)


# img = cv2.imread("./JointLoad Data/test2.png")
# locate_dots(img, [450, 950, 100, 600])


# Cropped location  Found just by testing
F1_cropped_location = [220, 480, 50, 280]
F2_cropped_location = [180, 400, 100, 300]
F3_cropped_location = [150, 380, 100, 300]

# Number of frames to shift for each mat file to align them
F1_shift = [27, 9, 9, 9, 12, 6, 11, 9, 7, 9, 12, 9, 6, 12, 6, 9, 10, 8]
F2_shift = [6, 8, 9, 6, 7, 14, 8, 6, 12, 5, 10, 13, 8, 9, 8, 9, 8, 9]
F3_shift = [13, 8, 9, 7, 9, 9, 8, 8, 7, 9, 12, 10, 9, 8, 10, 8, 10, 12]


# video = cv2.VideoCapture("./JointLoad Data/Midium_F1.mov")
# video = cv2.VideoCapture("./JointLoad Data/Low_F2.mov")
video = cv2.VideoCapture("./JointLoad Data/High_F3.mov")
# video = cv2.VideoCapture("./JointLoad Data/trimmedLow_F2.mov")

# foot_data, size = get_raw("Foot", "F1")
# foot_data, size = get_raw("Foot", "F2")
foot_data, size = get_raw("Foot", "F3")

# main_function(
#     video, F1_cropped_location, "./JointLoad Data/F1_Angle.csv", foot_data, F1_shift
# )
# main_function(
#     video, F2_cropped_location, "./JointLoad Data/F2_Angle.csv", foot_data, F2_shift
# )
# main_function(
#     video, F3_cropped_location, "./JointLoad Data/F3_Angle.csv", foot_data, F3_shift
# )


# main_function(
#     video,
#     F1_cropped_location,
#     "./JointLoad Data/F1_Angle_Entire.csv",
#     foot_data,
#     F1_shift,
# )
# main_function(
#     video,
#     F2_cropped_location,
#     "./JointLoad Data/F2_Angle_Entire.csv",
#     foot_data,
#     F2_shift,
# )
main_function(
    video,
    F3_cropped_location,
    "./JointLoad Data/F3_Angle_Entire.csv",
    foot_data,
    F3_shift,
)
