Summary:	Privileged helper for utmpx updates
Summary(pl):	Program pozwalaj�cy na zapisywanie w utmpx
Name:		utempter
Version:	0.5.2
Release:	6
License:	MIT
Group:		Base
Group(de):	Gr�nds�tzlich
Group(es):	Base
Group(pl):	Podstawowe
Group(pt_BR):	Base
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-lastlog.patch
Prereq:		/sbin/ldconfig
Prereq:		SysVinit >= 2.76-14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utempter is a utility which allows programs to log information to a
privileged file (/var/run/utmpx), without compromising system
security. It accomplishes this task by acting as a buffer between root
and the programs.

%description -l pl
Utempter jest programem pozwalaj�cym u�ytkownikom na zapisywanie do
pliku /var/run/utmpx bez naruszania bezpiecze�stwa systemu.

%package devel
Summary:	utempter library header files
Summary(pl):	Pliki nag��wkowe biblioteki utemptera
Group:		Development/Libraries
Group(de):	Entwicklung/Libraries
Group(es):	Desarrollo/Bibliotecas
Group(fr):	Development/Librairies
Group(pl):	Programowanie/Biblioteki
Group(pt_BR):	Desenvolvimento/Bibliotecas
Group(ru):	����������/����������
Group(uk):	��������/��̦�����
Requires:	%{name} = %{version}

%description devel
utempter library header files.

%description -l pl devel
Pliki nag��wkowe biblioteki utemptera.

%prep
%setup -q
%patch -p1

%build
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} PREFIX=$RPM_BUILD_ROOT install

install -d $RPM_BUILD_ROOT/var/run
:> $RPM_BUILD_ROOT/var/run/utmpx

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(2755,root,utmp) %{_sbindir}/*
%attr(0755,root,root) %{_libdir}/lib*.so.*

%attr(664,root,utmp) %ghost /var/run/utmpx

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/utempter.h
