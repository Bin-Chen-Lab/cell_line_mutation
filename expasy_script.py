#########################################################
#
# This program will run a script that will 
# search basic information for a cell line. See the Readme
# on the cell_line_mutation repository for more info
# on what data is pulled and the general functionality
# of the program.
#
# @Author: Anthony Sciarini
# @Version: 6/20/2018
#
##########################################################

###############
#IMPORTED LIBS#
###############
import sys				#System commands lib
import unicodedata			#Unicode lib
import requests				#HTTP request lib
import re				#Regular Expression lib
import csv				#Comma seperated values lib
from bs4 import BeautifulSoup	        #Process HTML documents lib

#############################################################################################
#
# This class contains the functions needed to use a script to search through HTML documents 
# retrived via the Expasy database for cancer cell line, and to grab various data about the 
# cell ine such as: Primary name, Aliases, Year of origin, Age of the individual the cells 
# were taken from, and the Ethnicity. If any of the previously mentioned data was not 
# available then the script will return 'NA'. When the script is run it opens a csv document
# containing all of the cell ine names and then uses that with a url qury template for the
# expasy database to search for each cell line on the database and grab whatever data is
# available for the cell line. 
#
# @Author Anthony Sciarin
# @Version 6/20/2018
#
############################################################################################
class Cell_search:

	#####################################################################################
	# 
	# The constructor of this class takes a string containing the url to search for the
	# the cell line on the expasy database. The first link in the result of that search
	# is then chosen to have data retrieved from. If no results are returned then 'NA'
	# is returned for all data and the year is set to zero.
	# 
	# @Param The url of the the search results page for a particular cell line.
	#
	####################################################################################
	def __init__(self, url):		
		'''				#OLD WAY#
		#Make HTTP request
		req = requests.request('GET', url)

		#Grab the HTML that contains the search results for the cell
		self.results_page = BeautifulSoup(req.content, 'html.parser')

		#Find the first hyper link if it exists
		first_link = self.results_page.find('tr')
		
                #If the search was successful then a web page for the cell line on the expasy database was found.
		#The variable self.page_found is set to be True, meaning that we will be able to use all of the 
		#functions for grabbing information that this class has to offer. 
		if str(first_link) != 'None':				
			next_url = 'https://web.expasy.org/' + first_link.a['href']		
			# ~ Get HTML page that the first hyper link leads to.
			req = requests.request('GET', next_url)		
			self.page = BeautifulSoup(req.content, 'html.parser')
			self.page_found = True			

		#If no results came back then no page was found. self.page_found gets set to False, meaning none
		#of the functions for grabbing data can be used.
		else:
			self.page_found = False
		'''	
		
		#USED TO PROCESS A LIST OF URLS/SEARCH BY ACCESSION CODE#
		req = requests.request('GET', url)         
                self.page = BeautifulSoup(req.content, 'html.parser')
                self.page_found = True   		
				
		#Initialize data fields for the cell line.
		self.accession = 'NA'
		self.primary_name = 'NA'
		self.aliases = 'NA'
		self.sex = 'NA'
		self.age = 'NA'
		self.pub_yr = 'NA'
		self.og_yr = 'NA'
		self.ethnicity = 'NA'
		self.cl_links = []
		self.og_yr_url = 'NA'
		self.eth_url = 'NA'

	#########################################################################################				
	# 
	# If a page for the cell line was found, this function looks up data stored in the table 
	# the table that expasy organizes all the data for the cell line in.
	#
	# @Param table_row The name of the label in the tabel whose data we are looking up.
	# @Return A string containing the data if it is available, otherwise it returns 'NA'.
        #
	########################################################################################
	def table_look_up(self, table_row):	
		if self.page_found == True:	
			#Loop through each row in the page's table
			for row in self.page.find_all('tr'):
				if str(row.th) != 'None':
					if str(row.th.string) == table_row:
						return str(row.td.contents[0].string)
			return 'NA'
		else:
			return 'NA'

	#############################################################################
	#
	# This function uses the table_took_up() to accession data for the cell line.
	#
	#############################################################################
	def search_for_accession(self):
		self.accession = self.table_look_up('Accession')

	###################################################################################
	#
	# This function uses the table_look_up() function to grab the sex of the cell line.
	# 
	###################################################################################
	def search_for_sex(self):								
		sex = self.table_look_up('Sex of cell')
		
		if sex == 'Male':
			self.sex = 'M'
		elif sex == 'Female':
			self.sex = 'F'
		else:
			self.sex = 'NA'		

	###################################################################################
	#
	# This function uses the table_look_up() function to grab the age of the cell line.
	#
	###################################################################################
	def search_for_age(self):								
		age = self.table_look_up('Age at sampling')
		self.age = age.replace('Y',' ')

	############################################################################################
	#
	# This function uses the table_look_up() function to grab the primary name of the cell line. 
	#
	############################################################################################	
	def search_for_primary_name(self):
		self.primary_name = self.table_look_up('Cell line name')

	#######################################################################################
	#
	# This function uses the table_look_up() function to grab the aliases of the cell line.
	#
	#######################################################################################
	def search_for_alias(self):
		self.aliases = self.table_look_up('Synonyms')
						  	
	######################################################################################################
        #
	# If a page for the cell line was found, this function grabs all of the years (If available) from 
        # the publication section of the expasy database and returns the earliest year from the 
        # publications section.
        # 
        # @Return A string containing the lowest year from the publication section, otherwise it returns 'NA'.
        #        
	######################################################################################################
	def search_pub_yr(self):	
		if self.page_found == True:
			#Search for all years in the publication page
			yrs = []		
			yrs += re.findall('[ \( , ' ' ]19\d{2}[\) , ' ' , \.]' , str(self.page))
			yrs += re.findall('[ \( , ' ' ]20\d{2}[\) , ' ' , \.]' , str(self.page))
	
			#Convert list to string
			yrs = map(self.str_trim, yrs)
			yrs = map(int, yrs)
	
			#Set the pub year to the samllest year, if years from the publication were available
			if len(yrs) is 0:	#If no years were found print NA
				return
			else:			#Else return all of the years
				self.pub_yr = str(min(yrs))
	
	#############################################################################################################
	#
	# This is a helper function used to remove the characers surrounding years found by the regular expression
	# used to find all of the years. It returns said modified string. This funcion is used as a lambda function		
	# along with map() function to gracefully removes the non digit characters years returned from the regular 
	# expressions to find years so they can be converted into integers with the int() and map() functions 
	# and compared so the minimum year cab be found with the min() function.
        #
	# @Return A string with the first and last character removed.
	# 
	#############################################################################################################
	def str_trim(self,str):
		return str[1:len(str)-1]
	
	#####################################################################################################################
	#
	# If a page for the cell line was found, this function goes to the cell line collection portion of the current 
	# cell lines expasy page and appends the urls of the all the cell line collections web pages to a list and passes 
	# all of these to the open_cell_line_collections function where the cell lines ethnicity and year of origin will be 
	# searched for.  
	#
	# @Return A string with the ethnicity and year of origin.
	#
	#################################################################################################################### 
	def grab_clc_links(self):

		#TODO Grab links from Biological Sample resources and cell line database resources

		if self.page_found == True:		
			#Return message
			rtn = ''		
	
			#Grab the HTML of the web page that contains the urls (if any are available) of the 
			#cell line collections that reference the cell line.

			#String that will contain the HTML containing the URLS of all the cell line collections
			clc = ''
			
			#String that will contain the HTMl containing the URLS of all the cell line data-base resources
			cl_dbr = ''

			#String that will contain the HTML containing the URLS of all the biological sample resources
			bsr = ''

			#Strint 
			for row in self.page.find_all('tr'):
				if str(row.th) != 'None':
					if str(row.th.string) == 'Cell line collections':
						clc = row
					if str(row.th.string) == 'Cell line databases/resources':
						cl_dbr = row
					if str(row.th.string) == 'Biological sample resources':
						bsr = row
						

			#If there are no links to look through	
			if clc == '' and cl_dbr == '' and bsr == '':
				return
	
			#If there links that could be grabbed, then put there url's into the cell line links list 
			if clc != '':
				for link in clc.find_all('a'):
					#print link.string
					self.cl_links.append(link['href'])
			if cl_dbr != '':
				for link in cl_dbr.find_all('a'):
       	                        	#print link.string
       	                        	self.cl_links.append(link['href'])
			if bsr != '':
				for link in bsr.find_all('a'):
       	                        	#print link.string
       	                        	self.cl_links.append(link['href'])

	#########################################################################################################
	#
	# This funtion searches through specific HTML tags known to contain the year of origin for a cell line in
	# the page of a cell line collection known to contain years of origin for cell lines. The years are
	# searched for with a regular expression and every year found is stored in a list.
	#
	# @Param tag_type The HTML tags that will be serached for in the in the web page.
	# @Param clc_page The HTML document for the cell line collection web page.
	# @Return A list containing all of the years of origin found for the cell line.
	# 
	#########################################################################################################
	def grab_years(self, tag_type, clc_page):
		yrs = []
		for tag in clc_page.find_all(tag_type):
			#Filter out any unreadable characters that would prevent valid years to be searched and convert the HTML tag to a String.				
			tag_str = unicodedata.normalize('NFKD', unicode(tag)).encode('ascii' , 'ignore')  	
			
			#################################################################################################			
			#Uses a regular expresssion to search through each HTML tag for years in the following formats...
			#	Any year that is...
			#	-In the 1900s
			#	-In the 2000s
			#       -At the start of a line
			#	-At the end of a line
			#	-At the end of a sentence, for instance 1968.
			#	-Surrounded in parentheses (1968)
			#	-At the start or end of a HTML tag, for instance <p>1968</p>
			#	-Has a semi colon following it 1968;
			#	-And any combination of the above!
			##################################################################################################

       			yrs += re.findall('[ ^ , \( , \s , \> ]19\d{2}[ \) , \s , \. , ; , $ , \< ]' , str(tag_str))
			yrs += re.findall('[ ^ , \( , \s , \> ]20\d{2}[ \) , \s , \. , ; , $ , \< ]' , str(tag_str))
			
		return yrs

	#########################################################################################################
	#
	# If a page for the cell line was found, opens up each cell line collection pages for the cell line and 
	# uses the search_years and search_ethnicity() function to grab the year of origin and ethnicity if it is 
	# available.
	# 													
	# @Param links A list of the links to cell line collection web pages for the cell line.
	# @Return A string containing the ethnicity and year of origin for the cell line.
	#
	#########################################################################################################
	def search_clc_pages(self):

		if self.page_found == True:
			
			#List to contian the min years from each web page
			master_yr_list = {}

			#String to contain the ethncity of the cell
			ethnicity = 'NA'
			
			#For each valid cell line collection url, grab the ethnicity and the minimum year of origin if they are available. 
			for url in self.cl_links:

				#Create list to store years and a String to store the ethnicity#
				yrs = []
				
				#URL LISTS#		TODO
	
				#List of cell line collection webiste urls that do not have any useful information relating to ethnicity or years
				#i.e bad urls.
				bad_url = ['en.pasteur.ac' , 'clsgmbh' , 'ibvr.org' , 'kcb.kiz' , 'cellbank.snu.ac.kr' , 'coriell.org', 
					  'www.fli.de/en/services', 'dtp.cancer.gov', 'portals.broadinstitute.org', 'www.cancerrxgene.org', 
					  'knowledge.lonza', 'www.cghtmd.jp', 'cellresource.cn', 'cell-lines.toku-e.com']
				
				#Boolean value that gets flipped if the web page has no useful data.
	                        no_data = False  

				#Check if the cell line collection web page is one of the bad urls.
				for url_str in bad_url:
					if url_str in url:	
						no_data = True
						break

				#If if the cell line collection has no useful data then skip it.
				if no_data is True:
					continue
			
				#If there is some issue in connecting to that page then skip this cell line collection.
				try:
			        	url_req = requests.request('GET', url)
				except requests.exceptions.SSLError:
					#'Failed to connect to web page'
					continue
				except requests.exceptions.ConnectionError:
					#'Failed to connect to web page'
					continue			

				#Grab HTML from the page, prepare lists for years
       				url_page = BeautifulSoup(url_req.content,'html.parser')

				#TODO add case for - https://www.aidsreagent.org/reagentdetail.cfm?t=cell_lines&id=322
				
				#Search for the cells ethnicity
				if 'brc.riken' in url:						#TODO find tag type
					ethnicity = self.grab_ethnicity(url_page, 'td', ethnicity, url)

			        #Search years from <span> tags
				if 'www.phe-culturecollections.org' in url:
					#Search for years
					yrs += self.grab_years('span' , url_page)	
					
					#Search for ethnicity
					ethnicity = self.grab_ethnicity(url_page,'span', ethnicity, url)
					
				#Search years and ethnicity from <dd> tags
				if 'dsmz.de/catalogues' in url or 'cancer.sanger' in url or 'www.encodeproject.org' in url:
					#Search for years
					yrs += self.grab_years('dd' , url_page)	
					
					#Search for ethnicity
					ethnicity = self.grab_ethnicity(url_page, 'dd', ethnicity, url)
					
				#Search years and ethnicity from <p> tags	
				if 'www.atcc.org' in url or 'www.addexbio.com' in url:
					#Search for years
					yrs += self.grab_years('p' , url_page)	
					
					#Search for ethnicity
					ethnicity = self.grab_ethnicity(url_page, 'p', ethnicity, url)
					
				#Search years and ethnicity from <td> tags
				#TODO specify where ethncity is searched from only in this case do to issues with cellbank.nibiohn
				if 'www.atcc.org' in url or 'lincs.hms.harvard.edu' in url or 'ncbi.nlm.nih.gov' in url or 'catalog.bcrc.firdi.org' in url or 'iclc.it/details' in url or 'http://cellbank.nibiohn.go.jp' in url or 'idac.tohoku.ac' in url:	
					#Search for years
					yrs += self.grab_years('td' , url_page)	
					
					#Search for ethnicity
					ethnicity = self.grab_ethnicity(url_page, 'td', ethnicity, url)
					
				#Search years and ethnicity from <div> tags
				if 'http://bcrj.org.br' in url:
					#Search for years
					yrs += self.grab_years('div' , url_page)	
					
					#Search for ethnicity
					ethnicity = self.grab_ethnicity(url_page, 'div', ethnicity, url)			
				
				#Search for years and ethnicity on the entire page 				
				if '/bioinformatics.hsanmartino' in url:
					#Search for years
                                        yrs += self.grab_years('html' , url_page)

                                        #Search for ethnicity
                                        ethnicity = self.grab_ethnicity(url_page, 'html', ethnicity, url)
                                 
								
	
			        #Remove any characters surrounding that years.
				yrs = map(self.str_trim, yrs)  
				
				#Convert each year to an in the minimum year can be found			
				yrs = map(int, yrs)

				#Print years from testing
				#print 'Years pulled from ' + str(url)
				#print yrs

				#Append the minimum year if one exists
			        if len(yrs) is not 0 :
			                master_yr_list[url] = min(yrs)
				
			#Remove all years less than 1958
			for key in master_yr_list:
				if master_yr_list[key] < 1958:
					master_yr_list[key] = 3000 #Cant delete elements during run time, so we will make them stupidly huge

			#Find the earliest year and the URL that it came from
			
			if len(master_yr_list) is not 0:
				min_yr = 3000
				for key in master_yr_list:				
					if master_yr_list[key] < min_yr:
						min_yr = master_yr_list[key] 
						self.og_yr_url = key
				
				#Set the min year from the cell line publications	
				self.og_yr = str(min_yr)
			
			#Set the ethnicities from the cell line publications
			self.ethnicity = ethnicity

	###############################################################################
	#               
	# This function will search for the ethnicity of the cell line in on of the
	# cell line collection pages that contains information for the cell line.
	#
	# @Param clc_page The HTML document of the cell line collection being 
	#	 searched through.
	# @Param current_cell_eth The current known ethnicity for the cell line.
	# @Return A string containing the ethinicty of the cell ine collection. 
	#
	##############################################################################

	def grab_ethnicity(self, clc_page, tag_type, current_cell_eth, page_url):
		#Types of possible ethinicites for cell lines.
		categories = ['Caucasian' , 'caucasian' , 'Chinese' ,'chinese' , 'Japanese' , 'japanese' , 
			      'Filipino' , 'filipino' , 'Korean' , 'korean' , 'Vietnamese', 'vietnamese',
			      'African American' , 'african american' , 'Black' , 'black' , 'white' , 'White']
		
		#Filter out any unkown characeters the would interfere with grabbing valid data
                page_str = unicodedata.normalize('NFKD', unicode(clc_page)).encode('ascii' , 'ignore')			
		
		#If no ethnicity has been found for the cell line then search for one
		if current_cell_eth == 'NA':
			for ethnicity in categories:
				for tag in clc_page.find_all(tag_type):
					tag_str = unicodedata.normalize('NFKD', unicode(tag)).encode('ascii' , 'ignore')
					if ethnicity in str(tag_str):
						self.eth_url = page_url
						return ethnicity
			else:
				return current_cell_eth
		#If one has already been found then return the current cell line.
		else:
			return current_cell_eth
	
