#!/usr/bin/env python3

"""Runs cppcheck, collects and reports results."""

import glob
import json
import os.path
import subprocess
import sys
import tempfile

from lxml import etree

CONFIG_FILE_PATH = '/config.json'

def get_config_and_paths():
    """Returns command line arguments by parsing codeclimate config file."""
    arguments = []

    if os.path.exists(CONFIG_FILE_PATH):
        contents = open(CONFIG_FILE_PATH).read()
        config = json.loads(contents)
        include_paths = config.get('include_paths', [])
        print('[cppcheck] config: {}', config, file=sys.stderr)

        config = config.get('config', {})
        arguments.append('--enable={}'.format(config.get('check', 'all')))
        if config.get('project'):
            arguments.append('--project={}'.format(config.get('project')))
        if config.get('language'):
            arguments.extend(['-x', config.get('language')])
        arguments.extend(['--std={}'.format(s) for s in config.get('stds', [])])
        if config.get('platform'):
            arguments.append('--platform={}'.format(config.get('platform')))
        arguments.extend(['-D{}'.format(d) for d in config.get('defines', [])])
        arguments.extend(['-U{}'.format(u)
                          for u in config.get('undefines', [])])
        arguments.extend(['-I{}'.format(i)
                          for i in config.get('includes', [])])
        if config.get('max_configs'):
            arguments.append('--max-configs={}'.format(
                config.get('max_configs')))
        if config.get('inconclusive', 'true') == 'true':
            arguments.append('--inconclusive')

    return arguments, include_paths


def get_cppcheck_command():
    args, paths = get_config_and_paths()
    command = ['cppcheck']
    command.extend(args)
    command.extend(['--xml', '--xml-version=2'])

    for path in paths:
        command.append(path)

    print('[cppcheck] command: {}'.format(command), file=sys.stderr)

    return command


def run_cppcheck():

    # cppcheck errors out on empty directories
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
    location['lines']['begin'] = int(line)
    location['lines']['end'] = int(line)

    return location


def derive_category_and_severity(severity):
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
        return ('Clarity', 'info')


def cppcheck_error_to_codeclimate_issue(error):
    """Converts a cppcheck error into a codeclimate issue."""
    if len(error) == 0:
        # No location for this issue: likely to be a general information issue,
        # should be safe to ignore.
        return None

    issue = {}
    issue['type'] = 'issue'
    issue['check_name'] = error.get('id')
    issue['description'] = error.get('msg').replace("'", "`")

    issue['content'] = {}
    issue['content']['body'] = error.get('verbose').replace("'", "`");
    if error.get('cwe'):
        # Include CWE link for detailed information.
        issue['content']['body'] += (
            ' ([detailed CWE explanation](https://cwe.mitre.org/data/'
            'definitions/{}.html))'.format(error.get('cwe')))

    category, issue['severity'] = (
        derive_category_and_severity(error.get('severity')))
    issue['categories'] = [category]

    issue['location'] = convert_location(error[0])
    issue['other_locations'] = []
    if len(error) > 1:
        locations = list(error)[1:]
        for l in locations:
            if l.get('line') is not None:
                location = convert_location(l)
                issue['other_locations'].append(location)

    return issue


def parse_cppcheck_results(results):
    if results is not None:
        root = etree.fromstring(results)
        for node in root:
            if node.tag == 'errors':
                for error in node:
                    issue = cppcheck_error_to_codeclimate_issue(error)
                    if issue:
                        # codeclimate requires the string to be null-terminated.
                        print('{}\0'.format(json.dumps(issue)))

if __name__ == '__main__':
    parse_cppcheck_results(run_cppcheck())
