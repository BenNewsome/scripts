# Calculates the metrics we are interested in for the rate sensetivity.

# Uses the generated netCDF files.

from MChem_tools import species as get_species
import netCDF4
from netCDF4 import Dataset
import numpy as np


default_netCDF_file = '/work/home/bn506/Rate_Sensetivity/Batch_runs/NO_OH_p0/results.nc'

pertubated_netCDF_file = 'results.nc'


debug=True


def main():
     
   if debug: print 'started'
   O3 = get_species('O3')
   OH = get_species('OH')

   Calculate_fractional_burden_increase(O3)

#   Calculate_fractional_burden_increase(OH)
#
#   Calculate_largest_gridbox_increase(O3)
#
#   Calculate_largest_gridbox_increase(OH)
#
#   Calculate_mean_surface_increase(O3)

   return;

def Calculate_fractional_burden_increase(species):

   if debug: print 'Calculating the fractional burden increase for ' + species.name

   default_netCDF_data     = Dataset(default_netCDF_file, mode='r')
   pertubated_netCDF_data  = Dataset(pertubated_netCDF_file, mode='r+')

   times, latitudes, longitudes, altitudes, lats, lons, alts = pull_dimensions( default_netCDF_data )

   if debug:
      print ' default netCDF data variables are:'
      print default_netCDF_data.variables

   default_species = default_netCDF_data.variables[species.name]
   pertubated_netCDF_data = pertubated_netCDF_data.variables[species.name]

   default_monthly_total = np.sum(default_species, axis=(1,2,3))
   default_monthly_mean = np.mean(default_monthly_total)
   if debug: print 'mean default ' + species.name + ' = ' + str(default_monthly_mean)

   max_default = np.amax(default_species)
   if debug: print 'maximum default ' + species.name + ' = ' + str(max_default)

   return;
   

   
def pull_dimensions(netcdf_file):

   if debug:
      print netcdf_file.variables

   times       = netcdf_file.variables['time']
   latitudes   = netcdf_file.variables['latitude']
   longitudes  = netcdf_file.variables['longitude']
   altitudes   = netcdf_file.variables['altitude']
   lats = latitudes[:].tolist()
   lons = longitudes[:].tolist()
   alts = altitudes[:].tolist()

   return times, latitudes, longitudes, altitudes, lats, lons, alts;

main()
