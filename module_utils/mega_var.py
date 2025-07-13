from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator


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
