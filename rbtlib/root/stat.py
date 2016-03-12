#-------------------------------------------------------------------------------
# rbt: stat.py
#
# Validate the stat key returned with a Review Board resource.
#-------------------------------------------------------------------------------
# The MIT License (MIT)
# Copyright (c) 2016 Brian Minard
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#-------------------------------------------------------------------------------
from functools import wraps
import resource


def key(get):
    """ Check response status from Review Board instance.
    """
    @wraps(get)
    def _stat_decorator(url, query_dict = None):
        """ Check the stat returned by the Review Board instance.

        URL is the fully qualified domain name, including the scheme, of the Review Board
        instance to query.

        query_dict are parameters passed with the URL.
        """
        response = get(url, query_dict)
        assert 'ok' == response.stat or 'fail' == response.stat
        return response
    return _stat_decorator
