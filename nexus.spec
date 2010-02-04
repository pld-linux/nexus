
%include	/usr/lib/rpm/macros.java
Summary:	Maven Repository Manager
Name:		nexus
Version:	1.5.0
Release:	1
License:	GPL v3
Group:		Networking/Daemons/Java
Source0:	http://nexus.sonatype.org/downloads/%{name}-webapp-%{version}.war
# Source0-md5:	bcf59d3a8ab3bd598293473798a89352
Source1:	%{name}-context.xml
Source2:	%{name}-plexus.properties
URL:		http://nexus.sonatype.org/
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

install -d $RPM_BUILD_ROOT{%{_sysconfdir}/nexus,%{_datadir}/nexus,/var/log/nexus,%{_sharedstatedir}/{nexus/conf,tomcat/conf/Catalina/localhost}}
install %{SOURCE1} $RPM_BUILD_ROOT%{_sharedstatedir}/tomcat/conf/Catalina/localhost/nexus.xml
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/nexus/plexus.properties

cp -a . $RPM_BUILD_ROOT%{_datadir}/nexus

mv $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/web.xml $RPM_BUILD_ROOT%{_sysconfdir}/nexus/web.xml
ln -sf %{_sysconfdir}/nexus/web.xml $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/web.xml
ln -sf %{_sysconfdir}/nexus/plexus.properties $RPM_BUILD_ROOT%{_datadir}/nexus/WEB-INF/plexus.properties

# These files are configs, but they should be created by nexus. So lets
# install them as %%ghost %%config, and link to /etc/nexus
touch $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/log4j.properties
touch $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/nexus.xml
touch $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/security.xml
touch $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/conf/lvo-plugin.xml
ln -sf %{_sharedstatedir}/nexus/conf/log4j.properties $RPM_BUILD_ROOT%{_sysconfdir}/nexus/log4j.properties
ln -sf %{_sharedstatedir}/nexus/conf/nexus.xml $RPM_BUILD_ROOT%{_sysconfdir}/nexus/nexus.xml
ln -sf %{_sharedstatedir}/nexus/conf/security.xml $RPM_BUILD_ROOT%{_sysconfdir}/nexus/security.xml
ln -sf %{_sharedstatedir}/nexus/conf/lvo-plugin.xml $RPM_BUILD_ROOT%{_sysconfdir}/nexus/lvo-plugin.xml

# log directory
ln -s /var/log/nexus $RPM_BUILD_ROOT%{_sharedstatedir}/nexus/logs

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%attr(770,root,servlet) %{_datadir}/nexus
%dir %attr(770,root,servlet) %{_sharedstatedir}/nexus
%dir %attr(770,root,servlet) %{_sharedstatedir}/nexus/logs
%dir %attr(770,root,servlet) %{_sharedstatedir}/nexus/conf
%attr(770,root,servlet) /var/log/nexus

%dir %{_sysconfdir}/nexus
%attr(644,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nexus/plexus.properties
%attr(660,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/nexus/web.xml
%attr(660,root,servlet) %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/tomcat/conf/Catalina/localhost/nexus.xml

# These files are created by nexus, but they are config files.
%ghost %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/log4j.properties
%ghost %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/nexus.xml
%ghost %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/security.xml
%ghost %config(noreplace) %verify(not md5 mtime size) %{_sharedstatedir}/nexus/conf/lvo-plugin.xml
%{_sysconfdir}/nexus/log4j.properties
%{_sysconfdir}/nexus/nexus.xml
%{_sysconfdir}/nexus/security.xml
%{_sysconfdir}/nexus/lvo-plugin.xml
