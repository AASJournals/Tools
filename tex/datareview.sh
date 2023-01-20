# datareview.sh
#
# - grep latex source for specific terms
# - create HTML versions of lines for review  
#
# LaTeX Source (change as appropriate => vi `which datareview.sh`
#       Reviews/new.ms.tex
#
# Dependencies:
#       gnu grep   : for colors
#       ansi2html  : to convert ANSI colors to HTML
#       pandoc     : to convert LaTeX to other output (HTML)
#       latexpand  : clean up files
#
#   Written by AAMN on 2015/02/12
#       2015-02-16 : added pandoc conversion of LaTeX source to HTML
#       2015-02-17 : added documentation; tweaked GNU color codes
#       2015-05-19 : consolidate data review editing to Reviews/
#       2016-12-02 : added 'suite' to code grep
#       2018-05-01 : added 'framework' because of snoopy
#       2022-01-22 : added latexpand due to eJP requirements
#
##############################################################################
# gnu grep params
#
# software: 'algorithm\|software\|suite\|code\|program\|package\|ASCL\|github\|pipeline\|routine\|framework'
# data:     'FITS\|DOI\|doi\|epository\|tar\.gz\|upplementa\|figset\|nimation\|ovie\|ideo\|online'
# links:    'http\|ftp\|rsync\|smtp\|ssh\|www\|\\url'
# colors: 
#       ms=01;31  {Matching string Selected line}
#       mc=01;37  {Matching string Context line}
#       sl=43     {whole Selected Lines}
#       cx=00;30  {whole Context Lines}
#       fn=35     {File Name}
#       ln=01;35  {Line Number}
#       bn=32     {Byte Number}
#       se=36     {SEparator}
##############################################################################

export GREP_COLORS="ms=01;31:mc=01;37:sl=43:cx=00;30:fn=35:ln=01;35:bn=32:se=36"

