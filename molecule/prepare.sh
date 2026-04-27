#!/usr/bin/env bash
set -ueo pipefail
umask 0022
: "${APPIMAGE_RELEASE:="latest"}"
: "${APPIMAGE_NAME:="ansible-11-001.AppImage"}"
[[ -v ANSIBLE_GITHUB_TOKEN ]] || {
  echo 'mandatory variable [ANSIBLE_GITHUB_TOKEN] not found, exiting…'
  exit 1
}
export DEBIAN_FRONTEND=noninteractive
/usr/bin/env which sponge >/dev/null || {
  /usr/bin/env sudo apt-get update &&
    /usr/bin/env sudo su -c 'DEBIAN_FRONTEND=noninteractive apt-get install -y moreutils'
}
_gh_base='https://github.com/raven428/container-images/releases'
_appimage_bin="${HOME}/bin/ansible-current.AppImage"
if [[ ! -x "${_appimage_bin}" ]]; then
  if [[ "${APPIMAGE_RELEASE}" == 'latest' ]]; then
    _url="${_gh_base}/latest/download/${APPIMAGE_NAME}"
  else
    _url="${_gh_base}/download/${APPIMAGE_RELEASE}/${APPIMAGE_NAME}"
  fi
  /usr/bin/env mkdir -p "${HOME}/bin"
  /usr/bin/env curl -fSL --progress-bar -o "${_appimage_bin}" "${_url}"
  /usr/bin/env chmod 755 "${_appimage_bin}"
fi
export ANSIBLE_ROLES_PATH='/tmp/ansible/roles2test'
/usr/bin/env mkdir -vp "${ANSIBLE_ROLES_PATH}"
/usr/bin/env rm -vf "${ANSIBLE_ROLES_PATH}/ansible-mega-var"
/usr/bin/env ln -sfv "${PWD}" "${ANSIBLE_ROLES_PATH}/ansible-mega-var"
