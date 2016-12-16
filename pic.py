import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--file","-f",dest="file",required=True)
args=parser.parse_args()
print(json.load(open(args.file,"r"))[2])

