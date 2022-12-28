import json
import subprocess
import sys
import tempfile

from lxml import etree

from command import Command
from issue_formatter import IssueFormatter
from workspace import Workspace

CONFIG_FILE_PATH = '/config.json'


class Runner:
    """Runs cppcheck, collects and reports results."""
    def __init__(self):
        self._config = None


    def run(self):
        config = self._decode_config()
        self._print_debug('[cppcheck] config: {}'.format(config))

        workspace = Workspace(config.get('include_paths'))
        workspace_files = workspace.calculate()

        if not len(workspace_files) > 0:
            return

        self._print_debug('[cppcheck] analyzing {} files'.format(len(workspace_files)))

        file_list_path = self._build_file_list(workspace_files)
        plugin_config = config.get('config', {})
        command = Command(plugin_config, file_list_path).build()

        self._print_debug('[cppcheck] command: {}'.format(command))

        results = self._run_command(command)
        issues = self._parse_results(results)

        for issue in issues:
            # cppcheck will emit issues for files outside of the workspace,
            # like header files. This ensures that we only emit issues for
            # files in the workspace.
            if issue and workspace.should_include(issue["location"]["path"]):
                print('{}\0'.format(json.dumps(issue)))


    def _decode_config(self):
        contents = open(CONFIG_FILE_PATH).read()

        return json.loads(contents)


    def _build_file_list(self, workspace_files):
        _, path = tempfile.mkstemp()

        with open(path, 'w') as file:
            for workspace_file in workspace_files:
                file.write('{}\n'.format(workspace_file))

        return path


    def _run_command(self, command):
        process = subprocess.Popen(command,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

        _stdout, stderr = process.communicate()

        if process.returncode != 0:
            self._print_debug('[cppcheck] error: {}'.format(stderr))
            sys.exit(process.returncode)

        return stderr


    def _parse_results(self, results):
        root = etree.fromstring(results, parser=etree.XMLParser(huge_tree=True))
        issues = []

        for node in root:
            if node.tag == 'errors':
                for error in node:
                    issue = IssueFormatter(error).format()
                    issues.append(issue)

        return issues


    def _print_debug(self, message):
        print(message, file=sys.stderr)
