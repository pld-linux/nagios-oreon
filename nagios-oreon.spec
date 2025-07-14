# TODO
# - merge update from oreon.spec, then cvs rm oreon.spec
# - specify perms in files, not post
# - plugins
# NOTE
# - works with nagios 1.2 (nagios 2.0 not yet)
# - works with php 4 (php 5 not yet)
%define	_rc RC2
Summary:	Monitoring solution based on Nagios
Summary(pl.UTF-8):	Rozwiązanie monitorujące oparte na Nagiosie
Name:		nagios-oreon
Version:	1.2.3
Release:	%{_rc}.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://download.oreon-project.org/tgz/oreon-%{version}-%{_rc}.tar.gz
# Source0-md5:	905a194a8e4925c89e586378855f3676
Patch0:		oreon-pld.patch
URL:		http://www.oreon-project.org/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	nagios-common
Requires:	perl-GD
Requires:	php(gd)
Requires:	php(snmp)
Requires:	webapps
Requires:	webserver(php) >= 4.0
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

%description -l pl.UTF-8
Oreon to kompletne rozwiązanie monitorujące o otwartych źródłach
oparte na Nagiosie. Cel tego projektu wykracza poza proste narzędzie
do zgłaszania alarmów.

%package setup
Summary:	Oreon setup package
Summary(pl.UTF-8):	Pakiet do wstępnej konfiguracji Oreona
Group:		Applications/WWW
Requires:	%{name} = %{version}-%{release}

%description setup
Install this package to configure initial Oreon installation. You
should uninstall this package when you're done, as it considered
insecure to keep the setup files in place.

%description setup -l pl.UTF-8
Ten pakiet należy zainstalować w celu wstępnej konfiguracji Oreona po
pierwszej instalacji. Potem należy go odinstalować, jako że
pozostawienie plików instalacyjnych mogłoby być niebezpieczne.

%prep
%setup -q -n oreon-%{version}%{?_rc:-%{_rc}}
# undos the source
find . -type f -print0 | xargs -0 sed -i -e 's,\r$,,'
%patch -P0 -p1

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
chown -R http %{_appdir}/nagios_cfg

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
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