#####################################
#	
# Where the script is run and tested.
#
#####################################
def main():

	#Open a csv file containing the names of all the spread sheets
	with open('accession_codes.csv') as csvfile:
		
		#Make a csv reader
		reader = csv.DictReader(csvfile)
		
		#String that contains the url template to search for a specific cell ine on the Expasy database.
		query_url = 'https://web.expasy.org/cellosaurus/'
	
		#A list to contain all of the URLs that lead to the search results for each cell line on the expasy search page.
		query_list = []
		
		#For each cell line primary name that was scanned by the reader, a url to search for that cell line is created and then.  
		for row in reader:
                	query_list.append(query_url + row['Accession'])
			
		#The row number of the cell line in the spread sheet.
		index = 1
		
	print 'Cell.Primary.Name,Aliases,Sex,Age,Ethnicity,Min.Pub.Year,Min.Clc.Year,Clc.Year.Url,Eth.Url'
	for query in query_list:
		cell = Cell_search(query)

		#Search for data for the cell line	
		cell.search_for_accession()
		cell.grab_clc_links()			
		#cell.search_clc_pages()	
		#cell.search_pub_yr()					
		#cell.search_for_sex()		
		#cell.search_for_age()	
		#cell.search_for_primary_name()	
		#cell.search_for_alias()	
		
		
	
		#Print data in a csv format.
		print cell.accession +','+ cell.ethnicity +','+ cell.eth_url	
		#print cell.primary_name +','+ cell.aliases +','+ cell.accession  +','+ cell.sex +','+ cell.age +','+ cell.ethnicity +','+ cell.pub_yr +','+ cell.og_yr +','+ cell.og_yr_url +','+ cell.eth_url

	
