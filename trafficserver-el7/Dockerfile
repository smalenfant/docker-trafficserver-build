FROM centos:7

RUN yum update -y && yum clean all

RUN yum install -y make install git autoconf automake libtool gcc gcc-c++ pkgconfig pcre-devel tcl-devel expat-devel openssl-devel && yum clean all

RUN yum install -y libcap libcap-devel hwloc hwloc-devel ncurses-devel libcurl-devel rpm-build perl-ExtUtils-MakeMaker && yum clean all

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

ENV FLAVOR=rpmbuild OS=centos DIST=el7

#CMD /srv/pkg
