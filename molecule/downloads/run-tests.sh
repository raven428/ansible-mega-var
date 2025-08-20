#!/usr/bin/env bash
set -ueo pipefail
umask 0022
MY_BIN="$(readlink -f "$0")"
MY_PATH="$(dirname "${MY_BIN}")"
cd "${MY_PATH}/../.."
# shellcheck disable=1091
source "${MY_PATH}/../prepare.sh"
sce='downloads'
LOG_PATH="/tmp/molecule-$(/usr/bin/env date '+%Y%m%d%H%M%S.%3N')"
for action in create check converge; do
  printf "\n\n\nmolecule [%s] action\n" $action
  ANSIBLE_LOG_PATH="${LOG_PATH}-0${action}" \
    ansible-docker.sh molecule -v ${action} -s ${sce}
done
printf "\n\n\nmolecule [converge] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-1converge" \
  ansible-docker.sh molecule -v converge -s ${sce} -- --check --extra-vars post_dem=1
printf "\n\n\nmolecule [idempotence] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-1idempotence" \
  ansible-docker.sh molecule -v idempotence -s ${sce} -- --check

export ANSIBLE_DOWNLOAD_TAG='001'
printf "\n\n\nmolecule [update] action\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-2converge" \
  ansible-docker.sh molecule -v converge -s ${sce}
printf "\n\n\nmolecule [update] check\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-2check" \
  ansible-docker.sh molecule -v check -s ${sce}
printf "\n\n\nmolecule [idempotence] update\n"
ANSIBLE_LOG_PATH="${LOG_PATH}-2idempotence" \
  ansible-docker.sh molecule -v idempotence -s ${sce} -- --check
/usr/bin/env docker rm -f "${CONT_NAME}"
