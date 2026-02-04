from __future__ import annotations

ANSIBLE_METADATA = {
  'metadata_version': '1.0.0',
  'status': ['preview'],
  'supported_by': 'community',
}

DOCUMENTATION = r'''
---
module: meva_pro
short_description: Calculate files and directories names for _down2unp.yaml
version_added: "1.0.0"
description:
  - Calculate files and directories names for _down2unp.yaml
options:
  src_dir:
    description:
      - Path of f.name location
    required: false
    type: str
  f_name:
    description:
      - Value of f.name
    required: false
    type: str
  f_dest:
    description:
      - Value of f.dest, can be any even undefined
    required: false
    type: str
  i_dest:
    description:
      - Value of i.dest, should be absolute if defined
    required: false
    type: str
  f_src:
    description:
      - Source path replacing src_dir+f_name
    required: false
    type: str
  get_checksum:
    description:
      - Calculate sha512 checksum for source file
    required: false
    type: bool
    default: false
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

# pylint: disable=import-error
import hashlib
from pathlib import Path

from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)
from ansible.module_utils.mega_var import (  # type: ignore[reportMissingImports]
  resolve_paths,
)


def get_file_stat(file_path: str) -> dict[str, object] | None:
  path = Path(file_path)
  if not path.exists():
    return None

  stat_info = path.stat()
  checksum = ''

  if path.is_file():
    sha512 = hashlib.sha512()
    with path.open('rb') as f:
      for chunk in iter(lambda: f.read(65536), b''):
        sha512.update(chunk)
    checksum = sha512.hexdigest()

  return {
    'exists': True,
    'checksum': checksum,
    'size': stat_info.st_size,
    'mode': oct(stat_info.st_mode)[-4:],
  }


def main() -> None:
  module = AnsibleModule(
    argument_spec={
      'src_dir': {
        'type': 'str',
        'required': False,
        'default': '',
      },
      'f_name': {
        'type': 'str',
        'required': False,
        'default': '',
      },
      'f_dest': {
        'type': 'str',
        'required': False,
        'default': '',
      },
      'i_dest': {
        'type': 'str',
        'required': False,
        'default': '',
      },
      'f_src': {
        'type': 'str',
        'required': False,
        'default': '',
      },
      'get_checksum': {
        'type': 'bool',
        'required': False,
        'default': False,
      },
    },
    supports_check_mode=True,
  )
  f_src = module.params['f_src']
  f_name = module.params['f_name']
  f_dest = module.params['f_dest']
  i_dest = module.params['i_dest']
  src_dir = module.params['src_dir']
  get_checksum = module.params['get_checksum']

  if not i_dest and not f_dest:
    module.fail_json(msg='Either i.dest or f.dest must be defined and non-empty')
  if i_dest and not i_dest.startswith('/'):
    module.fail_json(msg='i_dest must be an absolute path')

  result = resolve_paths(src_dir, f_name, f_dest, i_dest, f_src)

  if get_checksum and not result['src_is_dir']:
    result['src_checksum'] = get_file_stat(result['src4copy'])
  else:
    result['src_checksum'] = None

  module.exit_json(changed=False, **result)


if __name__ == '__main__':
  main()
