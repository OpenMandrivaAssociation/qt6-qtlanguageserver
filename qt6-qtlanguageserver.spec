#define beta rc
#define snapshot 20200627
%define major 6
%undefine _debugsource_packages

%define _qtdir %{_libdir}/qt%{major}

Name:		qt6-qtlanguageserver
Version:	6.9.1
Release:	%{?beta:0.%{beta}.}%{?snapshot:0.%{snapshot}.}1
%if 0%{?snapshot:1}
# "git archive"-d from "dev" branch of git://code.qt.io/qt/qtlanguageserver.git
Source:		qtlanguageserver-%{?snapshot:%{snapshot}}%{!?snapshot:%{version}}.tar.zst
%else
Source:		http://download.qt-project.org/%{?beta:development}%{!?beta:official}_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}%{?beta:-%{beta}}/submodules/qtlanguageserver-everywhere-src-%{version}%{?beta:-%{beta}}.tar.xz
%endif
Group:		System/Libraries
Summary:	Qt %{major} Network Authentication module
BuildRequires:	cmake
BuildRequires:	ninja
BuildRequires:	cmake(Qt%{major}Core)
BuildRequires:	cmake(Qt%{major}Network)
BuildRequires:	cmake(Qt%{major}Widgets)
BuildRequires:	qt%{major}-cmake
License:	LGPLv3/GPLv3/GPLv2

%description
Qt %{major} network authentication module

%define extra_devel_files_LanguageServer \
%{_qtdir}/lib/cmake/Qt6BuildInternals/StandaloneTests/QtLanguageServerTestsConfig.cmake \
%{_qtdir}/sbom/*

# These used to be shared libraries before 6.8.0
%define extra_devel_reqprov_LanguageServer \
Requires:	cmake(Qt%{major}JsonRpcPrivate) \
Obsoletes:	%{mklibname Qt6LanguageServer} < %{EVRD} \
Obsoletes:	%{mklibname -d Qt6LanguageServer} < %{EVRD}

%define extra_devel_reqprov_JsonRpc \
Obsoletes:	%{mklibname Qt6JsonRpc} < %{EVRD} \
Obsoletes:	%{mklibname -d Qt6JsonRpc} < %{EVRD}

%qt6staticlibs LanguageServer JsonRpc

%prep
%autosetup -p1 -n qtlanguageserver%{!?snapshot:-everywhere-src-%{version}%{?beta:-%{beta}}}
%cmake -G Ninja \
	-DCMAKE_INSTALL_PREFIX=%{_qtdir} \
	-DQT_BUILD_EXAMPLES:BOOL=ON \
	-DQT_WILL_INSTALL:BOOL=ON

%build
export LD_LIBRARY_PATH="$(pwd)/build/lib:${LD_LIBRARY_PATH}"
%ninja_build -C build

%install
%ninja_install -C build
%qt6_postinstall
