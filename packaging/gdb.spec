Name:           gdb
Version:        7.8.1
Release:        0
License:        GPL-3.0+
Summary:        A GNU source-level debugger for C, C++, Java and other languages
Url:            http://gnu.org/software/gdb/
Group:          Development/Toolchain
Source:         ftp://ftp.gnu.org/gnu/gdb/gdb-%{version}.tar.bz2
Source1001:     gdb.manifest
%define gdb_src gdb-%{version}
%define gdb_build build-%{_target_platform}

BuildRequires:  bison
BuildRequires:  expat-devel
BuildRequires:  flex
BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  gcc-c++
BuildRequires:  ncurses-devel
BuildRequires:  rpm-devel
BuildRequires:  texinfo

%description
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

%package devel
Summary:        Development files for gdb

%description devel
Development files for gdb.

%package server
Summary:        A standalone server for GDB (the GNU source-level debugger)

%description server
GDB, the GNU debugger, allows you to debug programs written in C, C++,
Java, and other languages, by executing them in a controlled fashion
and printing their data.

This package provides a program that allows you to run GDB on a different machine than the one which is running the program being debugged.

%prep
%setup -q 
cp %{SOURCE1001} .

# Remove the info and other generated files added by the FSF release
# process.
rm -f libdecnumber/gstdint.h
rm -f bfd/doc/*.info
rm -f bfd/doc/*.info-*
rm -f gdb/doc/*.info
rm -f gdb/doc/*.info-*

%build
%configure						\
	--with-gdb-datadir=%{_datadir}/gdb		\
	--enable-gdb-build-warnings=,-Wno-unused	\
	--disable-werror				\
	--with-separate-debug-dir=/usr/lib/debug	\
	--disable-sim					\
	--disable-rpath					\
	--with-expat					\
	--with-python=no				\
	--enable-64-bit-bfd				\
	--enable-static --disable-shared --enable-debug

make %{?_smp_mflags}


%install
%make_install

%find_lang opcodes
%find_lang bfd
mv opcodes.lang %{name}.lang
cat bfd.lang >> %{name}.lang

%docs_package

%lang_package

%files
%defattr(-,root,root)
%manifest %{name}.manifest
%license COPYING COPYING.LIB 
%{_bindir}/*
%{_datadir}/gdb

%files server
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/gdbserver
%{_mandir}/*/gdbserver.1*
%ifarch %{ix86} x86_64
%{_libdir}/libinproctrace.so
%endif

%files devel
%manifest %{name}.manifest
%{_includedir}/*.h
%{_includedir}/gdb/*.h
