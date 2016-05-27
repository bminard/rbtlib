#-------------------------------------------------------------------------------
# rbtlib: user.py
#
# User management.
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


def login(session, url, username, password):
    """User login.

    Args:
        session: the HTTP session.
        url: the Review Board URL.
        username: account user name.
        password: account password.

    Returns:
        The HTTP status code, not an indicator of a successful login.

    Raises:
        requests.exceptions.HTTPError: whenever an HTTP error occurs
    """
    # FIXME: should return an indication of sucessful or unsuccessful login
    URL = url + '/account/login/'
    r = session.get(URL)
    r.raise_for_status()
    login_data  =  dict(username = username, password = password,
        csrfmiddlewaretoken = session.cookies['csrftoken'], next = '/')
    r = session.post(URL, data = login_data, headers = dict(Referer = URL))
    r.raise_for_status()
    return r.status_code
