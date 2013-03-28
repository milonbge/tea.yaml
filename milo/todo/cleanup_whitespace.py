#!/usr/bin/env python

import sys

if len(sys.argv) == 1:
    sys.stderr.write('Please pass one or more filenames.')
    sys.exit()

for filename in sys.argv[1:]:

    infile = open(filename, 'r')
    data = infile.read()
    infile.close()

    output = []

    paren_depth = 0

    for index, char in enumerate(data):
    
        if char == '(':
            paren_depth += 1
        elif char == ')':
            paren_depth -= 1
        elif char == ' ' and paren_depth:

            #skip spaces after open-parens
            if data[index - 1] == '(':
                continue

            #skip spaces before open-parens
            if data[index + 1] == ')' and data[index - 1] != ' ':
                continue

            #skip spaces around '=' signs
            if data[index + 1:index + 2] == '= ':
                continue
            if data[index - 1:index + 1] == ' =':
                continue

        output.append(char)

    outfile = open(filename, 'w')
    outfile.write(''.join(output))
    outfile.close()
