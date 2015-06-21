"""
rcfuncs.py:  Functions imported by repcalc.py and rcgraphics.py

Manifest: 
    getconfig(filename)
        Reads config file then returns mapping of search terms to replacements.
    gethelp(filename)
        Reads formatted help file; returns mapping of topics to help strings.

    fasgenome(fas_filename, replace_dict)
        Reads .fas file; returns mapping {TEClass}>{Subclass}>[Frequency, Length].
    outgenome(fas_filename, out_filename, classes, region_length)
        Writes .tbl file based on output from fasgenome().

    pidensity(pi_filename)
        Reads RoI data; returns mapping {Chromosome Label}>[TE Start,TE End].
    fasdensity(fas_filename, chromosomes, replace_dict)
        Reads .fas file; returns map {TEClass}>{Subclass}>[Freq., OverlapLength].
    outdensity(fas_filename, out_filename, classes, region_length)
        Writes .tbl file based on output from fasdensity().

    fasmatrix(fas_filename, replace_dict)
        Reads .fas file; returns {Chromosome}>{TEClass}>{Sub}>[Pairs]>(Start,End).
    pimatrix(pi_filename, te_dict)
        Reads RoI data. Returns: dict of TE x RoI %-overlaps, list of keys.
    outmatrix(out_filename, region_dict, region_keys)
        Takes output from pimatrix() to write TE x RoI %-overlaps to file.
    transpose(filename)
        Rewrites filename using the transpose of tab-delimited data in filename.
"""

import re
import os
import sys
LOCAL_PATH = os.path.dirname(os.path.realpath(__file__)).strip('modules')

###############################################################################
# Application functions

def getconfig(filename):
    """
    Take config filename.  Return dict of replacements.
    """

    def checkformat(string):
        """
        Check format of string.  Return ???
        """
        equal = '=' in string and not ':' in string
        colon = ':' in string and not '=' in string
        if equal:
            try:
                splits = re.split('=', string)
                replacement = splits[1].strip()
                format = (len(splits) == 2) and (len(replacement) > 0)
            except IndexError:
                print("Equal index error") #TESTCODE
                format = False
        elif colon:
            try:
                splits = re.split(':', string)
                replacement = splits[1].strip()
                format = len(replacement) > 0
            except IndexError:
                format = False
        else:
            # Error.  Not a comment, but also not valid line.
            return(False, False)
    
        formatted = (equal or colon) and format
        return(formatted, equal)

    comments = [';', '#']
    config_dict = {'explicit': {},
        'wildcard class': {},
        'wildcard subclass': {}}

    with open(filename, 'r') as f:
        for full_line in f:
            line = full_line.strip()

            # Skip blank lines and comment-only lines
            if not line:
                continue

            first_char = line[0]
            if first_char in comments:
                continue

            # Remove comments
            line = re.split(';', re.split('#', line)[0])[0]
        
            strings = re.split('/', line)
            # Strip new whitespace
            strings = [x.strip() for x in strings]

            formatted, equal_sign = checkformat(line)

            if formatted:

                if equal_sign:
                    terms = re.split('=', line)
                else:
                    terms = re.split(':', line)

                terms = [x.strip() for x in terms]
                match_term = terms[0]
                replace_term = terms[1]

                match_splits = re.split('/', match_term)
                match_splits = [x.strip() for x in match_splits]
                replace_splits = re.split('/', replace_term)
                replace_splits = [x.strip() for x in replace_splits]

                ###
                # Parse match term
                # Case match based on number of /
                slashes = len(match_splits) - 1

                if slashes > 1:
                    # Too many slashes.  Formatting error.
                    print("Bad config line in " + filename + ":\n\t" + full_line)
            
                #elif slashes == 0:
                    # Shouldn't be possible; blank lines should have already been skipped.
            
                elif slashes == 0:
                    # Simple case.  Just a class.  Assume no wildcards.
                    config_dict["explicit"][match_term] = replace_term
                    continue
            
                elif slashes == 1:
                    # Complex case.  Class and subclass.
                    match_left = match_splits[0]
                    match_right = match_splits[1]
                    wildcard_class = False
                    wildcard_subclass = False

                    # Is left $?
                    if match_left == '$':
                        wildcard_class = True

                    # Is right *?
                    if match_right == '*':
                        wildcard_subclass = True

                    # Check for explicit class
                    if not (wildcard_class or wildcard_subclass):
                        config_dict['explicit'][match_term] = replace_term
                        continue

                    # Were both wildcards given?
                    if (wildcard_class and wildcard_subclass):
                        print("Error - Both wildcards * and $ were given.  Omitting term.")
                        continue

                    # Handle last cases.
                    if wildcard_class:
                        config_dict['wildcard class'][match_right] = replace_splits[0:2]
                    elif wildcard_subclass:
                        config_dict['wildcard subclass'][match_left] = replace_splits[0:2]

                else:
                    #TODO error message.  Somehow, left_splits is negative.
                    print("Bad config line in " + filename + ":\n\t" + full_line)
                    print("Class/subclass structure violated.")
                    sys.exit(1)

            else:
                #TODO error message.
                print("Bad config line format in " + filename + ":\n\t" + full_line)
                sys.exit(1)

    return(config_dict)

