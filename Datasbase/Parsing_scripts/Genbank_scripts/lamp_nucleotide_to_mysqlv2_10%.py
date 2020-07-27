import pymysql, os, json
from datetime import datetime

cwd = os.getcwd() #getting the current working directory.

#connecting to the mysql database 
con = pymysql.connect(
    host = 'localhost', 
    user = 'lampuser', 
    password = 'changeme', 
    database = 'Covid_19')
cur = con.cursor()

for file in os.listdir(cwd): # searching all the files in the current working directory.
    filename = os.fsdecode(file)
    if filename.endswith(".json"): # if the current file is a .json file, open the file for reading.
        with open(filename, "r") as json_data:
            json_obj = json.load(json_data) #AttributeError: 'list' object has no attribute 'get' - didn't allow for    
                                            # the .get method shown in previous version so had to workaround with
                                            # the list index approach.

            exceptions = 0  # allows me to check if any entries have not made it into the database - successful runs should have exceptions.
            entry_count = 0 # variable to control the number of entries to put into the database for each file.

            for k, v in json_obj.items(): # for entry, annotation in the json object
                accession = k
                release_date = datetime.strptime(v[0], "%d-%b-%Y") # converting the dates in the json files to date time compatible string for the mySQL database.
                orf_product = ' '.join(map(str, v[2]))
                orf_coordinates = ' '.join(map(str, v[4]))
                reference = ' '.join(map(str, v[6])) # converting list to string allowing input into the database.
                fasta = ' '.join(map(str, v[8])) # workaround for the SQL error 'Operand should contain 1 column(s)'

                try: # attempt to insert the variables above into the respective MySQL table
                    cur.execute("""INSERT INTO covid_nucleotide (ACCESSION, ORF_COORDINATES, 
                        ORF_PRODUCT, FASTA, RELEASE_DATE, REFERENCE) VALUES (%s, %s, %s, %s, %s, %s)""", (accession,
                        orf_coordinates, orf_product, fasta, release_date, reference))
                except Exception as e: # if the insert statement fails, print the exception error and the entry information for the entry that did not make it in.
                    print(e, "\n", accession,
                        orf_coordinates, orf_product, release_date, reference)
                    exceptions += 1
                if entry_count == 110: # this limits the entry of 10 strains into the databse
                    print("entries are finished for this file!")
                    break
                #print(exceptions)
                con.commit()
