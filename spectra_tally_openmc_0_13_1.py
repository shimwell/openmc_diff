import matplotlib.pyplot as plt
import openmc

# MATERIALS

# defined from internal database
#todo put this back once merged in
# my_material = openmc.Material.from_library(name="Concrete, Portland")
# my_material.name = "mat1"  # renaming to match the contents of the dagmc h5m tags
my_material = openmc.Material(name="mat1")
my_material.add_element("H", 0.168759, percent_type="ao")
my_material.set_density("g/cm3", 2.3)


my_materials = openmc.Materials([my_material])


# GEOMETRY

# universe is automatically bounded with a correctly sized vacuum cell
bound_dag_univ = openmc.DAGMCUniverse("dagmc.h5m").bounded_universe()

my_geometry = openmc.Geometry(root=bound_dag_univ)


# SIMULATION SETTINGS

# Instantiate a Settings object with parameters
my_settings = openmc.Settings()#batches=10, particles=1000, run_mode="fixed source")
my_settings.batches=10
my_settings.particles=1000
my_settings.run_mode="fixed source"

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((0.5, 0.5, 0.5))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
my_settings.source = source

# sets up filters for the tallies
particle_filter = openmc.ParticleFilter(["neutron"])
energy_filter = openmc.EnergyFilter.from_group_structure("VITAMIN-J-175")
material_filter = openmc.MaterialFilter(my_material)

# create the tally
cell_spectra_tally = openmc.Tally(name="cell_spectra_tally")
cell_spectra_tally.scores = ["flux"]
cell_spectra_tally.filters = [material_filter, particle_filter, energy_filter]

my_tallies = openmc.Tallies([cell_spectra_tally])

# combine all the required parts to make a model
model = openmc.Model(my_geometry, my_materials, my_settings, my_tallies)

results_filename = model.run()

# open the results file
results = openmc.StatePoint(results_filename)

# extracts the tally values from the simulation results
cell_tally = results.get_tally(name="cell_spectra_tally")

energy_filter = cell_tally.find_filter(filter_type=openmc.filter.EnergyFilter)

# lethargy normalization values are now easily accessible
norm_flux = cell_tally.mean.flatten() / energy_filter.lethargy_bin_width

plt.figure()
plt.step(energy_filter.values[:-1], norm_flux)
plt.xscale("log")
plt.yscale("log")
plt.ylabel("Flux per unit lethargy [n/cm2-s]")
plt.xlabel("Energy [eV]")
plt.show()