def configreplace(string, config_dict):
    """
    Take a class.  Return replacement class or original class.
    """

    string = string.strip()
    output = string
    strings = re.split('/', string)
    slashes = len(strings) - 1

    if slashes > 1:
        #TODO error message.
        print("Formatting error:  string %s does not meet input requirements for transposable element class/subclass labels." % string)
        sys.exit(1)

    elif slashes == 0:
        # Simple case.  Just a class.  Check against explicit matches.
        for key in config_dict['explicit']:
            if key == string:
                return(config_dict['explicit'][key])

        return(string)
  
    elif slashes == 1:
        # Complex case.  Class and subclass.
        # First, see if it's explicit.
        for key in config_dict['explicit']:
            if key == string:
                return config_dict['explicit'][key]

        # If not, check wildcards.

        class_key = strings[0]
        subclass_key = strings[1]

        wcc = subclass_key in config_dict['wildcard class']
        wcsc = class_key in config_dict['wildcard subclass']

        if wcc and wcsc:
            print(
                "Processing error:  TE annotation class %s matches " % string +
                "patterns for both class and subclass.  In such cases, " +
                "class matches are given priority."
                )
            # i.e. prioritize an explicit class match
            wcc = False

        if wcc:
            replacements = config_dict['wildcard class'][subclass_key][0:2]

        elif wcsc:
            replacements = config_dict['wildcard subclass'][class_key][0:2]

        else:
            # Nothing to replace, so return the original string.
            return str(string)

        replacements = [class_key if x == '$' else x for x in replacements]
        replacements = [subclass_key if x == '*' else x for x in replacements]
        #NOTE If, in either case, two classes are reduced to one class,
        # we won't hit a problem. join() will simply condense the list of one
        # string into a string, without adding a / character.
        return str('/'.join(replacements))

def gethelp(filename):
    """
    Reads formatted help file, then returns mapping of topics to help strings.

    Input:
        filename:  path to '.helpfiles.txt'
        #TESTCODE using 'helpfiles.txt' for now, since version control has trouble with hidden files.
    Output:
        help_dict:  mapping of topics to doc strings
    """

   
    help_dict = {}
    
    with open(filename, "r") as f:
        # Ignore lines until section found.
        section_found = False
        while not section_found:
            line = f.readline().strip('\n')

            try:
                if not line:
                    # Reached EOF without finding section heading.
                    print("Error:  Help file lacks section headings.") #TESTCODE
                    print(line + '\n') #TESTCODE
                    sys.exit(1)
    
                elif line[0] == '[' and line[-1] == ']':
                    section = line.strip('[').strip(']')
                    help_dict[section] = ""

                    break
            except IndexError:
                continue

        # If we got this far, we've now found a section heading.
        for line in f:
            line = line.strip('\n')
            try:
                if line[0] == '[' and line[-1] == ']':
                    section = line.strip('[').strip(']')
                    help_dict[section] = ""
                else:
                    help_dict[section] += '\n' + line
            except IndexError:
                    continue
    return(help_dict)


