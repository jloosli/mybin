#!/usr/bin/env python

# To make meld work with git diff
# See http://nathanhoad.net/how-to-meld-for-git-diffs-in-ubuntu-hardy

import sys
import os

os.system('meld "%s" "%s"' % (sys.argv[2], sys.argv[5]))
