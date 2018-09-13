class IssueFormatter:
    """Converts a cppcheck error into a codeclimate issue."""
    def __init__(self, node):
        self.node = node

    def format(self):
        if len(self.node) == 0:
            # No location for this issue: likely to be a general information issue,
            # should be safe to ignore.
            return None

        issue = {}
        issue['type'] = 'issue'
        issue['check_name'] = self.node.get('id')
        issue['description'] = self.node.get('msg').replace("'", "`")

        issue['content'] = {}
        issue['content']['body'] = self.node.get('verbose').replace("'", "`");
        if self.node.get('cwe'):
            # Include CWE link for detailed information.
            issue['content']['body'] += (
                ' ([detailed CWE explanation](https://cwe.mitre.org/data/'
                'definitions/{}.html))'.format(self.node.get('cwe')))

        category, issue['severity'] = (
            self._derive_category_and_severity(self.node.get('severity')))
        issue['categories'] = [category]

        issue['location'] = self._convert_location(self.node[0])
        issue['other_locations'] = []
        if len(self.node) > 1:
            locations = list(self.node)[1:]
            for l in locations:
                if l.get('line') is not None:
                    location = self._convert_location(l)
                    issue['other_locations'].append(location)

        return issue

    def _convert_location(self, location):
        """Converts cppcheck error location to the format codeclimate requires."""
        path = location.get('file')
        line = location.get('line')

        location = {}
        location['path'] = path
        location['lines'] = {}
        location['lines']['begin'] = int(line)
        location['lines']['end'] = int(line)

        return location


    def _derive_category_and_severity(self, severity):
        """Derives codeclimate issue category & severity from cppcheck severity."""
        # http://cppcheck.sourceforge.net/devinfo/doxyoutput/classSeverity.html
        # https://github.com/codeclimate/spec/blob/master/SPEC.md
        if severity == 'error':
            return ('Performance', 'critical')
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
