%bcond_without cairo_xcb_backend 
%bcond_without cairo_gl_backend
%bcond_with wayland


Name:           cairo
Version:        1.12.14
Release:        0
License:        LGPL-2.1+ or MPL-1.1
Summary:        Vector Graphics Library with Cross-Device Output Support
Url:            http://cairographics.org/
Group:          Graphics/Libraries
Source:         http://cairographics.org/releases/%{name}-%{version}.tar.xz
Source99:       baselibs.conf
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  xz
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(x11)
BuildRequires:  which
%if %{with cairo_xcb_backend}
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-shm)
%endif
%if %{with cairo_gl_backend}
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(egl)
%if %{with wayland}
BuildRequires:	pkgconfig(wayland-egl)
%endif
%endif
BuildRequires:  pkgconfig(xrender)

%description
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

%package -n libcairo
License:        LGPL-2.1+ or MPL-1.1
Summary:        Vector Graphics Library with Cross-Device Output Support
Group:          Graphics/Libraries
Provides:       cairo = %{version}
Obsoletes:      cairo < %{version}

%description -n libcairo
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

%package -n libcairo-gobject
License:        LGPL-2.1+ or MPL-1.1
Summary:        Vector Graphics Library with Cross-Device Output Support
Group:          Graphics/Libraries

%description -n libcairo-gobject
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

This library contains GType declarations for Cairo types. It is also
meant to support gobject-introspection binding creation.

%package -n libcairo-script-interpreter
License:        LGPL-2.1+ or MPL-1.1
Summary:        Vector Graphics Library with Cross-Device Output Support
Group:          Graphics/Libraries

%description -n libcairo-script-interpreter
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

%package tools
License:        GPL-3.0+
Summary:        Vector Graphics Library with Cross-Device Output Support -- Utilities
Group:          Development/Libraries
# We need an explicit requires since nothing links to the cairo library
Requires:       libcairo = %{version}

%description tools
Cairo is a vector graphics library with cross-device output support.
Currently supported output targets include the X Window System,
in-memory image buffers, and PostScript. Cairo is designed to produce
identical output on all output media while taking advantage of display
hardware acceleration when available.

This package contains various cairo utilities.

%package devel
License:        LGPL-2.1+ or MPL-1.1
Summary:        Development environment for cairo
Group:          Development/Libraries
Requires:       libcairo = %{version}
Requires:       libcairo-gobject = %{version}
Requires:       libcairo-script-interpreter = %{version}

%description devel
This package contains all files necessary to build binaries using
cairo.

%prep
%setup -q

%build
# Disable Atom optimizations in order to make binaries executable in buildroot
export RPM_OPT_FLAGS=`echo $RPM_OPT_FLAGS | sed s'/atom/i686/g'`
export CFLAGS=`echo $CFLAGS | sed s'/atom/i686/g'`
export CXXFLAGS=`echo $CXXFLAGS | sed s'/atom/i686/g'`

# Needed by patch0
NOCONFIGURE=1 ./autogen.sh
%configure \
    --with-pic \
    --enable-fc \
    --enable-ft \
%if %{with cairo_gl_backend}
    --enable-gl  \
    --enable-egl \
%ifnarch %ix86
    --enable-glesv2=yes \
%endif
%endif
    --enable-ps \
    --enable-pdf \
    --enable-script \
    --enable-svg \
    --enable-tee \
%if %{with cairo_xcb_backend}
    --enable-xcb \
%endif
    --enable-xlib \
    --disable-gtk-doc \
    --disable-static
make %{?_smp_mflags} V=1

%install
%make_install

%post -n libcairo -p /sbin/ldconfig

%postun -n libcairo -p /sbin/ldconfig

%post -n libcairo-gobject -p /sbin/ldconfig

%postun -n libcairo-gobject -p /sbin/ldconfig

%post -n libcairo-script-interpreter -p /sbin/ldconfig

%postun -n libcairo-script-interpreter -p /sbin/ldconfig

%files -n libcairo
%defattr(-, root, root)
%license COPYING COPYING-LGPL-2.1 COPYING-MPL-1.1
%{_libdir}/libcairo.so.*

%files -n libcairo-gobject
%defattr(-, root, root)
%{_libdir}/libcairo-gobject.so.2*

%files -n libcairo-script-interpreter
%defattr(-, root, root)
%license util/cairo-script/COPYING
%{_libdir}/libcairo-script-interpreter.so.*

%files tools
%defattr(-, root, root)
%license util/cairo-trace/COPYING util/cairo-trace/COPYING-GPL-3
%{_bindir}/cairo-sphinx
%{_bindir}/cairo-trace
%dir %{_libdir}/cairo
%{_libdir}/cairo/cairo-fdr.so
%{_libdir}/cairo/cairo-sphinx.so
%{_libdir}/cairo/libcairo-trace.so

%files devel
%defattr(-, root, root)
%doc PORTING_GUIDE
%doc %{_datadir}/gtk-doc/html/cairo
%{_includedir}/cairo/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog