import math
import meep as mp
from meep import mpb
import matplotlib
#matplotlib.use('Agg')

import matplotlib.pyplot as plt


# Determining the number of eigenstates computed at each k points.
num_bands=50

# k_points=Bloch wavevectors we want to compute the bands at.
# Setting it to the corners of irreducible Brillouin zone.
k_points=[mp.Vector3(),				# Gamma
		  mp.Vector3(0.5),			# X
		  mp.Vector3(0.5,0.5),		# M
		  mp.Vector3()]				# Gamma

# Computing bands at a lot of intermediate points to get a continuous band structure
k_points=mp.interpolate(4,k_points)

# Setting up the size of the computational cells
geometry_lattice=mp.Lattice(size=mp.Vector3(1,1))

# Setting up geometric objects at the center of the lattice
geometry=[mp.Cylinder(0.2,material=mp.Medium(epsilon=12))]
geometry = mp.geometric_objects_lattice_duplicates(geometry_lattice, geometry)


# Setting the resolution
resolution=32

# Creating a ModeSolver object - 
ms=mpb.ModeSolver(num_bands=num_bands,
				  k_points=k_points,
				  geometry=geometry,
				  geometry_lattice=geometry_lattice,
				  resolution=resolution)

# Printing and running
print("Square lattice of rods: TE bands")
ms.run_te()

# This outputs the z field components of the tm mode of the wave.
ms.run_tm(mpb.output_efield_z)

# This outputs the magnetic field z components for the te_modes,
# at the point X, and the energy density power (D power).
ms.run_te(mpb.output_at_kpoint(mp.Vector3(0.5),mpb.output_hfield_z,mpb.output_dpwr))

# sample points - 

ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list


ms.run_tm()
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
print("tm gaps: ", tm_gaps)
print("freqs: ", tm_freqs)

tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list
ms.run_te()
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

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