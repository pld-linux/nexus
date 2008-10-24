#
%include	/usr/lib/rpm/macros.java
Summary:	Maven Repository Manager
Name:		nexus
Version:	1.0.2
Release:	0.1
License:	GPL v3
Group:		Networking/Daemons/Java
Source0:	http://nexus.sonatype.org/downloads/%{name}-%{version}-bundle.tar.gz
# Source0-md5:	f9980d7d3a2ebf12e409d49e093839e7
Source1:	%{name}.init
Source2:	%{name}-plexus.properties
Source3:	%{name}-classworlds.conf
Source4:	%{name}-wrapper.conf
URL:		http://nexus.sonatype.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires(post,preun):	/sbin/chkconfig
Requires(postun):	/usr/sbin/groupdel
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(pre):	/usr/sbin/useradd
# We do need exactly 3.2.3 version (it is tagged as JSW_3_2)
Requires:	java-service-wrapper = 3.2.3
Requires:	jpackage-utils
Requires:	rc-scripts
Provides:	group(nexus)
Provides:	user(nexus)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Nexus is a powerful and robust Maven repository manager, created to
provide reliable access to artifacts required for development and
provisioning. Maven's central repository has always served as a great
convenience for users of Maven, but it has always been recommended to
maintain your own repositories to ensure stability within your
organization. Nexus greatly simplifies the maintenance of your own
internal repositories and access to external repositories. With Nexus
you can completely control access to, and deployment of, every
artifact in your organization from a single location.

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{init.d,sysconfig},%{_javadir},%{_datadir},%{_sharedstatedir}/nexus/conf}

install %SOURCE1 $RPM_BUILD_ROOT%{_sysconfdir}/init.d/nexus
install %SOURCE2 $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/plexus.properties
install %SOURCE3 $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/classworlds.conf
install %SOURCE4 $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/wrapper.conf
install %{name}-webapp-%{version}/conf/plexus.xml $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/plexus.xml

cp -a %{name}-webapp-%{version}/lib/plexus-platform-jsw-1.5.jar $RPM_BUILD_ROOT%{_javadir}/plexus-platform-jsw-1.5.jar
ln -s plexus-platform-jsw-1.5.jar $RPM_BUILD_ROOT%{_javadir}/plexus-platform-jsw.jar

cp -a %{name}-webapp-%{version}/runtime/apps/nexus $RPM_BUILD_ROOT%{_datadir}/nexus

ln -s %{_sharedstatedir}/nexus/conf $RPM_BUILD_ROOT%{_sysconfdir}/nexus

%pre
%groupadd -g 200 nexus
%useradd -u 200 -d %{_sharedstatedir}/nexus -s /bin/false -c "nexus user" -g nexus nexus

%post
/sbin/chkconfig --add nexus
%service nexus restart "nexus daemon"

%preun
if [ "$1" = "0" ]; then
	%service nexus stop
	/sbin/chkconfig --del nexus
fi

%postun
if [ "$1" = "0" ]; then
	%userremove nexus
	%groupremove nexus
fi


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%attr(754,root,root) /etc/rc.d/init.d/nexus

%{_sysconfdir}/nexus

%{_javadir}/plexus-platform-jsw-1.5.jar
%{_javadir}/plexus-platform-jsw.jar

%{_datadir}/nexus

%dir %attr(770,nexus,nexus) %{_sharedstatedir}/nexus
%dir %attr(770,nexus,nexus) %{_sharedstatedir}/nexus/conf
%attr(660,nexus,nexus) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/plexus.properties
%attr(660,nexus,nexus) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/plexus.xml
%attr(660,nexus,nexus) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/classworlds.conf
%attr(660,nexus,nexus) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/wrapper.conf
