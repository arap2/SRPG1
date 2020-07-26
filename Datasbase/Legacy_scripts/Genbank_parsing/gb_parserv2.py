import re, pprint, os, json
from Bio import SeqIO

directory = os.fsencode("/home/arap2/Documents/structured_project/ncbi_dataset/data/genbank_files")
record_counter = 0
CDS_counter = 0
covid_dictionary = {}
filename = "covid01_06-22_06.gb"

CDS_sequences = []
for rec in SeqIO.parse(filename, "genbank"):
	record_counter +=1
	if (record_counter%100) == 0:
		print(record_counter)
	print(rec.id)
	record_name = rec.id # this is the key for the nested dictionary
	if rec.features:
		for feature in rec.features:
			annotation = []
			if feature.type == "CDS":
				CDS_counter +=1
				# print(feature.location)
				# print(feature.type)
				for key, value in feature.qualifiers.items(): # object is of type ordered dict
				#	print(value) # 
					if key == "ribosomal_slippage" or key == "codon_start":
						continue
					else:
						annotation.append(value) # this list holds in order, for a CDS, the ORF name
												 # the ORF product, the protein_id, and the protein sequence.
				#print(annotation)
				#print(feature.location)
				#print(feature.qualifiers["protein_id"])
				#print(feature.location.extract(rec).seq)
				sequence = (feature.location.extract(rec).seq)
				seq_list = []
				for char in sequence:
					seq_list.append(char)
					# print(seq_list)
					# exit()
					#print(sequence)
					CDS_sequences.append(seq_list)
				CDS_data = (annotation[0], annotation[1], annotation[2], # old version that works
			annotation[3], seq_list)
				dictionary_entry = {f"{record_name}_ORF{CDS_counter}":CDS_data}
				covid_dictionary.update(dictionary_entry)
				CDS_counter = 0
				seq_list = []


				# print(covid_dictionary)
				# exit()

		output_file = f"{filename[:-3]}_out"
		with open(output_file, "w") as data_file:
			json.dump(covid_dictionary, data_file) # the Seqobject in biopython is not JSON serialisable, since this is not
							 					 # a primative python DataType.


#ADD DATES FROM THE GENBANK TO THE TABLES.
# if different from the ref sequence, note it in undercase.



