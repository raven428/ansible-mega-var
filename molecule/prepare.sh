#!/usr/bin/env bash
set -ueo pipefail
umask 0022
: "${CONT_NAME:="ans2dkr-${USER}"}"
: "${IMAGE_NAME:="ansible-11_1_0:latest"}"
: "${SSH_AUTH_SOCK:="/dev/null"}"
: "${CONTENGI:="podman"}"
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
[[ -v GITHUB_JOB ]] && /usr/bin/env curl -fsSLm 11 \
  https://raw.githubusercontent.com/raven428/container-images/refs/heads/master/podman.sh | /usr/bin/env sudo bash
[[ "${SSH_AUTH_SOCK}" == "/dev/null" ]] && export SSH_AUTH_SOCK
mkdir -vp "${HOME}"/.{ansible_async,cache}
ANSIBLE_CONT_NAME="${CONT_NAME}"
ANSIBLE_IMAGE_NAME="ghcr.io/raven428/container-images/docker-${IMAGE_NAME}"
export ANSIBLE_CONT_NAME ANSIBLE_IMAGE_NAME CONTENGI
{
  cd "${MY_PATH}/../.."
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
