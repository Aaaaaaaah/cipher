import json
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("--file","-f",dest="file",required=True)
args=parser.parse_args()
data=json.load(open(args.file,"r"))
print(len(data[2]))
ruleM=data[1][data[2].index(max(data[2]))]
print("".join(map(lambda x:ruleM[x],"qwertyuioplkjhgfdsazxcvbnm")))
