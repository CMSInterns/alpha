


import re
from netmiko import ConnectHandler

#src=input(" Enter Source ")
#dst=input(" Enter destination ")
src='10.8.14.14'
dst='10.1.7.1'

class router(object):
    def __init__(self,name):
        self.name=name
        self.entry=set()
        self.exit=set()
        self.dictint=dict()
        self.gennodedict=dict()

    def addentry(self,ent):
        self.entry.add(ent)

    def addconnect(self,conn):
        self.handle=conn

    def addexit(self,ext):
        self.exit.add(ext)

    def adddictip(self,interf,ip):
        if interf not in self.dictint.keys():
            self.dictint[interf]=dict()
        self.dictint[interf]['ip']=ip
    def objprint(self):
        print(" Name "+self.name)
        print(" Entry interfaces ")
        print(self.entry)
        print(" Exit interfaces ")
        print(self.exit)
        print(" Interface Dictionary ")
        print(self.dictint)
        print()
        print(" General Node Information ")
        print(self.gennodedict)
        
        print("------------------------------")
        
arr=[]
count=0

setofnames=set()
dictofnames={}
dictofobj={}

name=''
s={src}
now=src
honame=set()
exit=dict()
entry=dict()
entryrev=dict()
ls=[]
ls.append(now)
extract=set()
p=''
boo=True
while(len(s)>0):
    now=ls[0]
    boo=True
    while boo:
        try:
            ssh=ConnectHandler(device_type="cisco_ios",host=now,username="rit",password="pan")
            boo=False
        except:
            boo=True
            print(" Connection error, trying again ")


    #ret=ssh.send_command("en")
    boo=True
    while boo:
        try:
            name=ssh.find_prompt()
            boo=False
        except Exception as e:
            print(str(e))
            print("Trying again")
            boo=True
        if not(re.match("^[A-Z]{3}-{2}[A-Z]{2}[0-9]{2}#{1}$",name)):
            boo=True
            print(" Name Received Incorrect- Trying again "+name)
    
    name=name[:-1]


    if name not in setofnames:
        setofnames.add(name)
        dictofnames[name]=count
        k=router(name)
        arr.append(k)
        dictofobj[name]=k
        dictofobj[name].addconnect(ssh)
        count+=1
        
    
    print(name)
    honame.add(name)
    print("dict of names ")
    print(dictofnames)
    boo=True
    while boo:
        try:
            ret=ssh.send_command("sh ip route "+dst+" | include Known via")
            boo=False
        except Exception as e:
            boo=True
            print(" Exception Handled- Trying again")
        print(" return from sh ip route | inc known via ")
        print(ret)
        if not ret:
            print("Trying again")
            boo=True
        elif len(ret.split())>=3:
            boo=False
        else:
            print("Trying Again sh ip route")
            boo=True
    print(" Name "+name+" show ip route | i known via")
    print(ret)
    ret=ret.split()
    prot=ret[2][1:]
    print("PROT- "+prot)
    if prot=='bgp':
        dst1=dst
        fl=0
        print("Prot BGP")
        while fl!=2:
            boo=True
            while boo:
                try:
                    ret=ssh.send_command("sh ip route "+dst1)
                    boo=False
                except:
                    boo=True
                    print(" Exception Handled- Trying again")

                if not ret:
                    boo=True
                    print("Trying again")
                elif len(ret.split("\n"))>1:
                    boo=False
                else:
                    boo=True
                    print("Trying again")
            print("\tBGP- sh ip route for dst "+dst1)
            print(ret)
            ret=ret.split("\n")
            fl=0
            for i in ret:
                i=i.split()
                print("splitting ret")
                print(i)
                if i[0]=='*':
                    nxt=i[1]
                    if nxt=='directly':
                        x=i.index('via')
                        hop=i[x+1]
                        fl=2
                        break
                    elif re.match('^(?:[0-9]{1,3}\.){3}([0-9]{1,3})',nxt):
                        dst1=nxt
                        if nxt[-1]==',':
                            dst1=nxt[:-1]

                        fl=1
                        break
        print("Name "+name+" BGP: next hop "+dst1+" exit interface "+hop)
        extract.add(dst1)
        s.add(dst1)
        ls.append(dst1)
        p=''
        p=hop+' '+dst1
        if name not in exit.keys():
            exit[name]=set()
        exit[name].add(p)
        boo=True
        while boo:
            try:    
                ret=ssh.send_command("sh ip int brief | include "+hop)
                boo=False
            except:
                print(" Exception Handled- Trying again")
                boo=True
            if not ret:
                boo=True
            elif len(ret.split())<3:
                boo=True
                
        ip=ret.split()[1]



        ctobj=dictofnames[name]
        arr[ctobj].addexit(p)
        dictofobj[name].adddictip(hop,ip)
        



        p=''
            
    elif prot=='connected",':
        boo=True
        while boo:
            try:
                ret=ssh.send_command("sh ip route "+dst+" | include directly")
                boo=False
            except:
                boo=True
                print(" Exception Handled- Trying again")

            if not ret:
                boo=True
                print("Trying again")
            elif len(ret.split())>3:
                boo=False
            else:
                print("Trying again")
                boo=True
        
        print("Connected route- show ip route| i directly ")
        print(ret)
        ret=ret.split()
        p=''
        x=ret.index('via')
        p=ret[x+1]
        hop=ret[x+1]
        p=p+' directly'
        if name not in exit.keys():
                exit[name]=set()
        exit[name].add(p)
        print(" Name "+name+" is connected to dst via "+p)

        ctobj=dictofnames[name]
        arr[ctobj].addexit(p)
        boo=True
        while boo:
            try:    
                ret=ssh.send_command("sh ip int brief | include "+hop)
                boo=False
            except:
                print(" Exception Handled- Trying again")
                boo=True
            if not ret:
                boo=True
            elif len(ret.split())<3:
                boo=True
                
        ip=ret.split()[1]

        dictofobj[name].adddictip(hop,ip)

        p=''

    else:
        boo=True
        while boo:
            try:
                ret=ssh.send_command("sh ip route "+dst+" | include via")
                boo=False
            except:
                boo=True
                print(" Exception Handled- Trying again")

            if not ret:
                boo=True
                print("Trying again")
            elif len(ret.split('\n'))>1:
                boo=False
            else:
                print("Trying again")
                boo=True
        print("output from sh ip route | inc via ")
        print(ret)
        print("Splitting")
        ret=ret.split('\n')
        for i in ret:
            i=i.split()
            print(i)
            t=0
            for j in i:
                #print(j)
                if re.match('^(?:[0-9]{1,3}\.){3}([0-9]{1,3})',j):
                    print("extract- "+j[:-1])
                    j=j[:-1]
                    if j not in extract:
                        extract.add(j)
                        s.add(j)
                        ls.append(j)     
                    t=1
               
                if t==1:
                    num=i.index('via')
                    p=i[num+1]
                    hop=i[num+1]
                    p=p+' '+j
                    if name not in exit.keys():
                        exit[name]=set()
              
                    exit[name].add(p)

                    ctobj=dictofnames[name]
                    #print("ctobj "+ctobj)
                    arr[ctobj].addexit(p)
                    print("hop ",hop)
                    boo=True
                    ret1=""
                    while boo:
                        try:    
                            ret1=ssh.send_command("sh ip int brief | include "+hop)
                            boo=False
                        except:
                            print(" Exception Handled- Trying again")
                            boo=True
                        print(" Return ")
                        print(ret1)
                        if not ret1:
                            boo=True
                        elif len(ret1.split())<3:
                            boo=True
                
                    ip=ret1.split()[1]
                    dictofobj[name].adddictip(hop,ip)

                    p=''
                    break
    extract.clear()
    s.remove(now)
    ls.remove(now)
 
    if now!=src:
        boo=True
        while boo:
            try:    
                ret=ssh.send_command("sh ip int brief | include "+now)
                boo=False
            except:
                print(" Exception Handled- Trying again")
                boo=True
            print(" return from sh ip int brief | inc dest at dest ")
            print(ret)
            if len(ret.split())>2:
                boo=False
            else:
                print("Trying Again")
                boo=True
        print(" Name "+name+" sh ip int brief | include "+now)
        print(ret)
        ret=ret.split()
 
        if name not in entry.keys():
            entry[name]=set()
        p=''
        p=ret[0]
        hop=ret[0]
        ip=now
        p=p+' '+now
        entry[name].add(p)

        ctobj=dictofnames[name]
        arr[ctobj].addentry(p)
        dictofobj[name].adddictip(hop,ip)
        

        entryrev[now]=set()
        p=''
        p=name+' '+ret[0]
        entryrev[now].add(p)
     
