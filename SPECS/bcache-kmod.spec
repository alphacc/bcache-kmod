Source10: kmodtool-bcache-el7.sh
%define kmodtool bash %{SOURCE10}

%{!?kversion: %define kversion 3.10.0-123.4.2.el7.%{_target_cpu}}

%define kmod_name bcache
%define kverrel %(%{kmodtool} verrel %{?kversion} 2>/dev/null)

%define upvar ""
%ifarch i586 i686 ppc
%define smpvar smp
%endif
%ifarch i686 x86_64
%endif
%{!?kvariants: %define kvariants %{?upvar} %{?smpvar} %{?xenvar} %{?kdumpvar}}

Name:		%{kmod_name}-kmod	
Version:	3.10
Release:	1%{?dist}
Summary:	%{kmod_name} kernel module(s)

Group:		System Environment/Kernel		
License:	GPLv2
URL:		http://www.kernel.org
Source0:	%{kmod_name}-%{version}.tar.gz


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	redhat-rpm-config

ExclusiveArch:  x86_64

%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kverrel} %{kvariants} 2>/dev/null)}

%define debug_package %{nil}
%define __find_requires sh %{_builddir}/%{buildsubdir}/filter-requires.sh

%description
This package provides the RHEL-7 %{kmod_name} kernel module.
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -c -T -a 0
pushd %{kmod_name}-%{version}*
popd
for kvariant in %{kvariants} ; do
    %{__cp} -a %{kmod_name}-%{version} _kmod_build_$kvariant
done

%build
for kvariant in %{kvariants}
do
  #ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}.%{_target_cpu}
  ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}
  pushd _kmod_build_$kvariant
  make -C "${ksrc}" SUBDIRS=${PWD} modules %{?_smp_mflags}
  popd
done

%install
rm -rf $RPM_BUILD_ROOT
for kvariant in %{kvariants}
do
  ksrc=%{_usrsrc}/kernels/%{kverrel}${kvariant:+-$kvariant}
  pushd _kmod_build_$kvariant
  export INSTALL_MOD_PATH=%{buildroot}
  export INSTALL_MOD_DIR=extra/%{kmod_name}
  make -C ${ksrc} SUBDIRS=${PWD} modules_install
  %{__rm} -f %{buildroot}/lib/modules/%{kversion}/modules.*
  popd
done
find %{buildroot} -type f -name \*.ko -exec %{__chmod} u+x \{\} \;

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jun 27 2014 Thomas Oulevey <thomas.oulevey@cern.ch> 3.10-1 
- Initial el7. 
- bcache source from kernel-3.10.0-123.4.2.el7.x86_64.src.rpm.
