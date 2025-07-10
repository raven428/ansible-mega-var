from __future__ import annotations

ANSIBLE_METADATA = {
  'metadata_version': '1.0.0',
  'status': ['preview'],
  'supported_by': 'community',
}

DOCUMENTATION = r'''
---
module: meva_pro
short_description: calculate files and directories names for _down2unp.yaml
version_added: "1.0.0"
description: calculate files and directories names for _down2unp.yaml
options:
  src_dir:
    description: path of f.name location
    required: false
    type: str
  f_name:
    description: value of f.name
    required: false
    type: str
  f_dest:
    description: value of f.dest, can be any even undefined
    required: false
    type: str
  i_dest:
    description: value of i.dest, should be absolute if defined
    required: false
    type: str
  f_src:
    description: source path replacing src_dir+f_name
    required: false
    type: str
author:
  - ChatGPT (https://chatgpt.com)
  - Dmitry Sukhodoyev (https://github.com/raven428/ansible-mega-var)
'''

EXAMPLES = r'''
- name: Calculate profile file path
  meva_prof_name:
    i_dest: "/opt/myapp/config"
    f_dest: ""
    f_name: "profile.yaml"
  register: result

- debug:
    var: result._meva_prof_name
'''

RETURN = r'''
destination:
  description: destination
  type: str
  returned: always
  sample: "/opt/myapp/config/profile.yaml"
message:
  description: Summary or detailed change report depending on verbose.
  returned: always
  type: str
changed:
  description: Whether any file modes were changed.
  returned: always
  type: bool
'''

import re
from pathlib import Path

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)


def resolve_paths(
  src_dir: str,
  f_name: str,
  f_dest: str,
  i_dest: str,
  f_src: str,
) -> dict[str, object]:
  src_path = f_src if f_src else (re.sub(r'/+$', '', src_dir) + '/' + f_name)
  if not f_name:
    f_name = Path(src_path).name

  prefix = ''
  if f_dest.startswith('/') and i_dest:
    prefix = ''
  elif i_dest:
    prefix = re.sub(r'/+$', '', i_dest) + '/'
  dest4copy = prefix + f_dest if f_dest else prefix + f_name

  if f_dest and f_dest.endswith('/'):
    dest4path = prefix + re.sub(r'/+$', '', f_dest)
    if not f_name.endswith('/'):
      dest4path = dest4path + '/' + Path(f_name).name
  elif f_dest:
    dest4path = prefix + f_dest
  else:
    dest4path = prefix + f_name

  src_is_dir = Path(src_path).is_dir()
  if dest4copy.endswith('/') or src_is_dir:
    dest4dir = ''
    if not dest4copy.endswith('/'):
      dest4copy += '/'
  else:
    dest4dir = str(Path(dest4copy).parent)

  # processing output to tests cases:
  # (echo 'cases_resolve_paths = ['
  # cat 3_test\ role*.txt |
  # sed -E -n 's/.*"a": "([^"]*)",[^}]*(, "dest4copy":.*)}/{ \1\2 },/p' |
  # sed -E 's/^([^"]*)("dest4copy":.*)/\1\2/; s/'\''/"/g' |
  # sed 's/true/True/ig' | sed 's/false/False/ig' | sed 's/001/000/g' |
  # sed -e 's/\x1b\[[0-9;]*m//g' | sort | uniq
  # echo ']') | yapf >main-data.py
  return {
    "a":
      f"'i_dest':'{i_dest}','f_dest':'{f_dest}','f_name':'{f_name}','f_src':'{f_src}',"
      f"'src_dir':'{src_dir}'",
    "dest4dir": dest4dir,
    "dest4copy": dest4copy,
    "dest4path": dest4path,
    "src4copy": src_path,
    "src_is_dir": src_is_dir,
  }


def main() -> None:
  module_args = dict(
    src_dir=dict(type='str', required=False, default=''),
    f_name=dict(type='str', required=False, default=''),
    f_dest=dict(type='str', required=False, default=''),
    i_dest=dict(type='str', required=False, default=''),
    f_src=dict(type='str', required=False, default=''),
  )
  module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
  f_src = module.params['f_src']
  f_name = module.params['f_name']
  f_dest = module.params['f_dest']
  i_dest = module.params['i_dest']
  src_dir = module.params['src_dir']

  if not i_dest and not f_dest:
    module.fail_json(msg="Either i.dest or f.dest must be defined and non-empty")
  if i_dest and not i_dest.startswith('/'):
    module.fail_json(msg="i_dest must be an absolute path")

  module.exit_json(changed=False, **resolve_paths(src_dir, f_name, f_dest, i_dest, f_src))


if __name__ == '__main__':
  main()
