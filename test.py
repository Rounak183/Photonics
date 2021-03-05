import math
import meep as mp
from meep import mpb

num_bands=50

geometry_lattice = mp.Lattice(size=mp.Vector3(5, 5))

geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]
geometry = mp.geometric_objects_lattice_duplicates(geometry_lattice, geometry)

geometry.append(mp.Cylinder(0.2, material=mp.air))

k_points = [mp.Vector3(0.5, 0.5)]

k_points = mp.interpolate(4,k_points)

resolution = 16

ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)

#mpb.output_efield_z(ms, 25)

#ms.get_efield(25)  # compute the D field for band 25
#ms.compute_field_energy()  # compute the energy density from D
#c = mp.Cylinder(1.0, material=mp.air)
#print("energy in cylinder: {}".format(ms.compute_energy_in_objects([c])))

#ms.num_bands = 1  # only need to compute a single band, now!
#ms.target_freq = (0.2812 + 0.4174) / 2
#ms.tolerance = 1e-8

ms.run_tm(mpb.output_at_kpoint(mp.Vector3(-1./3, 1./3), mpb.fix_efield_phase,
          mpb.output_efield_z))
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
ax.text(12, 0.04, 'TM bands', color='blue', size=15)
ax.text(13.05, 0.235, 'TE bands', color='red', size=15)

points_in_between = (len(tm_freqs) - 4) / 3
tick_locs = [i*points_in_between+i for i in range(4)]
tick_labs = ['Γ', 'X', 'M', 'Γ']
ax.set_xticks(tick_locs)
ax.set_xticklabels(tick_labs, size=16)
ax.set_ylabel('frequency (c/a)', size=16)
ax.grid(True)

plt.show()