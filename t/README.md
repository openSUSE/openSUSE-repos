Scripts to test using podman containers
-------------------

The goal is to cover following workflow:

* Change xml files.
* Spawn a container, add zypper service.
* Check basic installation of a package to verify outcome.

The test is set of bash commands.
The script relies on shebang to prepare an image and spawn a container.

###### Example: Run test for mysql states:

```bash
cd t
./01-tumbleweed.sh
```

#### By default, a container is destroyed when the test finishes.

This is to simplify re-run of tests and do not flood machine with leftover containers after tests.
To make sure container stays around after faiure - set environment variable *T_PAUSE_ON_FAILURE* to 1

###### Example: Connect to the container after test failure

```bash
> # terminal 1
> echo fail >> 01-tumbleweed.sh
> T_PAUSE_ON_FAILURE=1 ./01-tumbleweed.sh
...
bash: line 18: fail: command not found
Test failed, press any key to finish
```
The terminal will wait for any input to finish the test and clean up the container.
Now use another terminal window to check the running podman container and get into it for eventual troubleshooting:

