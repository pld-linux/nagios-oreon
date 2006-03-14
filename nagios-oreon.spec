# TODO
# - plugins
# NOTE
# - works with nagios 1.2 (nagios 2.0 not yet)
# - works with php 4 (php 5 not yet)
Summary:	Monitoring solution based on Nagios
Name:		nagios-oreon
Version:	1.2.2
Release:	0.7
License:	GPL v2
Group:		Applications/WWW
Source0:	http://download.oreon-project.org/tgz/oreon-%{version}.tar.gz
# Source0-md5:	44f4f3b9da38065235d40889809f2985
Patch0:		oreon-pld.patch
URL:		http://www.oreon-project.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	perl-GD
Requires:	nagios-common
Requires:	php >= 3:4
Requires:	php-gd
Requires:	php-snmp
Requires:	webapps
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		oreon
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Oreon is an Open Source monitoring solution based on Nagios. The
objective of this project goes beyond the simple supply of an alarm
reporting tool.

%package setup
Summary:	Oreon setup package
Summary(pl):	Pakiet do wst�pnej konfiguracji Oreon
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Oreon installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl
Ten pakiet nale�y zainstalowa� w celu wst�pnej konfiguracji Oreon po
pierwszej instalacji. Potem nale�y go odinstalowa�, jako �e
pozostawienie plik�w instalacyjnych mog�oby by� niebezpieczne.

%prep
%setup -q -n oreon-%{version}
# undos the source
find . -type f -print0 | xargs -0 sed -i -e 's,\r$,,'
%patch0 -p1

cat > apache.conf <<'EOF'
Alias /oreon %{_appdir}
<Directory %{_appdir}>
	Allow from all
	Options None
	AllowOverride None
</Directory>
EOF

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
cp -a oreon_src/* $RPM_BUILD_ROOT%{_appdir}
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
# TODO, fix %files instead
chown root:nagios %{_appdir}/rrd
chown root:nagios %{_appdir}/include/trafficMap/average
chown root:http %{_appdir}/include/trafficMap/{bg,png}
chmod g+w %{_appdir}/include/trafficMap/{bg,png}
touch %{_appdir}/oreon.conf.php
chown root:http %{_appdir}/oreon.conf.php
chmod g+w %{_appdir}/oreon.conf.php

%triggerin -- apache1
%webapp_register apache %{_webapp}

%triggerun -- apache1
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc CHANGELOG INSTALL
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%{_appdir}
%exclude %{_appdir}/install

%files setup
%defattr(644,root,root,755)
%{_appdir}/install
