#! /usr/bin/env python

# from astropy.table import Table
import sys
import ads
from pprint import pprint

def doiclean(doi):
    prefs = ["doi:",
            "https://doi.org/",
            "https://dx.doi.org/",
            "doi.og",
           ]
    for pref in prefs:
        if pref in doi: doi = doi.strip(pref)
    return doi


def main():
    """
    Main script for getting bibcodes from ADS
    
    doi2ads.py doi <options>
    
    Parameters
    ----------
    doi : str, digital object identifier in parsed (non-url) form
    options: 
        dump    : dump all the predefined keys
        bibcode : find the ads bibcode for the DOI
        
    
    """
    if len(sys.argv) < 2:
        print("")
        print("-------------------------------------------------------------------------------")
        print(" This toolkit is for getting ADS keys from a DOI")
        print("")
        print(" > doi2ads.py doi <options: dump|bibcode")
        print("")
        print(" options  ")
        print("   dump    : dump all the predefined keys")
        print("   bibcode : find the ads bibcode for the DOI)")
        print("-------------------------------------------------------------------------------")
        print("")
        return
    
    fl = ['id','bibcode','doi']
    
    if len(sys.argv) > 2:
        if sys.argv[2] == 'dump':
            doit = "dump"
        elif sys.argv[2] not in fl:
            fl.append(sys.argv[2])
            doit = sys.argv[2]
        else:
            doit = sys.argv[2]
    else:
        doit = "bibcode"

    doi = sys.argv[1]

    q = ads.SearchQuery(doi=doiclean(doi), fl=fl)
    
    for p in q:
        p
    
    if doit == "dump":
        pprint(p.__dict__)
    else:
        pprint(p.__getattribute__(doit))
    
if __name__ == '__main__': 
    main()

