#! /usr/bin/env python

import os, sys

from astroquery.ned import Ned
from astroquery.simbad import Simbad

def main():
    """
    Main script for validating names with astroquery.
    
    aas-names.py objectname <options> 
    
    Parameters
    ----------
    objectname : str
    options: 
        ned     : only print NED object information to terminal
        simbad  : only print Simbad object information to terminal
        show    : dump data to terminal
        quiet   : print tersely to the terminal
        csv     : dump data to csv version [not implemented]

       <none>   : if no option given then summarize object found info to terminal
    
    """
    if len(sys.argv) < 2:
        print("")
        print("-------------------------------------------------------------------------------")
        print(" This toolkit is for . ")
        print("")
        print(" > aas-names.py objectname <options: ned|simbad|show|quiet|csv|<none>>")
        print("")
        print(" options  ")
        print("   ned     : print summary NED object information to the terminal")
        print("   simbad  : print summary Simbad object information to the terminal")
        print("   show    : dump data to terminal.")
        print("   sameAs  : dump what the repository thinks the object is called.")
        print("   verbose : print verbosely to the terminal.")
        print("   csv     : dump data to csv version [not implemented]")
        print("-------------------------------------------------------------------------------")
        print("")
        return

    v = sys.argv[1]
    p = len(sys.argv) > 2 and sys.argv[2:] or ""

    if 'verbose' in p:
        print("")
        print("-------------------------------------------------------------------------------")
        print("aas-name.py checking...")
        print("")
        print("Object: ",v)
        print("Type: ",p)    
        print("")
        
    if 'ned' in p:
        try:
            neddata = Ned.query_object(v)
        except:
#           this is slightly wrong. The NED query can return an empty 
#           result or an error from the server. I'm not clear on why there
#           is a difference. 
            neddata = []
        if len(neddata) > 0: 
            if 'sameAs' in p: 
                print(v," sameAs ", neddata[0]['Object Name'], " in NED.")
            elif 'verbose' in p: 
                print("NED Objects: ",len(neddata))
            else: print(len(neddata))
            if 'show' in p: print(neddata)
        else: 
            if 'verbose':
                print(v," is not in NED.")
            else:
                print(0)
    elif 'simbad' in p:
        try:
            simdata = Simbad.query_object(v)
        except:
            simdata = []
        if simdata is not None: 
            if 'sameAs' in p: 
                print(v, " sameAs ", simdata[0]['MAIN_ID'].decode(), "in Simbad.") 
            elif 'verbose' in p: 
                print("Simbad Objects: ",len(simdata))
            else: print(len(simdata))
            if 'show' in p: print(simdata)
        else: 
            if 'verbose':
                print(v," is not in Simbad.")
            else:
                print(0)
    elif 'csv' in p:
          print("not implemented")
#         sur, ext = os.path.splitext(v)
#         data.write(sur+".csv", format="ascii.csv", overwrite=False)
    else:
        print("")
        
if __name__ == '__main__': 
    main()



