import os

SRC_SUFFIX = ['.c', '.cpp', '.cc', '.cxx']


class Workspace:
    def __init__(self, include_paths):
        self.include_paths = include_paths


    def calculate(self):
        paths = []

        for path in self.include_paths:
            if os.path.isdir(path):
                paths.extend(self._walk(path))
            elif self._should_include(path):
                paths.append(path)

        return paths


    def _walk(self, path):
        paths = []

        for root, _directories, files in os.walk(path):
            for name in files:
                if self._should_include(name):
                    path = os.path.join(root, name)
                    paths.append(path)

        return paths


    def _should_include(self, name):
        return name.lower().endswith(tuple(SRC_SUFFIX))
