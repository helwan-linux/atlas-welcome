# Maintainer: Saeed Badrelden <saeedbadrelden2021@gmail.com>

pkgname=atlas-welcome
_pkgname=atlas-welcome
pkgver=1
pkgrel=01
pkgdesc="Welcome application for HelwanLinux"
arch=('any')
url="https://github.com/helwan-linux/atlas-welcome"
license=('GPL3')
conflicts=('hel-welcome-app')
makedepends=('git')
depends=('python-pyqt5' 'gettext' 'libwnck3' 'arandr')
provides=("${pkgname}")
install='readme.install'
options=(!strip !emptydirs)
source=(${_pkgname}::"git+${url}")
sha256sums=('SKIP')



package() {
  # إنشاء مجلد التطبيق في /usr/share
  install -Dm755 -d "$pkgdir/usr/share/atlas-welcome"
  
  # نسخ ملفات التطبيق من usr/share/atlas-welcome
  cp -r "${srcdir}/${_pkgname}/usr/share/atlas-welcome/"* "$pkgdir/usr/share/atlas-welcome/"

  # تثبيت السكربت التنفيذي في /usr/bin
  install -Dm755 "${srcdir}/${_pkgname}/usr/local/bin/atlas-welcome-app" "$pkgdir/usr/bin/atlas-welcome-app"

  # تثبيت ملف .desktop في /usr/share/applications
  install -Dm644 "${srcdir}/${_pkgname}/usr/share/applications/atlas-welcome-app.desktop" "$pkgdir/usr/share/applications/atlas-welcome-app.desktop"

  # تثبيت الأيقونات (512x512 و scalable)
  install -Dm644 "${srcdir}/${_pkgname}/usr/share/hicolor/512x512/helwan-welcom.png" "$pkgdir/usr/share/icons/hicolor/512x512/apps/helwan-welcom.png"
  install -Dm644 "${srcdir}/${_pkgname}/usr/share/hicolor/scalable/helwan-welcom.svg" "$pkgdir/usr/share/icons/hicolor/scalable/apps/helwan-welcom.svg"

  # تثبيت ملفات الترجمة (base.mo) لكل لغة
  find "${srcdir}/${_pkgname}/usr/share/atlas-welcome/locales" -type f -name "base.mo" -print0 | while IFS= read -r -d $'\0' file; do
    lang_dir=$(basename "$(dirname "$(dirname "$file")")")  # اسم اللغة من مجلد locales/<lang>/LC_MESSAGES/
    install -Dm644 "$file" "$pkgdir/usr/share/locale/$lang_dir/LC_MESSAGES/base.mo"
  done

  # تثبيت ملف الإعدادات في /etc/skel
  install -Dm644 "${srcdir}/${_pkgname}/etc/skel/.config/atlas-welcome-app/settings.conf" "$pkgdir/etc/skel/.config/atlas-welcome-app/settings.conf"

  # تثبيت ملف الرخصة
  install -dm755 "$pkgdir/usr/share/licenses/${pkgname}"
  install -Dm644 "${srcdir}/${_pkgname}/LICENSE" "$pkgdir/usr/share/licenses/${pkgname}/LICENSE"
}
