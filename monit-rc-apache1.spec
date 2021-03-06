Summary:	monitrc file for monitoring Apache 1.x web server
Summary(pl.UTF-8):	Plik monitrc do monitorowania serwera WWW Apache 1.x
Name:		monit-rc-apache1
Version:	1.2
Release:	2
License:	GPL
Group:		Applications/System
Source0:	apache1.monitrc
Source1:	apache1.cron
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,postun):	monit
Requires:	apache1-base >= 1.3.39-2
Requires:	monit
Suggests:	crondaemon
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
monitrc file for monitoring Apache 1.x web server.

%description -l pl.UTF-8
Plik monitrc do monitorowania serwera WWW Apache 1.x.

%prep

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/monit,/etc/cron.d}

cp -p %{SOURCE0} $RPM_BUILD_ROOT%{_sysconfdir}/monit/apache.monitrc
cp -p %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q monit restart

%postun
%service -q monit restart

%triggerpostun -- apache1 < 1.3.34-5.9
# rename monitrc to be service name like other files
if [ -f /etc/monit/apache1.monitrc.rpmsave ]; then
	mv -f /etc/monit/apache.monitrc{,.rpmnew}
	mv -f /etc/monit/{apache1.monitrc.rpmsave,apache.monitrc}
fi

%files
%defattr(644,root,root,755)
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/monit/*.monitrc
%config(noreplace) %verify(not md5 mtime size) /etc/cron.d/%{name}
