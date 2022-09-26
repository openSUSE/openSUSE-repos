#
# spec file for package openSUSE-repos
#
# Copyright (c) 2022 SUSE LLC
# Copyright (c) 2022 Neal Gompa <ngompa13@gmail.com>
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global debug_package %{nil}
Name:           openSUSE-repos-LeapMicro
Version:        0
Release:        0
Summary:        openSUSE package repositories
License:        MIT
Group:          System/Management
URL:            https://github.com/openSUSE/openSUSE-repos
Source:        	openSUSE-repos-%{version}.tar.xz
#boo#1203715
BuildRequires:  -post-build-checks
# We're compatible with any SUSE Linux distribution
Requires:       suse-release
Requires:       zypper
Provides:	openSUSE-repos
Conflicts:      otherproviders(openSUSE-repos)
%description
Definitions for openSUSE repository management via zypp-services


%files

%dir %{_datadir}/zypp/local/
%dir %{_datadir}/zypp/local/service
%dir %{_datadir}/zypp/local/service/openSUSE
%dir %{_datadir}/zypp/local/service/openSUSE/repo
%ghost %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%{_sysconfdir}/zypp/vars.d/DIST_ARCH

%{_datadir}/zypp/local/service/openSUSE/repo/opensuse-leap-miro-repoindex.xml

%prep
%setup -n openSUSE-repos-%{version}


%build
# Nothing to build


%install

mkdir -p %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
mkdir -p %{buildroot}%{_sysconfdir}/zypp/vars.d/

# Setup for primary arches
install opensuse-leap-micro-repoindex.xml -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo

%ifarch %{ix86}
echo "x86" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch x86_64
echo "x86_64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch aarch64
echo "aarch64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch armv6l armv6hl
echo "armv6hl" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch armv7l armv7hl
echo "armv7hl" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch ppc ppc64 ppc64le
echo "ppc" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch riscv64
echo "riscv" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch s390x
echo "zsystems" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif


%post
ln -sf opensuse-leap-micro-repoindex.xml %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml

# We hereby declare that running this will not influence existing transaction
ZYPP_READONLY_HACK=1 zypper addservice %{_datadir}/zypp/local/service/openSUSE openSUSE

%postun
if [ "$1" = 0 ] ; then
  # We hereby declare that running this will not influence existing transaction
  ZYPP_READONLY_HACK=1 zypper removeservice openSUSE
  if [ -L "%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml" ] ; then
    rm -f %{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
  fi
fi



%changelog
