#!/usr/bin/env bash
set -ueo pipefail
umask 0022
MY_BIN="$(realpath "$0")"
MY_PATH="$(dirname "${MY_BIN}")"
cd "${MY_PATH}/.."
# shellcheck disable=1091
SKIP_DID=1 source "${MY_PATH}/../molecule/prepare.sh"
# shellcheck disable=2154
"${_appimage_bin}" pytest --color=yes \
  -vv -o cache_dir=/tmp/meva_pro/main tests/meva_pro/main_tests.py
