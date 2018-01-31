# jpres.py: Java precondition insertion script

**NOTE:** This is part of my unofficial collection of "Java source code
modification scripts written in Python". If you find this interesting, check
out [javimp.py](https://github.com/winterweird/javimp), which is about
semi-automating importing Java classes without relying on an IDE.

> Why does this exist?

Because checking your input in Java is a hassle. This is an attempt to make
input checking more declarative and less verbose.

**CAVEAT:** This script makes some assumptions about how you format your source
files. In particular, it assumes that `{` and `}` both occur on the end of
lines. If this is not the case across all lines of your source code, this script
results in undefined behavior.

This script has been tested with Python 2.7.12 and Python 3.5.2, and should
probably work with any version of Python 2.x/3.x

### DESCRIPTION:

Specify preconditions before a Java method or constructor to automatically
generate IllegalArgumentExceptions.

### USAGE:

`python jpres.py [-h|-i] [args]`

### OPTIONS:

```
-h: Displays the help message
-i: Insert mode; modify the files specified in the arguments by replacing the
    preconditions specified in metasyntax with IllegalArgumentException throw
    statements
```

### METASYNTAX COMPOSITION:

```
^\s*//\s*presume\s*:\s*.+?(?:$|\s*;\s*.+\s*$)
```

### EXAMPLES:

```
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
```
