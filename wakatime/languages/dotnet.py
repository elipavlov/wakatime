# -*- coding: utf-8 -*-
"""
    wakatime.languages.dotnet
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Parse dependencies from .NET code.

    :copyright: (c) 2013 Alan Hamlett.
    :license: BSD, see LICENSE for more details.
"""

from . import TokenParser
from ..compat import u


class CSharpParser(TokenParser):

    def parse(self, tokens=[]):
        if not tokens and not self.tokens:
            self.tokens = self._extract_tokens()
        for index, token, content in self.tokens:
            self._process_token(token, content)
        return self.dependencies

    def _process_token(self, token, content):
        if u(token).split('.')[-1] == 'Namespace':
            self._process_namespace(token, content)
        else:
            self._process_other(token, content)

    def _process_namespace(self, token, content):
        if content != 'import' and content != 'package' and content != 'namespace':
            content = content.split('.')
            content = content[0] if len(content) == 1 else '.'.join(content[0:len(content)-1])
            self.append(content, truncate=False)

    def _process_text(self, token, content):
        if self.state is not None:
            if content == "\n" and self.parens == 0:
                self.state = None
                self.nonpackage = False

    def _process_other(self, token, content):
        pass