#!/usr/bin/env bash
set -ueo pipefail
umask 0022
MY_BIN="$(readlink -f "$0")"
MY_PATH="$(dirname "${MY_BIN}")"
cd "${MY_PATH}/../.."
# shellcheck disable=1091
source "${MY_PATH}/../prepare.sh"
LOG_PATH="/tmp/molecule-$(/usr/bin/env date '+%Y%m%d%H%M%S.%3N')"
sce='default'

printf "\n\n\nmolecule [create] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-0create" \
  ansible-docker.sh molecule -v create -s "${sce}"

printf "\n\n\nmolecule [converge] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-2converge" \
  ansible-docker.sh molecule -v converge -s "${sce}" --

printf "\n\n\nmolecule [idempotence] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-3idempotence" \
  ansible-docker.sh molecule -v idempotence -s "${sce}" --

printf "\n\n\nmolecule [converge] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-4converge-check" \
  ansible-docker.sh molecule -v converge -s "${sce}" -- --check

printf "\n\n\nmolecule [idempotence] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-5idempotence-check" \
  ansible-docker.sh molecule -v idempotence -s "${sce}" -- --check
