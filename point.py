import math
import meep as mp
from meep import mpb
import matplotlib
import matplotlib.pyplot as plt

geometry_lattice = mp.Lattice(size=mp.Vector3(10, 10))
geometry = [mp.Cylinder(0.2, material=mp.Medium(epsilon=12))]
geometry = mp.geometric_objects_lattice_duplicates(geometry_lattice, geometry)

for i in range(10):
            geometry.append(mp.Cylinder(0.2, center=mp.Vector3(1+i), material=mp.air))
            geometry.append(mp.Cylinder(0.2, center=mp.Vector3(-(1+i)), material=mp.air))

#geometry.append(mp.Cylinder(0.2, material=mp.air))
resolution = 16
k_points = [mp.Vector3(0.5, 0.5)]
num_bands = 50



ms = mpb.ModeSolver(num_bands=num_bands,
                    k_points=k_points,
                    geometry=geometry,
                    geometry_lattice=geometry_lattice,
                    resolution=resolution)
ms.run_tm()
mpb.output_efield_z(ms, 25)

ms.compute_field_energy()  # compute the energy density from D
c = mp.Cylinder(1.0, material=mp.air)
print("energy in cylinder: {}".format(ms.compute_energy_in_objects([c])))

tm_gaps = ms.gap_list
print("gaps", tm_gaps)


eps = ms.get_epsilon()
plt.imshow(eps.T, interpolation='spline36', cmap='binary')
plt.axis('off')
plt.savefig("pic.png")