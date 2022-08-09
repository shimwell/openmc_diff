import openmc

# MATERIALS

my_material = openmc.Material(name='water')
my_material.add_element('H', 1, percent_type='ao')
my_material.add_element('O', 2, percent_type='ao')
my_material.set_density('g/cm3', 1)

mats = openmc.Materials([my_material])


# GEOMETRY

# surfaces
vessel_inner_surface = openmc.Sphere(r=500)
vessel_rear_surface = openmc.Sphere(r=530)
# Currently it is not possible to tally on boundary_type='vacuum' surfaces
outer_surface = openmc.Sphere(r=550, boundary_type='vacuum')

# cells
inner_vessel_cell = openmc.Cell(region=-vessel_inner_surface)
# inner_vessel_cell is filled with a void / vacuum by default

blanket_cell = openmc.Cell(region=-vessel_rear_surface & +vessel_inner_surface)
blanket_cell.fill = my_material

outer_vessel_cell = openmc.Cell(region=+vessel_rear_surface & -outer_surface)
# this is filled with a void / vacuum by default

universe = openmc.Universe(cells=[inner_vessel_cell,blanket_cell, outer_vessel_cell])
geom = openmc.Geometry(universe)


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

#creates an empty tally object
tallies = openmc.Tallies()

# sets up filters for the tallies
neutron_particle_filter = openmc.ParticleFilter(['neutron'])
energy_filter = openmc.EnergyFilter.from_group_structure('CCFE-709')


# setup the filters for the cell tally
cell_filter = openmc.CellFilter(blanket_cell) 

# create the tally
cell_spectra_tally = openmc.Tally(name='cell_spectra_tally')
cell_spectra_tally.scores = ['flux']
cell_spectra_tally.filters = [cell_filter, neutron_particle_filter, energy_filter]
tallies.append(cell_spectra_tally)

# sets up filters for the tallies
neutron_particle_filter = openmc.ParticleFilter(['neutron'])
energy_filter = openmc.EnergyFilter.from_group_structure('CCFE-709')

# setup the filters for the surface tally
front_surface_filter = openmc.SurfaceFilter(vessel_inner_surface)
back_surface_filter = openmc.SurfaceFilter(vessel_rear_surface)
# detects when particles across the surface

front_surface_spectra_tally = openmc.Tally(name='front_surface_spectra_tally')
front_surface_spectra_tally.scores = ['current']
front_surface_spectra_tally.filters = [front_surface_filter, neutron_particle_filter, energy_filter]
tallies.append(front_surface_spectra_tally)

back_surface_spectra_tally = openmc.Tally(name='back_surface_spectra_tally')
back_surface_spectra_tally.scores = ['current']
back_surface_spectra_tally.filters = [back_surface_filter, neutron_particle_filter, energy_filter]
tallies.append(back_surface_spectra_tally)



# combine all the required parts to make a model
model = openmc.model.Model(geom, mats, sett, tallies)

# remove old files and runs OpenMC
!rm *.h5
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
