#! /usr/bin/env python                                                                    

# Ver: Tue Sep  8 21:30:50 UTC 2020

# todo
#  - overcome 2000 row limit from astroquery
#  - add \object tag creation option
#  - fix? output byte strings maybe
#  - fix "perfect" comparison to remove extra spaces from Input & Simbad names
#  - move from astroquery.utils.tap.core to pyvo
  
import os, sys

from astropy.table import Table
from astroquery.utils.tap.core import TapPlus


def main():
    """
    Main script for validating names with astroquery.
    
    simbad-tap.py filename <stats>
    
    Parameters
    ----------
    filename : file with 1 column that is a list of object names. no header
    options: 
        stats   : print summary stats on exit
        nosave  : skip saving the output
    """
    if len(sys.argv) < 2:
        print("")
        print("-------------------------------------------------------------------------------")
        print(" This toolkit is for . ")
        print("")
        print(" > simbad-tap.py filename <options: stats|nosave|verbose>")
        print("")
        print(" options  ")
        print("   stats   : dump matching stats to command line.")
        print("   nosave  : skip saving output.")
        print("-------------------------------------------------------------------------------")
        print("")
        return

    p = len(sys.argv) > 2 and sys.argv[2:] or ""
    
    verbose = 'verbose' in p and True or False

    # check input
    filename = sys.argv[1]
    if os.path.isfile(filename):
        if verbose:
            print ("File {:s} exists".format(filename))
    else:
        print ("File does not exist")
        return
    # check output
    ofile = 'simbad-tap-output.csv'
    if os.path.isfile(ofile) and ('nosave' not in p):
        print ("Ouptut file {:s} exists. Disabling save".format(ofile))
        p.append('nosave')


    # this is for Simbad which accepts anonymous public uploads for joins
    tapurl = "http://simbad.u-strasbg.fr:80/simbad/sim-tap"
    simbad = TapPlus(url=tapurl, verbose=verbose)

    # this is the topcat query I wrote from the Simbad ADQL example.
    # "sources" the input table name
    # "inputnames" is the column of sources with the names
    query = "SELECT sources.inputnames AS MyID, ident.id AS SimbadId, basic.coo_bibcode \
              FROM TAP_UPLOAD.sources LEFT OUTER JOIN ident ON ident.id = sources.inputnames \
              LEFT OUTER JOIN basic ON ident.oidref = basic.oid"

    # the data are typically a undelimited list of names with no header line. 
    # trick is a useless delimiter
    sources = Table.read(filename, format="ascii.no_header", delimiter="|", names=["inputnames"]) 

    # simbad.upload_table(upload_resource=sources, table_name='sources')
    j = simbad.launch_job(query=query, upload_resource=sources, upload_table_name='sources', verbose=verbose)

    r = j.get_results()        

    # save if we can
    if 'nosave' not in p:
        r.write("simbad-tap-output.csv", format="ascii.csv", overwrite=True)  
    
    # simple stats
    if 'stats' in p:
        print("-------------------------------------------------------------------------------")
        print("")
        bad = sum(r['simbadid'] == b'') # blank matches == no alias matches
        perfect = sum(r['simbadid'] == r['myid'])
        good = len(r) # some kind of match. I could check to see MyID == SimbadId
        inlen = len(sources)
        print('TAP output contained {:d} of the {:d} input rows.'.format(good, inlen))
        print('There were {:d} matches ({:2.1%}) and {:d} unmatched ({:2.1%}).'.format(inlen-bad, (inlen-bad)/inlen, bad, (bad)/inlen))
        print('Of the matches {:d} ({:2.1%}) were exact name matches.'.format(perfect, perfect/(inlen-bad)))
        print('The remaining matches were to Simbad aliases ({:d}, {:2.1%}).'.format(inlen-bad-perfect, (inlen-bad-perfect)/(inlen-bad)))
        print("")
        print("-------------------------------------------------------------------------------")




if __name__ == '__main__': 
    main()
