#!/usr/bin/env python
import csv
import os
import argparse


def run_s1(
    case_dir='.',
    sasa_dir='examples',
    infile='Test_SASA.csv',
    outfile='Test_SASA_all.csv'
):
    """
    Process SASA features and compute S1 terms.

    Parameters
    ----------
    case_dir : str
        Case root directory
    sasa_dir : str
        Directory containing Test_SASA.csv (default: examples)
    infile : str
        Input SASA CSV file name
    outfile : str
        Output CSV file name (written to case_dir)
    """

    inpath = os.path.join(case_dir, sasa_dir, infile)
    outpath = os.path.join(case_dir, outfile)

    if not os.path.isfile(inpath):
        raise RuntimeError(f'Input file not found: {inpath}')

    with open(inpath, newline='') as fin:
        reader = list(csv.reader(fin))

    header = reader[0]
    data = reader[1:]

    # Extend header
    extra_cols = [
        'A.P','A.N','A.DA','A.D','A.A',
        'A.AR','A.H','A.PL','A.HA','A.SA'
    ]
    header = header + extra_cols + ['Sap', 'Sp', 'Ssol']

    with open(outpath, 'w', newline='') as fout:
        writer = csv.writer(fout)
        writer.writerow(header)

        for row in data:
            c = row.copy()
            A_vals = []

            # A = P2 - P2dl - P2dp
            for j in range(1, 11):
                a1 = float(row[j])
                b1 = float(row[j + 10])
                c1 = float(row[j + 20])
                diff = a1 - b1 - c1
                A_vals.append(diff)
                c.append(diff)

            # Sap / Sp / Ssol
            sa = (
                A_vals[-1] + A_vals[-2] + A_vals[-4] +
                A_vals[-5] + A_vals[-6] + A_vals[-7] +
                A_vals[-8] + A_vals[-9] + A_vals[-10]
            )
            sp = A_vals[-3]
            ssol = (-0.1152) * sa + 0.0304 * sp

            c.extend([sa, sp, ssol])

            # 输出统一两位小数
            out_row = []
            for v in c:
                if isinstance(v, float):
                    out_row.append(f"{v:.2f}")
                else:
                    out_row.append(v)

            writer.writerow(out_row)


def main():
    parser = argparse.ArgumentParser(
        description='Compute S1 features for MM_S pipeline'
    )
    parser.add_argument(
        '--case-dir', default='.',
        help='Case root directory'
    )
    parser.add_argument(
        '--sasa-dir', default='examples',
        help='Directory containing Test_SASA.csv (default: examples)'
    )
    parser.add_argument(
        '--infile', default='Test_SASA.csv',
        help='Input SASA CSV filename'
    )
    parser.add_argument(
        '--outfile', default='Test_SASA_all.csv',
        help='Output CSV filename (written to case dir)'
    )

    args = parser.parse_args()

    run_s1(
        case_dir=args.case_dir,
        sasa_dir=args.sasa_dir,
        infile=args.infile,
        outfile=args.outfile
    )


if __name__ == '__main__':
    main()
