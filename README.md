# CLLE-Script

Author: Anthony Sciarini  
Version: June 20, 2018

About
------
This program will access cell lines form the expasy database by their accession code and will search for various information for each cell line such as:
The primary name of the cell line, Aliases, Accession code, Age, Gender, Earliest year mentioned found in the the publication section and in the cell line collections contaiing the cell line, the url from where 
the year was pulled, the ethinicity, and the url from where the ethnicity was found.


DOWNLOADING AND RUNNING
------------------------
To run the script download the following files and place them all in the same directory: 
-expasy_script.py 
-accession_codes.csv

To run the expasy script from the terminal use the following command:

"python expasy_script"


SAVING AND VIEWING THE OUTPUT
------------------------------

By default the program prints to the standard out put in a csv format.
If you would like to save the output for later, simply pipe the output to a .csv file:

"python expasy_script > my_out_put_file.csv"
 
Once the script is done running the out_put csv can be opened with Excell and will automatically 
be converted into a spread sheet.
