#
# spec file for package msbuild
#
# Copyright (c) 2016 Xamarin, Inc (http://www.xamarin.com)
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

Name:           msbuild-libhostfxr
Version:	2.0.0.2017.07.06.00.01
Release:	0.nightly.3
Summary:        Build system for .NET projects - unmanaged helper library
License:        MIT
Group:          Development/Libraries/Other
Url:            https://github.com/dotnet/core-setup
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Source0:        core-setup-%{version}.tar.gz
Patch0:		avoid-gcc49-features.patch
Patch1:         avoid_cmake_unknown_command.patch
Patch2:         dont_use_add_compile_options.diff
Patch3:         23510ddc07acb714c1dace14322ef047f9f1c888.diff
%if 0%{?rhel} >= 7
BuildRequires:  cmake
BuildRequires:  gcc-c++
Requires:       msbuild-sdkresolver
%endif

%define debug_package %{nil}

%description
The Microsoft Build Engine is a platform for building applications.
This engine, which is also known as MSBuild, provides an XML schema
for a project file that controls how the build platform processes
and builds software. Visual Studio uses MSBuild, but MSBuild does
not depend on Visual Studio. By invoking msbuild.exe on your
project or solution file, you can orchestrate and build products
in environments where Visual Studio isn't installed. This package
contains unmanaged components for msbuild-sdkresolver
%if 0%{?rhel} <= 6
This package is intentionally left blank on CentOS 6, and
functionality is notavailable
%endif

%prep
%setup -n core-setup-release-2.0.0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
%if 0%{?rhel} >= 7
%{?exp_env}
%{?env_options}
cd src/corehost/cli/fxr/ && cmake . -DCLI_CMAKE_PLATFORM_ARCH_AMD64=1 -DCLI_CMAKE_HOST_POLICY_VER=1.0.0 -DCLI_CMAKE_HOST_FXR_VER=2.0.0-preview2-25407-01 -DCLI_CMAKE_HOST_VER=1.0.0 -DCLI_CMAKE_APPHOST_VER=1.0.0 -DCLI_CMAKE_PKG_RID=ubuntu.14.04-x64 -DCLI_CMAKE_COMMIT_HASH=bd3f818bad84f1296b4ee53f72ab8837b3caac98 -DCLI_CMAKE_PORTABLE_BUILD=1 && make
%endif

%install
%if 0%{?rhel} >= 7
%{?env_options}
%__mkdir_p %{buildroot}/%{_prefix}/lib/mono/msbuild/Current/bin/SdkResolvers/Microsoft.DotNet.MSBuildSdkResolver/
cp src/corehost/cli/fxr/libhostfxr.so %{buildroot}/%{_prefix}/lib/mono/msbuild/Current/bin/SdkResolvers/Microsoft.DotNet.MSBuildSdkResolver/
%endif

%files
%defattr(-,root,root)
%if 0%{?rhel} >= 7
%{_prefix}/lib/mono/msbuild/Current/bin/SdkResolvers/Microsoft.DotNet.MSBuildSdkResolver/*
%endif
