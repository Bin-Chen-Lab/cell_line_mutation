# CCLE-Expasy-Script

Author: Anthony Sciarini  
Version: June 20, 2018

ABOUT
------
This program will access cell lines form the expasy database by their accession code and will search for various information for each cell line such as:
The primary name of the cell line, Aliases, Accession code, Age, Gender, Earliest year mentioned found in the the publication section and in the cell line collections contaiing the cell line, the url from where 
the year was pulled, the ethinicity, and the url from where the ethnicity was found. The script loads a csv file "accessions_code.csv" to get the accession code for earch cell on the database and uses that to build a URL to access the web page for the cell line on the expasy data base. From there the script pulls the previously mentioned data from the expasy web page and any cell line collection pages that contain useful informatio about the cell line. The data for each cell is then printed to the standard out put.


DOWNLOADING AND RUNNING
------------------------
To run the script download the following files and place them all in the same directory: 
expasy_script.py 
accession_codes.csv

To run the expasy script from the terminal use the following command:

"python expasy_script"


SAVING AND VIEWING THE OUTPUT
------------------------------

By default the program prints to the standard out put in a csv format.
If you would like to save the output for later, simply pipe the output to a .csv file:

"python expasy_script > my_out_put_file.csv"
 
Once the script is done running the out_put csv can be opened with Excell and will automatically 
be converted into a spread sheet.
