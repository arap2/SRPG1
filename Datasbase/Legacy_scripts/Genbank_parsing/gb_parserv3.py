import re, pprint, os, json
from Bio import SeqIO

directory = os.fsencode("/home/arap2/Documents/structured_project/ncbi_dataset/data/genbank_files")
record_counter = 0
CDS_counter = 0
covid_dictionary = {}
filename = "covid01_06-22_06.gb"
part = 0

CDS_sequences = []
for rec in SeqIO.parse(filename, "genbank"):
	record_counter +=1
	CDS_counter = 0
	if (record_counter%100) == 0:
		print(record_counter)
	print(rec.id)
	record_name = (rec.id) # this is the key for the nested dictionary
	description = (rec.description)
	release_date = (rec.annotations["date"])
	# references = (rec.annotations["references"]) # Object of type Reference is not json serialisable.
	references = []
	r_count = 0
	for ref in rec.annotations["references"]:
		# references.append(ref.location)
		# print(ref.location)
		# exit()
		references.append(ref.title)
		references.append(ref.authors)
		#references.append(ref)
		#print(ref)
	#print(references)
	# print(references)
	# exit()
	#print(rec.annotations)
	# print(rec.annotations["date"])
	# print(rec.annotations["references"])
	# for k, v in rec.annotations.items(): # this still works, but it is easier to access 
	# 									 #  annotation data as achieved above.
	# 	print(k, v)									 
	# 	if k == "date":
	# 		date = v # extracting the date the genome was published
	if rec.features:
		for feature in rec.features:
			annotation = []
			if feature.type == "CDS":
				CDS_counter +=1
				#print(CDS_counter)
				# print(len(feature.location))
				# print(type(feature.location))
				#print(feature.location)
											 # this is a non-elegant workaround for the below error
											 # and the only way i was able to extract the CDS coordinates
											 # without iterating the entirety of feature.location
				CDS_coordinates = []		 # the biopython objext does not allow indexing 
				for pos in feature.location: # Object of type 'CompoundLocation' is not JSON serializable
					start = pos
					end = pos + len(feature.location)-1
					CDS_coordinates.append(f"{start}:{end} (+)")
					break
				# print(CDS_coordinates)
				# exit()
				# print(feature.type)
				for key, value in feature.qualifiers.items(): # object is of type ordered dict
				#	print(key, value) # 
					if key == "gene":
						ORF_name = value
					if key == "product":
						ORF_product = value
					if key ==  "protein_id":
						protein_id = value
					if key == "translation":
						protein_sequence = value
				#print(annotation)
				#print(feature.location)
				#print(feature.qualifiers["protein_id"])
				#print(feature.location.extract(rec).seq)
				sequence = (feature.location.extract(rec).seq)
				seq_list = []
				for char in sequence:
					seq_list.append(char)
					CDS_sequences.append(seq_list)
				CDS_data = (release_date, ORF_name, ORF_product, protein_id, # old version that works
			CDS_coordinates, description, references, protein_sequence, seq_list)
				if CDS_counter == 7:
					dictionary_entry = {f"{record_name}_ORF7a":CDS_data}
				if CDS_counter == 8:
					dictionary_entry = {f"{record_name}_ORF7b":CDS_data}
				dictionary_entry = {f"{record_name}_ORF{CDS_counter}":CDS_data}
				covid_dictionary.update(dictionary_entry)
				if(len(dictionary > 500)):
					part +=1
					output_file = f"new_{filename[:-3]}_out_part{part}.json"
					with open(output_file, "w") as data_file:
						json.dump(covid_dictionary, data_file)
				seq_list = []


# print(covid_dictionary)
# exit()

output_file = f"new_{filename[:-3]}_out.json"
with open(output_file, "w") as data_file:
	json.dump(covid_dictionary, data_file) # the Seqobject in biopython is not JSON serialisable, since this is not
					 					 # a primative python DataType.


#ADD DATES FROM THE GENBANK TO THE TABLES.
# if different from the ref sequence, note it in undercase.



