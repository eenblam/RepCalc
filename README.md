# RepCalc

Authors:  Ben Elam, Tamer Aldwairi, Andy Perkins

Contact:  bae53@msstate.edu


## Platforms

On Windows and Mac, a standard installation of Python 3.4 or higher is required.

On Linux, both Python 3.4 and an additional installation of the Tkinter package are required.

## Analysis Types

WG:  This analysis calculates TE density within the whole genome, considering the genome itself as a single region of interest.  At the command line, it is indicated by the `-a` option flag. Required inputs:  length of genome, transposable element annotation data, and output file path.

ROI:  The second analysis calculates TE density within an arbitrary number of regions of interest.  At the command line, it is indicated by the `-b` option flag.  Required inputs:  length of regions of interest, transposable element annotation data, regions of interest data, and output file path.

MXROI:  The third analysis computes TE densities within specific regions of interest for each class and subclass of TE’s, outputting them as a matrix (TE class and subclass by ROI label.)  At the command line, it is indicated by the `-c` option flag.  Required inputs:  transposable element annotation data, regions of interest data, and output file path.

## Format restrictions of input files

The arrangement of columns is irrelevant, as their positions may be specified in both GUI and command line modes.

The ”class/subclass” structure used by RepeatMasker for the transposable element ID strings is critical.

## Usage:  Graphical Mode

RepCalc comes with a graphical (GUI) mode for those who prefer a visual interface.  It is import to note that Python’s Tkinter module is imported when and only when RepCalc is launched without command line arguments.  Hence, Tkinter is strictly required for GUI functionality.

Limited documentation is available in this mode through the interface, but it is strongly recommended that the user consult this README file for further information regarding inputs.  Bear in mind that input options in GUI mode correspond directly to command line arguments of the same name despite being presented in a different order.

When using the GUI, analysis type is selected using a set of radiobuttons.  Hence, only one analysis type will be selected at a time.  Depending on the analysis selected, unnecessary arguments will be toggled off.  With the exception of the configuration file, all available input fields must be utilized.  Paths to data files are supplied by clicking the appropriate button, which launch a file browser in a new window.

In order to facilitate smooth pipelining at the command line, column numbers are assumed to begin at 0, not 1.  This convention carries over into the GUI mode to avoid confusing users of both modes.

Graphical mode can be accessed by clicking on repcalc.py in the RepCalc directory on all platforms.  Alternatively, Mac and Linux users can navigate to the RepCalc folder and  enter ‘./repcalc.py' at the command line without any arguments.

## Usage:  Command Line Mode

The RepCalc GUI will not be launched if any argument is supplied at the command line.  In this case, Tkinter will not be imported.  Hence, Tkinter is not a requirement for server installations of RepCalc.  Since the command line mode is not interactive, execution begins immediately.

RepCalc requires a varying number of arguments depending on the desired analysis.  When using the command line, arguments must be supplied in the order given below, from left to right.  Optional fields are indicated by square brackets.

General form:

`./repcalc.py -[abc][ABt] [length] te_data [te_columns] [roi_data] [roi_columns]output_file [config_file]`

## Command Line Option Flags

When running RepCalc from the command line, options are given by flags combined in sa single string prefixed by a hyphen, e.g. `-cBt`.  This string must given as the first argument to RepCalc, and including additional option arguments elsewhere will produce an error.  The ordering of the flags themselves is arbitrary.  However, the hyphen should always come prior to the actual flags.

Options:

- `-a`,    Choose analysis type WG:  Calculate TE density relative to the entire genome.
- `-b`,    Choose analysis type ROI:  Calculate TE density within regions of interest.
- `-c`,     Choose analysis type MXROI:  Calculate distribution of TEs within regions of interest.
- `-A`,    Columns will be given explicitly for TE data following path to TE data.
- `-B`,    Columns will be given explicitly for region of interest data following path to regions of interest data.
- `-t`,     Transpose output.  Does not apply unless -c is also selected.

