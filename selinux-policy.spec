%define distro redhat
%define polyinstatiate n
%define monolithic n
%if %{?BUILD_STRICT:0}%{!?BUILD_STRICT:1}
%define BUILD_STRICT 1
%endif
%if %{?BUILD_TARGETED:0}%{!?BUILD_TARGETED:1}
%define BUILD_TARGETED 1
%endif
%if %{?BUILD_MLS:0}%{!?BUILD_MLS:1}
%define BUILD_MLS 1
%endif
%define POLICYVER 21
%define libsepolver 2.0.1-2
%define POLICYCOREUTILSVER 2.0.7-5
%define CHECKPOLICYVER 2.0.1-2
Summary: SELinux policy configuration
Name: selinux-policy
Version: 2.5.12
Release: 11%{?dist}
License: GPL
Group: System Environment/Base
Source: serefpolicy-%{version}.tgz
patch: policy-20070219.patch
Source1: modules-targeted.conf
Source2: booleans-targeted.conf
Source3: Makefile.devel
Source4: setrans-targeted.conf
Source5: modules-mls.conf
Source6: booleans-mls.conf	
Source8: setrans-mls.conf
Source9: modules-strict.conf
Source10: booleans-strict.conf
Source12: setrans-strict.conf
Source13: policygentool
Source14: securetty_types-targeted
Source15: securetty_types-mls
Source16: securetty_types-strict

Url: http://serefpolicy.sourceforge.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
BuildRequires: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
PreReq: policycoreutils >= %{POLICYCOREUTILSVER} libsemanage >= 1.6.17-1
Obsoletes: policy 

%description 
SELinux Base package

