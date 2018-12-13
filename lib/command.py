class Command:
    """Returns command line arguments by parsing codeclimate config file."""
    def __init__(self, config, file_list_path):
        self.config = config
        self.file_list_path = file_list_path

    def build(self):
        command = ['cppcheck']

        command.append('--enable={}'.format(self.config.get('check', 'all')))

        if self.config.get('project'):
            command.append('--project={}'.format(self.config.get('project')))

        if self.config.get('language'):
            command.append('--language', self.config.get('language'))

        for identifier in self.config.get('stds', []):
            command.append('--std={}'.format(identifier))

        if self.config.get('platform'):
            command.append('--platform={}'.format(self.config.get('platform')))

        for symbol in self.config.get('defines', []):
            command.append('-D{}'.format(symbol))

        for symbol in self.config.get('undefines', []):
            command.append('-U{}'.format(symbol))

        for directory in self.config.get('includes', []):
            command.append('-I{}'.format(directory))

        if self.config.get('max_self.configs'):
            command.append('--max-configs={}'.format(self.config.get('max_configs')))

        if self.config.get('inconclusive', 'true') == 'true':
            command.append('--inconclusive')

        command.extend(['--xml', '--xml-version=2'])
        command.append('--file-list={}'.format(self.file_list_path))

        return command
