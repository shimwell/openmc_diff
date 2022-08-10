import matplotlib.pyplot as plt
import openmc

# MATERIALS

# defined from internal database
my_material = openmc.Material.from_library(name="Concrete, Portland")
my_material.name = "mat1"  # renaming to match the contents of the dagmc h5m tags

my_materials = openmc.Materials([my_material])


# GEOMETRY

bound_dag_univ = openmc.DAGMCUniverse("dagmc.h5m", auto_geom_ids=True).bounded_universe()
# todo once in the develop branch
# bound_dag_univ = openmc.DAGMCUniverse("dagmc.h5m", ).bounded_universe()

my_geometry = openmc.Geometry(root=bound_dag_univ)


# SIMULATION SETTINGS

# Instantiate a Settings object
my_settings = openmc.Settings()
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

# sets up filters for the tallies
neutron_particle_filter = openmc.ParticleFilter(["neutron"])
energy_filter = openmc.EnergyFilter.from_group_structure("VITAMIN-J-175")
material_filter = openmc.MaterialFilter(my_material)

# create the tally
cell_spectra_tally = openmc.Tally(name="cell_spectra_tally")
cell_spectra_tally.scores = ["flux"]
cell_spectra_tally.filters = [
    material_filter,
    neutron_particle_filter,
    energy_filter,
]

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
plt.ylabel("Energy [eV]")
plt.show()
