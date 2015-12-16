# example script to turn datatable into translation table
grep JW datafile1.txt | awk '{print$1".pdf,"$1","$7"\n"$1"rgb.pdf,"$1","$7}' >| translation.csv
