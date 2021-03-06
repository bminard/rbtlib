#-------------------------------------------------------------------------------
# rbtlib: conftest.py
#
# Common pytest fixtures.
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
import pytest
from rbtlib import Root, user
import re
import requests


class ReviewBoardServer(object):
    """Parameters common to Review Board servers used by the test suite.

    Attributes:
        scheme: URL scheme.
        fqdn: Fully qualified domain name.
    """

    def __init__(self, scheme, fqdn):
        self._fqdn = fqdn
        self._scheme = scheme

    @property
    def fqdn(self):
        return self._fqdn

    @property
    def scheme(self):
        return self._scheme

    @property
    def url(self):
        return self._scheme + '://' + self._fqdn

    def can_authenticate(self):
        """Determine if the these can authenticate to the server."""
        return False


class DemonstrationServer(ReviewBoardServer):
    """Server parameters for demo.reviewboard.org.
    """

    def __init__(self):
        super(DemonstrationServer, self).__init__('http', 'demo.reviewboard.org')

    def can_authenticate(self):
        """Determine if the these can authenticate to the server.

        Demo server authentication relies upon parsing the demo login page.
        """
        return True


def pytest_generate_tests(metafunc):
    """Create parameterized tests for different server classes."""
    if 'server' in metafunc.fixturenames:
        metafunc.parametrize("server", ['production', 'demonstration'], indirect=True)


@pytest.fixture
def server(request):
    """Return the server based upon the server class in the request."""
    if 'production' == request.param:
        return ReviewBoardServer('https', 'reviews.reviewboard.org')
    if 'demonstration' == request.param:
        return DemonstrationServer()
    raise ValueError("invalid internal test config")


@pytest.fixture
def session():
    """Return the HTTP session.

    Correct operation of tests requiring authentication requires they use the
    same HTTP session.
    """
    return requests.Session()


# Root List Resource top-level components defined in the Web API.
root_components = [ 'json', 'stat', 'links', 'site', 'capabilities',
        'product', 'uri_templates', ]


@pytest.fixture(params = root_components)
def root_resource_component(request):
    """Provide top-level Root List Resource components."""
    return request.param


# Root List Resource links defined in the Web API.
root_links = [ 'default_reviewers', 'extensions', 'groups',
    'hosting_service_accounts', 'hosting_services', 'info', 'repositories',
    'review_requests', 'search', 'self', 'session', 'users', 'validation',
    'webhooks', ]


@pytest.fixture(params = root_links)
def root_resource_link(request):
    """Provide top-level Root List Resource links."""
    return request.param


# Combine Root List Resource components and links.
extended_root_components = list(root_components)
extended_root_components.extend(root_links)


@pytest.fixture(params = extended_root_components)
def extended_root_resource(request):
    """Provide top-level Root List Resource components and links."""
    return request.param


# Regular expression for the user credentials on demo.reviewboard.org login page.
regex = re.compile('<p>To log into the demo server, use username &quot;(\w+)&quot;, password &quot;(\w+)&quot;</p>')


@pytest.fixture
def credentials(session, server):
    """Return the user credentials.

    Demo server authentication relies upon parsing the demo login page.
    """
    URL = server.url + '/account/login/'
    r = session.get(URL)
    assert 200 == r.status_code
    credentials = regex.findall(r.text.encode('utf-8'))
    if 0 == len(credentials):
        return { 'username': None, 'password': None }
    return { 'username': credentials[0][0], 'password': credentials[0][1] }


@pytest.fixture
def login(session, server, credentials):
    """Login to the specified server."""
    if False == server.can_authenticate():
        pytest.skip("cannot authenticate to server: {}".format(server.fqdn))
    if 200 != user.login(session, server.url, credentials['username'], credentials['password']):
        pytest.fail("cannot login to server: {}".format(server.fqdn))
