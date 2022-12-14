# openSUSE-repos

**Definitions for openSUSE repository management via zypp-services.**

This feature was originally requested as part of https://code.opensuse.org/leap/features/issue/91

See official [docs](https://doc.opensuse.org/projects/libzypp/HEAD/zypp-services.html#services-usecase-4) for zypp-services for more details.


## Example manual usage of zypper as
```
$ tree /somewhere # zypp expects repo/repoindex.xml
/somewhere
└── repo
    └── repoindex.xml

$ zypper addservice /somewhere openSUSE # Use openSUSE prefix for all reposistories managed by service
$ zypper ref -s # optionally force refresh services
```

## Cleanup of distribution repositories not managed by zypp-services

You might want to remove old duplicate entries in */etc/zypp/repos.d/*.

Repositories managed by zypp-services can be easily identified as they will have openSUSE: prefix (or any other that you have chosen).


```
$ ls -la /etc/zypp/repos.d/ | grep -v openSUSE: # skip service managed repos
openSUSE-20220923-0.repo download.opensuse.org-oss.repo
repo-debug.repo download.opensuse.org-tumbleweed.repo
repo-source.repo
```
**Cleanup of old distribution repositories on a freshly installed openSUSE Tumbleweed**

```
$ sudo rm -f /etc/zypp/repos.d/download.opensuse.org-non-oss.repo \
/etc/zypp/repos.d/openSUSE-*-0.repo \
/etc/zypp/repos.d/download.opensuse.org-oss.repo \
/etc/zypp/repos.d/repo-debug.repo \
/etc/zypp/repos.d/download.opensuse.org-tumbleweed.repo \
/etc/zypp/repos.d/repo-source.repo
```

**Cleanup of old distribution repositories on a freshly installed openSUSE Leap 15.X**

```
$ sudo rm -f  /etc/zypp/repos.d/repo-backports-debug-update.repo \
/etc/zypp/repos.d/repo-backports-update.repo \
/etc/zypp/repos.d/repo-sle-debug-update.repo \
/etc/zypp/repos.d/repo-sle-update.repo
```

## How to contribute?

Package is developed in [GitHub/openSUSE](https://github.com/openSUSE/openSUSE-repos/).

Package needs to be manually updated in [OBS](https://build.opensuse.org/package/show/Base:System/openSUSE-repos) once changes are merged in GitHub.

Make sure to install osc and required obs services by openSUSE-repos package

```
$ sudo zypper in openSUSE-release-tools obs-service-tar
```

Fork the repository in OBS, fetch latest request and make a submit request.

```
$ osc bco Base:System/openSUSE-repos
cd home:i*:branches:Base:System/openSUSE-repos
osc service runall
osc addremove
osc commit # changelog can be reviewed by osc vc
osc sr # submit request back to Base:System
```

Don't forget to send changes back to Tumbleweed and Leap once changes are merged to Base:System.

```
$ osc sr Base:System openSUSE-repos openSUSE:Factory
$ osc sr openSUSE:Factory openSUSE-repos openSUSE:Leap:15.5 # once merged to Factory
```

That's all. Happy Hacking
