import re, pprint, os, json
from Bio import SeqIO

directory = os.fsencode("/home/arap2/Documents/structured_project/ncbi_dataset/data/genbank_pdb") # setting the directory so that it contains the files to be parsed.
filename = "ORF9_pdb.gb" # name of the file to be parsed
ORF = "ORF9"
pdb_dict = {} # setting empty dict to contain annotation data for all records in the file.


for rec in SeqIO.parse(filename, "genbank"): # for each PDB entry in the genbank file
	for x, y in rec.annotations.items(): # iterate the annotations for that record (which are store as key:value paris in SeqIO)
		if x == "db_source": # experimental method is one part of a larger string which is the value paired to db_sorce
			split_string = y.split(";") # split the string so that just the method of producing the protein structure can be set
			exp_method = split_string[4] # to the variable exp_method.
	pdb_identifier = rec.id # name of the record
	description = rec.description # description of the structure.
	release_date =rec.annotations["date"] 
	comment = rec.annotations["comment"] # longer notes on the structure.
	references = []
	for ref in rec.annotations["references"]: # references = (rec.annotations["references"]) # Object of type Reference is not json serialisable - the loop below works around this.
		references.append(ref.title)
		references.append(ref.authors)

	dict_entry = {pdb_identifier:(release_date, description, comment, ORF, exp_method, references)} # creating the dictonary entry for all the annotation data of the current record
	pdb_dict.update(dict_entry)																		# in the file, where the record id is the key and record annotation is the value in a tuple.

output_file = f"{filename[:-3]}_out.json" # writing the dictionary into a json file names after the ORF the structures in the file are derived from.
with open(output_file, "w") as data_file:
	json.dump(pdb_dict, data_file)