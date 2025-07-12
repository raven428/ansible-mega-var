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

import os
from pathlib import Path
from typing import Iterator

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)


def ww2_file(
  path: Path,
  *,
  followlinks: bool = False,
) -> Iterator[tuple[str, list[str], list[str]]]:
  if path.is_file():
    yield str(path), [], []
  else:
    yield from os.walk(path, followlinks=followlinks)


def resolve_paths(  # noqa: C901,PLR0912
  src_dir: str,
  f_name: str,
  f_dest: str,
  i_dest: str,
  f_src: str,
) -> dict[str, object]:
  src_path = f_src if f_src else (src_dir.rstrip('/') + '/' + f_name)
  if not f_name:
    f_name = Path(src_path).name

  # Determine prefix
  prefix = ''
  if i_dest and not f_dest.startswith('/'):
    prefix = i_dest.rstrip('/') + '/'
  src_is_dir = Path(src_path).is_dir()

  # Compute dest4copy
  if f_dest:
    dest4copy = prefix + f_dest
  elif not src_is_dir:
    dest4copy = prefix + Path(f_name).name
  else:
    dest4copy = prefix

  # Compute dest4path
  list4path: dict[str, list[str]] = {}
  if f_dest:
    dest4path = prefix + f_dest.rstrip('/')
    if f_dest.endswith('/') and not f_name.endswith('/'):
      dest4path += '/' + Path(f_name).name
  elif f_name.endswith('/'):
    dest4path = ''
    for _root, dirs, files in ww2_file(Path(src_path), followlinks=True):
      prefix = dest4copy.rstrip('/') + '/'
      list4path["d"] = [prefix + d for d in dirs]
      list4path["f"] = [prefix + f for f in files]
  else:
    dest4path = prefix + Path(f_name).name

  # Compute dest4dir
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
    "list4path": list4path,
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
