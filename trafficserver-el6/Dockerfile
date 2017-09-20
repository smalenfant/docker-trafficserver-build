FROM centos:6

RUN yum update -y && yum clean all

RUN yum install -y --setopt=tsflags=nodocs \
                install git autoconf automake libtool gcc gcc-c++ \
                pkgconfig pcre-devel tcl-devel expat-devel openssl-devel \
                libcap libcap-devel hwloc hwloc-devel libcurl-devel rpm-build perl-ExtUtils-MakeMaker \
                make centos-release-scl sudo \
                && yum clean all

RUN yum install -y --setopt=tsflags=nodocs devtoolset-4-gcc-c++ \ 
                && yum clean all

RUN useradd builder -u 1000 -m -G users,wheel && \
    echo "builder ALL=(ALL:ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    echo "# macros"                      >  /home/builder/.rpmmacros && \
    echo "%_topdir    /home/builder/rpmbuild"  >> /home/builder/.rpmmacros && \
    echo "%_sourcedir %{_topdir}/SOURCES"        >> /home/builder/.rpmmacros && \
    echo "%_builddir  %{_topdir}/BUILD"        >> /home/builder/.rpmmacros && \
    echo "%_specdir   %{_topdir}/SPECS"        >> /home/builder/.rpmmacros && \
    echo "%_rpmdir    %{_topdir}/RPMS"        >> /home/builder/.rpmmacros && \
    echo "%_srcrpmdir %{_topdir}/SRPMS"        >> /home/builder/.rpmmacros && \
    mkdir /home/builder/rpmbuild && \
    chown -R builder /home/builder

USER builder

WORKDIR /home/builder/rpmbuild

ENV FLAVOR=rpmbuild OS=centos DIST=el6

#RUN /usr/bin/scl enable devtoolset-4 true

#RUN echo source /opt/rh/devtoolset-4/enable >> /home/builder/.bashrc

ENTRYPOINT ["scl","enable","devtoolset-4"]
#ENTRYPOINT ['source_scl','enable','devtoolset-3','true']

