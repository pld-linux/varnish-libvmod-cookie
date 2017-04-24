#
# Conditional build:
%bcond_without	tests		# build without tests

%define	vmod	cookie
Summary:	Cookie VMOD for Varnish
Name:		varnish-libvmod-%{vmod}
Version:	1.0
Release:	2
License:	BSD
Group:		Daemons
Source0:	https://github.com/lkarsten/libvmod-cookie/archive/libvmod-%{vmod}-%{version}.tar.gz
# Source0-md5:	cbd0f4c546d24896f0a1b81b4858621d
URL:		https://github.com/lkarsten/libvmod-cookie
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	python-docutils
BuildRequires:	varnish-source
%{?with_tests:BuildRequires:	varnish}
%requires_eq_to varnish varnish-source
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		vmoddir	%(pkg-config --variable=vmoddir varnishapi || echo ERROR)

%description
Cookie VMOD for Varnish.

%prep
%setup -qc
mv libvmod-%{vmod}-*/* .

%build
%{__aclocal} -I m4
%{__libtoolize}
%{__autoheader}
%{__automake}
%{__autoconf}

VARNISHSRC=$(pkg-config --variable=srcdir varnishapi)
%configure \
	VARNISHSRC=$VARNISHSRC \
	VMODDIR=%{vmoddir} \
	--disable-static

%{__make}
%{?with_tests:%{__make} check}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/varnish/vmods/libvmod_%{vmod}.la
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/libvmod-%{vmod}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE
%attr(755,root,root) %{vmoddir}/libvmod_%{vmod}.so
%{_mandir}/man3/vmod_%{vmod}.3*
