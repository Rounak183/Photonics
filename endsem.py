import math
import meep as mp
from meep import mpb
import matplotlib

import matplotlib.pyplot as plt

# Determining the number of eigenstates computed at each k points.
num_bands=8

# k_points are the Bloch wavevectors we want to compute the bands at.
# Setting it to the corners of irreducible Brillouin zone.
k_points=[mp.Vector3(0,0,0),				# Gamma
		  mp.Vector3(0.5,0,0),			# X
		  mp.Vector3(0.5,0.5,0),		# M
		  mp.Vector3(0,0,0)]				# Gamma

# Computing bands at a lot of intermediate points to get a continuous band structure
k_points=mp.interpolate(8,k_points)

# Setting up geometric objects at the center of the lattice
geometry_slab= [mp.Block(mp.Vector3(3,3,mp.inf), center=mp.Vector3(0,0,0), material=mp.Medium(epsilon=12.25))]
geometry_cylinder = [mp.Cylinder(0.3,material=mp.Medium(epsilon=1),center=mp.Vector3(0,0,0))]
geometry = geometry_slab+geometry_cylinder

# Setting up the size of the lattice or the computational cell
geometry_lattice=mp.Lattice(size=mp.Vector3(1,1,0))

# Setting the resolution
resolution=64

# Creating a ModeSolver object - 
ms=mpb.ModeSolver(num_bands=num_bands,
				  k_points=k_points,
				  geometry=geometry,
				  geometry_lattice=geometry_lattice,
				  resolution=resolution)

# Printing and running
print("Square lattice of rods: TE bands")
ms.run_te(mpb.output_at_kpoint(mp.Vector3(0.5),mpb.output_hfield_z,mpb.output_dpwr))
te_freqs = ms.all_freqs
te_gaps = ms.gap_list

print(" TE BANDS: ", te_freqs)
print("TE GAPS: ", te_gaps)


# This outputs the z field components of the tm mode of the wave.
print("Square lattice of rods: TM bands")
ms.run_tm(mpb.output_efield_z)
tm_freqs = ms.all_freqs
tm_gaps = ms.gap_list

print(" TM BANDS: ", tm_freqs)
print("TM GAPS: ", tm_gaps)


# This outputs the magnetic field z components for the te_modes,
# at the point X, and the energy density power (D power).
ms.run_te(mpb.output_at_kpoint(mp.Vector3(0.5),mpb.output_hfield_z,mpb.output_dpwr))

import matplotlib.pyplot as plt

fig, ax = plt.subplots()
x = range(len(tm_freqs))
# Plot bands
# Scatter plot for multiple y values
for xz, tmz, tez in zip(x, tm_freqs, te_freqs):
    ax.scatter([xz]*len(tmz), tmz, color='blue')
    #ax.scatter([xz]*len(tez), tez, color='red', facecolors='none')
ax.plot(tm_freqs, color='blue')
#ax.plot(te_freqs, color='red')
ax.set_ylim([0, 1])
ax.set_xlim([x[0], x[-1]])

Plot gaps
for gap in tm_gaps:
    if gap[0] > 1:
        ax.fill_between(x, gap[1], gap[2], color='blue', alpha=0.2)

#for gap in te_gaps:
#    if gap[0] > 1:
#        ax.fill_between(x, gap[1], gap[2], color='red', alpha=0.2)


# Plot labels
ax.text(12, 0.04, 'TM bands', color='blue', size=15)
#ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

points_in_between = (len(tm_freqs) - 4) / 3
tick_locs = [i*points_in_between+i for i in range(4)]
tick_labs = ['Γ', 'X', 'M', 'Γ']
ax.set_xticks(tick_locs)
ax.set_xticklabels(tick_labs, size=16)
ax.set_ylabel('frequency (c/a)', size=16)
ax.set_xlabel('Wave Vector (k index)',size = 16)
ax.grid(True)

plt.show()