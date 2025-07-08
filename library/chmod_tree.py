from __future__ import annotations

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
from typing import Iterator

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)


def update_mode(  # noqa: PLR0913
  module: AnsibleModule, path: Path, current_mode: int, target_mode: int, key: str,
  traverse_count: dict[str, int], changed_count: dict[str, int],
  changed_files: list[dict[str, str]], *, follow: bool, verbose: bool
) -> bool:
  traverse_count[key] += 1
  if current_mode != target_mode:
    if not module.check_mode:
      path.chmod(target_mode, follow_symlinks=follow)
    changed_count[key] += 1
    if verbose:
      changed_files.append({
        "path": str(path),
        "after": f"{target_mode:o}",
        "before": f"{current_mode:o}",
      })
    return True
  return False


def ww2_file(
  path: Path,
  *,
  followlinks: bool = False,
) -> Iterator[tuple[str, list[str], list[str]]]:
  if path.is_file():
    yield str(path), [], []
  else:
    yield from os.walk(path, followlinks=followlinks)


def main() -> None:  # noqa: C901
  module = AnsibleModule(
    argument_spec={
      "path": {
        "required": True,
        "type": "str"
      },
      "dir_mode": {
        "required": False,
        "type": "str",
        "default": None,
      },
      "file_mode": {
        "required": False,
        "type": "str",
        "default": "0644",
      },
      "exec_mode": {
        "required": False,
        "type": "str",
        "default": None,
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
      "skip_entry": {
        "required": False,
        "type": "bool",
        "default": True,
      },
      "exec_bit": {
        "required": False,
        "type": "str",
        "default": "0111",
      },
      "always_unchanged": {
        "required": False,
        "type": "bool",
        "default": False,
      },
    },
    supports_check_mode=True,
  )
  file_mode = int(module.params["file_mode"], 8)
  exec_bit = int(module.params["exec_bit"], 8)
  param = module.params.get("dir_mode")
  dir_mode = int(param, 8) if param is not None else file_mode | exec_bit
  param = module.params.get("exec_mode")
  exec_mode = int(param, 8) if param is not None else file_mode | exec_bit
  follow = module.params["follow"]
  verbose = module.params["verbose"]
  changed_count = {
    "d": 0,
    "e": 0,
    "f": 0,
  }
  traverse_count = changed_count.copy()
  changed_files: list[dict[str, str]] = []
  changed = False
  root_path = Path(module.params["path"])
  for root, dirs, files in ww2_file(root_path, followlinks=follow):
    root_path = Path(root)
    # Entrypoint:
    dirs1 = dirs.copy()
    files1 = files.copy()
    if not module.params["skip_entry"]:
      try:
        st = root_path.stat(follow_symlinks=follow)
        special_names = [""]
        if root_path.is_dir():
          dirs1 = special_names + dirs1
        else:
          files1 = special_names + files1
      except FileNotFoundError:
        continue
    # Directories:
    for name in dirs1:
      full_path = root_path / name
      try:
        current_mode = stat.S_IMODE(full_path.stat(follow_symlinks=follow).st_mode)
      except FileNotFoundError:
        continue
      if update_mode(
        module=module,
        path=full_path,
        current_mode=current_mode,
        target_mode=dir_mode,
        key="d",
        traverse_count=traverse_count,
        changed_count=changed_count,
        changed_files=changed_files,
        follow=follow,
        verbose=verbose
      ):
        changed = True
    # Files:
    for name in files1:
      full_path = root_path / name
      try:
        st = full_path.stat(follow_symlinks=follow)
      except FileNotFoundError:
        continue
      current_mode = stat.S_IMODE(st.st_mode)
      exec_mask = stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
      is_exec = bool(st.st_mode & exec_mask)
      if update_mode(
        module=module,
        path=full_path,
        current_mode=current_mode,
        target_mode=exec_mode if is_exec else file_mode,
        key="e" if is_exec else "f",
        traverse_count=traverse_count,
        changed_count=changed_count,
        changed_files=changed_files,
        follow=follow,
        verbose=verbose,
      ):
        changed = True

  module.exit_json(
    changed=False if module.params["always_unchanged"] else changed,
    message=f"Changed {changed_count} of {traverse_count} file modes: {changed_files}"
    if verbose else f"Changed {changed_count} modes of  {traverse_count} for d: "
    f"{dir_mode:o} e:{exec_mode:o} f:{file_mode:o} for '{root_path}' directory tree"
  )


if __name__ == '__main__':
  main()
