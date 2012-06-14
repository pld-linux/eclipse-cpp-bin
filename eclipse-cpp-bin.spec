Summary:	Eclipse - an open extensible IDE
Summary(pl.UTF-8):	Eclipse - otwarte, rozszerzalne środowisko programistyczne
Name:		eclipse-cpp-bin
Version:	3.7.2
Release:	1
License:	EPL v1.0
Group:		Development/Tools
Source0:	ftp://ftp.uninett.no/pub/eclipse/technology/epp/downloads/release/indigo/SR2/eclipse-cpp-indigo-SR2-incubation-linux-gtk.tar.gz
# Source0-md5:	98ba2db4c23957553ef332c6cbc1cc71
Source1:	ftp://ftp.uninett.no/pub/eclipse/technology/epp/downloads/release/indigo/SR2/eclipse-cpp-indigo-SR2-incubation-linux-gtk-x86_64.tar.gz
# Source1-md5:	0c4d3065478c0e4751b13a8bc6120082
Source2:	eclipse.desktop
URL:		http://www.eclipse.org/
BuildRequires:	rpm-pythonprov
BuildRequires:	unzip
Requires:	ant
Requires:	jdk >= 1.4
Provides:	eclipse = %{version}-%{release}
Provides:	eclipse-cpp
Obsoletes:	eclipse
Conflicts:	eclipse-SDK
Conflicts:	eclipse-bin
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		eclipse_arch	%(echo %{_target_cpu} | sed 's/i.86\\|athlon\\|pentium/x86/;s/amd64/x86_64/')
%define		no_install_post_chrpath		1

# list of script capabilities (regexps) not to be used in Provides
%define		_noautoprov			libcairo.so.2

%description
Eclipse is a kind of universal tool platform - an open extensible IDE
for anything and nothing in particular. Current package includes C/C++
development plugins.

%description -l pl.UTF-8
Eclipse to rodzaj uniwersalnej platformy narzędziowej - otwarte,
rozszerzalne IDE (zintegrowane środowisko programistyczne) do
wszystkiego i niczego w szczególności. Ten zestaw binarów zawiera
wtyczki do programowania w C/C++.

%prep
%ifarch %{ix86}
%setup -q -T -c -a0
%endif
%ifarch %{x8664}
%setup -q -T -c -a1
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{{%{_libdir},%{_datadir}}/eclipse/dropins,%{_bindir}} \
	$RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_sysconfdir}/eclipse}

cd eclipse
cp -a features p2 configuration plugins \
      libcairo-swt.so eclipse artifacts.xml \
      $RPM_BUILD_ROOT%{_libdir}/eclipse

install -p icon.xpm $RPM_BUILD_ROOT%{_pixmapsdir}/eclipse-icon.xpm

cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}/%{name}.desktop
cp -p eclipse.ini $RPM_BUILD_ROOT%{_sysconfdir}/eclipse/eclipse.ini

ln -s %{_libdir}/eclipse/eclipse $RPM_BUILD_ROOT%{_bindir}
ln -s %{_sysconfdir}/eclipse/eclipse.ini $RPM_BUILD_ROOT%{_libdir}/eclipse/eclipse.ini

# place for arch independent plugins
install -d $RPM_BUILD_ROOT%{_datadir}/eclipse/{features,plugins}
cat <<-'EOF'> $RPM_BUILD_ROOT%{_datadir}/eclipse/.eclipseextension
name=Eclipse Platform
id=org.eclipse.platform
version=%{version}
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc eclipse/{about_files,readme,*html}
%dir %{_libdir}/eclipse
%dir %{_libdir}/eclipse/dropins
%{_libdir}/eclipse/features
%{_libdir}/eclipse/p2
%{_libdir}/eclipse/configuration
%{_libdir}/eclipse/plugins
%{_libdir}/eclipse/eclipse.ini
%{_libdir}/eclipse/artifacts.xml
%{_desktopdir}/%{name}.desktop
%{_pixmapsdir}/eclipse-icon.xpm
%dir %{_sysconfdir}/eclipse
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/eclipse/eclipse.ini
%attr(755,root,root) %{_libdir}/eclipse/libcairo-swt.so
%attr(755,root,root) %{_libdir}/eclipse/eclipse
%attr(755,root,root) %{_bindir}/eclipse

%dir %{_datadir}/eclipse
%dir %{_datadir}/eclipse/dropins
%{_datadir}/eclipse/.eclipseextension
