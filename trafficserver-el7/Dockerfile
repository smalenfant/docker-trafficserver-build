FROM centos:7

RUN yum update -y
RUN yum install -y --setopt=tsflags=nodocs \
                install git autoconf automake libtool gcc gcc-c++ \
                pkgconfig pcre-devel tcl-devel expat-devel \
                libcap libcap-devel hwloc hwloc-devel libcurl-devel rpm-build perl-ExtUtils-MakeMaker \
                make centos-release-scl sudo epel-release wget \
                && yum clean all

# Default version of GCC and Python
RUN gcc --version && python --version

# Install some developer style software collections with intent to
# use newer version of GCC and Python than the OS provided
RUN yum install -y devtoolset-9 rh-python36 luajit-devel && yum clean all
#RUN yum install -y centos-release-scl && yum install -y devtoolset-8 rh-python36

RUN yum install -y ncurses-devel xz-devel brotli-devel openssl-devel && yum clean all
RUN yum install -y python3 systemd-rpm-macros perl-IPC-Cmd && yum clean all 

# Yum installed packages but the default OS-provided version is still used.
RUN gcc --version && python --version

# Okay, change our shell to specifically use our software collections.
# (default was SHELL [ "/bin/sh", "-c" ])
# https://docs.docker.com/engine/reference/builder/#shell
#
# See also `scl` man page for enabling multiple packages if desired:
# https://linux.die.net/man/1/scl
SHELL [ "/usr/bin/scl", "enable", "devtoolset-9", "rh-python36" ]

# Switching to a different shell has brought the new versions into scope.
RUN gcc --version && python --version

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

ENV OPENSSL_VERSION="openssl-3.1.3"
# RUN mkdir -p /usr/local/openssl
RUN mkdir -p /opt/trafficserver/openssl
WORKDIR /
RUN wget https://www.openssl.org/source/${OPENSSL_VERSION}.tar.gz
RUN tar xvfz ${OPENSSL_VERSION}.tar.gz
WORKDIR ${OPENSSL_VERSION}
RUN ./config --prefix=/opt/trafficserver/openssl --openssldir=/opt/trafficserver/openssl zlib
# RUN ./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl zlib

RUN make -j`nproc`
RUN make install_sw
WORKDIR ..

RUN git clone https://github.com/akheron/jansson.git
WORKDIR jansson
RUN autoreconf -i
RUN ./configure --disable-shared CC="gcc -fpic" --with-openssl=/opt/trafficserver/openssl
# RUN ./configure --disable-shared CC="gcc -fpic" --with-openssl=/usr/local/openssl
RUN make -j`nproc`
RUN ln -s src/.libs lib
RUN ln -s src include
WORKDIR ..

# RUN git clone https://github.com/cisco/cjose.git
# RUN wget https://github.com/OpenIDC/cjose/releases/tag/v0.6.2.2
# RUN wget https://github.com/apache/trafficserver/archive/refs/tags/%{version}.tar.gz
RUN git clone -b v0.6.2.2 https://github.com/OpenIDC/cjose.git
WORKDIR cjose
RUN autoreconf -i
RUN ./configure --with-openssl=/opt/trafficserver/openssl --with-jansson=/jansson --disable-shared CC="gcc -fpic"
# RUN ./configure --with-openssl=/usr/local/openssl --with-jansson=/jansson --disable-shared CC="gcc -fpic"
RUN make -j`nproc`
RUN ln -s src/.libs lib


USER builder
WORKDIR /home/builder/rpmbuild
RUN pwd

ENV FLAVOR=rpmbuild OS=centos DIST=el7
ARG TS_VERSION

ADD entrypoint.sh /usr/bin/entrypoint.sh
#ADD entrypoint.sh /entrypoint.sh
#RUN chmod +x /usr/bin/entrypoint.sh
ENTRYPOINT [ "/usr/bin/entrypoint.sh" ]
