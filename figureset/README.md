Simple python3 tool to create figure set markup using a YAML configuration
file and CSV input translation table. Assumes each figure set caption is
similar to the others. 

File | Explanation  
:--- | :----------  
`figset.tex` | AASTeX < 6 macros 
   |  (add to .tex header)
`figure1set.tex` | Example Figure Set  
`make_translation.sh` | table parsing script  
`newfigureset.py` | python newfigureset.py translation.yaml  
`translation.csv` | Example CSV input to translation.yaml  
`translation.yaml` | Figure Set parameters   
