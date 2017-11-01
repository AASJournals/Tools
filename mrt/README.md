The scripts provided here allow you to work with the [AAS](http://journals.aas.org/authors/MRT/
)/[CDS](http://cds.u-strasbg.fr/doc/catstd.htx
) machine readable format.

The simplest way to read the AAS/CDS format with `astropy` is: 

```
from astropy.table import Table
data = Table.read("dbf1.txt", format="ascii.cds")
```

File | Explanation  
:--- | :----------  
`aasmrt.py` | A python3 script to check, view, or convert the AAS MRT format using [astropy](http://www.astropy.org/).
