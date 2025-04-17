#!/usr/bin/env bash
set -ueo pipefail
umask 0022
: "${CONT_NAME:="ans2dkr-${USER}"}"
: "${IMAGE_NAME:="ansible-11_1_0:latest"}"
: "${SSH_AUTH_SOCK:="/dev/null"}"
MY_BIN="$(readlink -f "$0")"
MY_PATH="$(dirname "${MY_BIN}")"
[[ -v ANSIBLE_GITHUB_TOKEN ]] || {
  echo 'mandatory variable [ANSIBLE_GITHUB_TOKEN] not found, exiting…'
  exit 1
}
export DEBIAN_FRONTEND=noninteractive
/usr/bin/env which sponge >/dev/null || {
  /usr/bin/env sudo apt-get update &&
    /usr/bin/env sudo su -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y moreutils'
}
/usr/bin/env which ansible-docker.sh >/dev/null || {
  /usr/bin/env sudo curl -fsSLm 11 -o /usr/local/bin/ansible-docker.sh \
    https://raw.githubusercontent.com/raven428/container-images/refs/heads/master/_shared/install/ansible/ansible-docker.sh
  /usr/bin/env sudo chmod 755 /usr/local/bin/ansible-docker.sh
}
[[ "${SSH_AUTH_SOCK}" == "/dev/null" ]] && export SSH_AUTH_SOCK
mkdir -vp "${HOME}"/.{ansible_async,cache}
ANSIBLE_CONT_NAME="${CONT_NAME}"
ANSIBLE_IMAGE_NAME="ghcr.io/raven428/container-images/docker-${IMAGE_NAME}"
export ANSIBLE_CONT_NAME ANSIBLE_IMAGE_NAME
{
  cd "${MY_PATH}/.."
  ANSIBLE_CONT_ADDONS=" \
    --cgroupns=host --privileged \
    -v ${HOME}/.cache:${HOME}/.cache:rw \
    -v ${HOME}/.ansible_async:${HOME}/.ansible_async:rw \
    -v /sys/fs/cgroup:/sys/fs/cgroup:rw \
    --cap-add=NET_ADMIN --cap-add=SYS_MODULE \
  " ANSIBLE_CONT_COMMAND=' ' /usr/bin/env ansible-docker.sh true
}
count=7
while ! /usr/bin/env docker exec "${CONT_NAME}" systemctl status docker; do
  echo "waiting container ready, left [$count] tries"
  count=$((count - 1))
  if [[ $count -le 0 ]]; then
    break
  fi
  sleep 1
done
for action in create check converge; do
  printf "\n\n\nmolecule [%s] action\n" $action
  ansible-docker.sh molecule -v ${action}
done
printf "\n\n\nmolecule [converge] check\n"
ansible-docker.sh molecule -v converge -- --check --extra-vars post_dem=1
printf "\n\n\nmolecule [idempotence] check\n"
ansible-docker.sh molecule -v idempotence -- --check

printf "\n\n\nmolecule [update] action\n"
ANSIBLE_DOWNLOAD_TAG='001' ansible-docker.sh molecule -v converge
printf "\n\n\nmolecule [update] check\n"
ANSIBLE_DOWNLOAD_TAG='001' ansible-docker.sh molecule -v check
printf "\n\n\nmolecule [idempotence] update\n"
ANSIBLE_DOWNLOAD_TAG='001' ansible-docker.sh molecule -v idempotence -- --check
#/usr/bin/env docker rm -f "${CONT_NAME}"
