# docker-trafficserver-build

Traffic Server doesn't work right off the box with Traffic Control. This provides a trafficserver build which incorporate astats_over_http.

This is to provide some help to build Traffic Server using docker.

## Instructions

- Clone this repository

`git clone https://github.com/smalenfant/docker-trafficserver-build.git`

- Download the required Traffic Server version in the SOURCE directory

- Update the SPEC files accordingly. 


http://archive.apache.org/dist/trafficserver/

- Start the build container

```
CENTOS_VERSION=el6 TS_VERSION=6.2.2 docker-compose up trafficserver
CENTOS_VERSION=el7 TS_VERSION=7.1.1 docker-compose up trafficserver
CENTOS_VERSION=el8 TS_VERSION=8.1.2 docker-compose up trafficserver
```

The RPMS should be in the `rpmbuild/RPMS/x86_64` 

## Patches

To create traffic server patches, the following was executed from `https://github.com/smalenfant/trafficserver.git`

- `git diff 0b7b630858b4983d077a63074776abdfa48778f8 6.2.2-astats -- plugins/ configure.ac > ../docker-trafficserver-build/rpmbuild/SOURCES/astats_over_http-1.3-6.2.x.patch`
- `git diff 6f6a04aae105291c774d0c4116597fdc7b345121 7.1.1-astats -- plugins/ ../docker-trafficserver-build/rpmbuild/SOURCES/astats_over_http-1.3-7.1.x.patch`
- `git diff c080cc1ec39e21b04ba28e76a6ad80927b71f798 8.1.x-astats -- plugins/ ../docker-trafficserver-build/rpmbuild/SOURCES/astats_over_http-1.5-8.1.x.patch`

To create an archive of Traffic Server

- `git archive --prefix=trafficserver-7.1.7/ --format=tar -v HEAD | bzip2 -9 -c > ../docker-trafficserver-build/rpmbuild/SOURCES/trafficserver-7.1.7.tar.bz2`
- `git rev-list HEAD --count` - Use to update the spec file
