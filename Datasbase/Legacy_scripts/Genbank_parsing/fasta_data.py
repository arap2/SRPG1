import re, pprint, os, json
from Bio import SeqIO

directory = os.fsencode("/home/arap2/Documents/structured_project/ncbi_dataset/data/genbank_files")
file_number = 0

for file in os.listdir(directory):
	filename = os.fsdecode(file)
	if filename.endswith(".gbff"):
		CDS_dictionary = {}
		genbank_file = open(filename)
		file_number+=1

	# extracting fasta sequences at each ORF - takes the nucleotide sequences of each feature 
	# from the end of the genbank files that are input.
		CDS_sequences = []
		for rec in SeqIO.parse(genbank_file, "genbank"):
			if rec.features:
				for feature in rec.features:
					print(rec.id) # accession number
					exit()
					if feature.type == "CDS":
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

	#genbank = open("genomic.gbff") # genbank information 
		genbank_file.close()
	# print(len(CDS_sequences))
	# print(CDS_sequences)
	# exit()

		genbank_file = open(filename)
		genbank_file.rl = genbank_file.readlines()
		count = 0
		CDS = 0
	#print("hello")
		for index, line in enumerate(genbank_file.rl):
			#print("hello")
			line = line.rstrip("\n")

			CDS_data_complete = False

			if re.search("CDS", line):
				CDS +=1
				#print(line, ", CDS = " + str(CDS))
				coordinates = line
			if re.search("/gene=", line):
				ORF_name = line
		#		print(gene_name)
			if re.search("/db_xref", line):
				gene_id = line
			if re.search("/locus_tag", line):
				locus_tag = line
			if re.search("/product", line):
				protein_product = line
			if re.search("protein_id", line):
				protein_name = line
				CDS_data_complete = True

			if CDS_data_complete == True:
				count +=1
			#	print("\n" + "NEW SEQUENCE" + " " + str(count) + "\n")
			#	print(CDS_sequences[CDS])
			
				CDS_data = (ORF_name, coordinates, locus_tag, gene_id, 
					protein_product, protein_name, CDS_sequences[CDS])

				#CDS_data = (ORF_name, coordinates, locus_tag, gene_id, protein_product, protein_name)
				entry = {CDS:CDS_data}
				CDS_dictionary.update(entry)
			#	CDS +=1
			if CDS == len((CDS_sequences)):
				break

		print(CDS_dictionary)
		file_title = f"genabnk{file_number}_out"
		with open(file_title, "w") as data_file:
			json.dump(CDS_dictionary, data_file) # the Seqobject in biopython is not JSON serialisable, since this is not
		#					 					 # a primative python DataType.


# with open("genomic.gbff", "rU") as input_handle:
# 	for record in SeqIO.parse(input_handle, "genbank"):
# 		print(record.id)

# count = SeqIO.convert("genomic.gbff", "genbank", "genomic.fasta", "fasta")
# print("Converted %i records" % count)