%files 
%{_mandir}/man8/*
%doc %{_usr}/share/doc/%{name}-%{version}
%dir %{_usr}/share/selinux
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux

%package devel
Summary: SELinux policy development
Group: System Environment/Base
Prereq: checkpolicy >= %{CHECKPOLICYVER} m4 policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: selinux-policy = %{version}-%{release}

%description devel
SELinux Policy development package

%files devel
%dir %{_usr}/share/selinux/devel
%dir %{_usr}/share/selinux/devel/include
%{_usr}/share/selinux/devel/include/*
%{_usr}/share/selinux/devel/Makefile
%{_usr}/share/selinux/devel/policygentool
%{_usr}/share/selinux/devel/example.*
%attr(755,root,root) %{_usr}/share/selinux/devel/policyhelp

%post devel
[ -x /usr/sbin/sepolgen-ifgen ] && /usr/sbin/sepolgen-ifgen  > /dev/null

%define setupCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 bare \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024  conf \
cp -f ${RPM_SOURCE_DIR}/modules-%1.conf  ./policy/modules.conf \
cp -f ${RPM_SOURCE_DIR}/booleans-%1.conf ./policy/booleans.conf \

%define moduleList() %([ -f %{_sourcedir}/modules-%{1}.conf ] && \
awk '$1 !~ "/^#/" && $2 == "=" && $3 == "module" { printf "-i %%s.pp ", $1 }' %{_sourcedir}/modules-%{1}.conf )

%define installCmds() \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 modules \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 install-appconfig \
#%{__cp} *.pp %{buildroot}/%{_usr}/share/selinux/%1/ \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/policy \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/modules/active \
%{__mkdir} -p %{buildroot}/%{_sysconfdir}/selinux/%1/contexts/files \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
touch %{buildroot}/%{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
make NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4  MLS_CATS=1024 MCS_CATS=1024 enableaudit \
make -W base.conf NAME=%1 TYPE=%2 DISTRO=%{distro} DIRECT_INITRC=%3 MONOLITHIC=%{monolithic} POLY=%4 MLS_CATS=1024 MCS_CATS=1024 base.pp \
install -m0644 base.pp %{buildroot}%{_usr}/share/selinux/%1/enableaudit.pp \
rm -rf %{buildroot}%{_sysconfdir}/selinux/%1/booleans \
touch %{buildroot}%{_sysconfdir}/selinux/%1/seusers \
touch %{buildroot}%{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
touch %{buildroot}%{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
install -m0644 ${RPM_SOURCE_DIR}/securetty_types-%1 %{buildroot}%{_sysconfdir}/selinux/%1/contexts/securetty_types \
install -m0644 ${RPM_SOURCE_DIR}/setrans-%1.conf %{buildroot}%{_sysconfdir}/selinux/%1/setrans.conf \
%nil

%define fileList() \
%defattr(-,root,root) \
%dir %{_usr}/share/selinux/%1 \
%{_usr}/share/selinux/%1/*.pp \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %{_sysconfdir}/selinux/%1/setrans.conf \
%ghost %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/modules \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.read.LOCK \
%verify(not mtime) %{_sysconfdir}/selinux/%1/modules/semanage.trans.LOCK \
%attr(700,root,root) %dir %{_sysconfdir}/selinux/%1/modules/active \
#%verify(not md5 size mtime) %attr(600,root,root) %config(noreplace) %{_sysconfdir}/selinux/%1/modules/active/seusers \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%ghost %{_sysconfdir}/selinux/%1/policy/policy.* \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/initrc_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/userhelper_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/homedir_template \
%ghost %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%config %{_sysconfdir}/selinux/%1/contexts/files/media \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%{_sysconfdir}/selinux/%1/contexts/users/root

%define saveFileContext() \
if [ -s /etc/selinux/config ]; then \
	. %{_sysconfdir}/selinux/config; \
	FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
	if [ "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT} ]; then \
		cp -f ${FILE_CONTEXT} ${FILE_CONTEXT}.pre; \
	fi \
fi

%define rebuildpolicy() \
( cd /usr/share/selinux/%1; \
semodule -b base.pp %{expand:%%moduleList %1} -s %1; \
);\
rm -f %{_sysconfdir}/selinux/%1/policy/policy.*.rpmnew

%define relabel() \
. %{_sysconfdir}/selinux/config; \
FILE_CONTEXT=%{_sysconfdir}/selinux/%1/contexts/files/file_contexts; \
selinuxenabled; \
if [ $? == 0  -a "${SELINUXTYPE}" == %1 -a -f ${FILE_CONTEXT}.pre ]; then \
	fixfiles -C ${FILE_CONTEXT}.pre restore; \
	rm -f ${FILE_CONTEXT}.pre; \
fi; 

%description
SELinux Reference Policy - modular.
Based off of reference policy: Checked out revision 2261.

%prep 
%setup -q -n serefpolicy-%{version}
%patch -p1

%install
# Build targeted policy
%{__rm} -fR %{buildroot}
mkdir -p %{buildroot}%{_mandir}/man8/
install -m 644 man/man8/*.8 %{buildroot}%{_mandir}/man8/
mkdir -p %{buildroot}%{_sysconfdir}/selinux
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{_sysconfdir}/selinux/config
touch %{buildroot}%{_sysconfdir}/sysconfig/selinux

# Always create policy module package directories
mkdir -p %{buildroot}%{_usr}/share/selinux/{targeted,strict,mls}/

# Install devel
make clean
%if %{BUILD_TARGETED}
# Build targeted policy
# Commented out because only targeted ref policy currently builds
%setupCmds targeted targeted-mcs y y
%installCmds targeted targeted-mcs y y
%endif

%if %{BUILD_STRICT}
# Build strict policy
# Commented out because only targeted ref policy currently builds
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} POLY=n MLS_CATS=1024 MCS_CATS=1024 bare 
make NAME=strict TYPE=strict-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} POLY=n MLS_CATS=1024 MCS_CATS=1024 conf
cp -f ${RPM_SOURCE_DIR}/modules-strict.conf  ./policy/modules.conf 
%installCmds strict strict-mcs y n
%endif

%if %{BUILD_MLS}
# Build mls policy
%setupCmds mls strict-mls y y
%installCmds mls strict-mls y y 
%endif

make NAME=targeted TYPE=targeted-mcs DISTRO=%{distro} DIRECT_INITRC=y MONOLITHIC=%{monolithic} DESTDIR=%{buildroot} PKGNAME=%{name}-%{version} POLY=y MLS_CATS=1024 MCS_CATS=1024 install-headers install-docs
mkdir %{buildroot}%{_usr}/share/selinux/devel/
mv %{buildroot}%{_usr}/share/selinux/targeted/include %{buildroot}%{_usr}/share/selinux/devel/include
install -m 755 ${RPM_SOURCE_DIR}/policygentool %{buildroot}%{_usr}/share/selinux/devel/
install -m 644 ${RPM_SOURCE_DIR}/Makefile.devel %{buildroot}%{_usr}/share/selinux/devel/Makefile
install -m 644 doc/example.* %{buildroot}%{_usr}/share/selinux/devel/
echo  "htmlview file:///usr/share/doc/selinux-policy-%{version}/html/index.html"> %{buildroot}%{_usr}/share/selinux/devel/policyhelp
chmod +x %{buildroot}%{_usr}/share/selinux/devel/policyhelp


%clean
%{__rm} -fR %{buildroot}

%post
if [ ! -s /etc/selinux/config ]; then
	#
	#	New install so we will default to targeted policy
	#
	echo "
# This file controls the state of SELinux on the system.
# SELINUX= can take one of these three values:
#	enforcing - SELinux security policy is enforced.
#	permissive - SELinux prints warnings instead of enforcing.
#	disabled - No SELinux policy is loaded.
SELINUX=enforcing
# SELINUXTYPE= can take one of these two values:
#	targeted - Only targeted network daemons are protected.
#	strict - Full SELinux protection.
#	mls - Multi Level Security protection.
SELINUXTYPE=targeted 
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 

" > /etc/selinux/config

	ln -sf ../selinux/config /etc/sysconfig/selinux 
	restorecon /etc/selinux/config 2> /dev/null
else
	. /etc/selinux/config
	# if first time update booleans.local needs to be copied to sandbox
	[ -f /etc/selinux/${SELINUXTYPE}/booleans.local ] && mv /etc/selinux/${SELINUXTYPE}/booleans.local /etc/selinux/targeted/modules/active/
	[ -f /etc/selinux/${SELINUXTYPE}/seusers ] && cp -f /etc/selinux/${SELINUXTYPE}/seusers /etc/selinux/${SELINUXTYPE}/modules/active/seusers
	grep -q "^SETLOCALDEFS" /etc/selinux/config || echo -n "
# SETLOCALDEFS= Check local definition changes
SETLOCALDEFS=0 
">> /etc/selinux/config
fi

%postun
if [ $1 = 0 ]; then
	setenforce 0 2> /dev/null
	if [ ! -s /etc/selinux/config ]; then
		echo "SELINUX=disabled" > /etc/selinux/config
	else
		sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
	fi
fi

%if %{BUILD_TARGETED}
%package targeted
Summary: SELinux targeted base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-targeted-sources
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}

%description targeted
SELinux Reference policy targeted base module.

%pre targeted
%saveFileContext targeted

%post targeted
%rebuildpolicy targeted
%relabel targeted

%triggerpostun targeted -- selinux-policy-targeted <= 2.0.7
%rebuildpolicy targeted

%files targeted
%fileList targeted

%endif

%if %{BUILD_MLS}
%package mls 
Summary: SELinux mls base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-mls-sources
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER}
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}

%description mls 
SELinux Reference policy mls base module.

%pre mls 
%saveFileContext mls

%post mls 
%rebuildpolicy mls
%relabel mls

%files mls
%fileList mls

%endif

%if %{BUILD_STRICT}

%package strict 
Summary: SELinux strict base policy
Group: System Environment/Base
Provides: selinux-policy-base
Obsoletes: selinux-policy-strict-sources
Prereq: policycoreutils >= %{POLICYCOREUTILSVER}
Prereq: coreutils
Prereq: selinux-policy = %{version}-%{release}
Requires: policycoreutils-newrole >= %{POLICYCOREUTILSVER}

%description strict 
SELinux Reference policy strict base module.

%pre strict 
%saveFileContext strict

%post strict 
%rebuildpolicy strict
%relabel strict

%triggerpostun strict -- selinux-policy-strict <= 2.2.35-2
cd /usr/share/selinux/strict
x=`ls *.pp | grep -v -e base.pp -e enableaudit.pp | awk '{ print "-i " $1 }'`
semodule -b base.pp -r bootloader -r clock -r dpkg -r fstools -r hotplug -r init -r libraries -r locallogin -r logging -r lvm -r miscfiles -r modutils -r mount -r mta -r netutils -r selinuxutil -r storage -r sysnetwork -r udev -r userdomain -r vpnc -r xend $x -s strict

%triggerpostun strict -- strict <= 2.0.7
%rebuildpolicy strict 

%files strict
%fileList strict

%endif

%changelog
* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-11
- Allow iptbales to read etc_runtime_t

* Thu Apr 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-10
- MLS Fixes

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-8
- Fix path of /etc/lvm/cache directory
- Fixes for alsactl and pppd_t
- Fixes for consolekit

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-5
- Allow insmod_t to mount kvmfs_t filesystems

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-4
- Rwho policy
- Fixes for consolekit

* Fri Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-3
- fixes for fusefs

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-2
- Fix samba_net to allow it to view samba_var_t

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.12-1
- Update to upstream

* Tue Apr 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-8
- Fix Sonypic backlight
- Allow snmp to look at squid_conf_t

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-7
- Fixes for pyzor, cyrus, consoletype on everything installs

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-6
- Fix hald_acl_t to be able to getattr/setattr on usb devices
- Dontaudit write to unconfined_pipes for load_policy

* Thu Apr 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-5
- Allow bluetooth to read inotifyfs

* Wed Apr 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-4
- Fixes for samba domain controller.
- Allow ConsoleKit to look at ttys

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-3
- Fix interface call

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-2
- Allow syslog-ng to read /var
- Allow locate to getattr on all filesystems
- nscd needs setcap

* Mon Mar 26 2007 Dan Walsh <dwalsh@redhat.com> 2.5.11-1
- Update to upstream

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-2
- Allow samba to run groupadd

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.10-1
- Update to upstream

* Thu Mar 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-6
- Allow mdadm to access generic scsi devices

* Wed Mar 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-5
- Fix labeling on udev.tbl dirs

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-4
- Fixes for logwatch

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-3
- Add fusermount and mount_ntfs policy

* Tue Mar 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.9-2
- Update to upstream
- Allow saslauthd to use kerberos keytabs

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-8
- Fixes for samba_var_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-7
- Allow networkmanager to setpgid
- Fixes for hal_acl_t

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-6
- Remove disable_trans booleans
- hald_acl_t needs to talk to nscd

* Thu Mar 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-5
- Fix prelink to be able to manage usr dirs.

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-4
- Allow insmod to launch init scripts

* Tue Mar 13 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-3
- Remove setsebool policy

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-2
- Fix handling of unlabled_t packets

* Thu Mar 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.8-1
- More of my patches from upstream

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.7-1
- Update to latest from upstream
- Add fail2ban policy

* Wed Feb 28 2007 Dan Walsh <dwalsh@redhat.com> 2.5.6-1
- Update to remove security_t:filesystem getattr problems

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-2
- Policy for consolekit

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.5.5-1
- Update to latest from upstream

* Wed Feb 21 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-2
- Revert Nemiver change
- Set sudo as a corecmd so prelink will work,  remove sudoedit mapping, since this will not work, it does not transition.
- Allow samba to execute useradd

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.5.4-1
- Upgrade to the latest from upstream

* Thu Feb 15 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-3
- Add sepolgen support
- Add bugzilla policy

* Wed Feb 14 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-2
- Fix file context for nemiver

* Sun Feb 11 2007 Dan Walsh <dwalsh@redhat.com> 2.5.3-1
- Remove include sym link

* Mon Feb 5 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-6
- Allow mozilla, evolution and thunderbird to read dev_random.
Resolves: #227002
- Allow spamd to connect to smtp port
Resolves: #227184
- Fixes to make ypxfr work
Resolves: #227237

* Sun Feb 4 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-5
- Fix ssh_agent to be marked as an executable
- Allow Hal to rw sound device 

* Thu Feb 1 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-4
- Fix spamassisin so crond can update spam files
- Fixes to allow kpasswd to work
- Fixes for bluetooth

* Fri Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-3
- Remove some targeted diffs in file context file

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-2
- Fix squid cachemgr labeling

* Thu Jan 25 2007 Dan Walsh <dwalsh@redhat.com> 2.5.2-1
- Add ability to generate webadm_t policy
- Lots of new interfaces for httpd
- Allow sshd to login as unconfined_t

* Mon Jan 22 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-5
- Continue fixing, additional user domains

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-4
- Begin adding user confinement to targeted policy 

* Wed Jan 10 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-2
- Fixes for prelink, ktalkd, netlabel

* Mon Jan 8 2007 Dan Walsh <dwalsh@redhat.com> 2.5.1-1
- Allow prelink when run from rpm to create tmp files
Resolves: #221865
- Remove file_context for exportfs
Resolves: #221181
- Allow spamassassin to create ~/.spamassissin
Resolves: #203290
- Allow ssh access to the krb tickets
- Allow sshd to change passwd
- Stop newrole -l from working on non securetty
Resolves: #200110
- Fixes to run prelink in MLS machine
Resolves: #221233
- Allow spamassassin to read var_lib_t dir
Resolves: #219234

* Fri Dec 29 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-20
- fix mplayer to work under strict policy
- Allow iptables to use nscd
Resolves: #220794

* Thu Dec 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-19
- Add gconf policy and make it work with strict

* Sat Dec 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-18
- Many fixes for strict policy and by extension mls.

* Fri Dec 22 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-17
- Fix to allow ftp to bind to ports > 1024
Resolves: #219349

* Tue Dec 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-16
- Allow semanage to exec it self.  Label genhomedircon as semanage_exec_t
Resolves: #219421
- Allow sysadm_lpr_t to manage other print spool jobs
Resolves: #220080

* Mon Dec 18 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-15
- allow automount to setgid
Resolves: #219999

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-14
- Allow cron to polyinstatiate 
- Fix creation of boot flags
Resolves: #207433

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-13
- Fixes for irqbalance
Resolves: #219606

* Thu Dec 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-12
- Fix vixie-cron to work on mls
Resolves: #207433

* Wed Dec 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-11
Resolves: #218978

* Tue Dec 12 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-10
- Allow initrc to create files in /var directories
Resolves: #219227

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-9
- More fixes for MLS
Resolves: #181566

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-8
- More Fixes polyinstatiation
Resolves: #216184

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-7
- More Fixes polyinstatiation
- Fix handling of keyrings
Resolves: #216184

* Mon Dec 4 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-6
- Fix polyinstatiation
- Fix pcscd handling of terminal
Resolves: #218149
Resolves: #218350

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-5
- More fixes for quota
Resolves: #212957

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-4
- ncsd needs to use avahi sockets
Resolves: #217640
Resolves: #218014

* Thu Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-3
- Allow login programs to polyinstatiate homedirs
Resolves: #216184
- Allow quotacheck to create database files
Resolves: #212957

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 2.4.6-1
- Dontaudit appending hal_var_lib files 
Resolves: #217452
Resolves: #217571
Resolves: #217611
Resolves: #217640
Resolves: #217725

* Mon Nov 21 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-4
- Fix context for helix players file_context #216942

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-3
- Fix load_policy to be able to mls_write_down so it can talk to the terminal

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-2
- Fixes for hwclock, clamav, ftp

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.5-1
- Move to upstream version which accepted my patches

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Fixes for nvidia driver

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-2
- Allow semanage to signal mcstrans

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 2.4.4-1
- Update to upstream

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-13
- Allow modstorage to edit /etc/fstab file

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-12
- Fix for qemu, /dev/

* Mon Nov 13 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-11
- Fix path to realplayer.bin

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-10
- Allow xen to connect to xen port

* Fri Nov 10 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-9
- Allow cups to search samba_etc_t directory
- Allow xend_t to list auto_mountpoints

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-8
- Allow xen to search automount

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-7
- Fix spec of jre files 

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-6
- Fix unconfined access to shadow file

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-5
- Allow xend to create files in xen_image_t directories

* Wed Nov 8 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-4
- Fixes for /var/lib/hal

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-3
- Remove ability for sysadm_t to look at audit.log

* Tue Nov 7 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-2
- Fix rpc_port_types
- Add aide policy for mls

* Mon Nov 6 2006 Dan Walsh <dwalsh@redhat.com> 2.4.3-1
- Merge with upstream

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-8
- Lots of fixes for ricci

* Fri Nov 3 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-7
- Allow xen to read/write fixed devices with a boolean
- Allow apache to search /var/log

* Thu Nov 2 2006 James Antill <james.antill@redhat.com> 2.4.2-6
- Fix policygentool specfile problem.
- Allow apache to send signals to it's logging helpers.
- Resolves: rhbz#212731

* Wed Nov 1 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-5
- Add perms for swat

* Tue Oct 31 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-4
- Add perms for swat

* Mon Oct 30 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-3
- Allow daemons to dump core files to /

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-2
- Fixes for ricci

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.2-1
- Allow mount.nfs to work

* Fri Oct 27 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-5
- Allow ricci-modstorage to look at lvm_etc_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-4
- Fixes for ricci using saslauthd

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-3
- Allow mountpoint on home_dir_t and home_t

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4.1-2
- Update xen to read nfs files

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-4
- Allow noxattrfs to associate with other noxattrfs 

* Mon Oct 23 2006 Dan Walsh <dwalsh@redhat.com> 2.4-3
- Allow hal to use power_device_t

* Fri Oct 20 2006 Dan Walsh <dwalsh@redhat.com> 2.4-2
- Allow procemail to look at autofs_t
- Allow xen_image_t to work as a fixed device

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.4-1
- Refupdate from upstream

* Thu Oct 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-4
- Add lots of fixes for mls cups

* Wed Oct 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-3
- Lots of fixes for ricci


* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-2
- Fix number of cats

* Mon Oct 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.19-1
- Update to upstream

* Thu Oct 12 2006 James Antill <jantill@redhat.com> 2.3.18-10
- More iSCSI changes for #209854

* Tue Oct 10 2006 James Antill <jantill@redhat.com> 2.3.18-9
- Test ISCSI fixes for #209854

* Sun Oct 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-8
- allow semodule to rmdir selinux_config_t dir

* Fri Oct 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-7
- Fix boot_runtime_t problem on ppc.  Should not be creating these files.

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-6
- Fix context mounts on reboot
- Fix ccs creation of directory in /var/log

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-5
- Update for tallylog

* Thu Oct 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-4
- Allow xend to rewrite dhcp conf files
- Allow mgetty sys_admin capability

* Wed Oct 4 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-3
- Make xentapctrl work

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-2
- Don't transition unconfined_t to bootloader_t
- Fix label in /dev/xen/blktap

* Tue Oct 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.18-1
- Patch for labeled networking

* Mon Oct 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-2
- Fix crond handling for mls

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.17-1
- Update to upstream

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-9
- Remove bluetooth-helper transition
- Add selinux_validate for semanage
- Require new version of libsemanage

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-8
- Fix prelink

* Fri Sep 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-7
- Fix rhgb

* Thu Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-6
- Fix setrans handling on MLS and useradd

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-5
- Support for fuse
- fix vigr

* Wed Sep 27 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-4
- Fix dovecot, amanda
- Fix mls

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-2
- Allow java execheap for itanium

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.16-1
- Update with upstream

* Mon Sep 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-2
- mls fixes 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.15-1
- Update from upstream 

* Fri Sep 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-8
- More fixes for mls
- Revert change on automount transition to mount

* Wed Sep 20 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-7
- Fix cron jobs to run under the correct context

* Tue Sep 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-6
- Fixes to make pppd work

* Mon Sep 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-4
- Multiple policy fixes
- Change max categories to 1023

* Sat Sep 16 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-3
- Fix transition on mcstransd

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-2
- Add /dev/em8300 defs

* Fri Sep 15 2006 Dan Walsh <dwalsh@redhat.com> 2.3.14-1
- Upgrade to upstream

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-6
- Fix ppp connections from network manager

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-5
- Add tty access to all domains boolean
- Fix gnome-pty-helper context for ia64

* Mon Sep 11 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-4
- Fixed typealias of firstboot_rw_t

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-3
- Fix location of xel log files
- Fix handling of sysadm_r -> rpm_exec_t 

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-2
- Fixes for autofs, lp

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 2.3.13-1
- Update from upstream

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-2
- Fixup for test6

* Tue Sep 5 2006 Dan Walsh <dwalsh@redhat.com> 2.3.12-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.11-1
- Update to upstream

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-7
- Fix suspend to disk problems

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-6
- Lots of fixes for restarting daemons at the console.

* Wed Aug 30 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-3
- Fix audit line
- Fix requires line

* Tue Aug 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.10-1
- Upgrade to upstream

* Mon Aug 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-6
- Fix install problems

* Fri Aug 25 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-5
- Allow setroubleshoot to getattr on all dirs to gather RPM data

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-4
- Set /usr/lib/ia32el/ia32x_loader to unconfined_execmem_exec_t for ia32 platform
- Fix spec for /dev/adsp

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-3
- Fix xen tty devices

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-2
- Fixes for setroubleshoot

* Wed Aug 23 2006 Dan Walsh <dwalsh@redhat.com> 2.3.9-1
- Update to upstream

* Sun Aug 20 2006 Dan Walsh <dwalsh@redhat.com> 2.3.8-2
- Fixes for stunnel and postgresql
- Update from upstream

* Sat Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.7-1
- Update from upstream
- More java fixes

* Fri Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-4
- Change allow_execstack to default to on, for RHEL5 Beta.  
  This is required because of a Java compiler problem.
  Hope to turn off for next beta

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-3
- Misc fixes

* Wed Aug 9 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-2
- More fixes for strict policy

* Tue Aug 8 2006 Dan Walsh <dwalsh@redhat.com> 2.3.6-1
- Quiet down anaconda audit messages

* Mon Aug 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.5-1
- Fix setroubleshootd

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.4-1
- Update to the latest from upstream

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-20
- More fixes for xen

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-19
- Fix anaconda transitions

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-18
- yet more xen rules
 
* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-17
- more xen rules

* Mon Jul 31 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-16
- Fixes for Samba

* Sat Jul 29 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-15
- Fixes for xen

* Fri Jul 28 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-14
- Allow setroubleshootd to send mail

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-13
- Add nagios policy

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-12
-  fixes for setroubleshoot

* Wed Jul 26 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-11
- Added Paul Howarth patch to only load policy packages shipped 
  with this package
- Allow pidof from initrc to ptrace higher level domains
- Allow firstboot to communicate with hal via dbus

* Mon Jul 24 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-10
- Add policy for /var/run/ldapi

* Sat Jul 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-9
- Fix setroubleshoot policy

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-8
- Fixes for mls use of ssh
- named  has a new conf file

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-7
- Fixes to make setroubleshoot work

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-6
- Cups needs to be able to read domain state off of printer client

* Wed Jul 19 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-5
- add boolean to allow zebra to write config files

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-4
- setroubleshootd fixes

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-3
- Allow prelink to read bin_t symlink
- allow xfs to read random devices
- Change gfs to support xattr


* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-2
- Remove spamassassin_can_network boolean

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.3-1
- Update to upstream
- Fix lpr domain for mls

* Fri Jul 14 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-4
- Add setroubleshoot policy

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-3
- Turn off auditallow on setting booleans

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-2
- Multiple fixes

* Fri Jul 7 2006 Dan Walsh <dwalsh@redhat.com> 2.3.2-1
- Update to upstream

* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 2.3.1-1
- Update to upstream
- Add new class for kernel key ring

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.49-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.48-1
- Update to upstream

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-5
- Break out selinux-devel package

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-4
- Add ibmasmfs

* Thu Jun 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-3
- Fix policygentool gen_requires

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.47-1
- Update from Upstream

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-2
- Fix spec of realplay

* Tue Jun 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.46-1
- Update to upstream

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-3
- Fix semanage

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-2
- Allow useradd to create_home_dir in MLS environment

* Thu Jun 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.45-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.44-1
- Update from upstream

* Tue Jun 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-4
- Add oprofilefs

* Sun May 28 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-3
- Fix for hplip and Picasus

* Sat May 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-2
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.43-1
- Update to upstream

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-4
- fixes for spamd

* Wed May 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-3
- fixes for java, openldap and webalizer

* Mon May 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-2
- Xen fixes

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.42-1
- Upgrade to upstream

* Thu May 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.41-1
- allow hal to read boot_t files
- Upgrade to upstream

* Wed May 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-2
- allow hal to read boot_t files

* Tue May 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.40-1
- Update from upstream

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-2
- Fixes for amavis

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.39-1
- Update from upstream

* Fri May 12 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-6
- Allow auditctl to search all directories

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-5
- Add acquire service for mono.

* Thu May 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-4
- Turn off allow_execmem boolean
- Allow ftp dac_override when allowed to access users homedirs

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-3
- Clean up spec file
- Transition from unconfined_t to prelink_t

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-2
- Allow execution of cvs command

* Fri May 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.38-1
- Update to upstream

* Wed May 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.37-1
- Update to upstream

* Mon May 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-2
- Fix libjvm spec

* Tue Apr 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.36-1
- Update to upstream

* Tue Apr 25 2006 James Antill <jantill@redhat.com> 2.2.35-2
- Add xm policy
- Fix policygentool

* Mon Apr 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.35-1
- Update to upstream
- Fix postun to only disable selinux on full removal of the packages

* Fri Apr 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-3
- Allow mono to chat with unconfined

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-2
- Allow procmail to sendmail
- Allow nfs to share dosfs

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.34-1
- Update to latest from upstream
- Allow selinux-policy to be removed and kernel not to crash

* Tue Apr 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.33-1
- Update to latest from upstream
- Add James Antill patch for xen
- Many fixes for pegasus

* Sat Apr 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-2
- Add unconfined_mount_t
- Allow privoxy to connect to httpd_cache
- fix cups labeleing on /var/cache/cups

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.32-1
- Update to latest from upstream

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.31-1
- Update to latest from upstream
- Allow mono and unconfined to talk to initrc_t dbus objects

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-2
- Change libraries.fc to stop shlib_t form overriding texrel_shlib_t

* Tue Apr 11 2006 Dan Walsh <dwalsh@redhat.com> 2.2.30-1
- Fix samba creating dirs in homedir
- Fix NFS so its booleans would work

* Mon Apr 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-6
- Allow secadm_t ability to relabel all files
- Allow ftp to search xferlog_t directories
- Allow mysql to communicate with ldap
- Allow rsync to bind to rsync_port_t

* Mon Apr 10 2006 Russell Coker <rcoker@redhat.com> 2.2.29-5
- Fixed mailman with Postfix #183928
- Allowed semanage to create file_context files.
- Allowed amanda_t to access inetd_t TCP sockets and allowed amanda_recover_t
  to bind to reserved ports.  #149030
- Don't allow devpts_t to be associated with tmp_t.
- Allow hald_t to stat all mountpoints.
- Added boolean samba_share_nfs to allow smbd_t full access to NFS mounts.
  #169947
- Make mount run in mount_t domain from unconfined_t to prevent mislabeling of
  /etc/mtab.
- Changed the file_contexts to not have a regex before the first ^/[a-z]/
  whenever possible, makes restorecon slightly faster.
- Correct the label of /etc/named.caching-nameserver.conf
- Now label /usr/src/kernels/.+/lib(/.*)? as usr_t instead of
  /usr/src(/.*)?/lib(/.*)? - I don't think we need anything else under /usr/src
  hit by this.
- Granted xen access to /boot, allowed mounting on xend_var_lib_t, and allowed
  xenstored_t rw access to the xen device node.

* Tue Apr 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-4
- More textrel_shlib_t file path fixes
- Add ada support

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-3
- Get auditctl working in MLS policy

* Mon Apr 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-2
- Add mono dbus support
- Lots of file_context fixes for textrel_shlib_t in FC5
- Turn off execmem auditallow since they are filling log files

* Fri Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.29-1
- Update to upstream

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-3
- Allow automount and dbus to read cert files

* Thu Mar 30 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-2
- Fix ftp policy
- Fix secadm running of auditctl

* Mon Mar 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.28-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.27-1
- Update to upstream

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-3
- Fix policyhelp

* Wed Mar 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.25-2
- Fix pam_console handling of usb_device
- dontaudit logwatch reading /mnt dir

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 2.2.24-1
- Update to upstream

* Wed Mar 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-19
- Get transition rules to create policy.20 at SystemHigh

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-18
- Allow secadmin to shutdown system
- Allow sendmail to exec newalias

* Tue Mar 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-17
- MLS Fixes
	dmidecode needs mls_file_read_up
- add ypxfr_t
- run init needs access to nscd
- udev needs setuid
- another xen log file
- Dontaudit mount getattr proc_kcore_t

* Tue Mar 14 2006 Karsten Hopp <karsten@redhat.de> 2.2.23-16
- fix buildroot usage (#185391)

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-15
- Get rid of mount/fsdisk scan of /dev messages
- Additional fixes for suspend/resume

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-14
- Fake make to rebuild enableaudit.pp

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-13
- Get xen networking running.

* Thu Mar 9 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-12
- Fixes for Xen
- enableaudit should not be the same as base.pp
- Allow ps to work for all process

* Thu Mar  9 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-11
- more xen policy fixups

* Wed Mar  8 2006 Jeremy Katz <katzj@redhat.com> - 2.2.23-10
- more xen fixage (#184393)

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-9
- Fix blkid specification
- Allow postfix to execute mailman_que

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-8
- Blkid changes
- Allow udev access to usb_device_t
- Fix post script to create targeted policy config file

* Wed Mar 8 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-7
- Allow lvm tools to create drevice dir

* Tue Mar 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-5
- Add Xen support

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-4
- Fixes for cups
- Make cryptosetup work with hal

* Sun Mar 5 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-3
- Load Policy needs translock

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-2
- Fix cups html interface

* Sat Mar 4 2006 Dan Walsh <dwalsh@redhat.com> 2.2.23-1
- Add hal changes suggested by Jeremy
- add policyhelp to point at policy html pages

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-2
- Additional fixes for nvidia and cups

* Mon Feb 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.22-1
- Update to upstream
- Merged my latest fixes
- Fix cups policy to handle unix domain sockets

* Sat Feb 25 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-9
- NSCD socket is in nscd_var_run_t needs to be able to search dir

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-8
- Fixes Apache interface file

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-7
- Fixes for new version of cups

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-6
- Turn off polyinstatiate util after FC5

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-5
- Fix problem with privoxy talking to Tor

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-4
- Turn on polyinstatiation

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-3
- Don't transition from unconfined_t to fsadm_t

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-2
- Fix policy update model.

* Thu Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.21-1
- Update to upstream

* Wed Feb 22 2006 Dan Walsh <dwalsh@redhat.com> 2.2.20-1
- Fix load_policy to work on MLS
- Fix cron_rw_system_pipes for postfix_postdrop_t
- Allow audotmount to run showmount

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-2
- Fix swapon
- allow httpd_sys_script_t to be entered via a shell
- Allow httpd_sys_script_t to read eventpolfs

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.19-1
- Update from upstream

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-2
- allow cron to read apache files

* Tue Feb 21 2006 Dan Walsh <dwalsh@redhat.com> 2.2.18-1
- Fix vpnc policy to work from NetworkManager

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 2.2.17-2
- Update to upstream
- Fix semoudle polcy

* Thu Feb 16 2006 Dan Walsh <dwalsh@redhat.com> 2.2.16-1
- Update to upstream 
- fix sysconfig/selinux link

* Wed Feb 15 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-4
- Add router port for zebra
- Add imaze port for spamd
- Fixes for amanda and java

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-3
- Fix bluetooth handling of usb devices
- Fix spamd reading of ~/
- fix nvidia spec

* Tue Feb 14 2006 Dan Walsh <dwalsh@redhat.com> 2.2.15-1
- Update to upsteam

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-2
- Add users_extra files

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.14-1
- Update to upstream

* Fri Feb 10 2006 Dan Walsh <dwalsh@redhat.com> 2.2.13-1
- Add semodule policy

* Tue Feb 7 2006 Dan Walsh <dwalsh@redhat.com> 2.2.12-1
- Update from upstream


* Mon Feb 6 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-2
- Fix for spamd to use razor port

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 2.2.11-1
- Fixes for mcs
- Turn on mount and fsadm for unconfined_t

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.10-1
- Fixes for the -devel package

* Wed Feb 1 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-2
- Fix for spamd to use ldap

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.9-1
- Update to upstream

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 2.2.8-2
- Update to upstream
- Fix rhgb, and other Xorg startups

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.7-1
- Update to upstream

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-3
- Separate out role of secadm for mls

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-2
- Add inotifyfs handling

* Thu Jan 26 2006 Dan Walsh <dwalsh@redhat.com> 2.2.6-1
- Update to upstream
- Put back in changes for pup/zen

* Tue Jan 24 2006 Dan Walsh <dwalsh@redhat.com> 2.2.5-1
- Many changes for MLS 
- Turn on strict policy

* Mon Jan 23 2006 Dan Walsh <dwalsh@redhat.com> 2.2.4-1
- Update to upstream

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.3-1
- Update to upstream
- Fixes for booting and logging in on MLS machine

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.2-1
- Update to upstream
- Turn off execheap execstack for unconfined users
- Add mono/wine policy to allow execheap and execstack for them
- Add execheap for Xdm policy

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 2.2.1-1
- Update to upstream
- Fixes to fetchmail,

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.13-1
- Update to upstream

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 2.1.12-3
- Fix for procmail/spamassasin
- Update to upstream
- Add rules to allow rpcd to work with unlabeled_networks.

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 2.1.11-1
- Update to upstream
- Fix ftp Man page

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 2.1.10-1
- Update to upstream

* Wed Jan 11 2006 Jeremy Katz <katzj@redhat.com> - 2.1.9-2
- fix pup transitions (#177262)
- fix xen disks (#177599)

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.9-1
- Update to upstream

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-3
- More Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-2
- Fixes for hal and readahead

* Mon Jan 9 2006 Dan Walsh <dwalsh@redhat.com> 2.1.8-1
- Update to upstream
- Apply 
* Fri Jan 7 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-4
- Add wine and fix hal problems

* Thu Jan 6 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-3
- Handle new location of hal scripts

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-2
- Allow su to read /etc/mtab

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 2.1.7-1
- Update to upstream

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-24
- Fix  "libsemanage.parse_module_headers: Data did not represent a module." problem

* Tue Jan 3 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-23
- Allow load_policy to read /etc/mtab

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-22
- Fix dovecot to allow dovecot_auth to look at /tmp

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 2.1.6-21
- Allow restorecon to read unlabeled_t directories in order to fix labeling.

* Fri Dec 30 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-20
- Add Logwatch policy

* Wed Dec 28 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-18
- Fix /dev/ub[a-z] file context

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-17
- Fix library specification
- Give kudzu execmem privs

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-16
- Fix hostname in targeted policy

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-15
- Fix passwd command on mls

* Wed Dec 21 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-14
- Lots of fixes to make mls policy work

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-13
- Add dri libs to textrel_shlib_t
- Add system_r role for java
- Add unconfined_exec_t for vncserver
- Allow slapd to use kerberos

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-11
- Add man pages

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-10
- Add enableaudit.pp

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-9
- Fix mls policy

* Fri Dec 16 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-8
- Update mls file from old version

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-5
- Add sids back in
- Rebuild with update checkpolicy

* Thu Dec 15 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-4
- Fixes to allow automount to use portmap
- Fixes to start kernel in s0-s15:c0.c255

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-3
- Add java unconfined/execmem policy 

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-2
- Add file context for /var/cvs
- Dontaudit webalizer search of homedir

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.6-1
- Update from upstream

* Tue Dec 13 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-2
- Clean up spec
- range_transition crond to SystemHigh

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.4-1
- Fixes for hal
- Update to upstream

* Mon Dec 12 2005 Dan Walsh <dwalsh@redhat.com> 2.1.3-1
- Turn back on execmem since we need it for java, firefox, ooffice
- Allow gpm to stream socket to itself

* Mon Dec 12 2005 Jeremy Katz <katzj@redhat.com> - 2.1.2-3
- fix requirements to be on the actual packages so that policy can get
  created properly at install time

* Sun Dec  10 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-2
- Allow unconfined_t to execmod texrel_shlib_t

* Sat Dec  9 2005 Dan Walsh <dwalsh@redhat.com> 2.1.2-1
- Update to upstream 
- Turn off allow_execmem and allow_execmod booleans
- Add tcpd and automount policies

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-3
- Add two new httpd booleans, turned off by default
	* httpd_can_network_relay
	* httpd_can_network_connect_db

* Fri Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-2
- Add ghost for policy.20

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.1-1
- Update to upstream
- Turn off boolean allow_execstack

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-3
- Change setrans-mls to use new libsetrans
- Add default_context rule for xdm

* Thu Dec  8 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-2.
- Change Requires to PreReg for requiring of policycoreutils on install

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.1.0-1.
- New upstream release

* Wed Dec  7 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-2.
Add xdm policy

* Tue Dec  6 2005 Dan Walsh <dwalsh@redhat.com> 2.0.11-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.9-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.8-1.
Update from upstream

* Fri Dec  2 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- Also trigger to rebuild policy for versions up to 2.0.7.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- No longer installing policy.20 file, anaconda handles the building of the app.

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Fixes for dovecot and saslauthd

* Wed Nov 23 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-4
- Cleanup pegasus and named 
- Fix spec file
- Fix up passwd changing applications

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.5-1
-Update to latest from upstream

* Tue Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.4-1
- Add rules for pegasus and avahi

* Mon Nov 21 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Start building MLS Policy

* Fri Nov 18 2005 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Turn on bash

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Initial version
