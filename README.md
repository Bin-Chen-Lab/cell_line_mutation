# CLLE-Script

Author: Anthony Sciarini  
Version: May 29, 2018


This program will access cell lines form the expasy database by their accession code and will search for various information for each cell line. This includes:
The primary name of the cell line, Aliases, Age, Gender, Earliest year mentioned from the publication section and form cell line collections, the url from where 
the year was pulled, the ethinicity, and the url from where the ethnicity was found.

#########################
#DOWNLOADING AND RUNNING#
#########################

To run the script download the following files and place them all in the same directory: 
-expasy_script.py 
-accession_codes.csv

Then run the expasy script from the terminal with the following command:

"python expasy_script"

###############################
#SAVING AND VIEWING THE OUTPUT#
###############################

By default the program prints to the standard out put in a csv format.
If you would like to save the output for later, simply pipe the output to a .csv file:

"python expasy_script > my_out_put_file.csv"
 
Once the script is done running the out_put csv can be opened in excell and will automatically 
be formatted into a spread sheet.