boo=True
while boo:
        try:
            ssh=ConnectHandler(device_type="cisco_ios",host=dst,username="rit",password="pan")
            boo=False
        except:
            boo=True
            print(" Connection error, trying again ")



boo=True
while boo:
    try:
        name=ssh.find_prompt()
        boo=False
    except Exception as e:
        print(str(e))
        print("Find Prompt errTrying Again")
        boo=True
        
name=name[:-1]
honame.add(name)

if name not in setofnames:
    setofnames.add(name)
    dictofnames[name]=count
    k1=router(name)
    arr.append(k1)
    dictofobj[name]=k1
    dictofobj[name].addconnect(ssh)
    count+=1


boo=True
while boo:
    try:
        ret=ssh.send_command("sh ip int brief | include "+dst)
        boo=False
    except:
        print(" Exception Handled- Trying again")
        boo=True
    print(" return from sh ip int brief | inc dest ")
    print(ret)
    if not ret:
        boo=True
    elif len(ret.split())>2:
        boo=False
    else:
        print("Trying Again")
        boo=True

ret=ret.split()
#print(ret)
if name not in entry.keys():
    entry[name]=set()
p=''
p=ret[0]
p=p+' '+'directly'
entry[name].add(p)

hop=ret[0]
ip=dst

ctobj=dictofnames[name]
arr[ctobj].addentry(p)
dictofobj[name].adddictip(hop,ip)

