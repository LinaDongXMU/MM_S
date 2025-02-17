import sys

def read_mol2(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    atoms = []
    bonds = []
    Hlist = []
    read_atoms = False
    read_bonds = False
    for line in lines:
        if read_atoms:
            if line.strip() == "" or line.startswith("@<TRIPOS>BOND"):
                read_atoms = False
            else:
                    fields = line.split()
                    atom_id = int(fields[0])
                    atom_name = fields[1]
                    x = float(fields[2])
                    y = float(fields[3])
                    z = float(fields[4])
                    atoms.append((atom_id, atom_name, x, y, z))
        elif line.startswith("@<TRIPOS>ATOM"):
            read_atoms = True
    for line in lines:
        if read_bonds:
            if line.strip() == "" or line.startswith('@<TRIPOS>SUBSTRUCTURE'):
                read_bonds = False
            else:
                    fields = line.split()
                    bond_id = int(fields[0])
                    atom1_id = int(fields[1])
                    atom2_id = int(fields[2])
                    bond_type = str(fields[3])
                    bonds.append((bond_id, atom1_id, atom2_id, bond_type))
        elif line.startswith("@<TRIPOS>BOND"):
            read_bonds = True
    #print(atoms,bonds)
    for i in atoms:
        if i[1] == "H":
            Hlist.append(i[0])
    for k in bonds:
        if k[1] or k[2] in Hlist:
            bonds.remove(k)
    return atoms, bonds

def count_rotatable_bonds(atoms, bonds):
    rotatable_bonds = []
    for bond in bonds:
        bond_type = bond[3]
        if bond_type == str(1) or bond_type == str(2):  # single or double bond
            atom1_id = bond[1]
            atom2_id = bond[2]
            atom1_neighbors = []
            atom2_neighbors = []
            for neighbor_bond in bonds:
                if neighbor_bond != bond:
                    if neighbor_bond[1] == atom1_id:
                        atom1_neighbors.append(neighbor_bond[2])
                    elif neighbor_bond[2] == atom1_id:
                        atom1_neighbors.append(neighbor_bond[1])
                    elif neighbor_bond[1] == atom2_id:
                        atom2_neighbors.append(neighbor_bond[2])
                    elif neighbor_bond[2] == atom2_id:
                        atom2_neighbors.append(neighbor_bond[1])
            if len(atom1_neighbors) == 1 and len(atom2_neighbors) == 1:
                rotatable_bonds.append(bond[0])
    return len(rotatable_bonds)

if __name__ == "__main__":
    filename = sys.argv[1]
    atoms, bonds = read_mol2(filename)
    num_rotatable_bonds = count_rotatable_bonds(atoms, bonds)
    print("Number of rotatable bonds:", num_rotatable_bonds)

import os
import csv

path='./examples'
add=open('./RB.csv','w',newline='')
addWriter=csv.writer(add)
d=['id','rb','atoms']
addWriter.writerow(d)
for i in os.listdir(path):
    try:
        c=[]
        mol2=path+'/'+str(i)+'/'+str(i)+'_ligand.mol2'
        atoms, bonds = read_mol2(mol2)
        num_rotatable_bonds = count_rotatable_bonds(atoms, bonds)
        c.append(i)
        c.append(num_rotatable_bonds)
        c.append(len(atoms))
        addWriter.writerow(c)
    except:
        print(i)

add.close()