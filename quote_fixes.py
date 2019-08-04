import time
import os
import sys

# these variables will be changed with each protome, but stay constant throughout each run
Psvalue = 13
Psname= "Pholcidae/"
proteomefile= 'try.txt'
read1= "lane1-s007-indexRPI7-CAGATC-Sic3_VG_S7_L001_R1_001.fastq"
read2= "lane1-s007-indexRPI7-CAGATC-Sic3_VG_S7_L001_R2_001.fastq"

#this is so that later we can determine which are non-sus sequences (same proteome and label)
if Psvalue>9: 
	Psraw="s0" + str(Psvalue)
elif Psvalue<10:
	Psraw="s00" + str(Psvalue)

alignname="align" + str(Psvalue)

#code from Julia: cleans up files and creates individual files for each sequence
with open(proteomefile) as f:
	lines = f.readlines()
	subfile = 0
	for line in lines:
		if line[0] == '>':
			line = line.replace(".", "")
			line = line.replace("\n","")
			line = line.replace("|", "_")
			line = line.split(" ")[0]
			line = line[1::]
			with open('filenames.txt', 'a') as f: #this makes a new files called filenames.txt
				f.write(line + '.fasta' + '\n')
		else :
			next
with open(proteomefile) as f:
	lines = f.readlines()
	subfile = 0
	for line in lines:
		if line[0] == '>':
			line = line.replace(".", "")
			line = line.replace("|", "_") # must remove | and . characters, they confuse the computer
			line = line.split(" ")[0] # gets rid of annotations at the end of the seq name
			line = line[1::]
			line = line.replace("\n","")
			subfile = line + '.fasta'
			with open(subfile, 'w') as f:
				f.write('>' + line + '\n') 
		else :
				with open(subfile, 'a') as f:
					f.write(line)
					
#this is the loop, it should run a loop for every file 
directory= "/home/users/ellenrichards/"
os.system( "mkdir " + Psname)

for filename in os.listdir(directory):

	filename1 = "/home/users/ellenrichards/"  + filename 
	print(filename1)
	if filename.endswith(".fasta") and not filename.startswith(Psraw):
	
		#finds and sets mvalue (from filename)
		mvalue=filename.split("m")[1]
		mvalue=mvalue.split("\n") [0]
		mvalue=mvalue.split(".fasta")[0]	
		mvalue=str(mvalue)	
		
		#finds and sets svalue (from filename)
		svalue=filename.split("_")[0]
		svalue=svalue.split("0")[1] 
		svalue=str(svalue)
		alignname2= "align" + svalue	

		#this creates the folder and sub-folder for each file
		os.system ("mkdir " + mvalue)
		os.system ("mkdir " + mvalue + "/gd")
		
		#PROBLEM1: How do we automate raw read file selection???? 
		#for practice i've been putting the raw read file names, but obviously this changes every time, so I can't use this when it's running files with different s values. 
		#read3= 
		#read4= 
		
		os.path.join('/home/users/ellenrichards/' + mvalue + '/gd')
		genomeDir= '/home/users/ellenrichards/' + mvalue + '/gd'
		os.chdir(directory + "/" + mvalue)
		
		indexingstar='\"STAR --runThreadN 1 --runMode genomeGenerate --genomeDir \"' + genomeDir '+ \" --genomeFastaFiles \" '+ genomeFastaFiles + '\" --genomeSAindexNbases 2\"'
		indexing = "SGE_Batch -r 'genome_dir' -c " + indexingstar + " -P1"
		os.system(indexing)
		
		#EXITING: FATAL INPUT ERROR: empty value for parameter "genomeDir" in input "Command-Line" (this is the main error i'm getting)
		#SOLUTION: use non-empty value for this parameter (it's not empty)

		Psvalue = str(Psvalue)

		alignstar= "STAR --runMode alignReads --runThreadN 10 --genomeDir /home/users/ellenrichards/" + mvalue + "/gd --readFilesIn /home/users/ellenrichards/binfordlab/raw_reads/" + read1 + " /home/users/ellenrichards/binfordlab/raw_reads/" + read2 + " --outFileNamePrefix /home/users/ellenrichards/" + mvalue + "/" + Psvalue +  "--outSAMtype BAM SortedByCoordinate --limitBAMsortRAM 40000000000 "
		aligning = "SGE_Batch -r" + alignname + " -c " + alignstar + " -P 10" 
		os.system(aligning)

		alignstar2= "STAR --runMode alignReads --runThreadN 10 --genomeDir /home/users/ellenrichards/" + mvalue + "/gd --readFilesIn /home/users/ellenrichards/binfordlab/raw_reads/" + read3 + " /home/users/ellenrichards/binfordlab/raw_reads/" + read4 + " --outFileNamePrefix /home/users/ellenrichards/" + mvalue + "/" + Psvalue +  " --outSAMtype BAM SortedByCoordinate --limitBAMsortRAM 40000000000" 
		aligining2= "SGE_Batch -r "+ alignname2 +" -c " + alignstar2 + "-P 10" 
		os.system(aligning2)
		
		#this is moving the completed files into a folder by the name of the proteome and is resetting the directory to the original one
		os.chdir(directory)
		os.system("mv " + filename + " " + Psname + "/")
	else: 
		next
		
		#PROBLEM2: How do we have an automated output for this information? 
			#i. this takes 8-10 minutes
			#ii. it comes out as a file, I don't know how to output into an excel file