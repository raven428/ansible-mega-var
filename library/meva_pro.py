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

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)
from ansible.module_utils.mega_var import (  # type: ignore[reportMissingImports]
  resolve_paths,
)


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

  module.exit_json(
    changed=False,
    **resolve_paths(src_dir, f_name, f_dest, i_dest, f_src),
  )


if __name__ == '__main__':
  main()
