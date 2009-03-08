
%define name	subdownloader
%define version	2.0.9.3
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
Patch1:		subdownloader-disable-updates.patch
BuildRoot:	%{_tmppath}/%{name}-root
BuildArch:	noarch
BuildRequires:	imagemagick
BuildRequires:	python-qt4-devel
Requires:	python-qt4-gui

%description
Open Source tool written in Python for automatic download/upload
subtitles for videofiles (DIVX,MPEG,AVI,VOB,etc) and DVD's using fast
hashing.

%prep
%setup -q -n %name
%patch0 -p1
%patch1 -p1

# prebuilt files
rm gui/*_ui.py

%build
%make -Cgui

%install
rm -rf %{buildroot}
install -d -m755 %{buildroot}%{_datadir}/%{name}
cp -a */ __init__.py run.py %{buildroot}%{_datadir}/%{name}
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

