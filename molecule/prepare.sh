#!/usr/bin/env bash
set -ueo pipefail
umask 0022
: "${CONT_NAME:="ans2dkr-${USER}"}"
: "${IMAGE_NAME:="ansible-11:latest"}"
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
  # remove after replace docker to podman inside carrier
  /usr/bin/env sudo sed -i 's/--network=host//g' /usr/local/bin/ansible-docker.sh
}
[[ -v GITHUB_JOB ]] && /usr/bin/env curl -fsSLm 11 \
  https://raw.githubusercontent.com/raven428/container-images/refs/heads/master/podman.sh | /usr/bin/env sudo bash
[[ "${SSH_AUTH_SOCK}" == "/dev/null" ]] && export SSH_AUTH_SOCK
[[ -v SKIP_DID ]] || {
  export ANSIBLE_CONT_COMMAND=' '
  IMAGE_NAME="docker-${IMAGE_NAME}"
}
mkdir -vp "${HOME}"/.{ansible_async,cache}
ANSIBLE_CONT_NAME="${CONT_NAME}"
ANSIBLE_IMAGE_NAME="ghcr.io/raven428/container-images/${IMAGE_NAME}"
export CONTENGI ANSIBLE_CONT_NAME ANSIBLE_IMAGE_NAME
{
  ANSIBLE_CONT_ADDONS=" \
    -u 0 --privileged --userns=keep-id \
    --tmpfs /sys/fs/cgroup:rw,nosuid,noexec,nodev,mode=755 \
    -v ${HOME}/.cache:${HOME}/.cache:rw \
    -v ${HOME}/.ansible_async:${HOME}/.ansible_async:rw \
    --cap-add=NET_ADMIN,SYS_MODULE,SYS_ADMIN --replace \
  " /usr/bin/env ansible-docker.sh true
}
[[ -v SKIP_DID ]] || {
  /usr/bin/env "${CONTENGI}" exec "${CONT_NAME}" bash -c \
    'echo '\''{"bridge": "none","iptables":false}'\'' > /etc/docker/daemon.json'
  count=7
  while ! /usr/bin/env "${CONTENGI}" exec "${CONT_NAME}" systemctl status docker; do
    echo "waiting container ready, left [$count] tries"
    count=$((count - 1))
    if [[ $count -le 0 ]]; then
      echo "unable to start docker daemon inside ${CONTENGI} container"
      exit 1
    fi
    sleep 1
  done
}
