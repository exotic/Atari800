#
# spec file for package atari800 (Version 1.3.3)
#
# Copyright (c) 2004 SUSE LINUX Products GmbH, Nuernberg, Germany.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Please submit bugfixes or comments via http://www.suse.de/feedback/
#

# norootforbuild

BuildRequires: SDL-devel perl xorg-x11-devel
Name:         atari800
License:      GPL
Group:        System/Emulators/Other
Summary:      Atari800/XL/XE/5200 emulator
Autoreqprov:  on
Requires:     netpbm
Version:      1.3.6
Release:      0
URL:          http://atari800.atari.org/
Source0:      %{name}-%{version}.tar.bz2
Source1:      atari800.cfg
Source2:      README.SuSE
Source3:      atari800-ei
Patch0:       atari800-parser.patch
Patch1:       atari800-makefile.patch
Patch2:       atari800-decl.patch
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%define targets  x11 sdl ncurses
%define default_target sdl

%description
This is free and portable Atari800/XL/XE/5200 emulator, original
written by David Firth and now developed by many people on the Net.



Authors:
--------
    Ron Fries
    Alex Hornby <alex@zetnet.co.uk>
    Dave Bennett <bennett@halcyon.com>
    Chris Lam <lamcw@sun.aston.ac.uk>
    Ivo van Poorten <ipoorten@cs.vu.nl>
    Stephen Firth <stephen@signus.demon.co.uk>
    Rob Funk <rfunk@magnus.acs.ohio-state.edu>
    Preston F. Crow <preston.crow@dancer.dartmouth.edu>
    Cyrus Malek <Cyrus.Malek@amd.com>
    Chris F Chiesa <xetwnk@shell.portal.com>
    Neil Ship <nlshipp@dictator.uwaterloo.ca>
    Chris Palmer <crpalmer@solo.uwaterloo.ca>
    Maximum Entropy <entropy@zippy.bernstein.com>
    Ed Kaminski <ekamins@ibm.net>
    Nathan Monson <nathan@polaristel.net>
    Petr Stehlik <pstehlik@zln.cz>
    Karel Rous
    Radek Sterba <raster@infos.cz>
    Perry McFarlane <ce596@freenet.toronto.on.ca>
    Thomas Richter <thor@math.tu-berlin.de>
    Rich Lawrence <rich@kesmai.com>
    Petr Sumbera <xsumbe00@stud.fee.vutbr.cz>
    Robert Golias <golias@informatics.muni.cz>
    Robert W. Brewer <rbrewer@Op.Net>
    Michael Beck <beck@dresearch.de>
    Preston Crow
    Jason Duerstock <jason@sdi.cluephone.com>
    Kuba <kubad@zeus.polsl.gliwice.pl>
    Gerhard Janka <gerhard.janka@siemens.at>
    Jindroush <kubecj@asw.cz>
    Ken Sider
    Cameron Heide <cheide@home.com>
    Marek Zelem <marek@formax.elf.stuba.sk>
    Petr Mojzisek <mojzisek@bimbo.fjfi.cvut.cz>
    Krzysztof Nikiel <krzych00@priv7.onet.pl>
    Jari Karppinen <jakarppi@mail.student.oulu.fi>
    Marek Zelem <marek@fornax.elf.stuba.sk>
    ERU (Marcin Zukowski) <eru@ibb.waw.pl>
    Christian Groessler <cpg@aladdin.de>
    Piotr Fusik <P.Fusik@elka.pw.edu.pl>

%prep
%setup
%patch0
%patch1
%patch2
cp %{S:1} %{S:2} .

%build
cd src
%{?suse_update_config:%{suse_update_config -f}}
for target in %{targets}
do
	%{configure} --target=$target \
    --disable-slow \
%ifarch %ix86 x86_64 alpha
    --enable-riodevice \
%else
    --disable-riodevice \
%endif
    --enable-scancolor \
    --enable-crashmenu \
    --enable-break \
    --enable-hints \
    --enable-asm \
    --enable-meter \
    --enable-linuxjoy \
    --enable-sound \
    --enable-sersound \
    --enable-sndinter \
    --enable-sndclip \
    --enable-stereo \
    --enable-led \
	CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
    make 
	mv atari800 atari800-$target
	make clean
done
# build docs
make doc

%install
cd src
rm -rf $RPM_BUILD_ROOT
install -d -m 755 $RPM_BUILD_ROOT/usr/bin
install -d -m 755 $RPM_BUILD_ROOT/usr/share/man/man1
install -m 644 atari800.man $RPM_BUILD_ROOT/usr/share/man/man1/atari800.1
for target in %{targets}
do
	install -m 755 atari800-$target $RPM_BUILD_ROOT/usr/bin
    ln -sf atari800.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/atari800-$target.1.gz
done
ln -s atari800-%{default_target} $RPM_BUILD_ROOT/usr/bin/atari800
cd ..
#
# config
install -d $RPM_BUILD_ROOT/etc
install -m 644 atari800.cfg $RPM_BUILD_ROOT/etc
#
# for ROM images
install -d $RPM_BUILD_ROOT/usr/share/atari800
install -d $RPM_BUILD_ROOT/usr/lib/ei
install -m 644 %{S:3} $RPM_BUILD_ROOT/usr/lib/ei/atari800

%clean
rm -rf $RPM_BUILD_ROOT

