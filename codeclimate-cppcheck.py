#!/usr/bin/env python

"""Runs cppcheck, collects and reports results."""

import json
import os.path
import subprocess
import sys

from lxml import etree

CONFIG_FILE_PATH = '/config.json'


def get_config():
    """Returns command line arguments by parsing codeclimate config file."""
    arguments = []

    if os.path.exists(CONFIG_FILE_PATH):
        contents = open(CONFIG_FILE_PATH).read()
        config = json.loads(contents)

        exclude_paths = config.get('exclude_paths', [])
        arguments.extend(['-i{}'.format(p) for p in exclude_paths])

        config = config.get('config', {})
        arguments.append('--enable={}'.format(config.get('check', 'all')))
        arguments.extend(['--std={}'.format(s) for s in config.get('stds', [])])
        if config.get('inconclusive', 'true') == 'true':
            arguments.append('-inconclusive')

    return arguments


def get_cppcheck_command():
    command = ['cppcheck']
    command.extend(get_config())
    command.extend(['--xml', '--xml-version=2'])
    command.append('.')

    return command


def run_cppcheck():
    p = subprocess.Popen(get_cppcheck_command(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    _, stderr = p.communicate()
    if p.returncode != 0:
        sys.exit(p.returncode)

    return stderr


def convert_location(location):
    """Converts cppcheck error location to the format codeclimate requires."""
    path = location.get('file')
    line = location.get('line')

    location = {}
    location['path'] = path
    location['lines'] = {}
    location['lines']['begin'] = line
    location['lines']['end'] = line

    return location


def derive_category_severity(severity):
    """Derives codeclimate issue category & severity from cppcheck severity."""
    # http://cppcheck.sourceforge.net/devinfo/doxyoutput/classSeverity.html
    # https://github.com/codeclimate/spec/blob/master/SPEC.md
    if severity == 'error':
        return ('Security', 'critical')
    if severity == 'warning':
        return ('Bug Risk', 'normal')
    if severity == 'style':
        return ('Style', 'normal')
    if severity == 'performance':
        return ('Performance', 'normal')
    if severity == 'portability':
        return ('Compatibility', 'normal')
    if severity == 'none' or severity == 'information' or severity == 'debug':
        # TODO: Figure out the correct corresponding codeclimate category.
        return ('Clarity', 'info')


def cppcheck_error_to_codeclimate_issue(error):
    """Converts a cppcheck error into a codeclimate issue."""
    issue = {}
    issue['type'] = 'issue'
    issue['check_name'] = 'cppcheck'
    issue['description'] = error.get('msg')
    issue['content'] = error.get('verbose')
    issue['categories'], issue['severity'] = \
        derive_category_severity(error.get('severity'))
    issue['categories'] = [issue['categories']]

    if len(error) == 0:
        # No location for this issue:
        # likely to be a general information issue, should be safe to ignore.
        return None
    issue['location'] = convert_location(error[0])
    if len(error) > 1:
        locations = list(error)[1:]
        locations = [convert_location(l) for l in locations]
        issue['other_locations'] = locations

    return issue


def parse_cppcheck_results(results):
    root = etree.fromstring(results)
    for node in root:
        if node.tag == 'errors':
            for error in node:
                issue = cppcheck_error_to_codeclimate_issue(error)
                if issue:
                    # codeclimate requires the string to be null-terminated.
                    print '{}\0'.format(json.dumps(issue))

if __name__ == '__main__':
    parse_cppcheck_results(run_cppcheck())
