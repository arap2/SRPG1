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
                                            # the list index approach below.

            exceptions = 0 # allows me to check if any entries have not made it into the database - successful runs should have exceptions.
            for k, v in json_obj.items(): # for entry, annotation in the json object
                accession = k # get the accession
                release_date = datetime.strptime(v[0], "%d-%b-%Y") # converting the dates in the json files to date time
                                                                   # compatible string for the mySQL database.
                orf_name = v[1] 
                orf_product = v[2]
                CDS_coordinates = v[4]
                reference = ' '.join(map(str, v[6])) # converting list to string allowing input into the database.
                nucleotide_seq = v[8]

                try: # attempt to insert the variables above into the respective MySQL table
                    cur.execute("""INSERT INTO PDB_structures (accession, release_date, description, 
                        comment, orf, experimental_Method, reference) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (accession,
                        release_date, description, comment, orf, experimental_method, reference))
                except Exception as e: # if the insert statement fails, print the exception error and the entry information for the entry that did not make it in.
                    print(e, "\n", accession, 
                            release_date, description, comment, orf, experimental_method, reference)
                    exceptions += 1 # update the exceptions variable to show how many entries have been omitted.
                #print(exceptions) # print the number of omitted entries from the file.
                con.commit()
