%global install_prefix "/opt"

Name:		trafficserver
Version:	9.1.3
Release:	13496%{?dist}
Summary:	Apache Traffic Server
Group:		Applications/Communications
License:	Apache License, Version 2.0
URL:		https://github.com/apache/trafficserver
Epoch:          13496
Source0:       %{name}-%{version}-%{epoch}.tar.bz2
%undefine _disable_source_fetch
#Source0:        https://github.com/apache/trafficserver/archive/refs/tags/9.1.2.tar.gz
#Source1:        trafficserver.service
Source2:        trafficserver.sysconfig
Source3:        trafficserver.tmpfilesd
Source4:        trafficserver-rsyslog.conf
Patch0:         astats_over_http-1.6-9.1.x.patch
#Patch1:         https://patch-diff.githubusercontent.com/raw/apache/trafficserver/pull/7916.patch
#Patch2:         https://patch-diff.githubusercontent.com/raw/apache/trafficserver/pull/8589.patch
#Patch3:         https://patch-diff.githubusercontent.com/raw/apache/trafficserver/pull/8362.patch
#Patch4:         https://patch-diff.githubusercontent.com/raw/apache/trafficserver/pull/8480.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires:	tcl, hwloc, pcre, openssl, libcap
Requires:       rsyslog
Requires:       logrotate
BuildRequires:	autoconf, automake, libtool, gcc-c++, glibc-devel, openssl-devel, expat-devel, pcre, libcap-devel, pcre-devel, perl-ExtUtils-MakeMaker, tcl-devel, hwloc-devel, luajit-devel

Requires: initscripts
%if %{?fedora}0 > 140 || %{?rhel}0 > 60
# For systemd.macros
BuildRequires: systemd
Requires: systemd
Requires(postun): systemd
%else
Requires(post): chkconfig
Requires(preun): chkconfig initscripts
Requires(postun): initscripts
%endif

%description
Apache Traffic Server for Traffic Control with astats_over_http plugin

%prep
%setup
%patch0 -p1
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
#%patch4 -p1
autoreconf -vfi

#%setup

%build
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/trafficserver/openssl/lib:/usr/local/lib
./configure --prefix=%{install_prefix}/%{name} --with-user=ats --with-group=ats --with-build-number=%{release} --enable-experimental-plugins --with-jansson=/jansson --with-cjose=/cjose -with-openssl=/opt/trafficserver/openssl --disable-unwind
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

# Remove duplicate man-pages:
##rm -rf %{buildroot}%{_docdir}/trafficserver

mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 -p %{SOURCE2} \
   %{buildroot}%{_sysconfdir}/sysconfig/trafficserver

mkdir -p %{buildroot}%{_sysconfdir}/rsyslog.d
install -m 644 -p %{SOURCE4} \
   %{buildroot}%{_sysconfdir}/rsyslog.d/trafficserver.conf

#%{__install} -Dm 0644 trafficserver-rsyslog.conf $RPM_BUILD_ROOT/etc/rsyslog.d/trafficserver.conf

%if %{?fedora}0 > 140 || %{?rhel}0 > 60
#install -D -m 0644 -p %{SOURCE1} \
#   %{buildroot}/lib/systemd/system/trafficserver.service
mkdir -p %{buildroot}%{_unitdir}/
cp $RPM_BUILD_DIR/%{name}-%{version}/rc/trafficserver.service %{buildroot}%{_unitdir}/
install -D -m 0644 -p %{SOURCE3} \
   %{buildroot}%{_sysconfdir}/tmpfiles.d/trafficserver.conf
%else
mkdir -p %{buildroot}/etc/init.d/
cp $RPM_BUILD_DIR/%{name}-%{version}/rc/trafficserver %{buildroot}/etc/init.d
%endif

mkdir -p $RPM_BUILD_ROOT%{install_prefix}/trafficserver/etc/trafficserver/snapshots

mkdir -p $RPM_BUILD_ROOT/opt/trafficserver/openssl
cp -r /opt/trafficserver/openssl/lib $RPM_BUILD_ROOT/opt/trafficserver/openssl/lib

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group ats >/dev/null || groupadd -r ats -g 176 &>/dev/null
getent passwd ats >/dev/null || \
useradd -r -u 176 -g ats -d / -s /sbin/nologin \
	-c "Apache Traffic Server" ats &>/dev/null
id ats &>/dev/null || /usr/sbin/useradd -u 176 -r ats -s /sbin/nologin -d /

%post
/sbin/ldconfig
%if %{?fedora}0 > 170 || %{?rhel}0 > 60
  %systemd_post trafficserver.service
%else
  if [ $1 -eq 1 ] ; then
  %if %{?fedora}0 > 140
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
  %else
    /sbin/chkconfig --add %{name}
  %endif
  fi
%endif

%preun
#/etc/init.d/%{name} stop
%if %{?fedora}0 > 170 || %{?rhel}0 > 60
  %systemd_preun trafficserver.service
%else
if [ $1 -eq 0 ] ; then
  /sbin/service %{name} stop > /dev/null 2>&1
  /sbin/chkconfig --del %{name}
fi
%endif


%postun
# Helpful in understanding order of operations in relation to install/uninstall/upgrade:
#     http://www.ibm.com/developerworks/library/l-rpm2/
# if 0 uninstall, if 1 upgrade

%if %{?fedora}0 > 170 || %{?rhel}0 > 60
  %systemd_postun_with_restart trafficserver.service
  id ats &>/dev/null && /usr/sbin/userdel ats
%else
if [ $1 -eq 1 ] ; then
  /sbin/service trafficserver condrestart &>/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
#%attr(755,-,-) /etc/init.d/trafficserver
%dir /opt/trafficserver
%if %{?fedora}0 > 140 || %{?rhel}0 > 60
/usr/lib/systemd/system/trafficserver.service
%config(noreplace) %{_sysconfdir}/tmpfiles.d/trafficserver.conf
%else
/etc/init.d/trafficserver
%endif
/opt/trafficserver/openssl
/opt/trafficserver/bin
%config(noreplace) %{_sysconfdir}/sysconfig/trafficserver
%{_sysconfdir}/rsyslog.d/trafficserver.conf
/opt/trafficserver/include
/opt/trafficserver/lib
#/opt/trafficserver/man
#/opt/trafficserver/lib64
/opt/trafficserver/libexec
/opt/trafficserver/share
%dir /opt/trafficserver/var
%attr(-,ats,ats) /opt/trafficserver/var/trafficserver
%dir /opt/trafficserver/var/log
%attr(-,ats,ats) /opt/trafficserver/var/log/trafficserver
%dir /opt/trafficserver/etc
%attr(-,ats,ats) %dir /opt/trafficserver/etc/trafficserver
%attr(-,ats,ats) %dir /opt/trafficserver/etc/trafficserver/snapshots
/opt/trafficserver/etc/trafficserver/body_factory
/opt/trafficserver/etc/trafficserver/trafficserver-release
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/cache.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/hosting.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/ip_allow.yaml
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/logging.yaml
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/parent.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/plugin.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/records.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/remap.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/socks.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/splitdns.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/ssl_multicert.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/storage.config
#%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/update.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/volume.config
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/sni.yaml
%config(noreplace) %attr(644,ats,ats) /opt/trafficserver/etc/trafficserver/strategies.yaml
