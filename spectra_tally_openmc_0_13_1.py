import openmc

# MATERIALS


my_material = openmc.Material.from_(name='Concrete Portland')

mats = openmc.Materials([my_material])


# GEOMETRY

bound_dag_univ= openmc.DAGMCUniverse("dagmc.h5m").bounded_universe()

my_geometry = openmc.Geometry(root=bound_dag_univ)


# SIMULATION SETTINGS

# Instantiate a Settings object
sett = openmc.Settings()
sett.batches = 10
sett.inactive = 0 # the default is 10, which would be wasted computing for us
sett.particles = 1000
sett.run_mode = 'fixed source'

# Create a DT point source
source = openmc.Source()
source.space = openmc.stats.Point((0, 0, 0))
source.angle = openmc.stats.Isotropic()
source.energy = openmc.stats.Discrete([14e6], [1])
sett.source = source


# sets up filters for the tallies
neutron_particle_filter = openmc.ParticleFilter(['neutron'])
energy_filter = openmc.EnergyFilter.from_group_structure('VITAMIN-J-175')
material_filter = openmc.MaterialFilter(my_material) 

# create the tally
cell_spectra_tally = openmc.Tally(name='cell_spectra_tally')
cell_spectra_tally.scores = ['flux']
cell_spectra_tally.filters = [cell_filter, neutron_particle_filter, energy_filter]

tallies = openmc.Tallies([cell_spectra_tally])


# combine all the required parts to make a model
model = openmc.model.Model(my_geometry, mats, sett, tallies)

results_filename = model.run()

# open the results file
results = openmc.StatePoint(results_filename)

#extracts the tally values from the simulation results
cell_tally = results.get_tally(name='cell_spectra_tally')

import matplotlib.pyplot as plt

results = openmc.StatePoint(results_filename)
cell_tally = results.get_tally(name='cell_spectra_tally')
energy_filter = cell_tally.find_filter(filter_type=openmc.filter.EnergyFilter)

bin_boundaries = energy_filter.lethargy_bin_width()
flux = cell_tally.mean.flatten()
norm_flux = flux / bin_boundaries

plt.figure()
plt.step(energy_filter.values[:-1], norm_flux)
plt.xscale('log')
plt.yscale('log')
plt.ylable('Flux per unit lethargy [n/cm2-s]')
plt.show()
