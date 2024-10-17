# TODO rewrite initscript ( to create the device ), and load the module
#  check requires and buildrequires
#

Name: coda
Version: 6.9.4
Release: 4
Summary: Coda distributed filesystem
License: GPL
Group: Networking/Other
Url: https://www.coda.cs.cmu.edu/doc/html/index.html
Source: ftp://ftp.coda.cs.cmu.edu/pub/coda/src/coda-%{version}.tar.gz
Patch0:	venus_vol_cml.patch
BuildRequires: lwp-devel
BuildRequires: rvm-devel
BuildRequires: rpc2-devel
BuildRequires: rvm-tools
BuildRequires: ncurses-devel
BuildRequires: readline-devel
BuildRequires: byacc
BuildRequires: flex
Requires: bc
Requires(post,preun): rpm-helper

%description
Source package for the Coda filesystem.  Three packages are provided by
this rpm: the client and server and the backup components. Separately
you must install a kernel module, or have a Coda enabled kernel, and 
you should get the Coda documentation package.


%package client
Summary: Coda client
Group: Networking/Other
Requires: bc
Requires: ed
Obsoletes:  coda-debug-client
Requires(post,preun): rpm-helper

%description client
This package contains the main client program, the cachemanager Venus.
Also included are the binaries for the cfs, utilities for logging, ACL
manipulation etc, the hoarding tools for use with laptops and repair
tools for fixing conflicts. Finally there is the cmon and codacon
console utilities to monitor Coda's activities. You need a Coda
kernel-module for your kernel version, or Coda in your kernel, to have
a complete coda client.  Make sure to select the correct C library
version.

%package server
Summary: Coda server
Group: Networking/Other
Requires: bc
Requires: ed
Requires: rvm-tools
Obsoletes:  coda-debug-server
Requires(post,preun): rpm-helper

%description server
This package contains the fileserver codasrv for the coda filesystem,
as well as the volume utilities.  For highest performance you will
need a modified kernel with inode system calls.

%package backup
Summary: Coda backup coordinator
Group: Networking/Other
Requires: bc
Requires: ed
Obsoletes:  coda-debug-backup
Requires(post,preun): rpm-helper

%description backup
This package contains the backup software for the coda filesystem, as
well as the volume utilities.

%prep
%setup -q -n coda-%{version}
%patch0 -p0

%build
# chown -R $LOGNAME.users $RPM_BUILD_DIR/coda-%{version}
rm -rf $RPM_BUILD_DIR/obj-%{version}
mkdir $RPM_BUILD_DIR/obj-%{version}
cd $RPM_BUILD_DIR/obj-%{version}
$RPM_BUILD_DIR/coda-%{version}/configure --prefix=%{_prefix}
make

%install
cd $RPM_BUILD_DIR/obj-%{version}
mkdir -p %{buildroot}%{_prefix}/coda/venus.cache %{buildroot}/dev \
	 %{buildroot}%{_prefix}/coda/etc \
	 %{buildroot}/coda %{buildroot}%{_initrddir}\
	 %{buildroot}%{_libdir}/coda %{buildroot}%{_initrddir}
 %makeinstall_std

#make prefix=%{buildroot}%{_prefix} client-install 
#make prefix=%{buildroot}%{_prefix} server-install

touch %{buildroot}/coda/NOT_REALLY_CODA

