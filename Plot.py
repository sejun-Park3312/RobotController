import numpy as np
import matplotlib.pyplot as plt

def plot_bending_points_with_directions(xyz_trj, phi_trj, scale=0.05):
    """
    xyz_trj: (N, 3) trajectory points
    phi_trj: (N,) angles in radians (rotation about z-axis)
    scale: size of direction arrows
    """
    xyz_trj = np.array(xyz_trj)
    phi_trj = np.array(phi_trj)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(xyz_trj[:, 0], xyz_trj[:, 1], xyz_trj[:, 2], label='Trajectory', color='blue')

    # Initial direction vector
    init_dir = np.array([1, 0, 0])  # x-axis direction

    for i in range(len(xyz_trj)):
        phi = phi_trj[i]
        # Z-axis rotation matrix
        Rz = np.array([
            [np.cos(phi), -np.sin(phi), 0],
            [np.sin(phi),  np.cos(phi), 0],
            [0,            0,           1]
        ])
        dir_vec = Rz @ init_dir
        p = xyz_trj[i]
        ax.quiver(p[0], p[1], p[2],
                  dir_vec[0], dir_vec[1], dir_vec[2],
                  length=scale, color='red', normalize=True)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Trajectory with Tangent Directions (Z-axis Rotated)')
    plt.legend()
    plt.show()

pos = [[0,0,0], [0,-25,0], [40,-25,0], [40,25,0], [-40,25,0]]
rel = [[0,-25,0], [40,0,0], [0,50,0], [-80,0,0]]