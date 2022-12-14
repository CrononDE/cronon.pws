# -*- coding: utf-8 -*-
# Copyright (c) 2022, Ole Pannbacker <opannbacker@cronon.net>
# GNU General Public License v2.0+ see (https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
# SPDX-License-Identifier: GPL-2.0-or-later
from __future__ import (absolute_import, division, print_function)
from ansible.errors import AnsibleError
from ansible.module_utils.common.text.converters import to_native
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from subprocess import run, CalledProcessError
__metaclass__ = type

DOCUMENTATION = """
    name: bitwarden
    author:
      - Ole Pannbacker <opannbacker@cronon.net>
    requirements:
      - rbw (https://github.com/doy/rbw)
      - be logged into bitwarden via rbw
    short_description: Retrieve passwords from Bitwarden items.
    description:
      - Retrieve passwords from Bitwarden items.
    options:
      _terms:
        description: Item Id to fetch password for.
        required: true
        type: list
        elements: str
"""

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        ret = []

        for term in terms:
            try:
                display.debug(f"Lookup password for item id: {term}")
                p = run(["rbw", "get", term], check=True, capture_output=True)
                ret.append(bytes.decode(p.stdout, 'utf-8').rstrip())

            except CalledProcessError as msg:
                raise AnsibleError(to_native(msg))

        return ret
