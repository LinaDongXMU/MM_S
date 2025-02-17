import os
import shutil
import csv

path='./examples'
list1=os.listdir(path)
fault=[]
add=open(os.path.join(path,'Test_SASA.csv'),'a')
addWriter=csv.writer(add)
title=['id','P2.P','P2.N','P2.DA','P2.D','P2.A','P2.AR','P2.H','P2.PL','P2.HA','P2.SA','P2dl.P','P2dl.N','P2dl.DA','P2dl.D','P2dl.A','P2dl.AR','P2dl.H','P2dl.PL','P2dl.HA','P2dl.SA','P2dp.P','P2dp.N','P2dp.DA','P2dp.D','P2dp.A','P2dp.AR','P2dp.H','P2dp.PL','P2dp.HA','P2dp.SA']
addWriter.writerow(title)
for filename in list1:
    shutil.copy(os.path.join(path,filename,str(filename)+'_protein.pdb'),os.path.join(path,filename,str(filename)+'_protein_all.pdb'))
    j=os.path.join(path,filename)
    cmd='python run_DXGB.py --runfeatures --datadir '+j+' --pdbid '+filename+' --average'
    os.system(cmd)
    try:
        k=os.path.join(path,filename,'SASA.csv')
        results=open(k)
        resultsReader=csv.reader(results)
        resultsData=list(resultsReader)
        a=resultsData[1]
        #add=open(os.path.join(path,'Test_SASA.csv'),'a')
        addWriter=csv.writer(add)
        addWriter.writerow(a)
    except:
        fault.append(filename)
results.close()
add.close()
print(fault)