%global commit 61127c58ffe9a798cf0b3403efe9b1bbfcb80a5f
%global commitdate 20140705
%global checkout %{commitdate}git%{shortcommit}
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global shortname clc

Name:           libclc
Version:        0.0.1
Release:        5.%{checkout}%{?dist}
Summary:        An open source implementation of the OpenCL 1.1 library requirements

License:        BSD
URL:            http://libclc.llvm.org/
# created using:
# $ export PKG=libclc-$(date +%Y%m%d)git$(git describe --always)
# $ git archive --prefix $PKG/ --format tar HEAD | xz > $PKG.tar.xz
#Source0:        %{name}-%{checkout}.tar.xz
Source0:        https://github.com/llvm-mirror/%{name}/archive/%{commit}/%{name}-%{checkout}.tar.gz

# Only builds on x86
ExclusiveArch:	%{ix86} x86_64

BuildRequires:  llvm >= 3.3-0.6, llvm-devel, llvm-static
BuildRequires:  clang >= 3.3-0.6
BuildRequires:  libstdc++-devel
BuildRequires:  zlib-devel
BuildRequires:  python

%description
libclc is an open source, BSD licensed implementation of the library
requirements of the OpenCL C programming language, as specified by the
OpenCL 1.1 Specification. The following sections of the specification
impose library requirements:

  * 6.1: Supported Data Types
  * 6.2.3: Explicit Conversions
  * 6.2.4.2: Reinterpreting Types Using as_type() and as_typen()
  * 6.9: Preprocessor Directives and Macros
  * 6.11: Built-in Functions
  * 9.3: Double Precision Floating-Point
  * 9.4: 64-bit Atomics
  * 9.5: Writing to 3D image memory objects
  * 9.6: Half Precision Floating-Point

libclc is intended to be used with the Clang compiler's OpenCL frontend.

libclc is designed to be portable and extensible. To this end, it provides
generic implementations of most library requirements, allowing the target
to override the generic implementation at the granularity of individual
functions.

libclc currently only supports the PTX target, but support for more
targets is welcome.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n "%{name}-%{commit}"


%build
./configure.py --prefix=%{_prefix} --libexecdir=%{_libdir}/%{shortname}/ --pkgconfigdir=%{_libdir}/pkgconfig/

# fstack-protector-strin is currently not supported by clang++
sed -i "s/fstack-protector-strong/fstack-protector/" Makefile

make %{?_smp_mflags}


%install
%make_install


%files
%doc LICENSE.TXT README.TXT CREDITS.TXT
%{_libdir}/%{shortname}/*.bc
%{_includedir}/%{shortname}

%files devel
%doc
%{_libdir}/pkgconfig/%{name}.pc


%changelog
* Sat Jul 05 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-5
- Update to latest snapshot to support AMD Kaveri APUs
- Move bitcode files to an arch dependent dir, as they are arch dependent

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-4.20140429git4341094
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 29 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140429git4341094
- Update to latest snapshot
- Support for AMD Kabini

* Mon Jan 13 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-2.20140108gitc002f62
- Move headers to main package, needed by clover at runtime

* Wed Jan 08 2014 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-1.20140108gitc002f62
- Could not use latest master because it doesn't build
- Update to a fresher snapshot
- Limit to x86

* Sun Jul 14 2013 Fabian Deutsch <fabiand@fedoraproject.org> - 0.0.1-0.20130714git5217211
- Initial package
