#!lib/test-in-container-systemd.sh leap

set -e

mkdir -p /usr/share/zypp/local/service/openSUSE/repo/
ln -sf /opt/project/opensuse-leap-repoindex.xml /usr/share/zypp/local/service/openSUSE/repo/repoindex.xml
zypper addservice /usr/share/zypp/local/service/openSUSE/ openSUSE

echo =======================
curl -is https://cdn.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml
curl -is https://download.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml
echo =======================
curl -is https://cdn.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml.key
curl -is https://download.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml.key
echo =======================
curl -is https://cdn.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml.asc
curl -is https://download.opensuse.org/update/leap/15.5/sle/repodata/repomd.xml.asc
echo =======================

echo =======================
zypper -vvv ref -s || ( tail -n 200 /var/log/zypper.log && ( sleep 1; exit 1 ) )

echo =======================

grep -r baseurl /etc/zypp/repos.d
grep -r baseurl /etc/zypp/repos.d | grep -q cdn.opensuse.org

# make sure we can install a random package
zypper -vvvn in vim-small

echo success
