
%include	/usr/lib/rpm/macros.java
Summary:	Maven Repository Manager
Name:		nexus
Version:	1.3.6
Release:	0.1
License:	GPL v3
Group:		Networking/Daemons/Java
Source0:	http://nexus.sonatype.org/downloads/%{name}-webapp-%{version}.war
# Source0-md5:	1eec39a389ff86931237e00a5861bd2c
Source1:	%{name}-context.xml
Source2:	%{name}-plexus.properties
Source3:	%{name}-log4j.properties
URL:		http://nexus.sonatype.org/
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	group(servlet)
Requires:	jpackage-utils
Requires:	rc-scripts
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

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/nexus,%{_datadir}/nexus,/var/log/nexus,%{_sharedstatedir}/{nexus,tomcat/conf/Catalina/localhost}}
#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/nexus/web.xml
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/nexus.xml
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/nexus/plexus.properties
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/nexus/log4j.properties

cp -a . $RPM_BUILD_ROOT%{_datadir}/nexus

mv $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/web.xml $RPM_BUILD_ROOT%{_sysconfdir}/nexus/web.xml
ln -sf %{_sysconfdir}/nexus/web.xml $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/web.xml
ln -sf %{_sysconfdir}/nexus/plexus.properties $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/plexus.properties
ln -sf %{_sysconfdir}/nexus/log4j.properties  $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/log4j.properties

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%attr(770,root,servlet) %{_datadir}/nexus
%attr(770,root,servlet) %{_sharedstatedir}/nexus
%attr(770,root,servlet) /var/log/nexus

%dir %{_sysconfdir}/nexus
%attr(644,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nexus/log4j.properties
%attr(644,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nexus/plexus.properties
%attr(660,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nexus/web.xml
%attr(660,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/nexus.xml
