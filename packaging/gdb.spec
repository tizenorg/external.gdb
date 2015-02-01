Summary: A GNU source-level debugger for C, C++, Java and other languages
Name: gdb
Version: 7.2
Release: 2
License: GPLv3+
Group: Development/Debuggers
URL: http://gnu.org/software/gdb/
Source: ftp://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
Source101: gdb-rpmlintrc
Source1001: gdb.manifest
Patch0: gdb-7.2-noreturn.patch
Patch1: gdb-7.2-lib-order.patch

%define gdb_src gdb-%{version}
%define gdb_build build-%{_target_platform}

BuildRequires: ncurses-devel
BuildRequires: gettext
BuildRequires: texinfo
BuildRequires: flex
BuildRequires: bison
BuildRequires: expat-devel
BuildRequires: readline-devel
BuildRequires: rpm-devel
#=BuildRequires: python-devel
BuildRequires: libstdc++

Requires: readline
 
%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%package server
Summary: A standalone server for GDB (the GNU source-level debugger)
Group: Development/Debuggers

%description server
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides a program that allows you to run GDB on a different machine than the one which is running the program being debugged.

%prep
%setup -q -n %{gdb_src}
%patch0 -p1
%patch1 -p1

# Files have `# <number> <file>' statements breaking VPATH / find-debuginfo.sh .
rm -f gdb/ada-exp.c gdb/ada-lex.c gdb/c-exp.c gdb/cp-name-parser.c gdb/f-exp.c
rm -f gdb/jv-exp.c gdb/m2-exp.c gdb/objc-exp.c gdb/p-exp.c

# Remove the info and other generated files added by the FSF release
# process.
rm -f libdecnumber/gstdint.h
rm -f bfd/doc/*.info
rm -f bfd/doc/*.info-*
rm -f gdb/doc/*.info
rm -f gdb/doc/*.info-*

%build
rm -fr %{gdb_build}
mkdir %{gdb_build}
cd %{gdb_build}
cp %{SOURCE1001} $RPM_BUILD_DIR/%{gdb_src}

export CFLAGS="$RPM_OPT_FLAGS"

../configure						\
	--prefix=%{_prefix}				\
	--libdir=%{_libdir}				\
	--sysconfdir=%{_sysconfdir}			\
	--mandir=%{_mandir}				\
	--infodir=%{_infodir}				\
	--with-gdb-datadir=%{_datadir}/gdb		\
	--enable-gdb-build-warnings=,-Wno-unused	\
	--disable-werror				\
	--with-separate-debug-dir=/usr/lib/debug	\
	--disable-sim					\
	--disable-rpath					\
	--with-system-readline				\
	--with-expat					\
	--enable-tui					\
	--without-python				\
	--without-libunwind				\
	--enable-64-bit-bfd				\
	--enable-static --disable-shared --enable-debug	\
	%{_target_platform}

make %{?_smp_mflags}

# Copy the <sourcetree>/gdb/NEWS file to the directory above it.
cp $RPM_BUILD_DIR/%{gdb_src}/gdb/NEWS $RPM_BUILD_DIR/%{gdb_src}

%check
# Initially we're in the %{gdb_src} directory.
cd %{gdb_build}

%install
# Initially we're in the %{gdb_src} directory.
cd %{gdb_build}
rm -rf $RPM_BUILD_ROOT

make %{?_smp_mflags} install DESTDIR=$RPM_BUILD_ROOT

# install the gcore script in /usr/bin
cp $RPM_BUILD_DIR/%{gdb_src}/gdb/gdb_gcore.sh $RPM_BUILD_ROOT%{_bindir}/gcore
chmod 755 $RPM_BUILD_ROOT%{_bindir}/gcore

# Remove the gdb/gdbtui binaries duplicity.
test -x $RPM_BUILD_ROOT%{_prefix}/bin/gdbtui
ln -sf gdb $RPM_BUILD_ROOT%{_prefix}/bin/gdbtui
cmp $RPM_BUILD_ROOT%{_mandir}/*/gdb.1 $RPM_BUILD_ROOT%{_mandir}/*/gdbtui.1
ln -sf gdb.1 $RPM_BUILD_ROOT%{_mandir}/*/gdbtui.1

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/
rm -rf $RPM_BUILD_ROOT%{_infodir}/*
rm -rf $RPM_BUILD_ROOT%{_includedir}
rm -rf $RPM_BUILD_ROOT/%{_libdir}/lib{bfd*,opcodes*,iberty*,mmalloc*}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%manifest gdb.manifest
%defattr(-,root,root)
%doc COPYING COPYING.LIB README NEWS
%{_bindir}/gcore
%{_bindir}/gdb
%{_bindir}/gdbtui
%{_mandir}/*/gdb.1*
%{_mandir}/*/gdbtui.1*
%{_datadir}/gdb

%files server
%manifest gdb.manifest
%defattr(-,root,root)
%{_bindir}/gdbserver
%{_mandir}/*/gdbserver.1*
%ifarch %{ix86} x86_64
%{_libdir}/libinproctrace.so
%endif
