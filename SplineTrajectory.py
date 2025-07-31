import numpy as np
from scipy.spatial.transform import Rotation as R
from Plot import plot_bending_points_with_directions

def SplineTrajectory(pos, radius = 10, dtheta = 10):

    PoseArray = np.array(pos)

    xyz_trj = [list(pos[0])]
    phi_trj = [[0]]
    xyzphi_trj = [xyz_trj[-1] + phi_trj[-1]]
    for i in range(len(pos)-2):
        u1 = (PoseArray[i+1] - PoseArray[i])/np.linalg.norm(PoseArray[i+1] - PoseArray[i])
        u2 = (PoseArray[i+2] - PoseArray[i+1])/np.linalg.norm(PoseArray[i+2] - PoseArray[i+1])
        u3 = (u2 - u1) / np.linalg.norm(u2 - u1)

        theta = np.arccos(u1 @ np.transpose(u2))
        x = radius / np.tan(theta/2)
        y = radius / np.sin(theta/2)

        Pn = PoseArray[i+1] + y*u3
        n = np.cross(u1, u2)/np.linalg.norm(np.cross(u1, u2))
        r = (PoseArray[i+1]-u1*x) - Pn

        for j in range(round(theta/(dtheta/180*np.pi))+1):
            rot = R.from_rotvec(n*(theta/round(theta/(dtheta/180*np.pi)))*j)
            rotm = rot.as_matrix()
            r_pos = rotm @ np.transpose(r)
            xyz_trj.append(list(r_pos + Pn))
            if j == 0:
                phi_trj.append(phi_trj[-1])
            else:
                phi_trj.append(list(phi_trj[-1] + theta/round(theta/(dtheta/180*np.pi)) * 180/np.pi ))

            xyzphi_trj.append(xyz_trj[-1] + phi_trj[-1])

    xyz_trj.append(list(pos[-1]))
    phi_trj.append(phi_trj[-1])
    xyzphi_trj.append(xyz_trj[-1] + phi_trj[-1])

    return xyzphi_trj