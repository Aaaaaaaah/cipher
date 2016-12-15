import json
import math
import numpy.random
import traceback
import ahocorasick
import argparse

# file
this_file_name="ciphertext"

# letter => mat_poss
letter_T=2.0
base_order="etaoinhsrdlucmwgfypbkvxjzq"
base_param=[1174913,862434,756008,716854,641296,628461,581186,579195,545403,425327,395178,272732,238199,237851,218206,206612,198625,187488,170499,143028,92313,87447,17096,15347,9200,8102]
base_mat=[[math.exp(-(math.log(1.*base_param[i]/base_param[j]))**2/letter_T**2) for j in range(26)]for i in range(26)]
for i in range(26):
    base_mat[i][i]=0
flatten=sum(base_mat,[])
flatten_sum=sum(flatten)
mat_poss=map(lambda x:x/flatten_sum,flatten)

# word => ac_auto
word_T=10000000000
ddict=json.load(open("wordlist/ddict","r"))
multi_order={i[0]:i[1]*2**len(i[0]) for i in ddict.iteritems()}
ac_auto = ahocorasick.Automaton()
for word in multi_order.iterkeys():
    i=str(word)
    ac_auto.add_word(i,i)
ac_auto.make_automaton()

def get_content(file_name):
    content_file=open(file_name,"r")
    data=content_file.read()
    content_file.close()
    return data

def put_content(data,file_name):
    content_file=open(file_name,"w")
    content_file.write(data)
    content_file.close()

def count_letter(file_name):
    data=get_content(file_name)
    letter="qwertyuioplkjhgfdsazxcvbnm"
    return {i:data.count(i) for i in letter}

def get_init(file_name):
    data=count_letter(file_name).items()
    data.sort(key=lambda x:x[1],reverse=True)
    this_order="".join([i[0] for i in data])
    return {this_order[i]:base_order[i] for i in range(26)}

def replace_str(src,rule):
    return "".join(map(lambda x:rule[x] if rule.has_key(x) else x,src))

def mutate_order(src_rule):
    key=numpy.random.choice(range(26**2),p=mat_poss)
    a=key/26
    b=key%26
    ans=src_rule.copy()
    temp=ans[base_order[a]]
    ans[base_order[a]]=ans[base_order[b]]
    ans[base_order[b]]=temp
    return ans

def energy_func(data,rule=None):
    if rule!=None:
        data=replace_str(data,rule)
    energy=0
    data=str(data)
    for pos, word in ac_auto.iter(data):
        energy+=multi_order[word]
    return energy

def anneal(times=1000,back=None,starter=1):
    if back==None:
        data=get_content(this_file_name)
        rule=get_init(this_file_name)
        E = energy_func(data)
        EP = 10*E
        EM = E
        ruleM = rule
        rules=[rule]
        Es=[E]
    else:
        data=get_content(this_file_name)
        Es=back[2]
        rules=back[1]
        EP=Es[0]*10
        EM=max(Es)
        ruleM=rules[Es.index(EM)]
    try:
      for i in range(times):
        T=(1-1.*i/times)*starter*word_T
        Ts=[math.exp((j-EP)/T) for j in Es]
        Tsum = sum(Ts)
        Ts=map(lambda x:x/Tsum,Ts)
        #to_p="";
        #for j in Ts:to_p+="%.2f "%(j*(i+1));
        #print to_p
        s_rule=numpy.random.choice(rules,p=Ts)
        temp_rule=mutate_order(s_rule)
        while temp_rule in rules:
            temp_rule=mutate_order(temp_rule)
        temp_E=energy_func(data,temp_rule)
        rules.append(temp_rule)
        Es.append(temp_E)
        if i!=0:
            print "Step : %i\tE : %d"%(i,temp_E)
        if temp_E>EM:
            EM=temp_E
            ruleM=temp_rule
    except:
        traceback.print_exc()
    return [replace_str(data,ruleM),rules,Es]

if __name__=="__main__":
    parser = argparse.ArgumentParser(description='cipher')
    parser.add_argument('--times','-t',dest='times',type=int,default=1000,help='times to anneal')
    parser.add_argument('--file','-f',dest='file',required=True,help='file to store',)
    parser.add_argument('--starter','-s',dest='starter',type=float,default=1.)
    args = parser.parse_args()
    try:
        back=json.load(open(args.file,"r"))
    except IOError:
        back=None
    ans=anneal(times=args.times,back=back,starter=args.starter)
    json.dump(ans,open(args.file,"w"))
