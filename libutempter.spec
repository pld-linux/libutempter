Summary:	Privileged helper for utmpx updates
Summary(es.UTF-8):	Programa para actualización del utmp/wtmp
Summary(pl.UTF-8):	Program pozwalający na zapisywanie w utmpx
Summary(pt_BR.UTF-8):	Programa para atualização do utmp/wtmp
Summary(ru.UTF-8):	Привилегированная программа для изменений в utmp/wtmp
Summary(uk.UTF-8):	Привілейована програма для внесення змін до utmp/wtmp
Name:		utempter
Version:	0.5.5
Release:	7
License:	MIT or LGPL
Group:		Base
Source0:	%{name}-%{version}.tar.gz
# Source0-md5:	a628f149132e2f729bc4601e6a4f6c29
Patch0:		%{name}-lastlog.patch
Patch1:		%{name}-utmp-cleanup.patch
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Provides:	group(utmp)
Obsoletes:	libutempter0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utempter is a utility which allows programs to log information to a
privileged file (/var/run/utmpx), without compromising system
security. It accomplishes this task by acting as a buffer between root
and the programs.

%description -l es.UTF-8
Programa para actualización del utmp/wtmp.

%description -l pl.UTF-8
Utempter jest programem pozwalającym użytkownikom na zapisywanie do
pliku /var/run/utmpx bez naruszania bezpieczeństwa systemu.

%description -l pt_BR.UTF-8
O Utempter é um utilitários que permite a programas guardar informação
à arquivos privilegiados (/var/run/utmp), sem comprometer a segurança
do sistema. Ele faz esta tarefa atuando como um "buffer" entre o
usuário root e os programas.

%description -l ru.UTF-8
Utempter - это утилита, которая позволяет программам записывать
информацию в привилегированный файл (/var/run/utmp) без нарушения
системной безопасности. Она исполняет эту задачу, выступая буфером
между root'ом и пользовательскими программами.

%description -l uk.UTF-8
Utempter - це утиліта, що дозволяє програмам записувати інформацію в
привілейований файл (/var/run/utmp) без порушення системної безпеки.
Вона виконує цю задачу, виступаючи буфером між root'ом та програмами
користувача.

%package devel
Summary:	Header file for utempter library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki utemptera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	libutempter0-devel

%description devel
Header file for utempter library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki utemptera.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	LIBDIR="%{_libdir}" \
	RPM_BUILD_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/run
:> $RPM_BUILD_ROOT/var/run/utmpx

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 22 utmp

%post
/sbin/ldconfig
if [ ! -f /var/run/utmpx ]; then
	umask 002
	touch /var/run/utmpx
	chown root:utmp /var/run/utmpx
	chmod 0664 /var/run/utmpx
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

%files
%defattr(644,root,root,755)
%attr(2755,root,utmp) %{_sbindir}/utempter
%attr(755,root,root) %{_sbindir}/utmp-cleanup
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%attr(664,root,utmp) %ghost /var/run/utmpx

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/lib*.so
%{_includedir}/utempter.h
