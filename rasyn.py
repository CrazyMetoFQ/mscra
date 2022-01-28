"""
provides input to the asyncronous lib
run throught the cli

works in ipython through this work around
"""

from asyn import asyn as ayn
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("base_link")
parser.add_argument("min_")
parser.add_argument("max_")
parser.add_argument("single")
parser.add_argument("raw_csv")


parser.add_argument("base_path")

parser.add_argument("save_As")
parser.add_argument("file_Format")

parser.add_argument("do_print")
parser.add_argument("round_to")

parser.add_argument("img_args")
parser.add_argument("debug__")
parser.add_argument("ikey")

args = parser.parse_args()

if args.do_print == "True":
  print(1 ,": " ,args, '\n')
else: pass

#changing str to none or int
imar = args.img_args.split(',')
for  sno,ima in enumerate(imar):
  if ima == "None":
    imar[sno] = None
  else: 
    imar[sno] = int(ima)


if args.debug__ == "False":
  args.debug__ = False
elif args.debug__ == "True":
  args.debug__ = True
else:
  print("eror")
  
  
if args.raw_csv == "False":
  args.raw_csv = False
elif args.raw_csv == "True":
  args.raw_csv = True
else:
  print("eror")
  

# base_link where the number will change in the link such as ch-1, ch-2 put {}
base_link = args.base_link
# putting numbers in the link
if args.single != "True" and not args.raw_csv:
  pg_links = [base_link.format(i) for i in range(int(args.min_),int(args.max_))]
else:
  
  if args.raw_csv:
    with open("mscra/pg_links_.csv") as f:
      rcsv = f.read()
      
    pg_links = [s.replace(" ", "") for s in rcsv.split(",")]
   
  else: 
      pg_links = [base_link]

      
# path to where the pdfs will reside
ch_path = args.base_path

# # base_link where the number will change in the link such as ch-1, ch-2 put {}
# base_link = "https://www.readdemonslayerarc.com/demon-slayer-chapter-{}/"



# MAIN FUNCTION
ayn.main_func(pg_links, 
              ch_path, 
              (args.save_As, args.file_Format),
              int(args.round_to),
              args.debug__,
              args.ikey,
              imgs_kwargs={'strt':imar[0],'stp':imar[1],'step':imar[2] }
              )
