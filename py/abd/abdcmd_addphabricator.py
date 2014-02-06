"""Make a new phabricator instance known to the Arcyd instance."""
# =============================================================================
# CONTENTS
# -----------------------------------------------------------------------------
# abdcmd_addphabricator
#
# Public Functions:
#   getFromfilePrefixChars
#   setupParser
#   process
#
# -----------------------------------------------------------------------------
# (this contents block is generated, edits will be lost)
# =============================================================================

from __future__ import absolute_import

import os

import phlsys_conduit
import phlsys_fs

_CONFIG = """
--instance-uri
{instance_uri}
--arcyd-user
{arcyd_user}
--arcyd-cert
{arcyd_cert}
""".strip()

_CONFIG_HTTPS_PROXY = """
--https-proxy
{https_proxy}
""".strip()


def getFromfilePrefixChars():
    return None


def setupParser(parser):
    parser.add_argument(
        '--name',
        type=str,
        metavar='STR',
        required=True,
        help="string name of the phabricator instance, [_a-zA-Z0-9]+")

    parser.add_argument(
        '--instance-uri',
        type=str,
        metavar='ADDRESS',
        required=True,
        help="URI to use to access the conduit API, e.g. "
             "'http://127.0.0.1/api/'.")

    parser.add_argument(
        '--arcyd-user',
        type=str,
        metavar='USERNAME',
        required=True,
        help="username of admin account registered for arcyd to use.")

    parser.add_argument(
        '--arcyd-cert',
        metavar="CERT",
        type=str,
        required=True,
        help="Phabricator Conduit API certificate to use, this is the "
        "value that you will find in your user account in Phabricator "
        "at: http://your.server.example/settings/panel/conduit/. "
        "It can also be found in ~/.arcrc.")

    parser.add_argument(
        '--https-proxy',
        type=str,
        default=None,
        metavar='ADDRESS',
        help="(OPTIONAL) proxy URI for arcyd to use when connecting to "
             "conduit to https.")


def _make_config_phabricator_path(name):
    return 'phabricator-{}.config'.format(name)


def process(args):

    # make sure the file doesn't exist already
    path = _make_config_phabricator_path(args.name)
    if os.path.exists(path):
        raise Exception('{} already exists'.format(path))

    # make sure we can connect with those parameters
    conduit = phlsys_conduit.Conduit(
        args.instance_uri,
        args.arcyd_user,
        args.arcyd_cert,
        https_proxy=args.https_proxy)
    conduit.ping()

    content = _CONFIG.format(
        instance_uri=args.instance_uri,
        arcyd_user=args.arcyd_user,
        arcyd_cert=args.arcyd_cert)

    if args.https_proxy:
        content = '\n'.join([
            content,
            _CONFIG_HTTPS_PROXY.format(
                https_proxy=args.https_proxy)])

    phlsys_fs.write_text_file(path, content)


#------------------------------------------------------------------------------
# Copyright (C) 2014 Bloomberg Finance L.P.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#------------------------------- END-OF-FILE ----------------------------------
