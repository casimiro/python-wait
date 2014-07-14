#!/usr/bin/env python

import os
import re
import time

def tail(path):
    """
    Implements file tailing as a generator.  Yields line content or None.
    """
    with open(path) as f:
        # Seek to the end of the file
        size = os.stat(path)[6]
        f.seek(size)

        while True:
            where = f.tell()
            line = f.readline()

            if not line:
                # Reset position if line was empty
                f.seek(where)
                time.sleep(1)
                yield None

            else:
                yield line

def pattern(path, patterns, timeout=None):
    """
    Wait until pattern(s) are detected by tailing a file.  Returns True when complete.

    If optional timeout is set and exceed then it returns False.
    """

    if isinstance(patterns, str):
        patterns = [patterns]

    if timeout:
        start = time.time()

    for line in tail(path):
        if line is not None:
            for pattern in patterns:
                if re.search(pattern, line):
                    patterns.remove(pattern)

        if not len(patterns):
            # Stop looping over generator when all patterns have been matched
            break

        if timeout:
            if time.time() - start > timeout:
                return False

    return True

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