###############################################################################
# Analysis functions

def analysisA(args, opt_dict):
    try:
        length = int(args[0])
    except ValueError:
        return(3)

    fas_filename = args[1]
    skip = 0
    columns = [0,2,3]

    if opt_dict['A']:
        # Expects repeat class, start, end
        skip = 3
        columns = args[2:5]
        try:
            columns = [int(x) for x in columns]
        except ValueError:
            return(2)

    out_filename = args[2 + skip]

    if "/" not in out_filename:
        out_filename = os.path.join(LOCAL_PATH, 'output', out_filename)

    try:
        config_filename = args[3 + skip]
        config = getconfig(config_filename)
    except IndexError:
        config = {}

    classes = fasgenome(fas_filename, config, columns)
    writetbl(fas_filename,
        out_filename,
        classes,
        length)
    return(0)

def analysisB(args, opt_dict):
    try:
        length = int(args[0])
    except ValueError:
        return(3)

    fas_filename = args[1]
    fas_skip = 0
    fas_columns = [0,1,2,3]

    if opt_dict['A']:
        # Expects repeat class, chromosome, start, end
        fas_skip = 4
        fas_columns = args[2:6]
        try:
            fas_columns = [int(x) for x in fas_columns]
        except ValueError:
            return(2)

    pi_filename = args[2 + fas_skip]
    pi_skip = 0
    pi_columns = [1,2,3]

    if opt_dict['B']:
        # Expects chromosome, start, end
        pi_skip = 3
        pi_columns = args[(2 + fas_skip) : (5 + fas_skip)]
        try:
            pi_columns = [int(x) for x in pi_columns]
        except ValueError:
            return(2)

    out_filename = args[3 + fas_skip + pi_skip]
    if "/" not in out_filename:
        out_filename = os.path.join(LOCAL_PATH, 'output', out_filename)

    try:
        config_filename = args[4 + fas_skip + pi_skip]
        config = getconfig(config_filename)
    except IndexError:
        config = {}

    chromosomes = pidensity(pi_filename, pi_columns)

    classes = fasdensity(fas_filename, chromosomes, config, fas_columns)

    writetbl(fas_filename,
        out_filename,
        classes,
        length)
    return(0)

def analysisC(args, opt_dict):
    fas_filename = args[0]
    fas_skip = 0
    fas_columns = []

    if opt_dict['A']:
        # Expects repeat class, chromosome, start, end
        fas_skip = 4
        fas_columns = args[1:5]
        try:
            fas_columns = [int(x) for x in fas_columns]
        except ValueError:
            return(2)

    pi_filename = args[1 + fas_skip]
    pi_skip = 0
    pi_columns = [0,1,2,3]

    if opt_dict['B']:
        # Expects id, chromosome, start, end
        pi_skip = 4
        pi_columns = args[(2 + fas_skip) : (6 + fas_skip)]
        try:
            pi_columns = [int(x) for x in pi_columns]
        except ValueError:
            return(2)

    out_filename = args[2 + fas_skip + pi_skip]
    if "/" not in out_filename:
        out_filename = os.path.join(LOCAL_PATH, 'output', out_filename)

    try:
        config_filename = args[3 + fas_skip + pi_skip]
        config = getconfig(config_filename)
    except IndexError:
        config = {}

    print("Loading TE data...") #TESTCODE
    te_dict = fasmatrix(fas_filename, config, fas_columns)
    print("Done.  Loading region of interest data...") #TESTCODE
    region_dict, region_keys = pimatrix(pi_filename, te_dict, pi_columns)
    print("Done.  Writing output data...") #TESTCODE

    result = outmatrix(out_filename, region_dict, region_keys)

    if opt_dict['t']:
        result = transpose(out_filename)

    return(result)

