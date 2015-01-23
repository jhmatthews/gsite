'''
to get level populations 

radial1d = run_tardis(yml_file="basic.yml")
radial1d.plasma_array.calculate_nlte_level_populations()
level_pops = radial1d.plasma_array.level_populations[0].ix[2,0]
'''

import numpy as np
from tardis.io import config_reader
from tardis import model, simulation


def run_tardis(yml_file="basic.yml"):
	'''
	runs a tardis model and returns a class instance of Radial1dModel type
	'''
	#read the config file and create a model
	tardis_config = config_reader.TARDISConfiguration.from_yaml(yml_file)
	radial1d = model.Radial1DModel(tardis_config)
	simulation.run_radial1d(radial1d)

	return radial1d


def set_model_params(radial1d, t_r, w, t_e, ne, tau):
	'''
	set the model parameters in tardis, returns model 
	of same type as input
	'''
	radial1d.t_rads[:] = t_r * units.K
	radial1d.ws[:] = w
	radial1d.plasma_array.electron_densities.values[:] = ne

	##interfere with any details - e.g. electron temperature - like this ...can also do electron density etc.
	frac_te = t_e / t_r
	radial1d.plasma_array.link_t_rad_to_t_electron = frac_te
	##might want to set tau_sobolev optical depths to zero (or some other set of values) for ease of comparison
	radial1d.plasma_array.tau_sobolevs.values[:] = tau

	#calculate the mean intensities in the lines for chosen conditions
	radial1d.calculate_j_blues()

	#propagate rad field settings to plasma
	radial1d.plasma_array.j_blues = radial1d.j_blues
	radial1d.plasma_array.t_rads = radial1d.t_rads.value

	return radial1d


def get_tardis_pops(radial1d, t_r, w, t_e, ne, tau):

	'''
	takes a tardis model and calculates the level populations 
	in these physical conditions (t_r, w, t_e, ne, tau)

	returns a numpy array, x, which contains the level populations summed so that 
	Python and Tardis can be compared.
	'''

	# set the model parameters and Jblues
	radial1d = set_model_params(radial1d, tr, w, te, ne, 0.0)
	radial1d.plasma_array.calculate_nlte_level_populations()

	# get He I level populations
	ch = radial1d.plasma_array.level_populations[0].ix[2,0]

	return ch




