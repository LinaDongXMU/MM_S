#!/usr/bin/env python
import os
import csv
import argparse
import shutil

from sasa.featureSASA import sasa


def run_sasa(case_dir='.', examples_dir='examples'):
    examples_path = os.path.join(case_dir, examples_dir)
    if not os.path.isdir(examples_path):
        raise RuntimeError(f'examples directory not found: {examples_path}')

    out_csv = os.path.join(examples_path, 'Test_SASA.csv')

    header = [
        'id','P2.P','P2.N','P2.DA','P2.D','P2.A','P2.AR','P2.H','P2.PL',
        'P2.HA','P2.SA',
        'P2dl.P','P2dl.N','P2dl.DA','P2dl.D','P2dl.A',
        'P2dl.AR','P2dl.H','P2dl.PL','P2dl.HA','P2dl.SA',
        'P2dp.P','P2dp.N','P2dp.DA','P2dp.D','P2dp.A',
        'P2dp.AR','P2dp.H','P2dp.PL','P2dp.HA','P2dp.SA'
    ]

    faults = []

    with open(out_csv, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(header)

        for pdb_id in os.listdir(examples_path):
            pdb_dir = os.path.join(examples_path, pdb_id)
            if not os.path.isdir(pdb_dir):
                continue

            prot = os.path.join(pdb_dir, f'{pdb_id}_protein.pdb')
            lig  = os.path.join(pdb_dir, f'{pdb_id}_ligand.mol2')

            if not (os.path.isfile(prot) and os.path.isfile(lig)):
                faults.append(pdb_id)
                continue

            # 保留你原来的行为
            shutil.copy(
                prot,
                os.path.join(pdb_dir, f'{pdb_id}_protein_all.pdb')
            )

            try:
                sasa_obj = sasa(
                    datadir=pdb_dir,
                    prot=f'{pdb_id}_protein.pdb',
                    lig=f'{pdb_id}_ligand.mol2'
                )

                # 原始 float 结果
                values = (
                    sasa_obj.sasa +       # complex
                    sasa_obj.sasa_lig +   # ligand
                    sasa_obj.sasa_pro     # protein
                )

                # 统一保留两位小数
                row = [pdb_id] + [f"{v:.2f}" for v in values]

                writer.writerow(row)

            except Exception as e:
                print(f'Warning: SASA failed for {pdb_id}: {e}')
                faults.append(pdb_id)

    return faults


def main():
    parser = argparse.ArgumentParser(
        description='Run MSMS-based SASA for MM_S (2-decimal output)'
    )
    parser.add_argument('--case-dir', default='.')
    parser.add_argument('--examples-dir', default='examples')

    args = parser.parse_args()
    faults = run_sasa(args.case_dir, args.examples_dir)

    if faults:
        print('Failed cases:', faults)


if __name__ == '__main__':
    main()