###############################################################################
# Genome density function chain

def fasgenome(fas_filename, replace_dict, columns):
    """
    Reads .fas file, and returns mapping {TEClass}>{Subclass}>[Frequency, Length].

    replace_dict maps search terms to replacements.  These are specified by a
    config file.  See getconfig().
    Map class to subclass
    Map subclass to list
    List contains
        1.  Frequency of subclass
        2.  Total length of TE subclass, in bp's
    """

    id_index = columns[0]
    start_index = columns[1]
    end_index = columns[2]

    classes = {}
    
    with open(fas_filename, "r") as f:
        # Skip header line
        f.readline()
    
        for line in f:

            ## Remove newline, extraneous whitespace.
            line = line.strip('\n').strip()

            # Split line on white space
            line_list = re.split(r"\s*", line)

            # Handle special cases of classes.
            full_class = re.split(r"\?", line_list[id_index])[0]

            full_class = configreplace(full_class, replace_dict)

            # Determine if this chromosome was considered in other studies.
            chromosome = line_list[4]
            #TODO:  HARDCODING ISSUE
            # Should we consider chrY_random since we aren't matching to piRNA?
            if "_random" in chromosome:
                continue

            length = int(line_list[end_index]) - int(line_list[start_index])

            if "/" in full_class:
                # Split on /
                superclass, subclass = re.split(r"/", full_class)

                if superclass in classes:
                    # Found class.  Does it also have this subclass?
                    this_class = classes[superclass]

                    if subclass in this_class:
                        # Yes, so add to the data
                        this_class[subclass][0] += 1
                        this_class[subclass][1] += length
                    else:
                        # No, so add the subclass
                        this_class[subclass] = [1, length]

                else:
                    # Missing superclass - add superclass and subclass 
                    # to classes.  Initialize count and length of subclass.
                    classes[superclass] = {subclass: [1, length]}
            else:
                # No /, so route to subclass "No subclass".
                if full_class in classes:
                    try:
                        # Found class. Update data.
                        classes[full_class]["No subclass"][0] += 1
                        classes[full_class]["No subclass"][1] += length
                    except KeyError:
                        # Missing subclass.  Initialize.
                        classes[full_class]["No subclass"] = [1, length]
                else:
                    # full_class is missing altogether.
                    # Initialize full_class and OTHER.
                    classes[full_class] = {"No subclass": [1, length]}


    return(classes)

