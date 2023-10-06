Summary:	Privileged helper for utmp updates
Summary(es.UTF-8):	Programa para actualización del utmp/wtmp
Summary(pl.UTF-8):	Program pozwalający na zapisywanie w utmp
Summary(pt_BR.UTF-8):	Programa para atualização do utmp/wtmp
Summary(ru.UTF-8):	Привилегированная программа для изменений в utmp/wtmp
Summary(uk.UTF-8):	Привілейована програма для внесення змін до utmp/wtmp
%define	utempter_compat_ver	0.5.5
Name:		libutempter
Version:	1.2.1
Release:	1
License:	LGPL v2.1+
Group:		Base
Source0:	http://ftp.altlinux.org/pub/people/ldv/utempter/%{name}-%{version}.tar.gz
# Source0-md5:	afe828ce87262d7e043770553004e162
Patch0:		%{name}-utmp-cleanup.patch
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires(post,postun):	/sbin/ldconfig
Requires(postun):	/usr/sbin/groupdel
Provides:	group(utmp)
Provides:	utempter = %{utempter_compat_ver}
Obsoletes:	libutempter0
Obsoletes:	utempter
Conflicts:	rc-scripts < 0.4.9-1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Utempter is a utility which allows programs to log information to a
privileged file (/var/run/utmp), without compromising system
security. It accomplishes this task by acting as a buffer between root
and the programs.

%description -l es.UTF-8
Programa para actualización del utmp/wtmp.

%description -l pl.UTF-8
Utempter jest programem pozwalającym użytkownikom na zapisywanie do
pliku /var/run/utmp bez naruszania bezpieczeństwa systemu.

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
Provides:	utempter-devel = %{utempter_compat_ver}
Obsoletes:	libutempter0-devel
Obsoletes:	utempter-devel

%description devel
Header file for utempter library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki utemptera.

%package static
Summary:	Static utempter library
Summary(pl.UTF-8):	Statyczna biblioteka utemptera
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Provides:	utempter-static = %{utempter_compat_ver}

%description static
Static utempter library.

%description static -l pl.UTF-8
Statyczna biblioteka utemptera

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	RPM_OPT_FLAGS="%{rpmcppflags} %{rpmcflags}" \
	libdir="%{_libdir}" \
	libexecdir="%{_libexecdir}"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	libdir="%{_libdir}" \
	libexecdir="%{_libexecdir}" \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sbindir}
ln -s %{_libexecdir}/utempter/utempter $RPM_BUILD_ROOT%{_sbindir}
ln -s %{_libexecdir}/utempter/utmp-cleanup $RPM_BUILD_ROOT%{_sbindir}

install -d $RPM_BUILD_ROOT/var/run
:> $RPM_BUILD_ROOT/var/run/utmp

%clean
rm -rf $RPM_BUILD_ROOT

# not in trigger because utmpx is %%ghost, and %%ghost-ed files
# are removed when they'are uninstalled
%pretrans -p <lua>
utmpx = io.open("/var/run/utmpx", "rb")
if utmpx then
	utmpx:close()
	utmp_size = 0
	utmp = io.open("/var/run/utmp", "rb")
	if utmp then
		utmp_size = utmp:seek("end")
		utmp:close()
	end
	if utmp_size > 0 then
		os.remove("/var/run/utmpx")
	else
		os.remove("/var/run/utmp")
		os.rename("/var/run/utmpx", "/var/run/utmp")
	end
end

%pre
%groupadd -g 22 utmp

%post
/sbin/ldconfig
if [ ! -f /var/run/utmp ]; then
	umask 002
	touch /var/run/utmp
	chown root:utmp /var/run/utmp
	chmod 0664 /var/run/utmp
fi

%postun
/sbin/ldconfig
if [ "$1" = "0" ]; then
	%groupremove utmp
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_sbindir}/utempter
%attr(755,root,root) %{_sbindir}/utmp-cleanup
%dir %{_libexecdir}/utempter
%attr(2755,root,utmp) %{_libexecdir}/utempter/utempter
%attr(755,root,root) %{_libexecdir}/utempter/utmp-cleanup
%attr(755,root,root) %{_libdir}/libutempter.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libutempter.so.0
%attr(664,root,utmp) %ghost /var/run/utmp

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libutempter.so
%{_includedir}/utempter.h
%{_mandir}/man3/libutempter.3*
%{_mandir}/man3/utempter*.3*

%files static
%defattr(644,root,root,755)
%{_libdir}/libutempter.a
