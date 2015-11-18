#!/usr/bin/python
#PYTHON SCRIPT TO 
#
#
#to run type: python name.py
#
#written by Richard Wolfe
#
# 1. open uclust_assigned_taxonomy/rep_set_tax_assignments.txt and find the taxonomy in the 
#    otu_table then add the acession number to this file
# 2. find the acession number in rep_set.fna and copy the taxonomy to this file
#    (took about 2 minutes)
#
# uclust_assigned_taxonomy/rep_set_tax_assignments.txt has 74,934 lines
#    Acession#  Taxonomy value value
#Ex: EF096568	Bacteria; __Bacteroidetes; __Bacteroidia; __Bacteroidales; __S24-7; __uncultured_bacterium	1.00	3
#
# taxonomy_summaries/otu_table_mc2_w_tax_L7.txt has 836 lines (header + 835 otu's)
#
# rep_set.fna has 149,868 lines (fasta file of 74,934 sequences)
#
#
#version 2: add command line parameters
#
#Ex command:  python extract_taxonomy_v2.py  -r /home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/uclust_assigned_taxonomy/rep_set_tax_assignments.txt 
#                                        -t /home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/taxonomy_summaries/otu_table_mc2_w_tax_L7.txt
#                                        -p /home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/rep_set.fna
#                                        -d 7
#                                        -o /home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/taxonomy_summaries/test_otu_table_mc2_w_tax_L7_with_accession.txt
#                                        -f /home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/test_rep_set_with_taxonomy.fna

import sys  #for exit command
import argparse #to get command line args 
                #needed to install argparse module because using python 2.6
                #and argparse comes with python 2.7
                #  sudo easy_install argparse


#create an argument parser object
#description will be printed when help is used
parser = argparse.ArgumentParser(description='A script to extract taxonomy')

#add the available arguments -h and --help are added by default
#if the input file does not exist then program will exit
#if output file does not exit it will be created
# args.input is the input file Note: cant write to this file because read only
# args.output is the output file
# args.m is the minimum seq length
#parser.add_argument('-r', '--rep_set_tax_assignments', type=argparse.FileType('r'), help='Path and name of rep_set_tax_assignments.txt file',required=True)
parser.add_argument('-r', '--rep_set_tax_assignments', help='Path and name of rep_set_tax_assignments.txt file',required=True)
#parser.add_argument('-t', '--otu_table', type=argparse.FileType('r'), help='otu_table_mc2_w_tax_L7.txt file',required=True)
parser.add_argument('-t', '--otu_table', help='Path and name of otu_table_mc2_w_tax_L7.txt file',required=True)
parser.add_argument('-p', '--rep_set', help='Path and name of rep_set.fna file',required=True)


parser.add_argument('-d', '--depth', type=int, help='Depth of OTU table', required=True)
parser.add_argument('-o', '--new_otu_table', help='name of the new OTU table file',required=True)
parser.add_argument('-f', '--new_fasta', help='name of the new fasta file',required=True)


#get the args
args = parser.parse_args()

#additional argument tests
if args.depth <= 0:
	print "Error: argument -d <= 0"
	sys.exit(0)




#Test print the args
#print args


print "Script started...."





#paramaters

#rep_set_tax_assignments_path = '/home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/uclust_assigned_taxonomy/rep_set_tax_assignments.txt'

#otu_table_path = '/home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/taxonomy_summaries/otu_table_mc2_w_tax_L7.txt'
#new_otu_table_path = '/home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/taxonomy_summaries/otu_table_mc2_w_tax_L7_with_accession.txt'

#rep_set_path = '/home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/rep_set.fna'
#new_fasta_file = '/home/wolfe.759/Lindsey_project/STEP3_SILVA_chimera_filtered_OUT/rep_set_with_taxonomy.fna'

#the number of depths to the taxonomy
#taxonomy_depth = 7

rep_set_tax_assignments_path = args.rep_set_tax_assignments
otu_table_path = args.otu_table
new_otu_table_path = args.new_otu_table
rep_set_path = args.rep_set
new_fasta_file = args.new_fasta
taxonomy_depth = args.depth

############################################################################
#part 1
#put accession number into otu table and write new otu table
otu_file = open(otu_table_path, "r") 
otu_line_count = 0
otu_table = [] #empty list

#read first line
otu_line = otu_file.readline()

#read lines into list
while otu_line:
	otu_line_count = otu_line_count + 1
	otu_line = otu_line.rstrip() #remove endline from end of line
	otu_table.append(otu_line)  #add to list

	#read next line
	otu_line = otu_file.readline()

otu_file.close()



#open the file with the taxonomies
tax_in_file = open(rep_set_tax_assignments_path, "r")  #open read only

tax_line_count = 0

