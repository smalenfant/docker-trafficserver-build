FROM centos:8

RUN dnf -y install dnf-plugins-core && yum clean all
RUN dnf -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
RUN dnf install -y --setopt=tsflags=nodocs --enablerepo=powertools \
                git autoconf automake libtool gcc gcc-c++ \
                pkgconfig pcre-devel tcl-devel expat-devel openssl-devel \
                libcap python3 libcap-devel hwloc hwloc-devel libcurl-devel rpm-build perl-ExtUtils-MakeMaker \
                make sudo \
                && yum clean all

# Default version of GCC and Python
RUN gcc --version && python3 --version

# Install some developer style software collections with intent to
# use newer version of GCC and Python than the OS provided
#RUN yum install -y devtoolset-8 rh-python36 && yum clean all

# Yum installed packages but the default OS-provided version is still used.
#RUN gcc --version && python --version

# (default was SHELL [ "/bin/sh", "-c" ])
# https://docs.docker.com/engine/reference/builder/#shell
#
# See also `scl` man page for enabling multiple packages if desired:
# https://linux.die.net/man/1/scl
#SHELL [ "/usr/bin/scl", "enable", "devtoolset-8", "rh-python36" ]

# Switching to a different shell has brought the new versions into scope.
#RUN gcc --version && python --version

RUN useradd builder -u 1000 -m -G users,wheel && \
    echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "# macros"                            >  /home/builder/.rpmmacros && \
    echo "%_topdir    /home/builder/rpmbuild"  >> /home/builder/.rpmmacros && \
    echo "%_sourcedir %{_topdir}/SOURCES"      >> /home/builder/.rpmmacros && \
    echo "%_builddir  %{_topdir}/BUILD"        >> /home/builder/.rpmmacros && \
    echo "%_specdir   %{_topdir}/SPECS"        >> /home/builder/.rpmmacros && \
    echo "%_rpmdir    %{_topdir}/RPMS"         >> /home/builder/.rpmmacros && \
    echo "%_srcrpmdir %{_topdir}/SRPMS"        >> /home/builder/.rpmmacros && \
    echo "%_smp_mflags -j4"                    >> /home/builder/.rpmmacros && \
    #mkdir /home/builder/rpm && \
    chown -R builder /home/builder

USER builder

WORKDIR /home/builder/rpmbuild
RUN pwd

ENV FLAVOR=rpmbuild OS=centos DIST=el8
ARG TS_VERSION

ADD entrypoint.sh /usr/bin/entrypoint.sh

ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