The options `-a`, `-b`, and `-c` specify WG, ROI, and MXROI, respectively.  One and only one must be specified by the user, and using more than one of the three will result in an error.

The user may specify that column numbers will be explicitly provided for all 4 variables following the name of a given input file.  The column numbers should be provided as 4 distinct integer values delimited by a single space.  To specify that columns will be provided for transposable element data, use `-A`.  To specify that columns will be provided for regions of interest data, use `-B`.  

Neither `-A` nor `-B` is required.  Column numbers default to 0, 1, 2, and 3 for ID, Chromosome, Start, and End, respectively, for either input file.  Since WG utilizes only one data input (for transposable elements), using `-B` and supplying additional columns will produce an error due to the presence of extraneous arguments.

To transpose the output given by MXROI, include the option `-t`.  This will cause an error if specified with options `-a` or `-b`.

## Command Line Arguments

## Command Line Usage Examples

## Specifying Options Via the Graphical Interface

## Config File

The purpose of the configuration (or, “config”) file is to allow the user to specify a class/subclass pattern to be identified and replaced in memory as ID values are obtained from the transposable element data.  RepCalc does not require a config file input - this feature is entirely optional and is intended primarily for users with a basic intuition for pattern matching.  However, this feature is much less robust than the use of regular expressions.  Savvy users will likely find it more convenient to directly edit copies of data files using regular expressions.

The primary function of this replacement tool is to allow the user a means of manipulating the IDs of transposable elements so as to influence their inclusion in the calculation of total interspersed repeats in WG and ROI.  It is also useful when performing MXROI on the same data, as this keeps the results from displaying different classes across outputs.

There are only a few basic syntax rules to be concerned with.

- ”Match” and “Replacement” patterns may be separated by one of two characters, the colon ( : ) or the equality/assignment operator, ( = ).
- Only one “Match : Replacement” (or “Match=Replacement”) statement may be provided on one line.
- Users may include comments in a config file using the # or ; characters.  Lines beginning with either character will be skipped when the config file is read by RepCalc.
- White space at either end of a string, or about the “/”, is stripped and ignored.  However, including white space within a class or subclass will produce an error.  That is, “Class / Subclass” is legal, but “Class/Sub class” is not.

Finally, RepCalc accepts the $ and * characters as primitive wildcards.  $ may be used in a pattern to match any class, and * may be used in a pattern to match any subclass.  In the match expression, $ should appear only left of the /, and * should appear only on the right.  In either case, the wildcard will be ignored if not given alone - hence our description of the wildcard as primitive.  When either wildcard is properly used in a match expression, the user may then include the wildcard in the replacement pattern.  Again, this feature has not been extended to allow for the use of wildcards to match within a class or subclass via regular expressions.  The use of wildcards works only for matching and replacing entire classes or subclasses.[a]  Also note that $ is not treated as a wildcard in the subclass region of a match expression, and * is not treated as a wildcard in the class region of a match expression.

## Examples of Config Expressions

“m/n : x/y” will replace any instances of class m and subclass n with class x and subclass y.

“m/n = x/y” will do the exact same thing as “m/n : x/y”.

“RC/* : RC” replaces any instances of the RC class - regardless of subclass - with the class alone.  E.g. “RC/A” becomes “RC”.

“Class/* : NewClass/*” will match on class name “Class” - regardless of subclass - and replace “Class” in the original string with “NewClass” while retaining the subclass.  E.g. Class/A becomes NewClass/A.

“$/Subclass : $/NewSubclass” behaves similarly, only now the subclass is retained while the class is changed.  E.g.  “A/Subclass” becomes “A/NewSubclass”.

“$/*” in the match term would match all classes.  Presently, this match pattern will cause RepCalc to produce an error if found.

[a]With a little time, I could implement this.  However, if the user really wants to use regular expressions, I expect them to be able to write a simpler regex script to parse their own data.  Like I said, we're not trying to reinvent emacs here.