def writetbl(fas_filename, out_filename, classes, region_length):
    """
    Writes .tbl file based on output from fasgenome().

    Approximate layout of .tbl file:
    Header
    Class
        Subclass
    (For each Class)
    Total Interspersed Repeats
    Singleton Classes
    """

    eqblock = "="*50 + '\n'

    with open(out_filename,'w') as out:
        out.write(eqblock)
        out.write("filename: " + re.split(".out", fas_filename)[0] + '\n')
        out.write("total length: " + str(region_length) + '\n')
        out.write(eqblock)
        out.write("               number of      length   percentage\n")
        out.write("               elements*    occupied  of sequence\n")
        out.write("-"*50+'\n')

        precision = 3
        keys = list(classes.keys())
        tir = 0

        # SINE LINE LTR elements DNA elements 
        main_keys = ['SINE','LINE','LTR','DNA']

        for key in main_keys:
            subclass_keys = list(classes[key].keys())
            # Calculate total class data from subclass data
            # [sum of frequencies, sum of lengths, percent overlap with genome]
            class_totals = [0,0,0]

            for sub_key in subclass_keys:
                class_totals[0] += classes[key][sub_key][0]
                class_totals[1] += classes[key][sub_key][1]

            class_totals[2] = round(100 * class_totals[1] / region_length, precision)
            ir_string = str(class_totals[2])
            if ir_string == '0.0':
                ir_string = ''.join(['< 0.', ('0' * precision), '5'])

            tir += class_totals[1]

            # Write class data
            # Note that 'out.write('a' + 'b' + ...)' breaks in some Pythons.
            out_list = ['\n', key, ':', '\t' * 2, \
                str(class_totals[0]), '\t', \
                str(class_totals[1]), ' bp\t', \
                ir_string, ' %\n']
            out.write(''.join(out_list))

            # Write subclass data
            # Check for 'No subclass' data.  Remove from key list if present.
            try:
                subclass_keys.remove('No subclass')
                has_no_subclass = True
            except ValueError:
                has_no_subclass = False

            for sub_key in subclass_keys:
                totals = round(100 * classes[key][sub_key][1] / \
                    region_length, precision)
                ir_string = str(totals)
                if ir_string == '0.0':
                    ir_string = ''.join(['< 0.', ('0' * precision), '5'])

                out_list = [" " * 6, sub_key, '\t', \
                    str(classes[key][sub_key][0]), '\t', \
                    str(classes[key][sub_key][1]), ' bp\t', \
                ir_string, ' %\n']
                out.write(''.join(out_list))

            # Write 'No subclass' data, if present.
            if has_no_subclass:
                totals = round(100 * classes[key]['No subclass'][1] / \
                    region_length, precision)
                ir_string = str(totals)
                if ir_string == '0.0':
                    ir_string = ''.join(['< 0.', ('0' * precision), '5'])

                out_list = [" " * 6, 'No subclass\t', \
                    str(classes[key]['No subclass'][0]), '\t', \
                    str(classes[key]['No subclass'][1]), ' bp\t', \
                ir_string, ' %\n']
                out.write(''.join(out_list))


        # Handle Unknown, Other, and Unclassified
        un_keys = ['Unknown', 'Other', 'Unclassified']
        un_totals = [0,0,0]
        for key in un_keys:
            try:
                subclass_keys = list(classes[key].keys())
            except KeyError:
                continue
            for sub_key in subclass_keys:
                un_totals[0] += classes[key][sub_key][0]
                un_totals[1] += classes[key][sub_key][1]

        tir += un_totals[1]

        un_totals[2] += round(100 * un_totals[1] / region_length, precision)
        if un_totals[1]:
            # Don't execute anything here if there's nothing to report.
            # Thus, we condition on whether or not un_totals is 0.
            ir_string = str(un_totals[2])
            if ir_string == '0.0':
                ir_string = ''.join(['< 0.', ('0' * precision), '5'])
    
            un_list = ['\nUnclassified:\t\t', \
                str(un_totals[0]), '\t', \
                str(un_totals[1]), 'bp\t', \
                ir_string, '%\n']
            
            out.write(''.join(un_list))

        # Calculate and write total interspersed repeats
        tir_density = str(round((100 * tir / region_length), precision))
        if tir_density == '0.0':
            tir_density = ''.join(['< 0.', ('0' * precision), '5'])

        out.write("Total interspersed repeats:\t" + \
            str(tir) + 'bp\t' + \
            tir_density + '%\n\n\n')

        # Handle remaining classes
        keys = [x for x in keys if x not in (main_keys + un_keys)]
        for key in keys:
            subclass_keys = list(classes[key].keys())
            class_totals = [0,0,0]

            for sub_key in subclass_keys:
                class_totals[0] += classes[key][sub_key][0]
                class_totals[1] += classes[key][sub_key][1]

            class_totals[2] = 100 * class_totals[1] / region_length

            ir_string = str(round(class_totals[2], precision))
            if ir_string is '0.0':
                ir_string = ''.join(['< 0.', ('0' * precision), '5'])

            out_list = ['\n', key, ':', '\t' * 2, \
                str(class_totals[0]), '\t', \
                str(class_totals[1]), ' bp\t', \
                ir_string, ' %\n']
            out.write(''.join(out_list))

        out.write(eqblock)

###############################################################################
# Overlap density function chain

