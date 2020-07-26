import re, pprint, os, json
from Bio import SeqIO

directory = os.fsencode("/home/arap2/Documents/structured_project/ncbi_dataset/data/genbank_files") # setting the directory to work from.
record_counter = 0 # used to track the progress of the parsing script in the terminal.
covid_dictionary = {}
filename = "genomic.gbff" # setting the file to parse.
part = 1

for rec in SeqIO.parse(filename, "genbank"): # iterating each entry in the genbank file (filename).
	if(record_counter%500) == 0 and record_counter != 0: # splitting the output into separate files to overcome the memory error encountered on loading json files on the lamp server.
		print(str(record_counter), "A NEW FILE HAS BEEN CREATED") # an output json file is generated for every 500 entries that are parsed from a genbank file, these are numbered for
		output_file = f"2new_{filename[:-3]}_out_part{part}.json" # the file they came from using f_string string formatting 
		with open(output_file, "w") as data_file:				  
			json.dump(covid_dictionary, data_file)				  
		part +=1
		covid_dictionary = {} # emptying the dictionary once the json output file has been produceed.
	record_counter +=1 
	if (record_counter%100) == 0: # prints to the terminal each time 100 records have been parsed - shows how many records have been parsed in total.
		print(record_counter)
	record_name = (rec.id) # this is the key for the nested dictionary
	description = (rec.description)
	release_date = (rec.annotations["date"]) # this variable is not in the right format for the SQL date-time data type.
	references = [] # references = (rec.annotations["references"]) # Object of type Reference is not json serialisable - the loop below works around this.
	for ref in rec.annotations["references"]:
		references.append(ref.title) # title of the paper
		references.append(ref.authors) 
	if rec.features:
		for feature in rec.features:
			annotation = []
			if feature.type == "CDS": # once an open reading frame is reached in the current record (entry), extract the following information about the ORF:						
				CDS_coordinates = [] 
				for pos in feature.location: # loop which extracts the start and end location of the current ORF.
					start = pos
					end = pos + len(feature.location)-1
					CDS_coordinates.append(f"{start}:{end} (+)")
					break # this is a non-elegant workaround for the error Object of type 'CompoundLocation' is not JSON serializable - the biopython objext does not allow indexing.
	 					  # This is the only way i was able to extract the CDS coordinates without iterating the entirety of feature.location.
				for key, value in feature.qualifiers.items(): # object is of type ordered dict - itterating to extract annotation about the current ORF (feature) for the current record.
					if key == "gene":
						ORF_name = ' '.join(map(str, value))
						if len(ORF_name) == 1: # this fixes the issue of having varying one letter ORF names which is addressed in the paper.
							ORF_name = "ORF" + ORF_name
					if key == "product":
						ORF_product = value
					if key ==  "protein_id":
						protein_id = value
					if key == "translation":
						protein_sequence = value
				sequence = (feature.location.extract(rec).seq) #  the Seqobject in biopython is not JSON serialisable, since this is not
															   #  so the brelow for loop extracts the FASTA sequence into a standard python list.
				seq_list = []
				for char in sequence:
					seq_list.append(char)
				CDS_data = (release_date, ORF_name, ORF_product, protein_id, 
			CDS_coordinates, description, references, protein_sequence, seq_list) # creating a tuple containing all the annotation extracted above for the current ORF
																				  # of the current record.
				dictionary_entry = {f"{record_name}_{ORF_name}":CDS_data} # creating a dictionary entry where the entry accession + current ORF name are is the key and the above tuple is the value.
				covid_dictionary.update(dictionary_entry) # entreying this entry into the dictionary
				seq_list = []

output_file = f"2new_{filename[:-3]}_out_part{part}.json" # if the file did not contain 500 entries, the dictionary containing <500 entries is output here 
with open(output_file, "w") as data_file:				  # as a json file.
	json.dump(covid_dictionary, data_file)





