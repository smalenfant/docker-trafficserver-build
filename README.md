# docker-trafficserver-build

Traffic Server doesn't work right off the box with Traffic Control. This provides a trafficserver build which incorporate astats_over_http.

This is to provide some help to build Traffic Server using docker.

## Instructions

- Clone the repository

`TODO`

- Download the required Traffic Server version in the SOURCE directory

http://archive.apache.org/dist/trafficserver/


## Notes

- Please remove the `location` parameter in Traffic Ops, as astats_over_http is built-in.
- test rpmbuild --undefine=_disable_source_fetch
- `git diff 0b7b630858b4983d077a63074776abdfa48778f8 6.2.2-astats -- plugins/ configure.ac > ../docker-trafficserver-build/rpmbuild/SOURCES/astats_over_http-1.3-6.2.x.patch`

