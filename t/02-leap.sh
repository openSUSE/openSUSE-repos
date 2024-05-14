#!lib/test-in-container-systemd.sh leap

set -e

mkdir -p /usr/share/zypp/local/service/openSUSE/repo/
ln -sf /opt/project/opensuse-leap-repoindex.xml /usr/share/zypp/local/service/openSUSE/repo/repoindex.xml
zypper addservice /usr/share/zypp/local/service/openSUSE/ openSUSE

zypper -vvv ref -s || tail -n 2000 /var/log/zypper.log

grep -r baseurl /etc/zypp/repos.d
grep -r baseurl /etc/zypp/repos.d | grep -q cdn.opensuse.org

# make sure we can install a random package
zypper -vvvn in vim

echo success
