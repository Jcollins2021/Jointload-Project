import cv2
import numpy as np
from get_data import get_raw, get_magnitudes
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
    total = 0
    for i in data:
        total += np.argmin(i)
    return total / len(data)


def main_function(video, cropped_location, write_file, foot_data):
    less_than = 0
    more_than = 0

    written_lines = 0
    written = True
    angle_list = []

    count = 0

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
        angle_list.append(angle)

        count += 1

        # Write to file if 30 angles
        if count >= 30:
            # If new .mat file then need to readjust phase
            if written_lines % 100 == 0 and written == True:
                # Get the time stamp where we want the minimum to roughly be
                if (
                    len(
                        foot_data[
                            written_lines : min(written_lines + 100, len(foot_data))
                        ]
                    )
                    == 0
                ):
                    break
                time_stamp = find_average_min(
                    foot_data[written_lines : min(written_lines + 100, len(foot_data))]
                )
                time_stamp = math.floor(time_stamp / 1000 * 30)

                angle_min = np.argmax(angle_list)
                shift = time_stamp - angle_min
                if shift < 0:
                    angle_list = angle_list[np.abs(shift) :]
                    count = len(angle_list)
                    written = False
                elif shift > 0:
                    angle_list = angle_list[30 - shift :]
                    count = len(angle_list)
                    written = False
                else:
                    for n, i in enumerate(angle_list):
                        file.write(str(i))
                        if n < 29:
                            file.write(", ")
                    file.write("\n")
                    angle_list = []
                    written = True
                    count = 0
                    written_lines += 1
            else:
                for n, i in enumerate(angle_list):
                    file.write(str(i))
                    if n < 29:
                        file.write(", ")
                file.write("\n")
                angle_list = []
                written = True
                written_lines += 1
                count = 0

        if amount > 3:
            more_than += 1
        elif amount < 3:
            less_than += 1

    file.close()
    print(more_than)
    print(less_than)


# img = cv2.imread("./JointLoad Data/test2.png")
# locate_dots(img, [450, 950, 100, 600])


# Cropped location  Found just by testing
F1_cropped_location = [220, 480, 50, 280]
F2_cropped_location = [180, 400, 100, 300]
F3_cropped_location = [150, 380, 100, 300]


# video = cv2.VideoCapture("./JointLoad Data/Midium_F1.mov")
# video = cv2.VideoCapture("./JointLoad Data/Low_F2.mov")
video = cv2.VideoCapture("./JointLoad Data/High_F3.mov")

# foot_data, size = get_raw("Foot", "F1")
# foot_data, size = get_raw("Foot", "F2")
foot_data, size = get_raw("Foot", "F3")

# main_function(video, F1_cropped_location, "./JointLoad Data/F1_Angle.csv", foot_data)
# main_function(video, F2_cropped_location, "./JointLoad Data/F2_Angle.csv", foot_data)
main_function(video, F3_cropped_location, "./JointLoad Data/F3_Angle.csv", foot_data)
