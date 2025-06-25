ANSIBLE_METADATA = {
  'metadata_version': '1.0',
  'status': ['preview'],
  'supported_by': 'community',
}

DOCUMENTATION = r'''
---
module: chmod_tree
short_description: Apply file modes to directories, executable and non-executable files
version_added: "1.0.0"
description:
  - Applies file modes recursively to directories, executable files, and other files
    under a specified path.
options:
  path:
    description:
      - The target path to apply permissions to.
    required: true
    type: str
  dir_mode:
    description:
      - File mode to apply to directories.
    required: false
    type: str
    default: '0755'
  file_mode:
    description:
      - File mode to apply to regular files.
    required: false
    type: str
    default: '0644'
  exec_mode:
    description:
      - File mode to apply to executable files.
    required: false
    type: str
    default: '0755'
  follow:
    description:
      - Follow symlinks.
    required: false
    type: bool
    default: false
  verbose:
    description:
      - Return detailed list of changed files.
    required: false
    type: bool
    default: false
author:
  - ChatGPT (https://chatgpt.com)
  - Dmitry Sukhodoyev (https://github.com/raven428/ansible-mega-var)
'''

EXAMPLES = r'''
- name: Apply file modes
  chmod_tree:
    path: /opt/my_dir
    dir_mode: '0750'
    file_mode: '0640'
    exec_mode: '0751'
'''

RETURN = r'''
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
import stat
from pathlib import Path

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)


def main() -> None:
  module = AnsibleModule(
    argument_spec={
      "path": {
        "required": True,
        "type": "str",
      },
      "dir_mode": {
        "required": False,
        "type": "str",
        "default": "0755",
      },
      "file_mode": {
        "required": False,
        "type": "str",
        "default": "0644",
      },
      "exec_mode": {
        "required": False,
        "type": "str",
        "default": "0755",
      },
      "follow": {
        "required": False,
        "type": "bool",
        "default": False,
      },
      "verbose": {
        "required": False,
        "type": "bool",
        "default": False,
      },
    },
    supports_check_mode=True,
  )

  dir_mode = int(module.params["dir_mode"], 8)
  file_mode = int(module.params["file_mode"], 8)
  exec_mode = int(module.params["exec_mode"], 8)
  follow = module.params["follow"]
  verbose = module.params["verbose"]

  changed_count = 0
  changed_files = []
  changed = False

  for root, dirs, files in os.walk(
    Path(module.params["path"]), followlinks=follow
  ):
    root_path = Path(root)

    # Directories
    for name in dirs:
      full_path = root_path / name
      current_mode = stat.S_IMODE(
        full_path.stat(follow_symlinks=follow).st_mode
      )
      if current_mode != dir_mode:
        if not module.check_mode:
          full_path.chmod(dir_mode, follow_symlinks=follow)
        changed = True
        changed_count += 1
        if verbose:
          changed_files.append({
            "path": str(full_path),
            "before": oct(current_mode),
            "after": oct(dir_mode),
          })

    # Files
    for name in files:
      full_path = root_path / name
      st = full_path.stat(follow_symlinks=follow)
      current_mode = stat.S_IMODE(st.st_mode)
      exec_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
      is_exec = bool(st.st_mode & exec_mask)
      target_mode = exec_mode if is_exec else file_mode

      if current_mode != target_mode:
        if not module.check_mode:
          full_path.chmod(target_mode, follow_symlinks=follow)
        changed = True
        changed_count += 1
        if verbose:
          changed_files.append({
            "path": str(full_path),
            "before": oct(current_mode),
            "after": oct(target_mode),
          })

  module.exit_json(
    changed=changed,
    message=f"Changed [{changed_count}] file modes: {changed_files}"
    if verbose else f"Changed [{changed_count}] file modes"
  )


if __name__ == '__main__':
  main()
