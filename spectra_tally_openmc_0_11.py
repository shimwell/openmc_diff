import matplotlib.pyplot as plt
import numpy as np
import openmc

# MATERIALS

# user defined Portland Concrete
my_material = openmc.Material(name="mat1")
my_material.add_element("H", 0.168759, percent_type="ao")
my_material.add_element("C", 0.001416, percent_type="ao")
my_material.add_element("O", 0.562524, percent_type="ao")
my_material.add_element("Na", 0.011838, percent_type="ao")
my_material.add_element("Mg", 0.0014, percent_type="ao")
my_material.add_element("Al", 0.021354, percent_type="ao")
my_material.add_element("Si", 0.204115, percent_type="ao")
my_material.add_element("K", 0.005656, percent_type="ao")
my_material.add_element("Ca", 0.018674, percent_type="ao")
my_material.add_element("Fe", 0.004264, percent_type="ao")
my_material.set_density("g/cm3", 2.3)

my_materials = openmc.Materials([my_material])


# GEOMETRY

# makes use of the dagmc geometry
dag_univ = openmc.DAGMCUniverse("dagmc.h5m")

# creates an edge of universe boundary at a large radius
vac_surf = openmc.Sphere(r=10000, surface_id=9999, boundary_type="vacuum")

# specifies the region as below the universe boundary
region = -vac_surf

# creates a cell from the region and fills the cell with the dagmc geometry
containing_cell = openmc.Cell(cell_id=9999, region=region, fill=dag_univ)

my_geometry = openmc.Geometry(root=[containing_cell])


# SIMULATION SETTINGS

# Instantiate a Settings object
my_settings = openmc.Settings()
# TODO add once merged in
# my_settings = openmc.Settings(batches=10, particles=1000, run_mode="fixed source")
my_settings.batches = 10
my_settings.inactive = 0  # the default is 10
my_settings.particles = 1000
my_settings.run_mode = "fixed source"

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((0.5, 0.5, 0.5))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = source

VITAMIN_J_175_bins = [
    1.0000e-5, 1.0000e-1, 4.1399e-1, 5.3158e-1, 6.8256e-1, 8.7643e-1, 1.1253,
    1.4450, 1.8554, 2.3824, 3.0590, 3.9279, 5.0435, 6.4759, 8.3153, 1.0677e1,
    1.3710e1, 1.7604e1, 2.2603e1, 2.9023e1, 3.7266e1, 4.7851e1, 6.1442e1,
    7.8893e1, 1.0130e2, 1.3007e2, 1.6702e2, 2.1445e2, 2.7536e2, 3.5358e2,
    4.5400e2, 5.8295e2, 7.4852e2, 9.6112e2, 1.2341e3, 1.5846e3, 2.0347e3,
    2.2487e3, 2.4852e3, 2.6126e3, 2.7465e3, 3.0354e3, 3.3546e3, 3.7074e3,
    4.3074e3, 5.5308e3, 7.1017e3, 9.1188e3, 1.0595e4, 1.1709e4, 1.5034e4,
    1.9304e4, 2.1875e4, 2.3579e4, 2.4176e4, 2.4788e4, 2.6058e4, 2.7000e4,
    2.8501e4, 3.1828e4, 3.4307e4, 4.0868e4, 4.6309e4, 5.2475e4, 5.6562e4,
    6.7380e4, 7.2024e4, 7.9499e4, 8.2503e4, 8.6517e4, 9.8036e4, 1.1109e5,
    1.1679e5, 1.2277e5, 1.2907e5, 1.3569e5, 1.4264e5, 1.4996e5, 1.5764e5,
    1.6573e5, 1.7422e5, 1.8316e5, 1.9255e5, 2.0242e5, 2.1280e5, 2.2371e5,
    2.3518e5, 2.4724e5, 2.7324e5, 2.8725e5, 2.9452e5, 2.9721e5, 2.9849e5,
    3.0197e5, 3.3373e5, 3.6883e5, 3.8774e5, 4.0762e5, 4.5049e5, 4.9787e5,
    5.2340e5, 5.5023e5, 5.7844e5, 6.0810e5, 6.3928e5, 6.7206e5, 7.0651e5,
    7.4274e5, 7.8082e5, 8.2085e5, 8.6294e5, 9.0718e5, 9.6167e5, 1.0026e6,
    1.1080e6, 1.1648e6, 1.2246e6, 1.2874e6, 1.3534e6, 1.4227e6, 1.4957e6,
    1.5724e6, 1.6530e6, 1.7377e6, 1.8268e6, 1.9205e6, 2.0190e6, 2.1225e6,
    2.2313e6, 2.3069e6, 2.3457e6, 2.3653e6, 2.3851e6, 2.4660e6, 2.5924e6,
    2.7253e6, 2.8650e6, 3.0119e6, 3.1664e6, 3.3287e6, 3.6788e6, 4.0657e6,
    4.4933e6, 4.7237e6, 4.9658e6, 5.2205e6, 5.4881e6, 5.7695e6, 6.0653e6,
    6.3763e6, 6.5924e6, 6.7032e6, 7.0469e6, 7.4082e6, 7.7880e6, 8.1873e6,
    8.6071e6, 9.0484e6, 9.5123e6, 1.0000e7, 1.0513e7, 1.1052e7, 1.1618e7,
    1.2214e7, 1.2523e7, 1.2840e7, 1.3499e7, 1.3840e7, 1.4191e7, 1.4550e7,
    1.4918e7, 1.5683e7, 1.6487e7, 1.6905e7, 1.7332e7, 1.9640e7,
]

# sets up filters for the tallies
particle_filter = openmc.ParticleFilter(["neutron"])
energy_filter = openmc.EnergyFilter(values=VITAMIN_J_175_bins)
material_filter = openmc.MaterialFilter(my_material)

# create the tally
cell_spectra_tally = openmc.Tally(name="cell_spectra_tally")
cell_spectra_tally.scores = ["flux"]
cell_spectra_tally.filters = [material_filter, particle_filter, energy_filter]

my_tallies = openmc.Tallies([cell_spectra_tally])

# combine all the required parts to make a model
model = openmc.model.Model(my_geometry, my_materials, my_settings, my_tallies)

model.run()
# results filename is not returned but can be found from the batches
results_filename = f"statepoint.{my_settings.batches}.h5"

# open the results file
results = openmc.StatePoint(results_filename)

# extracts the tally values from the simulation results
cell_tally = results.get_tally(name="cell_spectra_tally")

energy_filter = cell_tally.find_filter(filter_type=openmc.filter.EnergyFilter)

# user must calculate bin widths
bin_norm_factor = np.log10(energy_filter.bins[:, 1] / energy_filter.bins[:, 0])
norm_flux = cell_tally.mean.flatten() / bin_norm_factor

plt.figure()
plt.step(energy_filter.values[:-1], norm_flux)
plt.xscale("log")
plt.yscale("log")
plt.ylabel("Flux per unit lethargy [n/cm2-s]")
plt.xlabel("Energy [eV]")
plt.show()
