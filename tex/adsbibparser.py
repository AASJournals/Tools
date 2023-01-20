#! /usr/bin/env python

import sys
from pybtex.database.input import bibtex

def bibclean(bibcode):
    URLs = ["http://adsabs.harvard.edu/abs/", 
            "https://ui.adsabs.harvard.edu/\#abs/",
            "http://cdsads.u-strasbg.fr/abs/",
            "http://ads.bao.ac.cn/abs/"
           ]
    for URL in URLs:
        if URL in bibcode: bibcode = bibcode.strip(URL)
    return bibcode

def main():
    """
    Main script for processing ADS bibtex
    
    adsbibparser.py infile <options> 
    
    Parameters
    ----------
    infile : str, a bibtex file from ADS
    options: 
        dump  : dump all the bibtex keys and ads bibcodes to the screen
        find  : find the ads bibcode for the key.
    
    """
    if len(sys.argv) < 2:
        print("")
        print("-------------------------------------------------------------------------------")
        print(" This toolkit is parsing ADS bibtext files")
        print("")
        print(" > absbibparser.py infile.bib <options: dump|find")
        print("")
        print(" options  ")
        print("   dump  : dump data to csv version of input")
        print("   find  : find the bibcode for a key (requires the key to be in the 3rd field)")
        print("-------------------------------------------------------------------------------")
        print("")
        return

    ifile = sys.argv[1]

    if len(sys.argv) > 2:
        if sys.argv[2] not in ["dump", "find"]:
            doit = "dump"
        else: 
            doit = sys.argv[2]
    else:
        doit = "dump"


    #open a bibtex file
    parser = bibtex.Parser()
    bibdata = parser.parse_file(ifile)

    if doit == "find":
        try: 
            b = bibdata.entries[sys.argv[3]].fields
            print(sys.argv[3], bibclean(b["adsurl"]))
        except:
            print(sys.argv[3], "unknown")
    else:
        #loop through the individual references
        for bib_id in bibdata.entries:
            b = bibdata.entries[bib_id].fields
            try:
                # change these lines to create a SQL insert
                bibcode = b["adsurl"]
            
                print(bib_id, bibclean(bibcode))
            # field may not exist for a reference
            except(KeyError):
                continue


if __name__ == '__main__': 
    main()

