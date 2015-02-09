#!/usr/local/bin/python

# This script is designed to scrape the bpch from my runs to obtain all the relevant metrics we want, and turn them into a nice netcdf file.

#inputs are .bpch files

#outputs:
# monthly_mass_of_O3(x,y,z,t)
# monthly_mass_of_OH(x,y,z,t)
# monthly_masS_of_Sulphide(x,y,z,t)
# Dobson_units(x,y,z,t)

#from bpch import bpch
import sys
import netCDF4
from netCDF4 import num2date, date2num
import numpy as np
from MChem_tools import species as get_species
from ben_tools import get_tropospheric_mass_values
from MChem_tools import gchemgrid
import datetime

months = [200607, 200608]

netcdf_name = 'results.nc'
debug=True

def main():

   netcdf_file = generate_netCDF()

   get_monthly_mass_of_O3(netcdf_file)

#   get_monthly_mass_of_OH()

#   get_monthly_mass_of_Sulphide()

#   get_dobson_units()


def generate_netCDF():

   # get the latitudes and longitudes from MChem_tools.
   c_lat_4x5 = gchemgrid('c_lat_4x5')
   c_lon_4x5 = gchemgrid('c_lon_4x5')
   c_alt_4x5 = gchemgrid('c_km_geos5_r')[:38]

   if debug:
      print "lat size = " + str(c_lat_4x5.size)
      print "lon size = " + str(c_lon_4x5.size)


   netcdf_file = netCDF4.Dataset( netcdf_name, 'w', format='NETCDF4')

   # Create dimensions of the data
   time = netcdf_file.createDimension('time', None )
   alt  = netcdf_file.createDimension('alt', c_alt_4x5.size )
   lat  = netcdf_file.createDimension('lat', c_lat_4x5.size )
   lon  = netcdf_file.createDimension('lon', c_lon_4x5.size )


   # Create Variables of the data
   times       = netcdf_file.createVariable('time', 'i8', ('time',))
   altitudes   = netcdf_file.createVariable('altitude', 'f4', ('alt',))
   latitudes   = netcdf_file.createVariable('latitude', 'f4', ('lat',))
   longitudes  = netcdf_file.createVariable('longitude', 'f4', ('lon',))

   # Input the data
   latitudes[:]  = c_lat_4x5
   longitudes[:] = c_lon_4x5
   altitudes[:]  = c_alt_4x5



   netcdf_file.description = 'This file contains the metrics for the hourly concentrations of some tracers for use in sensetivity studies'

   # Store the units
   latitudes.units   = 'Degrees north'
   altitudes.units   = 'KM'
   longitudes.units  = 'Degrees east'
   times.units       = 'Hours since 0001-01-01 00:00:00'
   times.calendar    = 'gregorian'

   

   return netcdf_file;

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

def pull_grids(netcdf_file):
   # get the latitudes and longitudes from MChem_tools.
   c_lat_4x5[:] = gchemgrid('c_lat_4x5')
   c_lon_4x5[:] = gchemgrid('c_lon_4x5')
   c_alt_4x5[:] = gchemgrid('c_km_geos5_r')
   
   return c_lat_4x5, c_lon_4x5, c_alt_4x5;

def get_time(times, months, i):
   
      year = int(str(months[i])[:4])
      month = int(str(months[i])[4:])
      day = int("01")
      hour = 00
      minute = 00
      second = 00
   
      input_time = datetime.datetime(year, month, day, hour, minute, second)
      
      input_time = date2num( input_time, units=times.units, calendar=times.calendar )
      time = input_time
      return time;
   

def get_monthly_mass_of_O3(netcdf_file):

   # Load the netcdf variables.
   times, latitudes, longitudes, altitudes, lats, lons, alts = pull_dimensions( netcdf_file )

   latitude_list = []
   latitude_list[:] = latitudes

#   bob, longitudes, altitudes = pull_grids()
#   latitudes[:]=bob

   # Scrape the data from the bpch and put it into the netcdf.

   species = get_species('O3')
   if debug:
      print "Species name = " + species.name
      print "Species group = " + species.group

   O3 = netcdf_file.createVariable(species.name, 'f8', ('time', 'alt', 'lat', 'lon',))

   file_location = ''

   # get_tropospheric_mass_values found in ben_tools.py
   O3_data, O3.units = get_tropospheric_mass_values(species, months, file_location, debug=False)

   if debug:   print "O3 data shape = " + str(O3_data)

   i = 0

   for item in O3_data:

      time = get_time(times, months, i)

      if debug: print "item shape = " + str(item.shape)

#      if debug: input("prompt")

      for alt in altitudes:
         for lat in latitudes:
            for lon in longitudes:
               
               lat_number = lats.index(float(lat))
               lon_number = lons.index(float(lon))
               alt_number = alts.index(float(alt))

               Concentration = item[alt_number, lat_number, lon_number]
   

               if debug:
                  print "Time = " + str(time)
                  print "Lat number = " + str(lat_number)
                  print "Lon number = " + str(lon_number)
                  print "alt number = " + str(alt_number)
                  print "item = " + str(Concentration)
               O3[ i, alt_number, lat_number, lon_number ] = Concentration


      i = i + 1

#   if debug:
#      print "O3 data shape = " + str(len(O3_data))
#      print O3_data


   return O3
       

main()

