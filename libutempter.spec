Summary: Privledged helper for utmp/wtmp updates
Name: utempter
%define version 0.5
Version: %{version}
Release: 1
Copyright: MIT
Group: System Environment/Base
Source: utempter-%{version}.tar.gz
BuildRoot: /var/tmp/utempter-root
Prereq: /usr/sbin/groupadd, /sbin/ldconfig, fileutils

%description
Utempter is a utility which allows programs to log information to a
privledged file (/var/run/utmp), without compromising system security.
It accomplishes this task by acting as a buffer between root and the
programs.

%prep
%setup 

%build
make RPM_OPT_FLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
make PREFIX=$RPM_BUILD_ROOT install

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
%attr(02755, root, utmp) /usr/sbin/utempter
/usr/lib/libutempter.so*
/usr/include/utempter.h
