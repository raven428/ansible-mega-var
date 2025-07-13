from __future__ import annotations

from typing import TYPE_CHECKING, Any
from unittest.mock import patch

# pylint: disable=import-error
import pytest  # type: ignore[reportMissingImports]

from module_utils.mega_var import resolve_paths
from tests.meva_pro.main_data import cases_resolve_paths, mock_dirs_list

if TYPE_CHECKING:
  from pathlib import Path


def mock_is_dir(self: Path) -> bool:
  return str(self) in mock_dirs_list


@patch('module_utils.mega_var.Path.is_dir', new=mock_is_dir)
@pytest.mark.parametrize("case", cases_resolve_paths)
def test_resolve_paths(case: dict[str, Any]) -> None:
  result = resolve_paths(
    case["src_dir"],
    case["f_name"],
    case["f_dest"],
    case["i_dest"],
    case["f_src"],
  )
  expected = {
    "dest4dir": case["dest4dir"],
    "dest4copy": case["dest4copy"],
    "dest4path": case["dest4path"],
    "src4copy": case["src4copy"],
    "src_is_dir": case["src_is_dir"],
  }
  result.pop("a", None)
  result.pop("list4path", None)
  assert result == expected  # noqa: S101
