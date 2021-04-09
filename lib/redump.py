#!/usr/bin/env python
import argparse
import Serializer

parser = argparse.ArgumentParser(description='Parser')
parser.add_argument('inf', type=str, help='Input file')
parser.add_argument('outf', type=str, help='Output file')
parser.add_argument('outform', type=str, help='Output format')
args = parser.parse_args()

if args.inf.endswith('.json') and args.outform == 'JSON':
    pass
elif args.inf.endswith('.pickle') and args.outform == 'PICKLE':
    pass
elif args.inf.endswith('.yaml') and args.outform == 'YAML':
    pass
elif args.inf.endswith('.toml') and args.outform == 'TOML':
    pass
else:
    serial = Serializer.Serializer()
    if args.inf.endswith('.json'):
        serial.form = 'JSON'
    elif args.inf.endswith('.pickle'):
        serial.form = 'Pickle'
    elif args.inf.endswith('.yaml'):
        serial.form = 'Yaml'
    elif args.inf.endswith('.toml'):
        serial.form = 'Toml'
    serial.load(args.inf, False)
    data = serial.data
    serial.change_form(args.outform)
    serial.data = data
    serial.dump(args.outf, False)
