import argparse
import agenda

if __name__ == "__main__":
    TEMPLATE = "agenda.tex"

    parser = argparse.ArgumentParser()
    parser.add_argument('metafile', metavar='M', type=str, nargs='*',
                        help='files with the metadata')
    args = parser.parse_args()
    agenda.main(infiles=args.metafile, basic=True)
