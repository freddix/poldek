# based on PLD Linux spec git://git.pld-linux.org/packages/.git
Summary:	RPM packages management helper tool
Name:		poldek
Version:	0.30.1
Release:	3
License:	GPL v2
Group:		Applications/System
Source0:	http://carme.pld-linux.org/~megabajt/releases/poldek/%{name}-%{version}.tar.xz
# Source0-md5:	e569c8454df0932df53b09cee9998927
Source1:	%{name}.conf
Source2:	%{name}-aliases.conf
Patch0:		%{name}-config.patch
Patch1:		%{name}-nodoc.patch
URL:		http://poldek.pld-linux.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bzip2-devel
BuildRequires:	check
BuildRequires:	db-devel
BuildRequires:	gettext-autopoint
BuildRequires:	libtool
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	pcre-devel
BuildRequires:	perl-tools-pod
BuildRequires:	popt-devel
BuildRequires:	python-devel
BuildRequires:	readline-devel
BuildRequires:	rpm-devel
#BuildRequires:	xmlto
BuildRequires:	zlib-devel
Requires:	%{name}-libs = %{version}-%{release}
Requires:	rpm
Requires:	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
poldek is an RPM package management tool which allows you to easily
perform package verification, installation (including system
installation from scratch), upgrading, and removal.

%package libs
Summary:	poldek libraries
Group:		Libraries

%description libs
poldek libraries.

%package devel
Summary:	Header files for poldek libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for poldek libraries.

%package -n python-poldek
Summary:	Python modules for poldek
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}
%pyrequires_eq	python-libs

%description -n python-poldek
Python modules for poldek.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__autoconf}
%{__automake}
cd tndb
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ../trurlib
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__autoconf}
%{__automake}
cd ..

CPPFLAGS="%{rpmcppflags} -std=gnu99 -fgnu89-inline"
%configure \
	--disable-static	\
	--enable-nls		\
	--with-python
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/var/cache/%{name}

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -j1 -C python install \
	DESTDIR=$RPM_BUILD_ROOT \
	libdir=%{py_sitedir}

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/freddix-source.conf
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/aliases.conf

# get rid of unneeded sources
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/{rh,fedora,centos}-source.conf
%{__rm} $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/repos.d/pld*

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la

%py_postclean
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/_poldekmod.la

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /usr/sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README* NEWS TODO conf/*.conf

%dir %{_libdir}/%{name}
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/repos.d

%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/%{name}/*
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/repos.d/*.conf

%dir /var/cache/%{name}

%if 0
%{_infodir}/poldek.info*
%{_mandir}/man1/%{name}*
%lang(pl) %{_mandir}/pl/man1/%{name}*
%endif

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libpoclidek.so.?
%attr(755,root,root) %ghost %{_libdir}/libpoldek.so.?
%attr(755,root,root) %ghost %{_libdir}/libtndb.so.?
%attr(755,root,root) %ghost %{_libdir}/libtrurl.so.?
%attr(755,root,root) %ghost %{_libdir}/libvfile.so.?
%attr(755,root,root) %{_libdir}/libpoclidek.so.*.*.*
%attr(755,root,root) %{_libdir}/libpoldek.so.*.*.*
%attr(755,root,root) %{_libdir}/libtndb.so.*.*.*
%attr(755,root,root) %{_libdir}/libtrurl.so.*.*.*
%attr(755,root,root) %{_libdir}/libvfile.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libpoclidek.so
%attr(755,root,root) %{_libdir}/libpoldek.so
%attr(755,root,root) %{_libdir}/libtndb.so
%attr(755,root,root) %{_libdir}/libtrurl.so
%attr(755,root,root) %{_libdir}/libvfile.so
%{_includedir}/*
%{_pkgconfigdir}/tndb.pc
%{_pkgconfigdir}/trurlib.pc

%files -n python-poldek
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_poldekmod.so
%{py_sitescriptdir}/poldek.py[co]
%{py_sitescriptdir}/poldekmod.py[co]

