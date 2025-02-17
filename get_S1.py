import csv

results=open('./Test_SASA.csv')
resultsReader=csv.reader(results)
resultsData=list(resultsReader)
add=open('./Test_SASA_all.csv','w',newline='')
addWriter=csv.writer(add)

d=resultsData[0]
e=['A.P','A.N','A.DA','A.D','A.A','A.AR','A.H','A.PL','A.HA','A.SA']
d=d+e
d.append('Sap')
d.append('Sp')
d.append('Ssol')
addWriter.writerow(d)

for i in resultsData[1:]:
    c=i
    for j in range(1,11):
        a1=float(i[j])
        b1=float(i[j+10])
        c1=float(i[j+20])
        d1="%.2f"%(a1-b1-c1)
        c.append(d1)
    sa1=float(c[-1])+float(c[-2])+float(c[-4])+float(c[-5])+float(c[-6])+float(c[-7])+float(c[-8])+float(c[-9])+float(c[-10])
    sp1=float(c[-3])
    ssol="%.4f"%((-0.1152)*sa1+0.0304*sp1)
    c.append(sa1)
    c.append(sp1)
    c.append(ssol)
    addWriter.writerow(c)


results.close()
add.close()