# Copy photo_default to reactant1_reactant2_p1

# Change reactant 1 and reactant 2 in sensetivity.dat

# fill in f298 and g in sensetivity.dat

# change the pertubation to 1 in sensetivity.dat

# run monthly-run --name = reactant1_reactant2_ --queue=batch --priority=-1000 --start-run=yes
import os, shutil, sys

source = photo_default


def main():



   species_1, species_2, f298, g = get_inputs()

   check_inputs(species_1, species_2, f298, g)

   destination = species_1 + "_" + species_2 + "_p1"

   copy_folder(source, destination)

   update_sentetivity(species_1, species_2, f298, g)

   run_queue_script(species_1, species_2)


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


def check_inputs(speices_1, species_2, f298, g):

   assert (len(species_1) > 1), "species_1 not defined"
   assert (len(species_2) > 1), "species_2 not defined"
   assert (len(f298) > 1), "f298 not defined"
   assert (len(g) > 1), "g not defined"

   

def clear_screen():
   os.system('cls' if os.name == 'nt' else 'clear')
   return




def copy_folder(source, destination):

   try:
      shutil.compytree(source, destination)
   except OSError:
      print "Copy error"

def update_sensetivity(species_1, species_2, f298, g, destination):


   file_location = destination + "/sensetivity.dat"
   tmp_file_locaiton = destination + "/sensetivity.dat.tmp"
   file = open( file_location, 'r' )
   tmp_file = open( tmp_file_location, 'w' )

   for line in file:
      if   line.starts_with("Species 1             ::"):
             tmp_file.write("Species 1             :: " + species_1)
      elif line.starts_with("Species 2             ::"):
             tmp_file.write("Species 2             :: " + species_2) 
      elif line.starts_with("f(298)                ::"):
             tmp_file.write("f(298)                :: " + f298) 
      elif line.starts_with("g                     ::"):
             tmp_file.write("g                     :: " + g )
      elif line.starts_with("Sigma Value           ::"):
             tmp_file.write("Sigma Value           :: " + "1" )  

      else:
      tmp_file.write(line)
   
   file.close()
   tmp_file.close()   

   
   shutil.copy(tmp_file, file_location)

def run_queue_script(species_1, species_2, destination)

   os.system( "cd " + destination ) 

   call_string = "monthly-run --queue-name="+species_1+"_"+speices_2+"_"

   os.system( call_string )


main()