p=''
entryrev['directly']=set()
p=name+' '+ret[0]
entryrev['directly'].add(p)

print("Entry interfaces ")
print(entry)
print()
print(" Exit  interfaces ")
print(exit)

print()
print(" Entry Reverse ")
print(entryrev)




for nme in setofnames:
    ssh=dictofobj[nme].handle


    #general_node_parameters
    boo=True
    while boo:
        try:
            ret=ssh.send_command("sh proc cpu | ex 0.0",use_textfsm=True)
            boo=False
        except:
            print("Exception Raised 1, Trying again")
            boo=True
            
    #parse the return from show environment and take out parameters like
    ct1=0
    for line in ret:
        if ct1==0:
            cpu={}
            cpu['cpu_5_sec']=line['cpu_5_sec']
            cpu['cpu_1_min']=line['cpu_1_min']
            cpu['cpu_5_min']=line['cpu_5_min']
            dictofobj[nme].gennodedict['cpu']=cpu                
            
        combine={}
        combine['process']=line['process']
        combine['proc_5_sec']=line['proc_5_sec']
        combine['proc_1_min']=line['proc_1_min']
        combine['proc_5_min']=line['proc_5_min']
        dictofobj[nme].gennodedict[line['pid']]=combine      
        ct1+=1


#parsing sh ip route

    boo=True
    while boo:
        try:
            ret=ssh.send_command("sh ip route")
            boo=False
        except:
            print("Exception Raised 1, Trying again")
            boo=True
        print(ret)
        if not ret:
            boo=True
        else:
            boo=False

    ret=ret.split('\n')
    gen={}
    ct1=0
    print(ret)
    for line in ret:
        
        line2=line.split()
        
        if not(not(line2)) and line2[0]!='S' and line2[0]!='C' and line2[0]!='S*' and 'via' in line2:
            pos=line2.index('via')
            if line2[pos+2][0:2]=='00':
                ct1+=1
                gen[ct1]=line
                print(line)        
    dictofobj[nme].gennodedict['ip_route_00']=gen
                
    #keys for gen dict is just numbers with no significance. display only values        
    #dictofobj[nme].gennodedict['redundant_power']=
    
    
    




    #interface_level_details
    for interf in dictofobj[nme].dictint.keys():
        print(interf+" in loop ")
        boo=True
        while boo:
            try:
                ret=ssh.send_command("sh interfaces "+interf,use_textfsm=True)
                boo=False
            except:
                print("Exception Raised 1, Trying again")
                boo=True
                continue
            print(ret)
            if not ret:
                boo=True
            else:
                boo=False
        #Parse the sh interface output and get the crc and other things out
        print(ret)
        line={}
        for line in ret:
            x=line.keys()
            if 'crc' in x:
                dictofobj[nme].dictint[interf]['crc']=line['crc']
            if 'duplex' in x:
                dictofobj[nme].dictint[interf]['duplex']=line['duplex']
            if 'reliability' in x:
                dictofobj[nme].dictint[interf]['reliability']=line['reliability']
            if 'txload' in x:
                dictofobj[nme].dictint[interf]['txload']=line['txload']
            if 'rxload' in x:
                dictofobj[nme].dictint[interf]['rxload']=line['rxload']
            if 'speed' in x:
                dictofobj[nme].dictint[interf]['speed']=line['speed']
            if 'collisions' in x:
                dictofobj[nme].dictint[interf]['collisions']=line['collisions']
            if 'late_collision' in x:
                dictofobj[nme].dictint[interf]['late_collision']=line['late_collision']
            if 'overrun' in x:
                dictofobj[nme].dictint[interf]['overrun']=line['overrun']
            if 'interf_reset' in x:
                dictofobj[nme].dictint[interf]['interf_reset']=line['interf_reset']
            if 'input_errors' in x:
                dictofobj[nme].dictint[interf]['input_errors']=line['input_errors']
            if 'output_errors' in x:
                dictofobj[nme].dictint[interf]['output_errors']=line['output_errors']
            if 'frame' in x:
                dictofobj[nme].dictint[interf]['frame']=line['frame']
            if 'ignored' in x:
                dictofobj[nme].dictint[interf]['ignored']=line['ignored']
            if 'bandwidth' in x:
                dictofobj[nme].dictint[interf]['bandwidth']=line['bandwidth']
            if 'ignored' in x:
                dictofobj[nme].dictint[interf]['output_drops']=line['output_drops']
        



        """boo=True
        while boo:
            try:
                ret=ssh.send_command("sh controllers "+interf)
                boo=False
            except:
                print("Exception Raised 2, Trying again")
                boo=True
            if not ret:
                boo=True
            elif len(boo.split('\n'))<4:
                boo=True
            else:
                boo=False
        #parse the ret and get the required parameters


        dictofobj[nme].dictint[interf]['']=
        dictofobj[nme].dictint[interf]['']=
        dictofobj[nme].dictint[interf]['']=
        dictofobj[nme].dictint[interf]['']=
        dictofobj[nme].dictint[interf]['']="""
        

        
        

for i in arr:
    i.objprint()








                
        
        






