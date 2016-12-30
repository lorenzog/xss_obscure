#!/usr/bin/env python
"""Turns a function and a payload into semi-obfuscated javascript for fun and profit."""
import argparse
import os


def main():
    p = argparse.ArgumentParser()
    p.add_argument('function', help="The function to call e.g. 'alert'")
    p.add_argument('-p', '--parameter', help="The parameter to the function e.g. 'XSS'")
    p.add_argument('-o', '--outfile')
    p.add_argument('-f', '--force', action='store_true')
    args = p.parse_args()

    encoded_s = list()

    for c in args.function:
        # Turn each letter into its ascii value
        # Then multiply 'A' for that value, and append 'undefined'
        _v = "A" * ord(c)
        encoded_s.append("'{}undefined'.indexOf()".format(_v))
        # so that 'AAAundefined'.indexOf() = 3

    payload = list()
    for p in encoded_s:
        # var chr = String.fromCharCode(97 + xxx
        payload.append('String.fromCharCode({})'.format(p))

    # var f = window['alert'];
    # var g = 'the parameter';
    # // will alert 'the parameter'
    # f(g);
    final = "var f = window[{}];".format('+'.join(payload))
    final += "\nf()\n"

    outfile = args.outfile
    if outfile is not None:
        if os.path.exists(outfile) and not args.force:
            raise SystemExit("Destination exists. Use '-f' to overwrite")
        with open(outfile, 'w') as f:
            f.write(final)
        print "Output saved to {}".format(outfile)
    else:
        print final


if __name__ == '__main__':
    main()