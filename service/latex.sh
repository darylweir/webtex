#!/bin/bash

#Find relevant files for latex
#??? Delete non zipped files
#Unzip latex files => files should be nammed <Filename>.tar.gz, only 1 per folder

localDirs=("./")

latexString=".*.tar.gz"
errorFile="MAIN_ERRORS.txt"


for i in *
do
	if [ -d $i ]; 
	then
		cd $i

		#probably should delete anything that is not gz 
		for FILE in *
		do	
			if [[ ! ${FILE} =~ ${latexString} ]];
			then
				echo deleting ${FILE}
				rm -rf ${FILE}
			fi 
		done

		# unzip the files
		for FILE in *
		do	
			if [[ ${FILE} =~ ${latexString} ]];
			then
				echo decompress ${FILE}
				tar -zxvf ${FILE}
			fi 
		done

		pdflatex -interaction batchmode -file-line-error main.tex
		pdflatex -interaction batchmode -file-line-error main.tex
		bibtex -terse main
		pdflatex -interaction batchmode -file-line-error main.tex
		
		rm -rf $errorFile
		#now look for errors
		touch $errorFile


		echo ----------------------- >> $errorFile
		echo OUTRIGHT ERRORS         >> $errorFile
		echo ----------------------- >> $errorFile
		cat main.log | grep  "\.tex:">> $errorFile

		echo ----------------------- >> $errorFile
		echo UNDERFULL AND OVERFULL  >> $errorFile
		echo ----------------------- >> $errorFile
		cat main.log | grep  erfull  >> $errorFile

		echo ----------------------- >> $errorFile		
		echo MISSING STUFF           >> $errorFile
		echo ----------------------- >> $errorFile		
		cat main.log | grep  issing  >> $errorFile

		
		#go home
		cd -
	else
		echo is not a directory  $i
	fi
done

