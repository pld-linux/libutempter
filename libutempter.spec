Summary:	Privledged helper for utmpx updates
Summary(pl):	Biblioteka pozwalaj�ca na zapisywanie w utmpx
Name:		utempter
Version:	0.5
Release:	3
Copyright:	MIT
Group:		Base
Group(pl):	Podstawowe
Source:		%{name}-%{version}.tar.gz
Prereq:		shadow
Requires:	SysVinit >= 2.76-14
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Utempter is a utility which allows programs to log information to a
privledged file (/var/run/utmpx), without compromising system security. It
accomplishes this task by acting as a buffer between root and the programs.

%description -l pl
Utempter jest programem pozwalaj�cym na zapisywanie uzytkownikom do pliku
/var/run/utmpx bez naruszania bezpiecze�stwa systemu.

%package	devel
Summary:	utempter library header files
Group:		Development/Libraties
Group(pl):	Programowanie/Biblioteki
Requires:	%{name} = %{version}

%description devel
utempter library header files.

%description -l pl devel
Pliki nag��wkowe utempter.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

strip --strip-unneeded $RPM_BUILD_ROOT%{_libdir}/lib*.so.*.*
strip $RPM_BUILD_ROOT%{_sbindir}/*

install -d $RPM_BUILD_ROOT/var/run
:> $RPM_BUILD_ROOT/var/run/utmpx
 
%pre 
%{_sbindir}/groupadd -g 60 utmpx
%{_bindir}/update-db

%post
/sbin/ldconfig

if [ -f /var/run/utmpx ]; then
	chown root.utmpx /var/run/utmpx
	chmod 664 /var/run/utmpx
fi

%postun
/sbin/ldconfig
%{_sbindir}/groupdel utmpx
%{_bindir}/update-db

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)

%attr(2711,root,utmpx) %{_sbindir}/*
%attr(0755,root, root) %{_libdir}/lib*.so.*

%attr(664,root,utmpx) %ghost /var/run/utmpx

%files devel
%defattr(644,root,root,755)

%attr(755,root,root) %{_libdir}/lib*.so

%{_includedir}/utempter.h

%changelog
* Sun Jun 13 1999 Wojtek �lusarczyk <wojtek@shadow.eu.org>
  [0.5-3]
- major changes,
- group utmpx with gid 60,
- only /var/run/utmpx is owned by this packet,
- groupdel in %post 
- /usr/bin/update-db in %pre & %postun

* Wed Apr 28 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.5-2]
- added -q %setup parameter,
- added stripping shared library and binaries,
- added devel subpackage,
- removed /sbin/ldconfig from Prereq (this is automatically generated).
