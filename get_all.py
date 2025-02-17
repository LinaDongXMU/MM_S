import csv

results=open('./gpbsa.csv')
resultsReader=csv.reader(results)
resultsData=list(resultsReader)
exp=open('./Test_SASA_all.csv')
expReader=csv.reader(exp)
expData=list(expReader)
exp1=open('./RB.csv')
expReader1=csv.reader(exp1)
expData1=list(expReader1)
add=open('./all.csv','w',newline='')
addWriter=csv.writer(add)

d=resultsData[0]
e=expData[0][1:]
g=expData1[0][1:]
h=['S-C','P-DP+S','G+S','P-DP+S_atoms','G+S_atoms']
f=d+e+g+h
addWriter.writerow(f)


for i in resultsData[1:]:
    a=i[0]
    for j in expData:
        b=j[0]
        if a==b:
            energy=i
            sasa=j[1:]
            c=energy+sasa
            for k in expData1:
                x=k[0]
                if x==b:
                    rb=k[1:]
                    c=c+rb
                    
                    sc=float(c[81])-1.76*float(c[82])+0.414*float(c[83])
                    ps=float(c[38])-float(c[37])+sc
                    gs=float(c[17])+sc
                    psa=ps-0.414*float(c[83])
                    gsa=gs-0.414*float(c[83])

                    c.append(sc)
                    c.append(ps)
                    c.append(gs)
                    c.append(psa)
                    c.append(gsa)
                    addWriter.writerow(c)

energylist=[]
for i in resultsData:
    a=i[0]
    energylist.append(a)
sasalist=[]
for j in expData:
    b=j[0]
    sasalist.append(b)
fault=[]
for k in energylist:
    if k not in sasalist:
        fault.append(k)
print(fault)
#print(len(fault))
results.close()
exp.close()
add.close()