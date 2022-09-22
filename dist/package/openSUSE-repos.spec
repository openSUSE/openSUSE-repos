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
# Main package version
%global mainversion 0
%if 0%{?suse_version} && (!0%{?sle_version})
%global distname Tumbleweed
%endif
%if 0%{?suse_version} && 0%{?sle_version} && 0%{?is_opensuse}
%global distname Leap
%endif
Name:           openSUSE-repos
Version:        %{mainversion}
Release:        0
Summary:        openSUSE package repositories
License:        MIT
Group:          System/Management
URL:            https://opensuse.org/
Source1:        opensuse-tumbleweed-repoindex.xml
Source2:        opensuse-tumbleweed-ports-repoindex.xml
Source3:        opensuse-leap-repoindex.xml
Source4:        opensuse-leap-ports-repoindex.xml

%description
A local service providing openSUSE repository definitions for zypp

# -------------------------------------------------------------------------------

%package %{distname}
Version:        0%{?suse_version}
Summary:        openSUSE %{distname} package repositories
# We're compatible with any SUSE Linux distribution
Requires:       suse-release
Requires:       zypper
BuildRequires:  zypper
# Prefer the version that matches our distribution
Suggests:       %{name}-%{distname}
Conflicts:      %{name}
# Only one instance of this package may be installed at a time...
Provides:       %{name}
%if "%{distname}" == "Tumbleweed"
Conflicts:      %{name}-Leap
# Unconditionally ensure Leap upgrades to Tumbleweed
Obsoletes:      %{name}-Leap
%endif

%description %{distname}
openSUSE %{distname} local service providing openSUSE repository definitions for zypp

%files %{distname}

%dir %{_datadir}/zypp/local/
%dir %{_datadir}/zypp/local/service
%dir %{_datadir}/zypp/local/service/openSUSE
%dir %{_datadir}/zypp/local/service/openSUSE/repo
%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%{_sysconfdir}/zypp/vars.d/DIST_ARCH

# -------------------------------------------------------------------------------

%if "%{distname}" == "Leap"
%package Tumbleweed
Version:        0%{?suse_version}
Summary:        openSUSE Tumbleweed package repositories
# We're compatible with any SUSE Linux distribution
Requires:       suse-release
Conflicts:      %{name}
Conflicts:      %{name}-Leap
# Only one instance of this package may be installed at a time...
Provides:       %{name}

%description Tumbleweed
openSUSE %{distname} package repository files for DNF and PackageKit.

%files Tumbleweed
%dir %{_datadir}/zypp/local/
%dir %{_datadir}/zypp/local/service
%dir %{_datadir}/zypp/local/service/openSUSE
%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%{_sysconfdir}/zypp/vars.d/DIST_ARCH

%endif

%prep
# Nothing to prepare


%build
# Nothing to build


%install

# ==== Primary Tumbleweed repository configuration ====

mkdir -p %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo
mkdir -p %{buildroot}%{_sysconfdir}/zypp/vars.d/

# Setup for primary arches
%ifarch %{ix86} x86_64
install %{SOURCE1} -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif

# Setup for ports
%ifarch aarch64 %{arm} %{power64} ppc s390x riscv64
install %{SOURCE2} -pm 0644%{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif

%if "%{distname}" == "Leap"

# ==== Primary Leap repository configuration ====

# Setup for main SLE/Leap arches
%ifarch ix86 x86_64 aarch64 power64 s390x
install %{SOURCE3} -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%else
install %{SOURCE4} -pm 0644 %{buildroot}%{_datadir}/zypp/local/service/openSUSE/repo/repoindex.xml
%endif
%endif

# Ports for both Leap and TW
# Used in baseurl needs to match with /ports/$directory on pontifex

%ifarch %{ix86} x86_64
echo "x86" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch x86_64
echo "x86_64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
%endif

%ifarch aarch64
echo "aarch64" >  %{buildroot}%{_sysconfdir}/zypp/vars.d/DIST_ARCH
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
zypper addservice %{_datadir}/zypp/local/service/openSUSE  openSUSE

%changelog
