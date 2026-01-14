#!/usr/bin/env python
import csv
import argparse
import os


def read_csv_dict(path):
    """Read CSV into dict keyed by first column"""
    with open(path, newline='') as f:
        reader = list(csv.reader(f))
    header = reader[0]
    data = {row[0]: row for row in reader[1:]}
    return header, data


def run_all(case_dir='.',
            energy_csv='gpbsa.csv',
            sasa_csv='Test_SASA_all.csv',
            rb_csv='RB.csv',
            outfile='all.csv'):

    energy_h, energy_d = read_csv_dict(os.path.join(case_dir, energy_csv))
    sasa_h, sasa_d = read_csv_dict(os.path.join(case_dir, sasa_csv))
    rb_h, rb_d = read_csv_dict(os.path.join(case_dir, rb_csv))

    # Final header
    final_header = (
        energy_h +
        sasa_h[1:] +
        rb_h[1:] +
        ['S-C', 'P-DP+S', 'G+S', 'P-DP+S_atoms', 'G+S_atoms']
    )

    outpath = os.path.join(case_dir, outfile)
    with open(outpath, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(final_header)

        for cid, energy_row in energy_d.items():
            if cid not in sasa_d:
                print(f'Warning: missing SASA for {cid}')
                continue
            if cid not in rb_d:
                print(f'Warning: missing RB for {cid}')
                continue

            sasa_row = sasa_d[cid][1:]
            rb_row = rb_d[cid][1:]

            c = energy_row + sasa_row + rb_row

            # ---- Composite scores (same as original script) ----
            # Column meaning (based on original indexing):
            # c[81] : Sap
            # c[82] : Sp
            # c[83] : Ssol

            Sap = float(c[81])
            Sp  = float(c[82])
            Ssol = float(c[83])

            sc = Sap - 1.76 * Sp + 0.414 * Ssol
            ps = float(c[38]) - float(c[37]) + sc
            gs = float(c[17]) + sc
            psa = ps - 0.414 * Ssol
            gsa = gs - 0.414 * Ssol

            c.extend([sc, ps, gs, psa, gsa])
            writer.writerow(c)


def main():
    parser = argparse.ArgumentParser(
        description='Final aggregation step for MM_S pipeline'
    )
    parser.add_argument('--case-dir', default='.')
    parser.add_argument('--energy-csv', default='gpbsa.csv')
    parser.add_argument('--sasa-csv', default='Test_SASA_all.csv')
    parser.add_argument('--rb-csv', default='RB.csv')
    parser.add_argument('--outfile', default='all.csv')

    args = parser.parse_args()
    run_all(
        args.case_dir,
        args.energy_csv,
        args.sasa_csv,
        args.rb_csv,
        args.outfile
    )


if __name__ == '__main__':
    main()
