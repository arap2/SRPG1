import pymysql, os, json
from datetime import datetime

cwd = os.getcwd()

#connecting to sqlite and insert json data with pymysql
con = pymysql.connect(
    host = 'localhost', 
    user = 'lampuser', 
    password = 'changeme', 
    database = 'Covid_19')
cur = con.cursor()

count = 0
for file in os.listdir(cwd):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
        print(filename)
        with open(filename, "r") as json_data:
            json_obj = json.load(json_data) #AttributeError: 'list' object has no attribute 'get' - didn't allow for    
                                            # the .get method shown in previous version so had to workaround with
                                            # the list index approach.

            exceptions = 0
    # parsing the json data into SQL inserts
            for k, v in json_obj.items():
                count +=1
                if (count%500) == 0:
                    print(count)
                accession = k
                release_date = datetime.strptime(v[0], "%d-%b-%Y") # converting the dates in the json files to date time
                                                                   # compatible string for the mySQL database.
                #orf_name = v[1]
                orf_name = ' '.join(map(str, v[1]))
                orf_product = ' '.join(map(str, v[2]))
                #protein_id = v[3]
                orf_coordinates = ' '.join(map(str, v[4]))
                reference = ' '.join(map(str, v[6])) # converting list to string allowing input into the database.
                fasta = ' '.join(map(str, v[8])) # workaround for the SQL error 'Operand should contain 1 column(s)'
                #print(release_date, description,  comment, orf, experimental_method, reference)
#                print(accession, orf_name, orf_product, orf_coordinates, release_date, reference, fasta)
#                exit()
              
    #if (int(position)%100000) == 0: 
    #print("Position = ", position, "\n", "read depth = ", rd, "Poisson Transformation = ", pt, 
    #	"Negative Binomial = ", nb, "win_length = ", win_length, "gc_count = ", gc_count)
                try:
                    cur.execute("""INSERT INTO covid_nucleotide (ACCESSION, ORF_NAME, ORF_COORDINATES, 
                        ORF_PRODUCT, FASTA, RELEASE_DATE, REFERENCE) VALUES (%s, %s, %s, %s, %s, %s, %s)""", (accession,
                        orf_name, orf_coordinates, orf_product, fasta, release_date, reference))
                except Exception as e:
                    print(e, "\n", accession,
                        orf_name, orf_coordinates, orf_product, release_date, reference)
                    exceptions += 1
                #print(exceptions)
                con.commit()
