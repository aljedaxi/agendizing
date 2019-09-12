"""
    jacob's magical agendizing software.
"""

import datetime
from jinja2 import Template, Environment
from jinja2_latexing import latex
from yml_to_tex import yml_to_tex
import argparse

TEMPLATE = "agenda.tex"

def get_metadata(in_data):
    for i, agendum in enumerate(in_data['agenda']):
        if not isinstance(agendum['body'], str):
            in_data['agenda'][i]['body'] = yml_to_tex.data_to_tex(agendum['body'], depth=1)
    return in_data

def format_to_title_body(agenda_section):
    agenda = [
        {'title': key, 'body': value} for key, value in agenda_section.items()
    ]
    return agenda

def main(infiles=("vars.yml",), basic=False):
    for filename in infiles:
        import yaml

        in_data = yaml.safe_load(open(filename).read())

        if basic:
            in_data['agenda'] = format_to_title_body(in_data['agenda'])

        META = get_metadata(in_data)

        try:
            outfile = META['outfile']
        except:
            outfile = "default.tex"

        latex.write_out(
            latex.fill(TEMPLATE, META),
            f"{datetime.datetime.now().isoformat().split('T')[0]}_{outfile}",
            latex=True,
            externalize="junk_drawer",
            backup="archives"
        )

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('metafile', metavar='M', type=str, nargs='*',
                        help='file with the metadata')
    args = parser.parse_args()
    main(infiles=args.metafile, basic=True)