#read each line
taxonomy_line = tax_in_file.readline()
while taxonomy_line:
	#print "Reading taxonomy line ", tax_line_count
	tax_line_count = tax_line_count + 1
	words = taxonomy_line.split()  #splits on whitespace
	accession = words[0]
	words.remove(words[0]) #remove first element
	words.pop() #remove last element
	words.pop()
	while len(words) < taxonomy_depth:
		words.append(";Other")
	taxonomy = ""
	#concat the words int 1 word
	for i in words:
		taxonomy = taxonomy + i

	#find taxonomy in the otu file 
	#there may be more than 1 line that starts with taxonomy
	otu_index = 0
	for i in otu_table:		
		if i.startswith(taxonomy):
                   	#print "i = ", i
			#print "acession = ", acession
			otu_table[otu_index] = otu_table[otu_index] + '\t' + accession
			#found = True
			#break
		otu_index = otu_index + 1

	#read another line
	taxonomy_line = tax_in_file.readline()

tax_in_file.close()


#write the new file
otu_out_file = open(new_otu_table_path, "w")

for i in otu_table:
	otu_out_file.write(i)
        otu_out_file.write("\n")

otu_out_file.close()

#print to screen
print "Lines read from otu_table = ", otu_line_count

#############################################################################
#Part 2
#put the taxonomy from uclust_assigned_taxonomy/rep_set_tax_assignments.txt into a new rep_set.fna file

#open the fasta file and read into 2 arrays, a header and a sequence
fasta_file = open(rep_set_path)
line_count = 0
seq_count = 0
header = []   #an empty list
sequence = [] #an empty list


#read first line
line = fasta_file.readline()



#if the file is not empty keep reading one at a time
while line:
	line_count = line_count + 1

	#if line starts with > it is the header line
	if ">" in line:
		seq_count = seq_count + 1
		line = line.rstrip()  #remove whitespace at end includung endl
		header.append(line)  #add to the array
		sequence.append("")  #add a blank sequence
		#words = line.split()  #splits on whitespace
		#words[0] = words[0].replace(">","")   #remove the >
		#new_id = ">" + timestamp + "_" + words[0] + "\n"
		#out_file.write(new_id)
	else: #this is the seq
		sequence[seq_count - 1] = sequence[seq_count - 1] + line
		#out_file.write(line)  
	
 
	#read another line
	line = fasta_file.readline()
	



#close the files
fasta_file.close()


#open the file with the taxonomies
in_file = open(rep_set_tax_assignments_path, "r")  #open read only
out_file = open(new_fasta_file, "w")
tax_line_count = 0

#read each line
taxonomy_line = in_file.readline()
while taxonomy_line:
	#print "Reading taxonomy line ", tax_line_count
	tax_line_count = tax_line_count + 1
	words = taxonomy_line.split()  #splits on whitespace
	acession = words[0]
	words.remove(words[0]) #remove first element
	words.pop() #remove last element
	words.pop()
	while len(words) < taxonomy_depth:
		words.append(";Other")
	taxonomy = ""
	#concat the words int 1 word
	for i in words:
		taxonomy = taxonomy + i

	#find acession in the fasta file header
	header_index = 0
	found = False
	for i in header:		
		if i.startswith('>' + acession):
                   	#print "i = ", i
			#print "acession = ", acession
			header[header_index] = header[header_index] + ' ' + taxonomy + "\n"
			found = True
			break
		header_index = header_index + 1

	#could write header[header_index] and sequence[header_index] to outputfile
	#then delete these from the header and sequence lists
	#then you wont search through the the headers already added
	#in case there are some headers left at end you can print these later
	#they will not be in the same order
        if not found:
		print "acession number " + acession + " was not found in rep_set.fna"
		taxonomy_line = in_file.readline()
		continue

	out_file.write(header[header_index])
        out_file.write(sequence[header_index])
	del header[header_index]
        del sequence[header_index]

	#print words  #print words to last
	#print taxonomy
        #print acession
	#print header[header_index]
	#sys.exit(0) #test exit to see value

	#if tax_line_count == 100:
        #	break

	taxonomy_line = in_file.readline()

#if there are any sequences that did not get a taxonomy added to the header line
#write them to the output file
if len(header) > 0:
	print "Writing " + str(len(header)) + " sequences without taxonomy to output file"

index = 0;
for header_item in header:
	out_file.write(header_item + "\n")
        out_file.write(sequence[index])
      	index = index + 1


#write the new fasta file

#out_file = open(new_fasta_file, "w")

#index = 0;
#for header_item in header:
#	out_file.write(header_item)
#        out_file.write(sequence[index])
#      	index = index + 1


out_file.close()
in_file.close()

#print results to screen
print 'Lines read = ', line_count
print 'Sequences read = ', seq_count
print 'taxonomy file lines read = ', #print results to screen
print 'Lines read = ', line_count
print 'Sequences read = ', seq_count

print "Script finished...."
