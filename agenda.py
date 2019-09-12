"""
    jacob's magical agendizing software.
"""

import datetime
from jinja2 import Template, Environment
from jinja2_latexing import latex
from yml_to_tex import yml_to_tex
import argparse

TEMPLATE = "agenda.tex"

def get_metadata(in_data, keys=('agenda',)):
    for key in keys:
        for i, agendum in enumerate(in_data[key]):
            if not isinstance(agendum['body'], str):
                in_data[key][i]['body'] = yml_to_tex.data_to_tex(agendum['body'], depth=1)
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

        if in_data['appendices']:
            keys = ('agenda', 'appendices')
        else:
            keys = ('agenda')

        if basic:
            for key in keys:
                in_data[key] = format_to_title_body(in_data[key])

        META = get_metadata(in_data, keys=keys)

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
