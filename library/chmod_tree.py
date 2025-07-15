from __future__ import annotations

ANSIBLE_METADATA = {
  'metadata_version': '1.0.0',
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
  skip_entry:
    description:
      - Skip entry record from chmod.
    required: false
    type: bool
    default: true
  exec_bit:
    description:
      - Apply this mask to filemode for executive files.
    required: false
    type: str
    default: '0111'
  always_unchanged:
    description:
      - Return always not changed result.
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

import stat
from pathlib import Path

# pylint: disable=import-error
from ansible.module_utils.basic import (  # type: ignore[reportMissingImports]
  AnsibleModule,
)
from ansible.module_utils.mega_var import (  # type: ignore[reportMissingImports]
  ww2_file,
)


def update_mode(  # noqa: PLR0913
  module: AnsibleModule, path: Path, current_mode: int, target_mode: int | None,
  key: str, traverse_count: dict[str, int], changed_count: dict[str, int],
  changed_files: list[dict[str, str]], *, follow: bool, verbose: bool
) -> bool:
  traverse_count[key] += 1
  changed = False
  log_change = False
  after = "None"
  if target_mode is None:
    changed_count[key] += 1
    log_change = True
  elif current_mode != target_mode:
    changed_count[key] += 1
    changed = True
    log_change = True
    after = f"{target_mode:o}"
    if not module.check_mode:
      path.chmod(target_mode, follow_symlinks=follow)
  if verbose and log_change:
    changed_files.append({
      "path": str(path),
      "before": f"{current_mode:o}",
      "after": after,
    })
  return changed


def main() -> None:  # noqa: C901
  module = AnsibleModule(
    argument_spec=dict(
      path=dict(type="str", required=True),
      dir_mode=dict(type="str", required=False, default=None),
      file_mode=dict(type="str", required=False, default=None),
      exec_mode=dict(type="str", required=False, default=None),
      follow=dict(type="bool", required=False, default=False),
      verbose=dict(type="bool", required=False, default=False),
      skip_entry=dict(type="bool", required=False, default=True),
      exec_bit=dict(type="str", required=False, default="0111"),
      always_unchanged=dict(type="bool", required=False, default=False),
    ),
    supports_check_mode=True,
  )
  dir_mode = module.params.get("dir_mode")
  file_mode = module.params.get("file_mode")
  exec_mode = module.params.get("exec_mode")
  exec_bit = int(module.params["exec_bit"], 8)
  if file_mode is not None:
    file_mode = int(file_mode, 8)
    exec_mode = int(exec_mode, 8) if exec_mode is not None else file_mode | exec_bit
    dir_mode = int(dir_mode, 8) if dir_mode is not None else file_mode | int("0111", 8)
  follow = module.params["follow"]
  verbose = module.params["verbose"]
  changed_count = dict(d=0, e=0, f=0)
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
    if verbose else f"Changed {changed_count} modes of {traverse_count} to d:"
    f"{dir_mode:o} e:{exec_mode:o} f:{file_mode:o} for '{root_path}' directory tree"
  )


if __name__ == '__main__':
  main()
