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

   calculate_fractional_burden_increase(O3)

#   calculate_fractional_burden_increase(OH)
#
   calculate_largest_gridbox_increase(O3)
#
#   calculate_largest_gridbox_increase(OH)
#
#   calculate_mean_surface_increase(O3)

   return;

def calculate_fractional_burden_increase(species):

   if debug: print 'Calculating the fractional burden increase for ' + species.name

   default_netCDF_data     = Dataset(default_netCDF_file, mode='r')
   pertubated_netCDF_data  = Dataset(pertubated_netCDF_file, mode='r')

   times, latitudes, longitudes, altitudes, lats, lons, alts = pull_dimensions( default_netCDF_data )

   default_species_data = default_netCDF_data.variables[species.name]
   pertubated_species_data = pertubated_netCDF_data.variables[species.name]

   default_burden = calculate_burden(default_species_data)
   pertubated_burden = calculate_burden(pertubated_species_data)

   if debug: print 'mean default ' + species.name + ' = ' + str(default_burden)
   if debug: print 'pertubated default ' + species.name + ' = ' + str(pertubated_burden)
   
   fractional_burden_increase = 100.0 * ( np.divide( pertubated_burden, default_burden ) -1.0 )
   if debug: print 'Fractional burden increase of ' + species.name + ' = ' + str(fractional_burden_increase)

   default_maximum = np.amax(default_species_data)

   default_netCDF_data.close()
   pertubated_netCDF_data.close()   

   return;
   
def calculate_largest_gridbox_increase(species):
   # Calculate the largest fractional increase for any gridbox and give the fractional increase
   # Also give the spacetime position

   # Open the datasets
   default_netCDF_data     = Dataset(default_netCDF_file, mode='r')
   pertubated_netCDF_data  = Dataset(pertubated_netCDF_file, mode='r')
 
   times, latitudes, longitudes, altitudes, lats, lons, alts = pull_dimensions( default_netCDF_data )

   default_species_data = default_netCDF_data.variables[species.name]
   pertubated_species_data = pertubated_netCDF_data.variables[species.name]

   fractional_difference = 100.0 * (np.divide( pertubated_species_data, default_species_data ) - 1.0)

   # Remove nans
   where_are_NaNs = np.isnan(fractional_difference)
   fractional_difference[where_are_NaNs] = 0.0

   

   print "Fractional difference shape = " + str(fractional_difference.shape)

   fractional_difference_maximum = np.amax( np.absolute(fractional_difference ) )
   print 'Fractional difference maximum = ' + str(fractional_difference_maximum)

   frac_diff_max_position = np.argmax(fractional_difference)
   frac_diff_max_position = np.unravel_index( frac_diff_max_position, fractional_difference.shape )
   
   max_pos_time   = times[frac_diff_max_position[0]]
   print "time = " + str(max_pos_time) + times.units
   max_pos_alt    = alts[frac_diff_max_position[1]]
   print "Altitude = " + str(max_pos_alt) + ' ' + altitudes.units
   max_pos_lat    = lats[frac_diff_max_position[2]]
   print "Latitude = " + str(max_pos_lat) + ' ' + latitudes.units
   max_pos_lon    = lons[frac_diff_max_position[3]]
   print "Longitude = " + str(max_pos_lon) + ' ' + longitudes.units

   print "Fractional difference maximum position = " + str(frac_diff_max_position)
   return;






def calculate_burden(data):
   monthly_totals = np.sum(data, axis=(1,2,3))
   monthly_mean   = np.mean(monthly_totals)

   return monthly_mean;

   
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
