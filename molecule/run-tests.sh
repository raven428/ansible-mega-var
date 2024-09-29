#!/usr/bin/env bash
set -ueo pipefail
: "${NSP_NAME:="nsp4ans"}"
/usr/bin/env which deploy-nspawn.sh >/dev/null || (
  /usr/bin/env curl -sL -o /usr/local/bin/deploy-nspawn.sh \
    https://raw.githubusercontent.com/raven428/container-images/refs/heads/raven428/some-fixes-001/sources/victim-ubuntu-22_04/files/deploy.sh
  /usr/bin/env chmod 755 /usr/local/bin/deploy-nspawn.sh
)
/usr/bin/env which ansible-docker.sh >/dev/null || (
  /usr/bin/env curl -sL -o /usr/local/bin/ansible-docker.sh \
    https://raw.githubusercontent.com/raven428/container-images/refs/heads/raven428/some-fixes-001/sources/ansible-9_9_0/ansible-docker.sh
  /usr/bin/env chmod 755 /usr/local/bin/ansible-docker.sh
)
# shellcheck disable=1090
source "$(which deploy-nspawn.sh)"
# (
#   cd "${MY_PATH}/../ansible"
#   ansible-docker.sh ansible-playbook site.yaml \
#     --diff -i inventory -u root -l "${NSP_NAME}" -t nonexistent
#   /usr/bin/env machinectl -la
#   ansible-docker.sh ansible-playbook site.yaml \
#     --diff -i inventory -u root -l "${NSP_NAME}"
# )