def pidensity(pi_filename, columns):
    """
    Reads .gff file; returns mapping {Chromosome Label}>[TE Start,TE End].

    Expects either 1 header line or no header line.
    This is checked by attempting to cast the first item in the first line
    as an int.
    If this succeeds, iteration proceeds as normal for the first line.
    If this check fails (ValueError), exactly 1 header line is assumed,
    and execution jumps to the next line in the file buffer.
    """

    chr_index = columns[0]
    start_index = columns[1]
    end_index = columns[2]

    # Create chromosome dict.
    chromosomes = {}
    
    # Fill chromosome dict.
    with open(pi_filename, "r") as pi:
        # Skip header line
        pi.readline()

        for line in pi:
            keys = list(chromosomes.keys())
            line = line.strip()
            line_list = re.split(r"\s*", line)

            key = line_list[chr_index].strip('chr')

            if key not in keys:
                chromosomes[key] = []

            # Append [start,end]
            try:
                chromosomes[key].append( [int(line_list[start_index]), \
                    int(line_list[end_index])] )
            except ValueError:
                print("ValueError in line:")
                print(line)
                sys.exit(1)
    # pi_filename closed.
    return(chromosomes)

def fasdensity(fas_filename, chromosomes, replace_dict, columns):
    """
    Reads .fas file; returns map {TEClass}>{Subclass}>[Frequency, OverlapLength].
    
    Records frequency of overlaps and sum of lengths by which TE overlaps RoI.
    This is stored in the dict `chromosomes`.

    Input:
        fas_filename:  File path to multiclass data
        chromosomes:  A dict mapping chromosome labels to a 
            list of integer pairs
        replace_dict: A dict mapping search terms to replacement terms
    Output:
        classes:  A dictionary mapping ????
    """

    id_index = columns[0]
    chr_index = columns[1]
    start_index = columns[2]
    end_index = columns[3]

    classes = {}
    
    with open(fas_filename, "r") as f:
        # Skip header line
        f.readline()
    
        #for count, line in enumerate(f,start=0):
        for line in f:
            ## Remove newline, extraneous whitespace.
            line = line.strip('\n').strip()

            # Split line on whitespace
            line_list = re.split(r"\s*", line)

            ## Handle special cases of classes.
            full_class = re.split(r"\?", line_list[id_index])[0]

            full_class = configreplace(full_class, replace_dict)

            ## Determine whether or not this transposable element overlaps one or
            ## more RoIs, and determine the total length of overlap.
            chromosome = line_list[chr_index].strip('chr')
            
            #TODO:  HARDCODING ISSUE
            # As before, can we legitimately hard code this?
            # If so, we better explain why!
            if "_random" in chromosome:
                continue

            try:
                ranges = chromosomes[chromosome]
            except KeyError:
                continue
    
            this_start = int(line_list[start_index])
            this_end = int(line_list[end_index])
            length = 0
            overlap_count = 0
    
            ## Look for overlaps and record length of overlap.
            for each_range in ranges:
                pi_start = each_range[0]
                pi_end = each_range[1]
    
                # Is the start of the transposable element in range?
                start_in_range = pi_start <= this_start <= pi_end
                # Is the end of the transposable element in range?
                end_in_range = pi_start <= this_end <= pi_end
                # Does the transposable element contain the RoI?
                te_contains_RoI = this_start <= pi_start <= \
                    pi_end <= this_end
                
                if te_contains_RoI:
                    # Find length of overlap:
                    length += pi_end - pi_start
                elif start_in_range and end_in_range:
                    length += this_end - this_start
                elif start_in_range and not end_in_range:
                    length += pi_end - this_start
                elif end_in_range and not start_in_range:
                    length += this_end - pi_start


            ## If an overlap exists, record class/subclass data.
            if length > 0:
                if "/" in full_class:
                    # Split on /
                    superclass, subclass = re.split(r"/", full_class)

                    if superclass in classes:
                        # Found class.  Does it also have this subclass?
                        this_class = classes[superclass]

                        if subclass in classes[superclass]:
                            # Yes, so add to the data
                            this_class[subclass][0] += 1
                            this_class[subclass][1] += length
                        else:
                            # No, so add the subclass
                            this_class[subclass] = [1, length]

                    else:
                        # Missing superclass - add superclass and subclass 
                        # to classes.  Initialize count and length of subclass.
                        classes[superclass] = {subclass: [1, length]}
                else:
                    # No /, so route to subclass "No subclass".
                    if full_class in classes:
                        try:
                            # Found class. Update data.
                            classes[full_class]["No subclass"][0] += 1
                            classes[full_class]["No subclass"][1] += length
                        except KeyError:
                            # Missing subclass.  Initialize.
                            classes[full_class]["No subclass"] = [1, length]
                    else:
                        # full_class is missing altogether.
                        # Initialize full_class and OTHER.
                        classes[full_class] = {"No subclass": [1, length]}

    return(classes)

