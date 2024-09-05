import scipy.io

F1_Foot = scipy.io.loadmat("./JointLoad Data/20240624-F1_Foot/20240624-F1_Foot_02.mat")
F1_Jointload = scipy.io.loadmat(
    "./JointLoad Data/20240624-F1_Jointload/20240624-F1_Jointload_02.mat"
)

# print(F1_Jointload)
print(F1_Foot)
