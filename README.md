
Helwan Welcome
This is a version of the Helwan Welcome program for the Helwan Linux distribution.
You can download a copy of the code, modify it, develop it, and communicate to offer your additions to the code.

About Helwan Welcome
Helwan Welcome is a versatile and user-friendly application designed for the Helwan Linux distribution to simplify system management tasks for users of all levels.

Key Features
Update Management
One-click button to update the system using pacman.

One-click button to update AUR packages using yay.

Kernel Installation
Easy installation of the Long-Term Support (LTS) kernel.

Easy installation of the Zen kernel.

Language Support
Change the program interface language among 25 supported languages.

Change the system language with a choice of 25 languages.

System Information
Displays free space available on the root hard disk.

Shows RAM size and processor type.

Quick Access
Direct links to the official documentation page.

Direct links to the Helwan Linux YouTube channel.

System Cleaner
Built-in cleaner for pacman to keep your system optimized and free from unnecessary files.

Directory Structure

```
atlas-welcome/
├── etc/
│   └── skel/
│       └── .config/
│           └── atlas-welcome-app/
│               └── settings.config
│
├── usr/
│   └── local/
│       ├── bin/
│       │   ├── atlas-welcome-app
│       │   └── atlas-welcome-app.desktop
│       │
│       └── share/
│           ├── applications/
│           │   └── atlas-welcome-app.desktop
│           │
│           └── atlas-welcome/
│               ├── locales/
│               │   └── ar_EG.UTF-8/
│               │       └── LC_MESSAGES/
│               │           ├── base.mo
│               │           └── base.po
│               │
│               ├── sources/
│               │   └── logo.png
│               │
│               ├── atlas.py
│               └── atlas-welcome-app.desktop
│
│           └── hicolor/
│               ├── 512x512/
│               │   └── helwan-welcom.png
│               │
│               └── scalable/
│                   └── helwan-welcom.svg
│
├── LICENSE
├── PKGBUILD
├── readme.install
└── README.md

## 📞 Contact

If you have any suggestions or additions, feel free to contact the development team of Helwan Linux.

## 📄 License

Helwan Welcome is open source and welcomes contributions.
