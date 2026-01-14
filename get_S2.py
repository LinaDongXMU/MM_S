#!/usr/bin/env python
import os
import csv
import argparse


def read_mol2(filename):
    atoms = []
    bonds = []
    H_atoms = set()

    with open(filename, 'r') as f:
        lines = f.readlines()

    read_atoms = False
    read_bonds = False

    for line in lines:
        if line.startswith("@<TRIPOS>ATOM"):
            read_atoms = True
            continue
        if line.startswith("@<TRIPOS>BOND"):
            read_atoms = False
            read_bonds = True
            continue
        if line.startswith("@<TRIPOS>SUBSTRUCTURE"):
            read_bonds = False

        if read_atoms:
            fields = line.split()
            if len(fields) < 6:
                continue
            atom_id = int(fields[0])
            atom_name = fields[1]
            x, y, z = map(float, fields[2:5])
            atoms.append((atom_id, atom_name, x, y, z))
            if atom_name.upper().startswith('H'):
                H_atoms.add(atom_id)

        elif read_bonds:
            fields = line.split()
            if len(fields) < 4:
                continue
            bond_id = int(fields[0])
            atom1_id = int(fields[1])
            atom2_id = int(fields[2])
            bond_type = fields[3]
            bonds.append((bond_id, atom1_id, atom2_id, bond_type))

    # remove bonds involving hydrogens
    bonds = [
        b for b in bonds
        if b[1] not in H_atoms and b[2] not in H_atoms
    ]

    return atoms, bonds


def count_rotatable_bonds(atoms, bonds):
    """
    Count rotatable bonds based on simple topology:
    - single or double bond
    - terminal on both sides
    """
    rotatable = 0

    for bond in bonds:
        bond_type = bond[3]
        if bond_type not in ('1', '2'):
            continue

        a1, a2 = bond[1], bond[2]
        neigh1 = 0
        neigh2 = 0

        for b in bonds:
            if b == bond:
                continue
            if a1 in b[1:3]:
                neigh1 += 1
            if a2 in b[1:3]:
                neigh2 += 1

        if neigh1 == 1 and neigh2 == 1:
            rotatable += 1

    return rotatable


def run_s2(examples_dir='examples', outfile='RB.csv'):
    outpath = outfile

    with open(outpath, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(['id', 'rb', 'atoms'])

        for case in os.listdir(examples_dir):
            mol2 = os.path.join(
                examples_dir, case, f'{case}_ligand.mol2'
            )
            if not os.path.isfile(mol2):
                continue

            try:
                atoms, bonds = read_mol2(mol2)
                rb = count_rotatable_bonds(atoms, bonds)
                writer.writerow([case, rb, len(atoms)])
            except Exception as e:
                print(f'Warning: failed on {case}: {e}')


def main():
    parser = argparse.ArgumentParser(
        description='Compute rotatable bonds for MM_S pipeline'
    )
    parser.add_argument(
        '--examples-dir', default='examples',
        help='Directory containing example cases'
    )
    parser.add_argument(
        '--outfile', default='RB.csv',
        help='Output RB CSV file'
    )

    args = parser.parse_args()
    run_s2(args.examples_dir, args.outfile)


if __name__ == '__main__':
    main()
