Summary:	Privledged helper for utmp/wtmp updates
Name:		utempter
Version:	0.5
Release:	2
Copyright:	MIT
Group:		Base
Source:		%{name}-%{version}.tar.gz
Prereq:		/usr/sbin/groupadd, fileutils
BuildRoot:	/tmp/%{name}-%{version}-root

%description
Utempter is a utility which allows programs to log information to a
privledged file (/var/run/utmp), without compromising system security. It
accomplishes this task by acting as a buffer between root and the programs.

%package devel
Summary:	utempter library header files
Group:		Development/Libraties
Requires:	%{name} = %{version}

%description devel
utempter library header files.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

strip --strip-unneeded $RPM_BUILD_ROOT/usr/{lib/lib*.so.*.*,sbin/*}

%pre 
/usr/sbin/groupadd -r -f utmp

%post
/sbin/ldconfig

if [ -f /var/log/wtmp ]; then
    chown root.utmp /var/log/wtmp
    chmod 664 /var/log/wtmp
fi

if [ -f /var/run/utmp ]; then
    chown root.utmp /var/run/utmp
    chmod 664 /var/run/utmp
fi

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(2755,root,utmp) /usr/sbin/utempter
%attr(0755,root,root) /usr/lib/lib*.so.*.*

%files devel
%defattr(644,root,root,755)
%attr(0755,root,root) /usr/lib/lib*.so
/usr/include/utempter.h

%changelog
* Wed Apr 28 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [0.5-2]
- added -q %setup parameter,
- added stripping shared library and binaries,
- added devel subpackage,
- removed /sbin/ldconfig from Prereq (this is automatically generated).