%files -n atari800
%defattr(-, root, root)
%doc README.1ST COPYING README.SuSE
%doc DOC/[A-Z]* DOC/*.txt src/*.html
%doc %{_mandir}/man1/*
%config /etc/atari800.cfg
%{_bindir}/atari800*
/usr/lib/ei/atari800
%dir /usr/share/atari800

%changelog -n atari800
* Wed Oct 13 2005 - utx@penguin.cz
- Updated to version 1.3.6.
* Tue Aug 24 2004 - mcihar@suse.cz
- update to 1.3.3
* Mon Mar 08 2004 - ro@suse.de
- fix build on non-x86
* Fri Mar 05 2004 - mcihar@suse.cz
- updated to 1.3.2
* Sat Jan 10 2004 - adrian@suse.de
- build as user
* Fri Jun 13 2003 - mcihar@suse.cz
- add ei to neededforbuild
* Tue May 27 2003 - mcihar@suse.cz
- ei script doesn't have to be executable
* Wed Feb 26 2003 - mcihar@suse.cz
- include proper readme.html not just template readme.html.in
* Mon Feb 17 2003 - mcihar@suse.cz
- updated to 1.3.0:
  *  new HiFi sound (you may en/disable it in the UI)
  * new cycle-exact Antic emulation
  * "H:" emulation complete (including subfolders)
  * Paged memory implementation (fast XE bank-switching)
  * new configuration file name and location ($HOME/.atari800.cfg)
* Fri Jan 10 2003 - mcihar@suse.cz
- updated to 1.2.5:
  * UI - the SpaceBar in disk management switches between the RW and RO
  flags (this didn't work for a long time, now fixed). Please note that
  this RW/RO switch is just temporary and does not change the writeprotect
  flag of ATR images. Besides, it cannot override this flag so you
  actually can't mount a writeprotected ATR image read/write using this
  Space Bar toggle.
  * MultiJoy4 interface and Amiga/AtariST right mouse button supported
  * 13 new cartridge types supported
  * ANTIC mode E + GTIA mode 9 added (used in "Unconventional 2k", "Ass
  Kisiel")
  * 576 and 1088 kB RAM supported (selection available in the UI)
  * separate Antic access to extended memory for 130 XE and 320 Compy Shop
  * 256K and 512K XEGS carts
  * SDL version now
- cleans up after unsuccessful initialization
- supports "-nosound" and "-dsprate"
- continues to run even if sound initialization failed
  * command line options "-help" and "-v" ("-version") now work better in
  most supported ports.
- include more supported interfaces (ncurses x11 sdl)
- include more doc
- changed comnfigure options to support more features
* Fri Aug 09 2002 - mcihar@suse.cz
- updated to 1.2.3:
  * 16 kB RAM machines (Atari 400/600XL) emulated
  * LPTjoy support added to the SDL port
  * SDL port is generally much improved. To get list of SDL specific options
  start the SDL version of Atari800 with -help.
  * casette image loading accessible from UI
  * -palette option (for loading an alternate ACT color palette file) fixed.
  * channel 1 in stereo mode fixed
  * antic: NMIST bit 5 fixed (is always zero)
  * input: second button in 5200 joystick generates "Break key" IRQ
  (you can now jump in "Moon Patrol" - use Shift)
  * monitor: "DLIST" now accepts address as an argument
  * antic: Dirty update scheme that allows slower machines to run Atari800
  at full speed now! See DOC/HOWTO-DIRTYRECT for more information.
  * pokey: allow high-speed disk i/o (Alpha-Load works, thanks to Paul Irvine)
- moved ROM location from /usr/lib/atari800 to /usr/share/atari800
* Wed Jun 05 2002 - mcihar@suse.cz
- moved script for fetching ROMs from ei to this package
* Wed Jan 30 2002 - pmladek@suse.cz
- updated to version 1.2.2:
  * serious memory overflow bug fixed
  * joysticks in SDL port fixed and improved
  * SDL support for 32-bit display, screen width switching (LALT+g)
  * documentation updated (still can be much improved :)
  * util/ folder contains new sethdr and act2html utilities
  * configure process is non-interactive
- atari800 is SDL version now
- xatari800 is still X Window version
- fixed man pages
- added netpbm to Requires
* Tue Dec 11 2001 - pmladek@suse.cz
- updated to version 1.2.0:
  * support for additional cartridge types
  * mouse can emulate another devices (joystick, light gun, ...)
  * cassette recorder emulation (experimental)
  * and many other fixes and features
- removed obsolete config patch, configure options used instead it
- regenerated default config file /etc/atari800.cfg
- /etc/atari800.cfg marked as %%config
- fixed includes because of ia64
* Mon Nov 12 2001 - pmladek@suse.cz
- removed svga version of atari800
- the binary for x11 renamed to atari800
- created link xtari800 due to compactibility with older version
* Wed Aug 22 2001 - pmladek@suse.cz
- updated to version 1.0.7
- fixed default configuration in new configure script
  according previous configuration
- removed old fix to run on ia64 (it is not needed now)
* Mon May 21 2001 - pmladek@suse.cz
- fixed include files on ia64
- fixed to run on ia64:
  * uncomented #define ATARI800_64_BIT in src/config.h but
  only for ia64
* Thu Mar 22 2001 - pblaha@suse.cz
- fix URL
* Fri Oct 20 2000 - smid@suse.cz
- new version 1.0.6
* Thu Aug 31 2000 - smid@suse.cz
- initial version
