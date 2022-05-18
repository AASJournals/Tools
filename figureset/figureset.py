
# coding: utf-8
import sys
import csv, yaml


# import yaml config
with open(sys.argv[1], "r") as stream:
    y = yaml.load(stream, Loader=yaml.FullLoader)

# open translation table
t = []
with open(y['translationfile'], "r") as tfile:
    treader = csv.reader(tfile)
    for row in treader:
        t.append(row)

# pad table rows to same length with strings
lt = max([len(row) for row in t])

markup = []
markup.append("\\figsetstart")
markup.append("\\figsetnum{{{0}}}".format(y['fignum']))
markup.append("\\figsettitle{{{0}}}".format(y['settitle']))
markup.append("")

ft = []
fn = 1
for i, row in enumerate(t):
    if row[1] == ft:
        markup.insert(len(markup)-3, "\\figsetplot{{{0}}}".format(row[0]))
    else:
        if len(row) < lt:
          row.extend((lt - len(row)) * [""])
          caption = ""
        else:
          caption = y['caption'].strip("\n")
        markup.append("\\figsetgrpstart")
        markup.append("\\figsetgrpnum{{{0}.{1}}}".format(y['fignum'], fn))
        markup.append("\\figsetgrptitle{{{0}}}".format(row[1]))
        markup.append("\\figsetplot{{{0}}}".format(row[0]))
        markup.append("\\figsetgrpnote{{{0}}}".format(caption.format(*row)))
        markup.append("\\figsetgrpend")
        markup.append("")
        fn = fn + 1
    ft = row[1]
    
markup.append("\\figsetend")

# write out
with open('fig{0}set.tex'.format(y['fignum']), mode='w', encoding='utf-8') as ofile:
    ofile.write('\n'.join(markup))
    ofile.write('\n')
        
        

