#!/usr/bin/env bash
set -ueo pipefail
umask 0022
MY_BIN="$(realpath "$0")"
MY_PATH="$(dirname "${MY_BIN}")"
cd "${MY_PATH}/../.."
# shellcheck disable=1091
source "${MY_PATH}/../prepare.sh"
LOG_PATH="/tmp/molecule-$(/usr/bin/env date '+%Y%m%d%H%M%S.%3N')"
sce='default'
printf "\n\n\nmolecule [create] action\n"
# shellcheck disable=2154
ANSIBLE_LOG_PATH="${LOG_PATH}-0create" "${_appimage_bin}" molecule -v create -s "${sce}"
printf "\n\n\nmolecule [converge] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-2converge" \
  "${_appimage_bin}" molecule -v converge -s "${sce}" --
printf "\n\n\nmolecule [idempotence] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-3idempotence" \
  "${_appimage_bin}" molecule -v idempotence -s "${sce}" --
printf "\n\n\nmolecule [converge] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-4converge-check" \
  "${_appimage_bin}" molecule -v converge -s "${sce}" -- --check
printf "\n\n\nmolecule [idempotence] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-5idempotence-check" \
  "${_appimage_bin}" molecule -v idempotence -s "${sce}" -- --check
