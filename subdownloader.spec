
%define name	subdownloader
%define version	2.0.13
%define rel	1

Summary:	Automatic subtitle downloader/uploader
Name:		%{name}
Version:	%{version}
Release:	%mkrel %{rel}
License:	GPLv2+
Group:		Video
URL:		http://subdownloader.net/
Source:		http://launchpad.net/subdownloader/trunk/%(A=%version; echo ${A%.*})/+download/subdownloader-%{version}.tar.gz
Patch0:		subdownloader-better-desktop-entry.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
BuildRequires:	imagemagick
BuildRequires:	python-qt4-devel
Requires:	python-qt4-gui
Requires:	python-sip

%description
Open Source tool written in Python for automatic download/upload
subtitles for videofiles (DIVX,MPEG,AVI,VOB,etc) and DVD's using fast
hashing.

%prep
%setup -q
%patch0 -p1

# prebuilt files
rm gui/*_ui.py

%build
%make -Cgui

%install
rm -rf %{buildroot}
install -d -m755 %{buildroot}%{_datadir}/%{name}
cp -a */ *.py %{buildroot}%{_datadir}/%{name}
chmod 0755 %{buildroot}%{_datadir}/%{name}/run.py

find %{buildroot}%{_datadir}/%{name} -name '*.pot' -delete
find %{buildroot}%{_datadir} -name '*.po' -delete
rm -rf %{buildroot}%{_datadir}/%{name}/gui/{*.ui,*.qrc,Makefile,images,Qt2Po.py}

mv %{buildroot}%{_datadir}/%{name}/locale %{buildroot}%{_datadir}/locale

install -d -m755 %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}/run.py %{buildroot}%{_bindir}/%{name}

install -d -m755 %{buildroot}%{_datadir}/applications
install -m644 %{name}.desktop %{buildroot}%{_datadir}/applications

for i in 64x64 48x48 32x32 16x16; do
	install -d -m755 %{buildroot}%{_iconsdir}/hicolor/$i
	convert gui/images/%{name}.png -resize $i %{buildroot}%{_iconsdir}/hicolor/$i/%{name}.png
done

install -d -m755 %{buildroot}%{_liconsdir} %{buildroot}%{_miconsdir}
ln %{buildroot}%{_iconsdir}/hicolor/48x48/%{name}.png %{buildroot}%{_liconsdir}
ln %{buildroot}%{_iconsdir}/hicolor/32x32/%{name}.png %{buildroot}%{_iconsdir}
ln %{buildroot}%{_iconsdir}/hicolor/16x16/%{name}.png %{buildroot}%{_miconsdir}

install -d -m755 %{buildroot}%{_mandir}/man1
install -m644 %{name}.1 %{buildroot}%{_mandir}/man1

%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_liconsdir}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/*/%{name}.png
%{_mandir}/man1/%{name}.1*



%changelog
* Sat Sep 04 2010 Anssi Hannula <anssi@mandriva.org> 2.0.13-1mdv2011.0
+ Revision: 575962
- new version

* Sat Apr 03 2010 Anssi Hannula <anssi@mandriva.org> 2.0.10-1mdv2011.0
+ Revision: 530856
- new version
  o fixes connection issues
- rediff better-desktop-entry.patch
- remove KDE entry from .desktop file as this is not a KDE application
- drop disable-updates.patch, fixed upstream

* Sun Sep 20 2009 Thierry Vignaud <tv@mandriva.org> 2.0.9.3-3mdv2010.0
+ Revision: 445267
- rebuild

* Mon Mar 09 2009 Anssi Hannula <anssi@mandriva.org> 2.0.9.3-2mdv2009.1
+ Revision: 353249
- requires python-sip

* Sun Mar 08 2009 Anssi Hannula <anssi@mandriva.org> 2.0.9.3-1mdv2009.1
+ Revision: 352734
- new version
- disable checking for updates (disable-updates.patch)

* Sun Nov 30 2008 Anssi Hannula <anssi@mandriva.org> 2.0.8.1-1mdv2009.1
+ Revision: 308457
- initial Mandriva release

