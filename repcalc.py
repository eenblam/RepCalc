#!/usr/bin/env python3
"""
Authors:  Ben Elam, Tamer Aldwairi, Andy Perkins
Contact:  bae53@msstate.edu
"""

import re
import sys
import modules.rcfuncs as rcf

if __name__ == '__main__':
    # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    # Parse input

    if len(sys.argv) == 1:
        # No command line arguments specified.  Launch GUI.
        import modules.rcgraphics as rcg
        rcg.maingui()
    else:
        # Arguments specified.  Do not launch GUI.
        # Command line mode

        # Check for options
        #NOTE For some reason, using 'is not' instead of '!=' has the opposite
        # result when comparing the '-' character from sys.argv, even after
        # coercing it explicitly to a string.
        if sys.argv[1][0] != '-':
            print("Options error - Please specify options using the '-' character")
            print("\tand specifying all options within the first argument to repcalc.")
            sys.exit(1)

        options = sys.argv[1].strip('-')

        opt_dict = {}
        for i in 'abcABt':
            opt_dict[i] = i in options

        # 'a','b', and 'c' switch analysis type.
        # Only one of the three may be given as an option.

        # 'A' handles binary case indicating TE input format.
        # If A is given, custom TE column numbers are expected.
        # Otherwise, these values default to [0, 1, 2, 3].

        # 'B' handles binary case indicating RoI input format.
        # If A is given, custom RoI column numbers are expected.
        # Otherwise, these values default to [0, 1, 2, 3].

        # 't' handles binary case indicating 
        # whether or not to transpose matrix output data.
        # Default is ??? #TODO

        # Handle mutually exclusive options:
        # One is required, and only one is allowed.
        optslist = [opt_dict['a'], opt_dict['b'], opt_dict['c']]
        test = len([x for x in optslist if x]) is 1
        if not test:
            print("Options error - multiple analyses specified.")
            sys.exit(1)

        # Toss out first two command line arguments.
        args = sys.argv[2:]

        commands = {'a': rcf.analysisA,
            'b': rcf.analysisB,
            'c': rcf.analysisC,}

        for letter in 'abc':
            if opt_dict[letter]:
                result = commands[letter](args, opt_dict)

        result_dict = {0: 'Program complete.',
            1: 'Column indexing error.  No output written.',
            2: 'Column value error.  Please provide positive integer values for column indices.  No output written.',
            3: 'Length error.  No output written.  Please provide a valid length.',}

        print(result_dict[result])
