#!/bin/bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT

mkdir -p "$tmpdir/checks" "$tmpdir/bin"

cp "$repo_root/checks/repo_checks" "$tmpdir/checks/repo_checks"

cat > "$tmpdir/opensuse-leap16-repoindex.xml" <<'XML'
<repoindex
    disturl="https://example.test"
    distsub="leap">
  <repo url="https://example.test/repo?mediahandler=curl2"/>
</repoindex>
XML

cat > "$tmpdir/bin/curl" <<'MOCK'
#!/bin/bash
for arg in "$@"; do
    url="$arg"
done
printf '%s\n' "$url" >> "$CURL_CAPTURE"
exit 0
MOCK
chmod +x "$tmpdir/bin/curl"

export CURL_CAPTURE="$tmpdir/curl-urls.txt"
export PATH="$tmpdir/bin:$PATH"

bash "$tmpdir/checks/repo_checks" > "$tmpdir/output.txt"

expected='https://example.test/repo/repodata/repomd.xml?mediahandler=curl2'

if ! grep -Fqx "$expected" "$CURL_CAPTURE"; then
    echo "FAIL: validator did not check the expected URL"
    cat "$tmpdir/output.txt"
    cat "$CURL_CAPTURE" 2>/dev/null || true
    exit 1
fi

echo "PASS: query parameter preserved and metadata path correctly placed"
