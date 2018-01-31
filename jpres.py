#!/usr/bin/env python

# jpres.py

helpStr = """
DESCRIPTION:
Specify preconditions before a Java method or constructor to automatically
generate IllegalArgumentExceptions.

USAGE:
python jpres.py [-h|-i] [args]

OPTIONS:
    -h: Displays the help message
    -i: Insert mode; modify the files specified in the arguments by
        replacing the preconditions specified in metasyntax with
        IllegalArgumentException throw statements

METASYNTAX COMPOSITION:
^\s*//\s*presume\s*:\s*.+?(?:$|\s*;\s*.+\s*$)

EXAMPLES:

// presume: d >= 0
public static double sqrt(double d) {
    return Math.sqrt(d);
}

The above translates to:
public static double sqrt(double d) {
    if (!(d >= 0)) {
        throw new IllegalArgumentException("d < 0");
    }
    return Math.sqrt(d);
}

An optional description clause can be specified using the syntax
"; <description>". Example:
// presume: d >= 0 ; you cannot take the square root of negative numbers
public static double sqrt(double d) {
    return Math.sqrt(d);
}

This translates to:
public static double sqrt(double d) {
    if (!(d >= 0)) {
        throw new IllegalArgumentException("you cannot take the square root of negative numbers");
    }
    return Math.sqrt(d);
}

Any number of leading, trailing or intermittent whitespace is allowed. In the
result, all intermittent whitespace will be normalized to a single space,
trailing whitespace will be dropped, and the output will have the correct level
of indentation.
"""

import sys, re

EXCEPTION_NAME = "IllegalArgumentException"

if __name__ == '__main__':
    if len(sys.argv) == 1 or '-h' in sys.argv:
        print(helpStr)
    else:
        anyspace = re.compile(r"\s+")
        valid = re.compile(r"^//\s?presume\s?:\s?.+?(?:$|;\s?.+$)")
        content = re.compile(r":\s?(.+?)\s?(?:$|;\s?)(.*$)")
        backslash = re.compile(r"\\")
        quotation = re.compile(r'"')
        for i in range(1, len(sys.argv)):
            if sys.argv[i].startswith('-'):
                continue # ignore
            res = ""
            pres = ""
            with open(sys.argv[i], "r") as f:
                ilevel = 0
                for line in f:
                    l = anyspace.sub(" ", line.strip());
                    if (valid.match(l)):
                        # TODO: do the thing
                        c = content.findall(l)
                        if len(c) != 1 or len(c[0]) != 2:
                            sys.stderr.write("Error: metasyntax error for line " + "'" + line + "'")
                        else:
                            condition = c[0][0]
                            description = quotation.sub(r"\"", backslash.sub(r"\\", c[0][1]))
                            if not description:
                                description = quotation.sub(r"\"", backslash.sub(r"\\", condition))
                            pres += "if (!(%s)) {\n    throw new %s(\"%s\");\n}\n"\
                                    %(condition, EXCEPTION_NAME, description)
                    else:
                        res += line 
                        rstres = res.rstrip()
                        if rstres.endswith("{"):
                            # assuming that { comes at the end of the line
                            ilevel += 1
                            if pres:
                                for presLine in pres.split('\n'):
                                    res += ' '*ilevel*4 + presLine + "\n"
                            pres = "" # reset pres
                        elif rstres.endswith("}"):
                            # assuming that } comes at the end of the line
                            ilevel -= 1
                            pres = "" # reset pres
            if ('-i' in sys.argv):
                with open(sys.argv[i], "w") as f:
                    f.write(res)
            else:
                print(res)