#############
#Run Program#
#############				
if __name__ == '__main__':
	main()

##############
#Testing Zone#
##############

bad_urls = ['https://portals.broadinstitute.org/ccle/page?cell_line=2313287_STOMACH',
	    'https://www.cancerrxgene.org/translation/CellLine/910924',
            'http://knowledge.lonza.com',
	    'http://www.cghtmd.jp/CGHDatabase/mapViewer?hid=54&aid=1&lang=en',
	    'http://cellresource.cn',
	    'http://cell-lines.toku-e.com/Cell-Lines_460.html',
	    '']

# TODO look at this HTML for biosample website
url = 'https://www.ncbi.nlm.nih.gov/biosample/?term=SAMN03471600'

# TODO look at HTML for cell line databases/resources website
url_2 = 'http//igrcid.ibms.sinica.edu.tw/cgi-bin/cell_line_view.cgi?cl_name=22Rv1'

# TODO look at HTML for cell line databases/resources
url_3 = 'http://bioinformatics.hsanmartino.it/cldb/cl38.html'

# TODO look at HTML for cell line databases/resources
url_4 = 'https://cancer.sanger.ac.uk/cell_lines/sample/overview?id=910924'

# TODO look at HTML for cell line databases/resources
url_5 = 'http://lincs.hms.harvard.edu/db/cells/50002/'

# TODO look at HTML for cell line for a bio samele, might be useful
url_6 = 'https://www.encodeproject.org/biosamples/ENCBS225AJI/'

# TODO look at HTML for ...
