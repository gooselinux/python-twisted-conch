%{!?python:%define python python}
%{!?python_sitearch: %define python_sitearch %(%{python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           %{python}-twisted-conch
Version:        8.2.0
Release:        3.2%{?dist}
Summary:        SSH and SFTP protocol implementation together with clients and servers
Group:          Development/Libraries
License:        MIT
URL:            http://twistedmatrix.com/trac/wiki/TwistedConch
Source0:        http://tmrc.mit.edu/mirror/twisted/Conch/8.2/TwistedConch-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  %{python}-twisted-core >= 8.2.0
BuildRequires:  %{python}-devel
Requires:       %{python}-twisted-core >= 8.2.0
Requires:       %{python}-crypto
# for tkconch
Requires:       tkinter

# a noarch-turned-arch package should not have debuginfo
%define debug_package %{nil}

%description
Twisted is an event-based framework for internet applications.

Conch is an SSHv2 implementation written in Python. SSH is a protocol designed
to allow remote access to shells and commands, but it is generic enough to
allow everything from TCP forwarding to generic filesystem access. Since conch
is written in Python, it interfaces well with other Python projects, such as
Imagination. Conch also includes a implementations of the telnet and vt102
protocols, as well as support for rudamentary line editing behaviors. A new
implementation of Twisted's Manhole application is also included, featuring
server-side input history and interactive syntax coloring.

%prep
%setup -q -n TwistedConch-%{version}

# Fix doc file dependencies
chmod -x doc/{benchmarks/buffering_mixin.py,examples/sshsimpleserver.py}

%build
%{python} setup.py build

%install
rm -rf %{buildroot}

# This is a pure python package, but extending the twisted namespace from
# python-twisted-core, which is arch-specific, so it needs to go in sitearch
%{python} setup.py install -O1 --skip-build \
    --install-purelib %{python_sitearch} --root %{buildroot}

# Man pages
mkdir -p %{buildroot}%{_mandir}/man1/
cp -a doc/man/*.1 %{buildroot}%{_mandir}/man1/
rm -rf doc/man

# See if there's any egg-info
if [ -f %{buildroot}%{python_sitearch}/Conch*.egg-info ]; then
    echo %{buildroot}%{python_sitearch}/Conch*.egg-info |
        sed -e "s|^%{buildroot}||"
fi > egg-info

%clean
rm -rf %{buildroot}

%post
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%postun
if [ -x %{_libexecdir}/twisted-dropin-cache ]; then
    %{_libexecdir}/twisted-dropin-cache || :
fi

%files -f egg-info
%defattr(-,root,root,-)
%doc LICENSE NEWS README doc/*
%{_bindir}/cftp
%{_bindir}/ckeygen
%{_bindir}/conch
%{_bindir}/tkconch
%{_mandir}/man1/cftp.1*
%{_mandir}/man1/ckeygen.1*
%{_mandir}/man1/conch.1*
%{_mandir}/man1/tkconch.1*
%{python_sitearch}/twisted/conch/
%{python_sitearch}/twisted/plugins/twisted_conch.py*

%changelog
* Wed Jan 27 2010 David Malcolm <dmalcolm@redhat.com> - 8.2.0-3.2
- fix source URL

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 8.2.0-3.1
- Rebuilt for RHEL 6

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Matthias Saou <http://freshrpms.net/> 8.2.0-1
- Update to 8.2.0.
- Change back spec cosmetic details from Paul's to Thomas' preference.

* Tue Dec 23 2008 Matthias Saou <http://freshrpms.net/> 8.1.0-2
- Update to 8.1.0.
- Merge back changes from Paul Howarth.
- Make sure the scriplets never return a non-zero exit status.
- Add tkinter requirement for tkconch (#440385).

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.0-6
- Fix locations for Python 2.6

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.8.0-5
- Rebuild for Python 2.6

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.8.0-4
- Handle the egg correctly, since the name is odd.

* Fri Mar 07 2008 Jesse Keating <jkeating@redhat.com> - 0.8.0-3
- Drop the pyver stuff, handle egg.

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.8.0-2
- Autorebuild for GCC 4.3

* Fri Aug 31 2007 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.8.0-1
- new version

* Tue Dec 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.0-4
- fixed URL
- added NEWS and LICENSE

* Wed Nov 01 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.0-3
- make doc files non-executable

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.0-2
- no longer ghost .pyo files
- rebuild dropin.cache

* Wed Jun 07 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 0.7.0-1
- update to new upstream release
- remove NoArch, since it is installed into an arch-specific twisted
  namespace

* Fri Sep 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.5.0-3
- normalize crypto name

* Tue Aug 23 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.5.0-2
- need twisted to build

* Fri Mar 25 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.5.0-1
- final release

* Wed Mar 16 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.5.0-0.1.a3
- upstream release

* Sat Mar 12 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.5.0-0.1.a2
- new prerelease; FE versioning

* Mon Feb 07 2005 Jeff Pitman <symbiont+pyvault@berlios.de> 0.1.0-1
- prep for split

