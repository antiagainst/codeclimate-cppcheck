class Command:
    """Returns command line arguments by parsing codeclimate config file."""
    def __init__(self, config, file_list_path):
        self.config = config
        self.file_list_path = file_list_path

    def build(self):
        command = ['cppcheck']

        if self.config.get('check'):
            command.append('--enable={}'.format(self.config.get('check')))

        if self.config.get('project'):
            command.append('--project={}'.format(self.config.get('project')))

        if self.config.get('language'):
            command.append('--language={}'.format(self.config.get('language')))

        for identifier in self.config.get('stds', []):
            command.append('--std={}'.format(identifier))

        if self.config.get('platform'):
            command.append('--platform={}'.format(self.config.get('platform')))
            
        if self.config.get('library'):
            command.append('--library={}'.format(self.config.get('library')))

        for symbol in self.config.get('defines', []):
            command.append('-D{}'.format(symbol))

        for symbol in self.config.get('undefines', []):
            command.append('-U{}'.format(symbol))

        for directory in self.config.get('includes', []):
            command.append('-I{}'.format(directory))

        if self.config.get('max_configs'):
            if self.config.get('max_configs') == 'force':
                command.append('--force')
            else:
                command.append('--max-configs={}'.format(self.config.get('max_configs')))

        if self.config.get('inconclusive', 'true') == True:
            command.append('--inconclusive')
            
        if self.config.get('suppressions-list'):
            command.append('--suppressions-list={}'.format(self.config.get('suppressions-list')))
        
        if self.config.get('inline-suppr', 'true') == True:
            command.append('--inline-suppr')

        if self.config.get('dump', 'true') == True:
            command.append('--dump')

        command.extend(['--xml', '--xml-version=2'])
        command.append('--file-list={}'.format(self.file_list_path))

        return command
