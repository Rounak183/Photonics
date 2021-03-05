import math
import meep as mp
from meep import mpb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Setting the lattice lattice constant 
a=0.19196678

# Setting the geometry lattice to be 20*lambda
geometry_lattice = mp.Lattice(size=mp.Vector3(11, 11))

# Setting our rods to be of radius 0.2*lattice_constant
geometry = [mp.Cylinder(0.2*a, material=mp.Medium(epsilon=12))]

# Duplicating our rods through the entire geometric lattice taken
geometry = mp.geometric_objects_lattice_duplicates(geometry_lattice, geometry)

# Creating a line defect through a for loop. This has the same radius=0.2*a.
for i in range(11):
            geometry.append(mp.Cylinder(0.2*a, center=mp.Vector3(1+i), material=mp.air))
            geometry.append(mp.Cylinder(0.2*a, center=mp.Vector3(-(1+i)), material=mp.air))

# Setting Resolution
resolution = 16

# Setting our k-points
k_points = [mp.Vector3(0.5, 0.5)]

# Setting number of eigenstates to calculate our at the wavevectors
num_bands = 100

# Interpolating the k-points
k_points=mp.interpolate(4,k_points)

# Creating a mode solver object
ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

# Code for plotting the obtained data after simulation
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = range(len(tm_freqs))
# Plot bands
# Scatter plot for multiple y values, see https://stackoverflow.com/a/34280815/2261298
for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
    ax.scatter([xz]*len(tmz), tmz, color='blue')
    ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
ax.plot(tm_freqs, color='blue')
ax.plot(te_freqs, color='red')
ax.set_ylim([0, 1])
ax.set_xlim([x[0], x[-1]])

# Plot gaps
for gap in tm_gaps:
    if gap[0] > 1:
        ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)

for gap in te_gaps:
    if gap[0] > 1:
        ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)


# Plot labels
#ax.text(12, 0.04, 'TM bands', color='blue', size=15)
ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

points_in_between = (len(tm_freqs) - 4) / 3
tick_locs = [i*points_in_between+i for i in range(4)]
tick_labs = ['Γ', 'X', 'M', 'Γ']
ax.set_xticks(tick_locs)
ax.set_xticklabels(tick_labs, size=16)
ax.set_ylabel('frequency (c/a)', size=16)
ax.grid(True)

plt.show()