###############################################################################
# Matrix function chain

def fasmatrix(fas_filename, replace_dict, columns):
    """
    Reads .fas file; returns {Chromosome}>{TEClass}>{Sub}>[Pairs]>(Start,End).

    Input:
        fas_filename:  File path to multiclass data
        replace_dict: A dictionary mapping search terms to replacement terms
    Output:
        te_dict:  Maps chromosomes to classes to subclasses to lists of range pairs
    Side effects:
    """

    id_index = columns[0]
    chr_index = columns[1]
    start_index = columns[2]
    end_index = columns[3]

    te_dict = {}
    
    with open(fas_filename, "r") as f:
        # Skip header line
        f.readline()
    
        for line in f:
            ## Remove newline, extraneous whitespace.
            line = line.strip('\n').strip()
            
            line_list = re.split(r"\s*",line)
    
            chromosome = line_list[chr_index].strip('chr')

            #TODO:  HARDCODING ISSUE
            if "_random" in chromosome:
                continue

            this_start = int(line_list[start_index])
            this_end = int(line_list[end_index])
            
            ## Handle special cases of classes.
            #TODO:  HARDCODING ISSUE - question mark.
            full_class = re.split(r"\?", line_list[id_index])[0]

            full_class = configreplace(full_class, replace_dict)

            ## Look for subclass
            if "/" in full_class:
                class_items = re.split(r"/", full_class)
                this_class = class_items[0]
                this_subclass = class_items[1]
            else:
                this_class = full_class
                this_subclass = "No subclass"
    
                    
            if chromosome not in te_dict.keys():
                te_dict[chromosome] = {}
            if this_class not in te_dict[chromosome].keys():
                te_dict[chromosome][this_class] = {}
            if this_subclass not in te_dict[chromosome][this_class].keys():
                te_dict[chromosome][this_class][this_subclass] = []

            te_dict[chromosome][this_class][this_subclass].append((this_start, \
                this_end))

    return(te_dict)

