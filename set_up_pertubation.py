#!/usr/bin/python
#
# Copy photo_default to reactant1_reactant2_p1

# Change reactant 1 and reactant 2 in sensetivity.dat

# fill in f298 and g in sensetivity.dat

# change the pertubation to 1 in sensetivity.dat

# run monthly-run --name = reactant1_reactant2_ --queue=batch --priority=-1000 --start-run=yes
import os, shutil, sys

source = "default_before_run"

debug=True

def main():

   

   species_1, species_2, f298, g = get_inputs()

   check_inputs(species_1, species_2, f298, g, debug)

   destination = species_1 + "_" + species_2 + "_p1"

   copy_folder(source, destination)

   update_sensetivity(species_1, species_2, f298, g, destination)

   run_queue_script(species_1, species_2, destination)


def get_inputs():

   # Make sure the variables are strings
   species_1 = ""
   species_2 = ""
   f928 = ""
   g = ""


   if (len(sys.argv)>1):

      for arg in sys.argv:
         if "name" in arg: continue
         if arg.startswith("--f298="):
            f298 = arg[7:]
         elif arg.startswith("--g="):
            g=arg[4:]
         elif arg.startswith("--species-1="):
            species_1 = arg[12:]
         elif arg.startswith("--species-2="):
            species_2 = arg[12:]
         elif arg.startswith("--help"):
            print "arguments are:"
            print "--f298="
            print "--g="
            print "--species-1="
            print "--species-2="
         else:
            print "Invalid argument. Try --help for more info."

   else:

      clear_screen()

      species_1 = str(raw_input('Please write species 1:\n'))
      clear_screen()
              
      species_2 = str(raw_input('Please write species 2:\n'))
      clear_screen()
   
      f298 = str(raw_input('Please write f298:\n'))
      clear_screen()

      g = str(raw_input('Please write g:\n'))
      clear_screen()

   return species_1, species_2, f298, g;


def check_inputs(species_1, species_2, f298, g, debug):

   if debug:
      print species_1
      print species_2
      print f298
      print g

   assert (len(species_1) > 0), "species_1 not defined, recived: " + species_1
   assert (len(species_2) > 0), "species_2 not defined, recived: " + species_2
   assert (len(f298) > 0), "f298 not defined, recived: " + f298
   assert (len(g) > 0), "g not defined, recived: " + g

   

def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')
   return




def copy_folder(source, destination):

   try:
      shutil.copytree(source, destination)
   except OSError:
      print "Copy error"

def update_sensetivity(species_1, species_2, f298, g, destination):


   file_location = destination + "/sensetivity.dat"
   tmp_file_location = destination + "/sensetivity.dat.tmp"
   file = open( file_location, 'r' )
   tmp_file = open( tmp_file_location, 'w' )

   if ( species_1 == "photo" ) :

      for line in file:
         
         if    line.startswith("Photolysis reaction # ::"):
                tmp_file.write("Photolysis reaction # :: " + species_2 + '\n')
   
         elif  line.startswith("Photolysis uncertanty ::"):
                tmp_file.write("Photolysis uncertanty :: 1.1d0\n")         
   
   else   
   
      for line in file:
         if    line.startswith("Species 1             ::"):
                tmp_file.write("Species 1             :: " + species_1 + '\n')
   
         elif  line.startswith("Species 2             ::"):
                tmp_file.write("Species 2             :: " + species_2 + '\n') 
   
         elif  line.startswith("f(298)                ::"):
                tmp_file.write("f(298)                :: " + f298 + '\n') 
   
         elif  line.startswith("g                     ::"):
                tmp_file.write("g                     :: " + g + '\n')
   
         elif  line.startswith("Sigma Value           ::"):
                tmp_file.write("Sigma Value           :: " + "1" + '\n')  
   
         else:
            tmp_file.write(line)
   
   file.close()
   tmp_file.close()   

   
   shutil.move(tmp_file_location, file_location)

def run_queue_script(species_1, species_2, destination):

   os.chdir(destination) 

   call_string = "monthly-run --job-name="+species_1+"_"+species_2+"_" +" --queue-name=run" + " --out-of-hours=yes"
   if debug: print call_string

   if debug: print os.getcwd()
   

   os.system( call_string )


main()
