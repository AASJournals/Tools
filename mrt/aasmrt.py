#! /usr/bin/env python

import os, sys

from astropy.table import Table

def main():
    """
    Main script for processing ADS/CDS MRT files.
    
    aasmrt.py infile <options> 
    
    Parameters
    ----------
    infile : str, an ADS/CDS MRT file
    options: 
        data  : print data table to terminal
        html  : open data table in browser
         csv  : dump data to csv version of input
       <none> : if no option given then print astropy table info to terminal
    
    """
    if len(sys.argv) < 2:
        print("")
        print("-------------------------------------------------------------------------------")
        print(" This toolkit is checking or converting an AAS/CDS table in astropy. ")
        print("")
        print(" > aasmrt.py infile <options: csv|data|html|<none>>")
        print("")
        print(" options  ")
        print("    csv  : dump data to csv version of input")
        print("   data  : print data table to terminal")
        print("   html  : open data table in browser")
        print("   info  : print table and column")
        print("  <none> : if no option given then print basic table info to terminal")
        print("-------------------------------------------------------------------------------")
        print("")
        return

    v = sys.argv[1]
    p = len(sys.argv) > 2 and sys.argv[2] or ""

    data = Table.read(v, format="ascii.cds")

    print("")
    print("-------------------------------------------------------------------------------")
    print("aasmrt.py checking...")
    print("")
    print("Type: ",p)
    print("File: ",v)
    print("Rows: ",len(data))
    print("Cols: ",len(data.colnames))
    print("")
    if p == 'html':
        data.show_in_browser()
    elif p == 'data':
        print(data)
    elif p == 'csv':
        sur, ext = os.path.splitext(v)
        data.write(sur+".csv", format="ascii.csv", overwrite=False)
    elif p == 'info':
        print(data.info)
    else:
        print("")
        
if __name__ == '__main__': 
    main()