def pimatrix(pi_filename, te_dict, columns):
    """
    Reads .gff file. Returns: dict of TE x RoI %-overlaps, list of keys.

    Gets TE ranges from te_dict.
    Gets RoI ranges from .gff file.
    Compares ranges, records percent overlap of each TE against each RoI
        on the same chromosome.

    NB:
    region_keys is used instead of region_dict.keys() to enforce a consistent
        ordering across columns in output and across outputs when the tool
        is run with different .fas inputs.
    

    Input:
        pi_filename:  File path to RoI range data
    Output:
        region_dict #TODO
        region_keys #TODO
    Side effects:
    """

    id_index = columns[0]
    chr_index = columns[1]
    start_index = columns[2]
    end_index = columns[3]

    region_dict = {}
    region_keys = []

    with open(pi_filename, "r") as pi:
        # Skip first line.
        pi.readline()

        for line in pi:
            line = line.strip()
            line_list = re.split(r"\s*", line)

            this_chr = line_list[chr_index].strip('chr')
            pi_start = int(line_list[start_index])
            pi_end = int(line_list[end_index])
            pi_length = pi_end - pi_start

            these_te_ranges = te_dict[this_chr]
    
            for this_class in these_te_ranges:
                # Find matches
                for this_subclass in these_te_ranges[this_class]:
                    # Iterate over ranges for this_chr

                    for this_range in these_te_ranges[this_class][this_subclass]:
                        # Check overlaps
                        overlap_length = 0
                        this_start = this_range[0]
                        this_end = this_range[1]
    
                        # Is the start of the transposable element in range?
                        start_in_range = pi_start <= this_start <= pi_end
                        # Is the end of the transposable element in range?
                        end_in_range = pi_start <= this_end <= pi_end
                        # Does the transposable element contain the RoI?
                        te_contains_RoI = this_start <= pi_start \
                            <= pi_end <= this_end
                        
                        if te_contains_RoI:
                            overlap_length = pi_end - pi_start
                        elif start_in_range and end_in_range:
                            overlap_length = this_end - this_start
                        elif start_in_range and not end_in_range:
                            overlap_length = pi_end - this_start
                        elif end_in_range and not start_in_range:
                            overlap_length = this_end - pi_start
    
                        # Record overlaps
                        if overlap_length > 0:
                            region_key = line_list[id_index]
                            if region_key not in region_keys:
                                region_keys.append(region_key)
                            if this_class not in region_dict:
                                region_dict[this_class] = { \
                                this_subclass: {region_key: 0}}
                            elif this_subclass not in region_dict[this_class]:
                                region_dict[this_class][this_subclass] = { \
                                    region_key: 0}
                            elif region_key not in region_dict[this_class][this_subclass]:
                                region_dict[this_class][this_subclass][region_key] = 0
                            percent_overlap = \
                                100 * overlap_length / float(pi_length)
                            region_dict[this_class][this_subclass][region_key] += percent_overlap

    return(region_dict, region_keys)

def outmatrix(out_filename, region_dict, region_keys):
    """                                                                         
    Takes output from pimatrix() to write TE x RoI %-overlaps to file.

    By "%-overlap," we mean "the percentage of the RoI region which overlaps
    with the specified TE."

    Output details:
    Delimiter:  tab (i.e. '\t')
    Left: TE Class/Subclass.
    Top:  RoI label
    Cell:  Percent overlap?  #TODO or is it percent of gene (or genome?) accounted for by overlap?

    Notes:
    For convenience, classes are written in square brackets, e.g. "[CLASS]".
    This format can be transposed using transpose().
    """

    with open(out_filename,"w") as out:
    
        # Write header line
        out.write("Class" + '\t' + '\t'.join(region_keys) + '\n')
    
        # Write data lines
        for this_class in region_dict:
            class_dict = {}
            
            # Build class data
            for this_subclass in region_dict[this_class]:
                for this_key in region_dict[this_class][this_subclass]:
                    if this_key not in class_dict:
                        class_dict[this_key] = 0
    
                    class_dict[this_key] += region_dict[this_class][this_subclass][this_key]
    
            # Write class data
            class_string = "[" + this_class + "]"
            for this_key in region_keys:
                try:
                    class_string += '\t' + str(round(class_dict[this_key], 5))
                except KeyError:
                    class_string += '\t' + "0.0"
    
            out.write(class_string + '\n')
            
            # Write subclass data  
            if len(region_dict[this_class]) == 1:
                continue
    
            for this_subclass in region_dict[this_class]:
                subclass_string = this_class + "/" + this_subclass
                for this_key in region_keys:
                    try:
                        subclass_string += '\t' + str(round(region_dict[this_class][this_subclass][this_key], 5)) 
                    except KeyError:
                        subclass_string += '\t' + "0.0"
    
                out.write(subclass_string + '\n')

def transpose(filename):
    """
    Rewrites filename using the transpose of tab-delimited data in filename.
    """

    with open(filename, "r") as fin:
        lines = []
        for line in fin:
            lines.append(re.split(r'\s*', line.strip('\n')))
    
    with open(filename, "w") as fout:
        length = len(lines[0])
        width = len(lines)
        for i in range(length):
            line_list = []
            for j in range(width):
                line_list.append(lines[j][i])
            fout.write('\t'.join(line_list) + '\n')

    return(0)