d=${PWD##*/} 

# setup Reviews with Review manuscript version, create web accessible figures
mkdir -p Reviews
wait

echo "% date := `date "+%Y-%m-%d%n"` " >| Reviews/new.ms.tex ; wait
echo "% editor := August Muench <august.muench@aas.org> " >> Reviews/new.ms.tex ; wait
echo "% prior version (name) := $1 " >> Reviews/new.ms.tex ; wait
echo "% prior version (timestamp:iso) := `gls -l --time-style=full-iso $1 | awk '{print$6" "$7}'`" >> Reviews/new.ms.tex ; wait
echo "% prior version (hash:MD5) := `md5 $1 | awk '{print$4}'` " >> Reviews/new.ms.tex ; wait
echo "% processing performed := latexpand" >> Reviews/new.ms.tex ; wait
echo "% " >> Reviews/new.ms.tex ; wait
echo "  " >> Reviews/new.ms.tex ; wait

# if meta already exists then assume you had to run dos2unix and copy original meta over
if [[ -e Reviews/meta.txt ]]; then
     sed 's/latexpand/latexpand\; dos2unix/g' Reviews/meta.txt >| Reviews/new.ms.tex ; wait
fi

# if meta.txt doesn't exist assume this is the first pass and save the meta
if [[ ! -e Reviews/meta.txt ]]; then
    cp -p Reviews/new.ms.tex Reviews/meta.txt ; wait
fi


latexpand $1 >| Reviews/latexpand.tex; wait
latexpand $1 >> Reviews/new.ms.tex; wait
#cat $1 >> Reviews/new.ms.tex

# grab manuscript related files, ignoring the certain types: tex, pdf
echo $1 | sed 's/\.tex//g' | xargs -n 1 -I {} find . -name "{}.*" | awk '$1!~/\.tex/ && $1!~/\.pdf/' | xargs -n 1 -I {} cp {} Reviews/
wait

# make sure to get the input files like tex and bib
cp -p *.bib Reviews/ ; wait
cp -p *.tex Reviews/ ; wait
wait

# try to find figures and convert to PNGs
# \ls *.eps | sed 's/.eps//g' | xargs -n 1 -I {} sh -c 'echo "converting {}.eps => Reviews/{}.png"; convert {}.eps Reviews/{}.png; wait; '
\cp -p *.eps Reviews/ ; wait
# \ls *.ps | sed 's/.ps//g' | xargs -n 1 -I {} sh -c 'echo "converting {}.ps => Reviews/{}.png"; convert {}.ps Reviews/{}.png; wait; '
\cp -p *.ps Reviews/ ; wait
# \ls *.jpg | sed 's/.jpg//g' | xargs -n 1 -I {} sh -c 'echo "converting {}.jpg => Reviews/{}.png"; convert {}.jpg Reviews/{}.png; wait; '
\cp -p *.jpg Reviews/ ; wait
\cp -p *.jpeg Reviews/ ; wait
# \ls *.png | sed 's/.png//g' | xargs -n 1 -I {} sh -c 'echo "converting {}.png => Reviews/{}.png"; convert {}.png Reviews/{}.png; wait; '
\cp -p *.png Reviews/ ; wait
# \gfind ./ -maxdepth 1 -iname "f*pdf" -printf '%f\n' | \
#   sed 's/\.pdf//g' | \
#   xargs -n 1 -I {} sh -c 'echo "converting {}.pdf => Reviews/{}.png"; convert {}.pdf Reviews/{}.png; wait;'
\cp -p *.pdf Reviews/ ; wait
wait

echo 'finished copying files'

# check for non-ascii characters
if ggrep -P '[^\x00-\x7f]' Reviews/new.ms.tex; then
    echo ''
    echo '*************************************'
    echo '**** non-ascii characters exist *****'
    echo ''
    ggrep --line-number -P '[^\x00-\x7f]' Reviews/new.ms.tex
    echo ''
    echo '**** non-ascii characters exist *****'
    echo '*************************************'
    echo ''
fi

if ggrep -a -v '^.*$' Reviews/new.ms.tex; then
    echo ''
    echo '*************************************'
    echo '**** non-ascii characters exist *****'
    echo ''
    ggrep --line-number -a -v '^.*$' Reviews/new.ms.tex
    echo ''
    echo '**** non-ascii characters exist *****'
    echo '*************************************'
    echo ''
fi

echo 'finished checking for bad characters'

# source
#pandoc -s --verbose Reviews/new.ms.tex -t html5 -o Reviews/ms.html
# wait
# 
# echo 'finished pandoc'

# software
ggrep --text --ignore-case --color=never --line-number --context=2 \
'algorithm\|software\|suite\|code\|program\|package\|ASCL\|github\|pipeline\|routine\|framework' \
Reviews/new.ms.tex >| \
Reviews/software_review.txt
wait

ggrep --text --ignore-case --color=always --line-number --context=2 \
'algorithm\|software\|suite\|code\|program\|package\|ASCL\|github\|pipeline\|routine\|framework' \
Reviews/new.ms.tex | \
ansi2html --scheme=osx --title='Software: '$d --light-background --markup-lines >| \
Reviews/software_review.html
wait

# data
ggrep --text --color=never --line-number --context=2 \
'FITS\|DOI\|doi\|epository\|tar\.gz\|upplementa\|figset\|nimation\|ovie\|ideo\|online' \
Reviews/new.ms.tex >| \
Reviews/data_review.txt
wait

ggrep --text --color=always --line-number --context=2 \
'FITS\|DOI\|doi\|epository\|tar\.gz\|upplementa\|figset\|nimation\|ovie\|ideo\|online' \
Reviews/new.ms.tex | \
ansi2html --scheme=osx --title='Data: '$d --light-background >| \
Reviews/data_review.html
wait

# links
ggrep --text --ignore-case --color=never --line-number --context=2 \
'http\|ftp\|rsync\|smtp\|ssh\|www\|\\url' \
Reviews/new.ms.tex >| \
Reviews/links_review.txt
wait

ggrep --text --ignore-case --color=always --line-number --context=2 \
'http\|ftp\|rsync\|smtp\|ssh\|www\|\\url' \
Reviews/new.ms.tex | \
ansi2html --linkify --scheme=osx --title='Links: '$d --light-background >| \
Reviews/links_review.html
wait

# echo 'opening pandoc file'
# open Reviews/ms.html
# sleep 0.5

echo 'opening reviews'
open Reviews/links_review.html
sleep 0.5

echo 'opening reviews'
open Reviews/software_review.html
sleep 0.5

echo 'opening reviews'
open Reviews/data_review.html
sleep 0.5

echo 'done with '$d