# for non debuging versions
if [ X1 != X1 ]; then
   strip %{buildroot}%{_bindir}/* %{buildroot}/vice/bin/* %{buildroot}%{_sbindir}/* || :
fi
for i in %{buildroot}/%{_initrddir}/*init ;
do 
    mv $i ${i//.init/}
done

#mkdir -p %{buildroot}/%{_mandir}
#mv -f %{buildroot}/%{_prefix}/man/* %{buildroot}/%{_mandir}

%clean
rm -rf $RPM_BUILD_DIR/obj-%{version}

%preun client
%_preun_service venus
	
%post client
%_post_service venus

%post server
%_post_service update
%_post_service auth2
%_post_service codasrv
#mknod /dev/cfs0 c 67 0

%preun server
%_preun_service update
%_preun_service auth2
%_preun_service codasrv
#rm -rf /dev/cfs0

%files client
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL ChangeLog LICENSE NEWS README*
%dir %{_prefix}/coda
%dir %{_prefix}/coda/etc
%dir %{_prefix}/coda/venus.cache
%dir /coda
%verify() /coda/NOT_REALLY_CODA
%config(noreplace)/etc/coda/venus.conf.ex
%{_initrddir}/venus
%{_sbindir}/codaconfedit
%{_sbindir}/venus
%{_sbindir}/venus-setup
%{_sbindir}/volmunge
%{_sbindir}/vutil
%{_bindir}/cfs
%{_bindir}/clog
%{_bindir}/cmon
%{_bindir}/codacon
%{_bindir}/gcodacon
%{_bindir}/cpasswd
%{_bindir}/ctokens
%{_bindir}/cunlog
%{_bindir}/filerepair
%{_bindir}/hoard
%{_bindir}/mklka
%{_bindir}/parser
%{_bindir}/removeinc
%{_bindir}/repair
%{_bindir}/coda_replay
%{_bindir}/spy
%{_bindir}/xaskuser
%{_bindir}/xfrepair
%{_bindir}/getvolinfo
%{_bindir}/rpc2ping
%{_bindir}/smon2

%{_mandir}/man1/cfs.1*
%{_mandir}/man1/clog.1*
%{_mandir}/man1/cmon.1*
%{_mandir}/man1/cunlog.1*
%{_mandir}/man1/hoard.1*
%{_mandir}/man1/repair.1*
%{_mandir}/man1/spy.1*
%{_mandir}/man1/coda_replay.1*
%{_mandir}/man1/cpasswd.1*
%{_mandir}/man1/ctokens.1*
%{_mandir}/man5/passwd.coda.5*
%{_mandir}/man8/venus.8*
%{_mandir}/man8/venus-setup.8*

%files server
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL ChangeLog LICENSE NEWS README*
%config(noreplace)/etc/coda/server.conf.ex
%config(noreplace)/etc/coda/realms
%{_sbindir}/auth2
%{_sbindir}/bldvldb.sh
%{_sbindir}/codasrv
%{_sbindir}/createvol_rep
%{_sbindir}/initpw
%{_sbindir}/inoder
%{_sbindir}/parserecdump
%{_sbindir}/partial-reinit.sh
%{_sbindir}/pdbtool
%{_sbindir}/printvrdb
%{_sbindir}/purgevol_rep
%{_sbindir}/startserver
%{_sbindir}/updatesrv
%{_sbindir}/updateclnt
%{_sbindir}/updatefetch
%{_sbindir}/vice-killvolumes
%{_sbindir}/vice-setup
%{_sbindir}/vice-setup-rvm
%{_sbindir}/vice-setup-srvdir
%{_sbindir}/vice-setup-user
%{_sbindir}/vice-setup-scm
%{_sbindir}/volutil
%{_bindir}/rvmsizer 
%{_sbindir}/codastart
%{_sbindir}/norton
%{_sbindir}/norton-reinit
%{_bindir}/reinit
%{_sbindir}/coda-server-logrotate
%{_bindir}/au
#%{_bindir}/gcodacon
%{_bindir}/mkcodabf
%{_sbindir}/asrlauncher
%{_sbindir}/tokentool
%{_mandir}/man1/au.1*
%{_mandir}/man1/mkcodabf.1*
%{_mandir}/man5/maxgroupid.5*
%{_mandir}/man5/servers.5*
%{_mandir}/man5/vicetab.5*
%{_mandir}/man5/volumelist.5*
%{_mandir}/man5/vrdb.5*
%{_mandir}/man8/auth2.8*
%{_mandir}/man8/backup.8*
%{_mandir}/man8/bldvldb.sh.8*
%{_mandir}/man8/codasrv.8*
%{_mandir}/man8/createvol_rep.8*
%{_mandir}/man8/initpw.8*
%{_mandir}/man8/merge.8*
%{_mandir}/man8/norton.8*
%{_mandir}/man8/pdbtool.8*
%{_mandir}/man8/purgevol_rep.8*
%{_mandir}/man8/readdump.8*
%{_mandir}/man8/startserver.8*
%{_mandir}/man8/updateclnt.8*
%{_mandir}/man8/updatesrv.8*
%{_mandir}/man8/vice-setup.8*
%{_mandir}/man8/volmunge.8*
%{_mandir}/man8/volutil.8*
%{_mandir}/man8/vutil.8*

%{_initrddir}/codasrv
%{_initrddir}/auth2
%{_initrddir}/update

%files backup
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL ChangeLog LICENSE NEWS README*
%{_sbindir}/backup
%{_sbindir}/backup.sh
%{_sbindir}/merge
%{_sbindir}/readdump
%{_sbindir}/tape.pl
#%{_sbindir}/updatesrv
#%{_sbindir}/updateclnt
#%{_sbindir}/updatefetch
#%{_sbindir}/volutil
%{_sbindir}/codadump2tar
%{_mandir}/man5/backuplogs.5.*
%{_mandir}/man5/dumpfile.5.*
%{_mandir}/man5/dumplist.5.*


%changelog
* Wed Jan 27 2010 Antoine Ginies <aginies@mandriva.com> 6.9.4-2mdv2010.1
+ Revision: 497223
- remove missing binaries
- fix the build

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - package renaming

* Fri Mar 06 2009 Guillaume Rousse <guillomovitch@mandriva.org> 6.9.4-1mdv2009.1
+ Revision: 349583
- new version
- rebuild for latest readline

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild
    - fix lwp buildrequires (b/c of breakage in lwp lib when adapting to new devel
      policy)
    - rebuild
    - fix prereq
    - kill re-definition of %%buildroot on Pixel's request
    - import coda-debug

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

