The `figureset.py` script is a simple python3 tool to create figure set markup using a YAML configuration
file (`translation.yaml`) and CSV input translation table. The script assumes each the captions of all the figure set elements are structured the same, but this can be modified in how the CSV translation and YAML files are setup.

File | Explanation  
:--- | :----------  
`figureset.py` | The main scrip run by `> python figureset.py translation.yaml`
`translation.yaml` | Figure set configuration parameters 
`translation.csv` | Example CSV input to translation.yaml  
`figset.tex` | AASTeX < 6 macros. Add these macros to the header of your main .tex file.
`test1set.tex` | Example Figure Set. Running `> python figureset.py translation.yaml` should produce a file `fig1set.tex` that is identical to `test1set.tex`  
`make_translation.sh` | Table parsing script  

