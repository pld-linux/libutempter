Summary:	Privileged helper for utmpx updates
Summary(es):	Programa para actualizaciСn del utmp/wtmp
Summary(pl):	Program pozwalaj╠cy na zapisywanie w utmpx
Summary(pt_BR):	Programa para atualizaГЦo do utmp/wtmp
Summary(ru):	Привилегированная программа для изменений в utmp/wtmp
Summary(uk):	Прив╕лейована програма для внесення зм╕н до utmp/wtmp
Name:		utempter
Version:	0.5.2
Release:	8
License:	MIT
Group:		Base
Source0:	%{name}-%{version}.tar.gz
Patch0:		%{name}-lastlog.patch
PreReq:		SysVinit >= 2.76-14
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utempter is a utility which allows programs to log information to a
privileged file (/var/run/utmpx), without compromising system
security. It accomplishes this task by acting as a buffer between root
and the programs.

%description -l es
Programa para actualizaciСn del utmp/wtmp.

%description -l pl
Utempter jest programem pozwalaj╠cym u©ytkownikom na zapisywanie do
pliku /var/run/utmpx bez naruszania bezpieczeЯstwa systemu.

%description -l pt_BR
O Utempter И um utilitАrios que permite a programas guardar informaГЦo
Ю arquivos privilegiados (/var/run/utmp), sem comprometer a seguranГa
do sistema. Ele faz esta tarefa atuando como um "buffer" entre o
usuАrio root e os programas.

%description -l ru
Utempter - это утилита, которая позволяет программам записывать
информацию в привилегированный файл (/var/run/utmp) без нарушения
системной безопасности. Она исполняет эту задачу, выступая буфером
между root'ом и пользовательскими программами.

%description -l uk
Utempter - це утил╕та, що дозволя╓ програмам записувати ╕нформац╕ю в
прив╕лейований файл (/var/run/utmp) без порушення системно╖ безпеки.
Вона викону╓ цю задачу, виступаючи буфером м╕ж root'ом та програмами
користувача.

%package devel
Summary:	utempter library and header files
Summary(pl):	Pliki nagЁСwkowe oraz biblioteki utemptera
Group:		Development/Libraries
Requires:	%{name} = %{version}

%description devel
utempter library and header files.

%description devel -l pl
Pliki nagЁСwkowe oraz biblioteki utemptera.

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
