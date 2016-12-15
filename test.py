import argparse

parser = argparse.ArgumentParser(description='cipher')
parser.add_argument('--times','-t',dest='times',type=int,default=1000,help='times to anneal')
parser.add_argument('--file','-f',dest='file',required=True,help='file to store',)
args = parser.parse_args()
print args.times
print args.file
