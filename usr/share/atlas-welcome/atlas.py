#!/usr/bin/env python3
# CREATED BY Saeed Badrelden <saeedbadrelden2021@gmail.com>
# Helwan Welcome App for Helwan Linux Distro
import sys
import os
import webbrowser
import subprocess
from PyQt5.QtWidgets import (
	QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox,
	QComboBox, QProgressBar, QDialog, QHBoxLayout, QMessageBox, QInputDialog,
	QLineEdit, QGroupBox, QGridLayout, QScrollArea, QTabWidget, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtGui import QPixmap
import gettext
import platform
import psutil
import shutil


# === إعداد الترجمة ===
def load_translation(language_code):
	current_dir = os.path.dirname(os.path.abspath(__file__))
	locale_path = os.path.join(current_dir, 'locales')
	try:
		translation = gettext.translation('base', localedir=locale_path, languages=[language_code])
		translation.install()
		return translation.gettext
	except FileNotFoundError:
		return lambda s: s


DEFAULT_LANGUAGE_CODE = 'en'
_ = load_translation(DEFAULT_LANGUAGE_CODE)

# قائمة بلغات النظام المدعومة مع الأسماء المقابلة
SYSTEM_LANGUAGES = languages = {
	'ar_EG.UTF-8': 'العربية (مصر)',
	'en_US.UTF-8': 'English (US)',
	'es_ES.UTF-8': 'Español (España)',
	'pt_PT.UTF-8': 'Português (Portugal)',
	'de_DE.UTF-8': 'Deutsch (Deutschland)',
	'fr_FR.UTF-8': 'Français (France)',
	'ru_RU.UTF-8': 'Русский (Россия)',
	'zh_CN.UTF-8': '中文 (简体)',
	'ja_JP.UTF-8': '日本語',
	'it_IT.UTF-8': 'Italiano',
	'pl_PL.UTF-8': 'Polski',
	'ro_RO.UTF-8': 'Română',
	'ur_PK.UTF-8': 'اردو',
	'fa_IR.UTF-8': 'فارسی',
	'hu_HU.UTF-8': 'Magyar',
	'da_DK.UTF-8': 'Dansk (Danmark)',
	'sv_SE.UTF-8': 'Svenska (Sverige)',
	'hi_HI.UTF-8': 'हिन्दी (भारत)',

	# الإضافات الجديدة:
	'bn_BD.UTF-8': 'বাংলা (বাংলাদেশ)',            # البنغالية
	'ta_IN.UTF-8': 'தமிழ் (இந்தியா)',             # التاميلية
	'tr_TR.UTF-8': 'Türkçe (Türkiye)',            # التركية
	'id_ID.UTF-8': 'Bahasa Indonesia',            # الإندونيسية
	'ko_KR.UTF-8': '한국어 (대한민국)',              # الكورية
	'fil_PH.UTF-8': 'Filipino (Pilipinas)',       # الفلبينية
	'vi_VN.UTF-8': 'Tiếng Việt (Việt Nam)',       # الفيتنامية
	'uk_UA.UTF-8': 'Українська (Україна)',        # الأوكرانية
	'nl_NL.UTF-8': 'Nederlands (Nederland)',      # الهولندية
	'nb_NO.UTF-8': 'Norsk (Norge)',               # النرويجية
	'fi_FI.UTF-8': 'Suomi (Suomi)',               # الفنلندية
	'th_TH.UTF-8': 'ไทย (ประเทศไทย)',             # التايلاندية
	'bg_BG.UTF-8': 'Български (България)',         # البلغارية
	'he_IL.UTF-8': 'עברית (ישראל)',                # العبرية

	# الإضافات المطلوبة:
	'ca_ES.UTF-8': 'Català (Espanya)',             # الكاتالونية
	'lv_LV.UTF-8': 'Latviešu (Latvija)',           # اللاتفية
	'sr_RS.UTF-8': 'Српски (Србија)',              # الصربية
	'sk_SK.UTF-8': 'Slovenčina (Slovensko)',       # السلوفاكية
	'mt_MT.UTF-8': 'Malti (Malta)',                # المالطية
	'sq_AL.UTF-8': 'Shqip (Shqipëri)',             # الألبانية
	'mn_MN.UTF-8': 'Монгол (Монгол)',
}


# قائمة لغة التطبيق بنفس الطريقة
APP_LANGUAGES = languages = {
	'ar_EG.UTF-8': 'العربية (مصر)',
	'en_US.UTF-8': 'English (US)',
	'es_ES.UTF-8': 'Español (España)',
	'pt_PT.UTF-8': 'Português (Portugal)',
	'de_DE.UTF-8': 'Deutsch (Deutschland)',
	'fr_FR.UTF-8': 'Français (France)',
	'ru_RU.UTF-8': 'Русский (Россия)',
	'zh_CN.UTF-8': '中文 (简体)',
	'ja_JP.UTF-8': '日本語',
	'it_IT.UTF-8': 'Italiano',
	'pl_PL.UTF-8': 'Polski',
	'ro_RO.UTF-8': 'Română',
	'ur_PK.UTF-8': 'اردو',
	'fa_IR.UTF-8': 'فارسی',
	'hu_HU.UTF-8': 'Magyar',
	'da_DK.UTF-8': 'Dansk (Danmark)',
	'sv_SE.UTF-8': 'Svenska (Sverige)',
	'hi_HI.UTF-8': 'हिन्दी (भारत)',

	# الإضافات الجديدة:
	'bn_BD.UTF-8': 'বাংলা (বাংলাদেশ)',            # البنغالية
	'ta_IN.UTF-8': 'தமிழ் (இந்தியா)',             # التاميلية
	'tr_TR.UTF-8': 'Türkçe (Türkiye)',            # التركية
	'id_ID.UTF-8': 'Bahasa Indonesia',            # الإندونيسية
	'ko_KR.UTF-8': '한국어 (대한민국)',              # الكورية
	'fil_PH.UTF-8': 'Filipino (Pilipinas)',       # الفلبينية
	'vi_VN.UTF-8': 'Tiếng Việt (Việt Nam)',       # الفيتنامية
	'uk_UA.UTF-8': 'Українська (Україна)',        # الأوكرانية
	'nl_NL.UTF-8': 'Nederlands (Nederland)',      # الهولندية
	'nb_NO.UTF-8': 'Norsk (Norge)',               # النرويجية
	'fi_FI.UTF-8': 'Suomi (Suomi)',               # الفنلندية
	'th_TH.UTF-8': 'ไทย (ประเทศไทย)',             # التايلاندية
	'bg_BG.UTF-8': 'Български (България)',         # البلغارية
	'he_IL.UTF-8': 'עברית (ישראל)',                # العبرية

	# الإضافات المطلوبة:
	'ca_ES.UTF-8': 'Català (Espanya)',             # الكاتالونية
	'lv_LV.UTF-8': 'Latviešu (Latvija)',           # اللاتفية
	'sr_RS.UTF-8': 'Српски (Србија)',              # الصربية
	'sk_SK.UTF-8': 'Slovenčina (Slovensko)',       # السلوفاكية
	'mt_MT.UTF-8': 'Malti (Malta)',                # المالطية
	'sq_AL.UTF-8': 'Shqip (Shqipëri)',             # الألبانية
	'mn_MN.UTF-8': 'Монгол (Монгол)',
}


class WelcomeApp(QWidget):

	def __init__(self):
		super().__init__()
		self.language_code = DEFAULT_LANGUAGE_CODE
		self.show_on_startup = self.check_startup_enabled()
		self.current_theme = "Default"  # السمة الافتراضية

		self.settings = QSettings("Helwan", "WelcomeApp")  # هنا غير "Helwan" باسم مؤسستك
		self.logo = self.load_logo()

		self.app_lang_label = None
		self.app_lang_combobox = None
		self.startup_check = None
		self.pacman_btn = None
		self.yay_btn = None  # هنا ضفنا تعريف yay_btn
		self.install_lts_btn = None
		self.install_zen_btn = None
		self.sys_lang_label = None
		self.system_language_combobox = None
		self.apply_lang_btn = None
		self.docs_btn = None
		self.youtube_btn = None
		self.neofetch_btn = None
		self.htop_btn = None
		self.system_info_group = None
		self.disk_space_label = None
		self.disk_space_status = None
		self.processor_label = None
		self.processor_info = None
		self.memory_label = None
		self.memory_info = None
		self.theme_label = None
		self.theme_combobox = None
		self.clean_paccache_keep_two_check = None  # تأكد من تعريف المتغير هنا

		self.tabs = QTabWidget()
		self.main_tab = QWidget()
		self.cleaner_tab = QWidget()

		self.init_ui()
		self.load_theme(self.current_theme)  # ثم قم بتحميل الثيم الذي يعتمد على عناصر الواجهة

		self.load_settings()  # ثم قم بتحميل الإعدادات التي تعتمد عليها

		self.check_disk_space()
		self.update_system_info()

		self.timer = QTimer()
		self.timer.timeout.connect(self.check_disk_space)
		self.timer.start(5000)

	def load_settings(self):
		# استرجاع اللغة المحفوظة وتطبيقها
		saved_language_index = self.settings.value("language_index", 0, type=int)
		if self.app_lang_combobox:
			self.app_lang_combobox.setCurrentIndex(saved_language_index)
			self.change_language(self.app_lang_combobox.currentText())

		# استرجاع السمة المحفوظة وتطبيقها
		saved_theme = self.settings.value("theme", "Default", type=str)
		if self.theme_combobox:
			index = self.theme_combobox.findText(saved_theme)
			if index != -1:
				self.theme_combobox.setCurrentIndex(index)
			self.load_theme(saved_theme)

	def check_startup_enabled(self):
		autostart_dir = os.path.expanduser("~/.config/autostart")
		startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
		return os.path.exists(startup_file_path)

	def load_theme(self, theme_name):
		# ... (نفس كود load_theme السابق)
		if theme_name == "Default":
			self.setStyleSheet("""
				QWidget { background-color: #f5f5f5; font-family: 'Segoe UI'; font-size: 13px; color: #333; }
				QLabel { color: #333; margin-bottom: 5px; }
				QPushButton { background-color: #e0e0e0; color: #333; border: 1px solid #ccc; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #d0d0d0; }
				QCheckBox { color: #333; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #fff; color: #333; border: 1px solid #ccc; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QGroupBox { border: 1px solid #ccc; border-radius: 5px; margin-top: 10px; padding: 10px; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #555; }
				QLabel#disk_space_status { font-weight: bold; }
				QLabel#disk_space_status_ok { color: green; }
				QLabel#disk_space_status_warning { color: orange; }
				QLabel#disk_space_status_error { color: red; }
				QLabel#system_info { margin-bottom: 2px; }
				QTabWidget::pane { border: 1px solid #C2C7CB; background: #f5f5f5; }
				QTabWidget::tab-bar QToolButton { background: #e0e0e0; color: #333; border: 1px solid #ccc; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #d0d0d0; }
				QTabWidget::tab-bar QToolButton:selected { background: #d0d0d0; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #555;")  # لون النص الافتراضي
		elif theme_name == "Sky Blue":
			self.setStyleSheet("""
				QWidget { background-color: #e0f7fa; font-family: 'Segoe UI'; font-size: 13px; color: #212121; }
				QLabel { color: #212121; margin-bottom: 5px; }
				QPushButton { background-color: #81d4fa; color: #212121; border: 1px solid #4fc3f7; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #4fc3f7; }
				QCheckBox { color: #212121; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #b3e5fc; color: #212121; border: 1px solid #81d4fa; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QGroupBox { border: 1px solid #4fc3f7; border-radius: 5px; margin-top: 10px; padding: 10px; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #0277bd; }
				QLabel#disk_space_status { font-weight: bold; color: #212121; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; }
				QTabWidget::pane { border: 1px solid #4fc3f7; background: #e0f7fa; }
				QTabWidget::tab-bar QToolButton { background: #81d4fa; color: #212121; border: 1px solid #4fc3f7; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #4fc3f7; }
				QTabWidget::tab-bar QToolButton:selected { background: #4fc3f7; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #212121;")  # لون النص للسمة الزرقاء
		elif theme_name == "Light Black":  # اسم جديد للسمة اللوكس
			self.setStyleSheet("""
				QWidget { background-color: #666666; font-family: 'Segoe UI'; font-size: 13px; color: #d0d0d0; } /* خلفية رمادي غامق، نص رمادي فاتح */
				QLabel { color: #d0d0d0; margin-bottom: 5px; }
				QPushButton { background-color: #808080; color: #d0d0d0; border: 1px solid #a0a0a0; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* أزرار رمادي متوسط */
				QPushButton:hover { background-color: #a0a0a0; } /* هوفر أفتح للأزرار */
				QCheckBox { color: #d0d0d0; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #737373; color: #d0d0d0; border: 1px solid #999999; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* قوائم منسدلة أغمق شوية */
				QGroupBox { border: 1px solid #999999; border-radius: 5px; margin-top: 10px; padding: 10px; color: #d0d0d0; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #cccccc; } /* عنوان المجموعة أفتح */
				QLabel#disk_space_status { font-weight: bold; color: #d0d0d0; }
				QLabel#disk_space_status_ok { color: lightgreen; }
				QLabel#disk_space_status_warning { color: yellow; }
				QLabel#disk_space_status_error { color: red; }
				QLabel#system_info { margin-bottom: 2px; color: #d0d0d0; }
				QTabWidget::pane { border: 1px solid #999999; background: #666666; color: #d0d0d0; }
				QTabWidget::tab-bar QToolButton { background: #808080; color: #d0d0d0; border: 1px solid #a0a0a0; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #a0a0a0; }
				QTabWidget::tab-bar QToolButton:selected { background: #a0a0a0; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #d0d0d0;")  # لون نص الترحيب للسمة اللوكس
		elif theme_name == "Light Purple":
			self.setStyleSheet("""
				QWidget { background-color: #e6ccff; font-family: 'Segoe UI'; font-size: 13px; color: #4d194d; } /* بنفسجي فاتح للخلفية، بنفسجي داكن للنص */
				QLabel { color: #4d194d; margin-bottom: 5px; }
				QPushButton { background-color: #f0d9ff; color: #4d194d; border: 1px solid #b388eb; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #b388eb; }
				QCheckBox { color: #4d194d; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #f3e5f5; color: #4d194d; border: 1px solid #ce93d8; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QGroupBox { border: 1px solid #ce93d8; border-radius: 5px; margin-top: 10px; padding: 10px; color: #4d194d; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #8e24aa; } /* بنفسجي أغمق لعنوان المجموعة */
				QLabel#disk_space_status { font-weight: bold; color: #4d194d; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #4d194d; }
				QTabWidget::pane { border: 1px solid #ce93d8; background: #e6ccff; color: #4d194d; }
				QTabWidget::tab-bar QToolButton { background: #f0d9ff; color: #4d194d; border: 1px solid #b388eb; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #b388eb; }
				QTabWidget::tab-bar QToolButton:selected { background: #b388eb; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #4d194d;")  # لون النص للسمة البنفسجية
		elif theme_name == "Light Black":
			self.setStyleSheet("""
				QWidget { background-color: #505050; font-family: 'Segoe UI'; font-size: 13px; color: #e0e0e0; } /* افتحنا الخلفية والنص */
				QLabel { color: #e0e0e0; margin-bottom: 5px; }
				QPushButton { background-color: #707070; color: #e0e0e0; border: 1px solid #909090; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* افتحنا الأزرار */
				QPushButton:hover { background-color: #909090; } /* افتحنا لونHover للأزرار */
				QCheckBox { color: #e0e0e0; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #606060; color: #e0e0e0; border: 1px solid #808080; border-radius: 3px; padding: 4px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; } /* افتحنا القوائم المنسدلة */
				QGroupBox { border: 1px solid #808080; border-radius: 5px; margin-top: 10px; padding: 10px; color: #e0e0e0; } /* افتحنا حدود وعنوان المجموعات */
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #c0c0c0; } /* افتحنا لون عنوان المجموعة */
				QLabel#disk_space_status { font-weight: bold; color: #e0e0e0; }
				QLabel#disk_space_status_ok { color: lightgreen; }
				QLabel#disk_space_status_warning { color: yellow; }
				QLabel#disk_space_status_error { color: red; }
				QLabel#system_info { margin-bottom: 2px; color: #e0e0e0; }
				QTabWidget::pane { border: 1px solid #808080; background: #505050; color: #e0e0e0; }
				QTabWidget::tab-bar QToolButton { background: #707070; color: #e0e0e0; border: 1px solid #909090; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #909090; }
				QTabWidget::tab-bar QToolButton:selected { background: #909090; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #e0e0e0;")  # لون النص للسمة السوداء الفاتحة)
		elif theme_name == "Mint Green":
			self.setStyleSheet("""
				QWidget { background-color: #e0f7f1; font-family: 'Segoe UI'; font-size: 13px; color: #2e7d6d; }
				QLabel { color: #2e7d6d; margin-bottom: 5px; }
				QPushButton { background-color: #a8e6cf; color: #004d40; border: 1px solid #4db6ac; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #81d4af; }
				QCheckBox { color: #2e7d6d; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #dcedc8; color: #2e7d6d; border: 1px solid #aed581; border-radius: 3px; padding: 4px; font-size: 10px; }
				QGroupBox { border: 1px solid #a5d6a7; border-radius: 5px; margin-top: 10px; padding: 10px; color: #2e7d6d; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #00796b; }
				QLabel#disk_space_status { font-weight: bold; color: #004d40; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #2e7d6d; }
				QTabWidget::pane { border: 1px solid #b2dfdb; background: #e0f7f1; color: #2e7d6d; }
				QTabWidget::tab-bar QToolButton { background: #a8e6cf; color: #004d40; border: 1px solid #4db6ac; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #81d4af; }
				QTabWidget::tab-bar QToolButton:selected { background: #4db6ac; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #2e7d6d;")
				
		elif theme_name == "Amber Sunset":
			self.setStyleSheet("""
				QWidget { background-color: #fff8e1; font-family: 'Segoe UI'; font-size: 13px; color: #e65100; }
				QLabel { color: #e65100; margin-bottom: 5px; }
				QPushButton { background-color: #ffd180; color: #bf360c; border: 1px solid #ffab40; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #ffb74d; }
				QCheckBox { color: #e65100; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #ffe0b2; color: #e65100; border: 1px solid #ffcc80; border-radius: 3px; padding: 4px; font-size: 10px; }
				QGroupBox { border: 1px solid #ffcc80; border-radius: 5px; margin-top: 10px; padding: 10px; color: #e65100; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #ef6c00; }
				QLabel#disk_space_status { font-weight: bold; color: #bf360c; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #e65100; }
				QTabWidget::pane { border: 1px solid #ffe082; background: #fff8e1; color: #e65100; }
				QTabWidget::tab-bar QToolButton { background: #ffd180; color: #bf360c; border: 1px solid #ffab40; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #ffb74d; }
				QTabWidget::tab-bar QToolButton:selected { background: #ffab40; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #e65100;")
				
		elif theme_name == "Rose Pink":
			self.setStyleSheet("""
				QWidget { background-color: #ffe4e1; font-family: 'Segoe UI'; font-size: 13px; color: #880e4f; }
				QLabel { color: #880e4f; margin-bottom: 5px; }
				QPushButton { background-color: #f8bbd0; color: #880e4f; border: 1px solid #f48fb1; border-radius: 5px; padding: 6px 10px; margin-top: 3px; margin-bottom: 3px; font-size: 10px; }
				QPushButton:hover { background-color: #f06292; }
				QCheckBox { color: #880e4f; margin-top: 5px; margin-bottom: 5px; }
				QComboBox { background-color: #fce4ec; color: #880e4f; border: 1px solid #f8bbd0; border-radius: 3px; padding: 4px; font-size: 10px; }
				QGroupBox { border: 1px solid #f48fb1; border-radius: 5px; margin-top: 10px; padding: 10px; color: #880e4f; }
				QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #ad1457; }
				QLabel#disk_space_status { font-weight: bold; color: #880e4f; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #880e4f; }
				QTabWidget::pane { border: 1px solid #f8bbd0; background: #ffe4e1; color: #880e4f; }
				QTabWidget::tab-bar QToolButton { background: #f8bbd0; color: #880e4f; border: 1px solid #f48fb1; border-radius: 3px; padding: 4px 10px; margin: 2px; font-size: 10px; }
				QTabWidget::tab-bar QToolButton:hover { background: #f06292; }
				QTabWidget::tab-bar QToolButton:selected { background: #f48fb1; font-weight: bold; }
			""")
			if self.greeting:
				self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #880e4f;")

		elif theme_name == "Sunset Gradient":
			self.setStyleSheet("""
				QWidget {
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffd1dc, stop:1 #ffe4b5);
					font-family: 'Segoe UI';
					font-size: 13px;
					color: #4b2e2e;
				}
				QLabel { color: #4b2e2e; margin-bottom: 5px; }
				QPushButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffe4e1, stop:1 #ffb6b9);
					color: #4b2e2e;
					border: 1px solid #ffa07a;
					border-radius: 5px;
					padding: 6px 10px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QPushButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffb6b9, stop:1 #ffa07a);
				}
				QCheckBox {
					color: #4b2e2e;
					margin-top: 5px;
					margin-bottom: 5px;
				}
				QComboBox {
					background-color: #fff0f5;
					color: #4b2e2e;
					border: 1px solid #ffa07a;
					border-radius: 3px;
					padding: 4px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QGroupBox {
					border: 1px solid #ffa07a;
					border-radius: 5px;
					margin-top: 10px;
					padding: 10px;
					color: #4b2e2e;
				}
				QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 5px;
					color: #e65100;
				}
				QLabel#disk_space_status { font-weight: bold; color: #4b2e2e; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #4b2e2e; }
				QTabWidget::pane {
					border: 1px solid #ffa07a;
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #ffd1dc, stop:1 #fff8e1);
					color: #4b2e2e;
				}
				QTabWidget::tab-bar QToolButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffe4e1, stop:1 #ffb6b9);
					color: #4b2e2e;
					border: 1px solid #ffa07a;
					border-radius: 3px;
					padding: 4px 10px;
					margin: 2px;
					font-size: 10px;
				}
				QTabWidget::tab-bar QToolButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffb6b9, stop:1 #ffa07a);
				}
				QTabWidget::tab-bar QToolButton:selected {
					background: #ffa07a;
					font-weight: bold;
				}
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #4b2e2e;")

		elif theme_name == "Ocean Gradient":
			self.setStyleSheet("""
				QWidget {
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c2f0f7, stop:1 #81d4fa);
					font-family: 'Segoe UI';
					font-size: 13px;
					color: #01579b;
				}
				QLabel { color: #01579b; margin-bottom: 5px; }
				QPushButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e1f5fe, stop:1 #4fc3f7);
					color: #01579b;
					border: 1px solid #4fc3f7;
					border-radius: 5px;
					padding: 6px 10px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QPushButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4fc3f7, stop:1 #0288d1);
				}
				QCheckBox {
					color: #01579b;
					margin-top: 5px;
					margin-bottom: 5px;
				}
				QComboBox {
					background-color: #bbdefb;
					color: #01579b;
					border: 1px solid #4fc3f7;
					border-radius: 3px;
					padding: 4px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QGroupBox {
					border: 1px solid #4fc3f7;
					border-radius: 5px;
					margin-top: 10px;
					padding: 10px;
					color: #01579b;
				}
				QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 5px;
					color: #0288d1;
				}
				QLabel#disk_space_status { font-weight: bold; color: #01579b; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #01579b; }
				QTabWidget::pane {
					border: 1px solid #4fc3f7;
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #c2f0f7, stop:1 #bbdefb);
					color: #01579b;
				}
				QTabWidget::tab-bar QToolButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #e1f5fe, stop:1 #4fc3f7);
					color: #01579b;
					border: 1px solid #4fc3f7;
					border-radius: 3px;
					padding: 4px 10px;
					margin: 2px;
					font-size: 10px;
				}
				QTabWidget::tab-bar QToolButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4fc3f7, stop:1 #0288d1);
				}
				QTabWidget::tab-bar QToolButton:selected {
					background: #0288d1;
					font-weight: bold;
				}
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #01579b;")

		elif theme_name == "Night Sky":
			self.setStyleSheet("""
				QWidget {
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a237e, stop:1 #0d47a1);
					font-family: 'Segoe UI';
					font-size: 13px;
					color: #c5cae9;
				}
				QLabel { color: #c5cae9; margin-bottom: 5px; }
				QPushButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3949ab, stop:1 #283593);
					color: #c5cae9;
					border: 1px solid #5c6bc0;
					border-radius: 5px;
					padding: 6px 10px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QPushButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5c6bc0, stop:1 #3949ab);
				}
				QCheckBox {
					color: #c5cae9;
					margin-top: 5px;
					margin-bottom: 5px;
				}
				QComboBox {
					background-color: #303f9f;
					color: #c5cae9;
					border: 1px solid #5c6bc0;
					border-radius: 3px;
					padding: 4px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QGroupBox {
					border: 1px solid #5c6bc0;
					border-radius: 5px;
					margin-top: 10px;
					padding: 10px;
					color: #c5cae9;
				}
				QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 5px;
					color: #7986cb;
				}
				QLabel#disk_space_status { font-weight: bold; color: #c5cae9; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #c5cae9; }
				QTabWidget::pane {
					border: 1px solid #5c6bc0;
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #1a237e, stop:1 #283593);
					color: #c5cae9;
				}
				QTabWidget::tab-bar QToolButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #3949ab, stop:1 #5c6bc0);
					color: #c5cae9;
					border: 1px solid #5c6bc0;
					border-radius: 3px;
					padding: 4px 10px;
					margin: 2px;
					font-size: 10px;
				}
				QTabWidget::tab-bar QToolButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #5c6bc0, stop:1 #3949ab);
				}
				QTabWidget::tab-bar QToolButton:selected {
					background: #3949ab;
					font-weight: bold;
				}
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #c5cae9;")


		elif theme_name == "Forest Breeze":
			self.setStyleSheet("""
				QWidget {
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a5d6a7, stop:1 #388e3c);
					font-family: 'Segoe UI';
					font-size: 13px;
					color: #1b5e20;
				}
				QLabel { color: #1b5e20; margin-bottom: 5px; }
				QPushButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c8e6c9, stop:1 #66bb6a);
					color: #1b5e20;
					border: 1px solid #66bb6a;
					border-radius: 5px;
					padding: 6px 10px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QPushButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #81c784, stop:1 #2e7d32);
				}
				QCheckBox {
					color: #1b5e20;
					margin-top: 5px;
					margin-bottom: 5px;
				}
				QComboBox {
					background-color: #a5d6a7;
					color: #1b5e20;
					border: 1px solid #66bb6a;
					border-radius: 3px;
					padding: 4px;
					margin-top: 3px;
					margin-bottom: 3px;
					font-size: 10px;
				}
				QGroupBox {
					border: 1px solid #66bb6a;
					border-radius: 5px;
					margin-top: 10px;
					padding: 10px;
					color: #1b5e20;
				}
				QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 5px;
					color: #2e7d32;
				}
				QLabel#disk_space_status { font-weight: bold; color: #1b5e20; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #1b5e20; }
				QTabWidget::pane {
					border: 1px solid #66bb6a;
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #a5d6a7, stop:1 #81c784);
					color: #1b5e20;
				}
				QTabWidget::tab-bar QToolButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #c8e6c9, stop:1 #66bb6a);
					color: #1b5e20;
					border: 1px solid #66bb6a;
					border-radius: 3px;
					padding: 4px 10px;
					margin: 2px;
					font-size: 10px;
				}
				QTabWidget::tab-bar QToolButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #81c784, stop:1 #2e7d32);
				}
				QTabWidget::tab-bar QToolButton:selected {
					background: #2e7d32;
					font-weight: bold;
				}
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #1b5e20;")

		elif theme_name == "Halwan":
			self.setStyleSheet("""
				QWidget {
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
						stop:0 #e0c3fc, stop:1 #8ec5fc);  /* خليط بين البنفسجي السماوي والأزرق الهادئ */
					font-family: 'Segoe UI';
					font-size: 13px;
					color: #3a1768;  /* بنفسجي غامق للنص */
				}
				QLabel {
					color: #3a1768;
					margin-bottom: 5px;
				}
				QPushButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
						stop:0 #fceabb, stop:1 #f8b500); /* ألوان دافئة صفراء/ذهبية */
					color: #4a2c67;
					border: 1px solid #d9a520;
					border-radius: 6px;
					padding: 6px 12px;
					margin-top: 4px;
					margin-bottom: 4px;
					font-size: 11px;
					font-weight: 600;
				}
				QPushButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
						stop:0 #f8b500, stop:1 #d18e00);
					color: #fff;
				}
				QCheckBox {
					color: #3a1768;
					margin-top: 6px;
					margin-bottom: 6px;
				}
				QComboBox {
					background: #c9b2ff; /* بنفسجي فاتح */
					color: #3a1768;
					border: 1px solid #7a42c1;
					border-radius: 4px;
					padding: 5px;
					margin-top: 4px;
					margin-bottom: 4px;
					font-size: 11px;
				}
				QGroupBox {
					border: 2px solid #7a42c1;
					border-radius: 7px;
					margin-top: 12px;
					padding: 12px;
					color: #3a1768;
					background: rgba(255, 255, 255, 0.15); /* شفافية خفيفة */
				}
				QGroupBox::title {
					subcontrol-origin: margin;
					left: 10px;
					padding: 0 6px;
					color: #d18e00; /* ذهبي للنص */
					font-weight: bold;
					font-size: 13px;
				}
				QLabel#disk_space_status { font-weight: bold; color: #3a1768; }
				QLabel#disk_space_status_ok { color: darkgreen; }
				QLabel#disk_space_status_warning { color: darkorange; }
				QLabel#disk_space_status_error { color: darkred; }
				QLabel#system_info { margin-bottom: 2px; color: #3a1768; }
				QTabWidget::pane {
					border: 1px solid #7a42c1;
					background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
						stop:0 #d8b4fe, stop:1 #a29bfe);
					color: #3a1768;
				}
				QTabWidget::tab-bar QToolButton {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
						stop:0 #fceabb, stop:1 #f8b500);
					color: #4a2c67;
					border: 1px solid #d9a520;
					border-radius: 4px;
					padding: 5px 14px;
					margin: 3px;
					font-size: 11px;
					font-weight: 600;
				}
				QTabWidget::tab-bar QToolButton:hover {
					background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
						stop:0 #f8b500, stop:1 #d18e00);
					color: #fff;
				}
				QTabWidget::tab-bar QToolButton:selected {
					background: #d18e00;
					font-weight: bold;
					color: #fff;
				}
			""")
			if self.greeting:
				self.greeting.setStyleSheet(
					"font-size: 16px; margin-top: 12px; margin-bottom: 16px; color: #3a1768; font-weight: bold;")



	def load_logo(self):
		logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png")
		if os.path.exists(logo_path):
			logo = QPixmap(logo_path)
			return logo.scaledToWidth(120, Qt.SmoothTransformation) if not logo.isNull() else None
		else:
			print(f"Warning: Logo not found at {logo_path}")
			return None

	def init_ui(self):
		main_layout = QVBoxLayout(self)
		self.tabs = QTabWidget()

		# تم تغيير self.tr() إلى _() هنا
		self.tabs.addTab(self.create_main_tab(), _("Welcome"))
		self.tabs.addTab(self.create_cleaner_tab(), _("System Cleaner"))
		# تم تغيير self.tr() إلى _() هنا
		self.tabs.addTab(self.create_software_groups_tab(), _("Software Groups"))  # تبويب جديد

		main_layout.addWidget(self.tabs)

		self.setLayout(main_layout)
		# تم تغيير self.tr() إلى _() هنا
		self.setWindowTitle(_("Welcome to Helwan Linux"))
		self.setGeometry(100, 100, 600, 400)

	# دالة لإنشاء تبويب منظف المزامنة (لسه هنضيف جواه عناصر واجهة المستخدم)
	def create_sync_cleaner_tab(self):
		sync_cleaner_tab = QWidget()
		sync_layout = QVBoxLayout(sync_cleaner_tab)

		sync_label = QLabel(_("Remove Sync Folders"))
		sync_layout.addWidget(sync_label)

		# هنا ممكن نضيف قائمة بمجلدات المزامنة اللي ممكن يحذفها المستخدم
		# وزر لبدء عملية الحذف

		sync_layout.addStretch(1)
		return sync_cleaner_tab

	def create_main_tab(self):
		main_tab_layout = QVBoxLayout(self.main_tab)
		main_tab_layout.setAlignment(Qt.AlignTop)
		main_tab_layout.setSpacing(1)

		if self.logo:
			logo_label = QLabel(self)
			logo_label.setPixmap(self.logo)
			logo_label.setAlignment(Qt.AlignCenter)
			main_tab_layout.addWidget(logo_label)

		self.greeting = QLabel()
		self.greeting.setAlignment(Qt.AlignCenter)
		self.greeting.setStyleSheet("font-size: 15px; margin-top: 10px; margin-bottom: 15px; color: #e0e0e0;")
		main_tab_layout.addWidget(self.greeting)

		controls = QVBoxLayout()
		controls.setSpacing(1)
		main_tab_layout.addLayout(controls)

		# System Updates Group
		update_group = QGroupBox(_("System Updates"))
		update_layout = QVBoxLayout()
		update_layout_buttons = QHBoxLayout()
		self.pacman_btn_bottom = self.create_button(_("Update System (Pacman)"),
													lambda: self.run_terminal_cmd("sudo pacman -Syu"))
		update_layout_buttons.addWidget(self.pacman_btn_bottom)
		self.yay_btn_bottom = self.create_button(_("Update System (Yay)"), lambda: self.run_terminal_cmd("yay -Syu"))
		if not self.is_yay_installed():
			self.yay_btn_bottom.setEnabled(False)
			self.yay_btn_bottom.setToolTip(_("Yay is not installed."))
		update_layout_buttons.addWidget(self.yay_btn_bottom)
		update_layout.addLayout(update_layout_buttons)

		kernel_install_layout = QHBoxLayout()
		self.install_lts_btn = self.create_button(_("Install Linux LTS"), self.install_linux_lts)
		kernel_install_layout.addWidget(self.install_lts_btn)
		self.install_zen_btn = self.create_button(_("Install Linux Zen"), self.install_linux_zen)
		kernel_install_layout.addWidget(self.install_zen_btn)
		update_layout.addLayout(kernel_install_layout)

		update_group.setLayout(update_layout)
		controls.addWidget(update_group)

		# Theme Selection
		theme_layout = QHBoxLayout()
		self.theme_label = QLabel(_("Application Theme:"))
		theme_layout.addWidget(self.theme_label)
		self.theme_combobox = QComboBox()
		self.theme_combobox.addItems(["Default", "Sky Blue", "Light Black", "Light Purple","Mint Green","Amber Sunset","Rose Pink","Sunset Gradient","Ocean Gradient","Night Sky","Forest Breeze","Halwan"])
		self.theme_combobox.setCurrentText(self.current_theme)
		self.theme_combobox.currentTextChanged.connect(self.save_theme)
		self.theme_combobox.setStyleSheet("font-size: 10px; padding: 1px;")
		theme_layout.addWidget(self.theme_combobox)
		controls.addLayout(theme_layout)

		# Application Language
		app_lang_layout = self.create_labeled_combobox(
			label_attr='app_lang_label',
			combo_attr='app_lang_combobox',
			label_text=_("Application Language:"),
			items=list(APP_LANGUAGES.values()),
			default=APP_LANGUAGES.get(self.language_code, 'English'),
			on_change=self.change_language
		)
		controls.addLayout(app_lang_layout)

		# Startup Settings
		startup_layout = QHBoxLayout()
		self.startup_check = QCheckBox(_("Show on startup"))
		self.startup_check.setChecked(self.show_on_startup)
		self.startup_check.stateChanged.connect(self.update_startup_file)
		startup_layout.addWidget(self.startup_check)
		controls.addLayout(startup_layout)

		# System Language
		sys_lang_layout = QHBoxLayout()
		self.sys_lang_label = QLabel(_("System Language:"))
		sys_lang_layout.addWidget(self.sys_lang_label)
		self.system_language_combobox = QComboBox()
		self.system_language_combobox.addItems(list(SYSTEM_LANGUAGES.values()))
		self.system_language_combobox.setCurrentText(
			'en_US.UTF-8' if 'en_US.UTF-8' in SYSTEM_LANGUAGES else list(SYSTEM_LANGUAGES.keys())[
				0] if SYSTEM_LANGUAGES else '')
		sys_lang_layout.addWidget(self.system_language_combobox)
		controls.addLayout(sys_lang_layout)

		self.apply_lang_btn = self.create_button(_("Apply System Language"), self.apply_system_language)
		controls.addWidget(self.apply_lang_btn)

		# Documentation and Support
		docs_layout = QHBoxLayout()
		self.docs_btn = self.create_button(_("Open Documentation"),
										   lambda: self.open_url("https://helwan-linux.mystrikingly.com/documentation"))
		docs_layout.addWidget(self.docs_btn)
		self.youtube_btn = self.create_button(_("Open YouTube Channel"),
											  lambda: self.open_url("https://www.youtube.com/@HelwanO.S"))
		docs_layout.addWidget(self.youtube_btn)
		controls.addLayout(docs_layout)

		# System Information Group
		self.system_info_group = QGroupBox(_("System Information"))
		system_info_layout = QGridLayout()
		self.disk_space_label = QLabel(_("Available Disk Space:"))
		self.disk_space_status = QLabel()
		self.disk_space_status.setObjectName("disk_space_status")
		system_info_layout.addWidget(self.disk_space_label, 0, 0)
		system_info_layout.addWidget(self.disk_space_status, 0, 1)
		self.processor_label = QLabel(_("Processor:"))
		self.processor_info = QLabel()
		self.processor_info.setObjectName("system_info")
		system_info_layout.addWidget(self.processor_label, 1, 0)
		system_info_layout.addWidget(self.processor_info, 1, 1)
		self.memory_label = QLabel(_("RAM:"))
		self.memory_info = QLabel()
		self.memory_info.setObjectName("system_info")
		system_info_layout.addWidget(self.memory_label, 2, 0)
		system_info_layout.addWidget(self.memory_info, 2, 1)
		self.system_info_group.setLayout(system_info_layout)
		self.system_info_group.setMaximumHeight(110)  # أو أي رقم يناسبك
		controls.addWidget(self.system_info_group)

		# System Information Buttons (Neofetch, Htop)
		sysinfo_layout = QHBoxLayout()
		self.neofetch_btn = self.create_button(_("Show System Info Details"), lambda: self.run_terminal_cmd("fastfetch"))
		sysinfo_layout.addWidget(self.neofetch_btn)
		self.htop_btn = self.create_button(_("Performance Monitor"), lambda: self.run_terminal_cmd("htop"))
		sysinfo_layout.addWidget(self.htop_btn)
		controls.addLayout(sysinfo_layout)

		# إضافة spacer في نهاية التخطيط لرفع كل المحتوى
		spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
		main_tab_layout.addItem(spacer)

		return self.main_tab

	def create_cleaner_tab(self):
		cleaner_layout = QVBoxLayout(self.cleaner_tab)
		cleaner_group = QGroupBox(_("Pacman Cleaner"))
		cleaner_group.setObjectName("Pacman Cleaner")
		pacman_cleaner_layout = QVBoxLayout()

		self.clean_pacman_cache_full_check = QCheckBox(
			_("Clean Pacman Cache (Full) - Warning! This will remove all downloaded packages."))
		self.clean_pacman_cache_full_check.setObjectName("clean_pacman_cache_full_check")  # عشان الترجمة
		pacman_cleaner_layout.addWidget(self.clean_pacman_cache_full_check)

		self.remove_orphan_packages_check = QCheckBox(
			_("Remove Orphan Packages - Packages that are no longer required by any installed package."))
		self.remove_orphan_packages_check.setObjectName("remove_orphan_packages_check")  # عشان الترجمة
		pacman_cleaner_layout.addWidget(self.remove_orphan_packages_check)

		self.clean_paccache_keep_two_check = QCheckBox(_("Clean Old Packages (Keep Last 2 Versions)"))
		self.clean_paccache_keep_two_check.setObjectName("clean_paccache_keep_two_check")  # عشان الترجمة
		pacman_cleaner_layout.addWidget(self.clean_paccache_keep_two_check)

		#self.clean_paccache_uninstalled_check = QCheckBox(_("Remove Uninstalled Packages from Cache"))
		#self.clean_paccache_uninstalled_check.setObjectName("clean_paccache_uninstalled_check")  # عشان الترجمة
		#pacman_cleaner_layout.addWidget(self.clean_paccache_uninstalled_check)

		self.run_pacman_cleanup_button = self.create_button(_("Run Pacman Cleanup"), self.run_pacman_cleanup)
		self.run_pacman_cleanup_button.setObjectName("run_pacman_cleanup_button")  # عشان الترجمة
		pacman_cleaner_layout.addWidget(self.run_pacman_cleanup_button)

		cleaner_group.setLayout(pacman_cleaner_layout)
		cleaner_layout.addWidget(cleaner_group)
		cleaner_layout.addStretch(1)
		return self.cleaner_tab
		
	def create_software_groups_tab(self):
		self.software_tab = QWidget()
		software_tab_layout = QVBoxLayout(self.software_tab)
		software_tab_layout.setAlignment(Qt.AlignTop)

		# تم تغيير self.tr() إلى _() هنا
		self.group_box = QGroupBox(_("Software Groups Installer"))
		self.group_box.setObjectName("Software Groups Installer") # إضافة اسم الكائن لتسهيل التحديث في retranslate_ui
		layout = QVBoxLayout()
		self.group_box.setLayout(layout)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		dev_btn = self.create_button(_("Install Development Tools"),
									 lambda: self.run_terminal_cmd(
										 "sudo pacman -S --needed base-devel git cmake geany code meld python-pyqt5 qtcreator qt5-tools dbeaver"))
		dev_btn.setObjectName("dev_tools_button")
		layout.addWidget(dev_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		prog_btn = self.create_button(_("Install Programming Languages"),
									 lambda: self.run_terminal_cmd(
										 "sudo pacman -S --needed rust lua php nodejs go sqlite mariadb"))
		prog_btn.setObjectName("prog_lang_button")
		layout.addWidget(prog_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		multimedia_btn = self.create_button(_("Install Multimedia Suite"),
										   lambda: self.run_terminal_cmd(
											   "sudo pacman -S --needed vlc gimp audacity shotcut audacious vokoscreen handbrake"))
		multimedia_btn.setObjectName("multimedia_suite_button")
		layout.addWidget(multimedia_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		internet_btn = self.create_button(_("Install Internet Tools"),
										 lambda: self.run_terminal_cmd(
											 "sudo pacman -S --needed firefox kdeconnect thunderbird"))
		internet_btn.setObjectName("internet_tools_button")
		layout.addWidget(internet_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		office_btn = self.create_button(_("Install Office Suite"),
									   lambda: self.run_terminal_cmd(
										   "sudo pacman -S --needed libreoffice-fresh hunspell-en_US"))
		office_btn.setObjectName("office_suite_button")
		layout.addWidget(office_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		gaming_btn = self.create_button(_("Install Gaming Tools"),
									   lambda: self.run_terminal_cmd(
										   "sudo pacman -S --needed steam lutris cuyo artikulate blurble openra vkd3d gamemode mangohud"))
		gaming_btn.setObjectName("gaming_tools_button")
		layout.addWidget(gaming_btn)

		# تم تغيير self.tr() إلى _() هنا وإضافة اسم الكائن
		docker_btn = self.create_button(_("Install Docker Tools"),
									   lambda: self.run_terminal_cmd(
										   "sudo pacman -S --needed docker docker-compose lazydocker"))
		docker_btn.setObjectName("docker_tools_button")
		layout.addWidget(docker_btn)

		software_tab_layout.addWidget(self.group_box)
		software_tab_layout.addStretch(1)

		return self.software_tab

	def run_pacman_cleanup(self):
		commands = []

		if self.clean_pacman_cache_full_check.isChecked():
			commands.append("sudo pacman -Scc")

		if self.remove_orphan_packages_check.isChecked():
			orphans = subprocess.getoutput("pacman -Qtdq")
			if orphans.strip():
				commands.append("sudo pacman -Rns $(pacman -Qtdq)")
			else:
				#print("No orphan packages found; skipping removal.")
				pass

		if self.clean_paccache_keep_two_check.isChecked():
			commands.append("sudo paccache -rk2 --quiet")

		#if self.clean_paccache_uninstalled_check.isChecked():
			#commands.append("sudo paccache -u -k0 --quiet")  # لازم -k0 مع -u

		if commands:
			full_command = " && ".join(commands)
			confirmation_text = _("You are about to run the following commands with root privileges:\n\n") + \
								"\n".join(commands) + _("\n\nAre you sure you want to continue?")
			reply = QMessageBox.question(self, _("Confirmation"), confirmation_text,
										 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

			if reply == QMessageBox.Yes:
				self.run_terminal_cmd(full_command, _("Running Pacman Cleanup"))
				QMessageBox.information(self, _("Cleanup Done"), _("Pacman cleanup tasks completed."))
		else:
			QMessageBox.information(self, _("Info"), _("No Pacman cleanup options selected."))

	def remove_sync_folder(self, folder_path):
		command = f"pkexec rm -rf '{folder_path}'"
		title = _("Removing Sync Folder")
		message = _(
			"This action requires administrator privileges to remove the sync folder. You might be asked for your password.")
		reply = QMessageBox.warning(self, title, message, QMessageBox.Ok | QMessageBox.Cancel)
		if reply == QMessageBox.Ok:
			self.run_terminal_cmd(command, title)
			QMessageBox.information(self, title, _("Sync folder removal initiated."))

	def create_labeled_combobox(self, label_attr, combo_attr, label_text, items, default, on_change=None):
		layout = QHBoxLayout()
		label = QLabel(label_text)
		combo = QComboBox()
		combo.addItems(items)
		index = combo.findText(default)
		if index != -1:
			combo.setCurrentIndex(index)
		if on_change:
			combo.currentTextChanged.connect(on_change)
		# تصغير حجم خط القائمة المنسدلة وتعديل الحشو
		combo.setStyleSheet("font-size: 10px; padding: 4px 8px;")  # تقليل حجم الخط والحشو
		setattr(self, label_attr, label)
		setattr(self, combo_attr, combo)
		layout.addWidget(label)
		layout.addWidget(combo)
		return layout

	def create_button(self, text, on_click):
		button = QPushButton(text)
		button.clicked.connect(on_click)
		# يمكنك هنا محاولة تصغير حجم الخط أو تغيير أبعاد الزر
		button.setStyleSheet("font-size: 10px; padding: 4px 8px;")  # تقليل حجم الخط والحشو
		return button

	def update_startup_file(self, state):
		autostart_dir = os.path.expanduser("~/.config/autostart")
		startup_file_path = os.path.join(autostart_dir, "helwan_welcome.desktop")
		if state == Qt.Checked:
			if not os.path.exists(autostart_dir):
				os.makedirs(autostart_dir, exist_ok=True)
			with open(startup_file_path, "w") as f:
				f.write("[Desktop Entry]\n")
				f.write("Type=Application\n")
				f.write(f"Exec={sys.executable} {os.path.abspath(__file__)}\n")
				f.write("Hidden=false\n")
				f.write("X-GNOME-Autostart-enabled=true\n")
				f.write("Name=Helwan Welcome\n")
				f.write("Comment=Welcome application for Helwan Linux\n")
				if self.logo:
					# افتراض أن الشعار موجود في نفس دليل السكريبت أو يمكنك توفير مسار مطلق
					logo_base_name = os.path.basename(
						os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources", "logo.png"))
					f.write(
						f"Icon={os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sources', logo_base_name)}\n")
		else:
			if os.path.exists(startup_file_path):
				os.remove(startup_file_path)
		self.show_on_startup = state == Qt.Checked

	def change_language(self, language_name):
		for code, name in APP_LANGUAGES.items():
			if name == language_name:
				new_gettext = load_translation(code)
				global _
				_ = new_gettext
				self.language_code = code
				self.retranslate_ui()
				self.settings.setValue("language_index", self.app_lang_combobox.currentIndex())
				QMessageBox.information(self, _("Language Changed"),
										_("Application language has been changed. Some changes may require an application restart."))
				return
		print(f"Warning: Language code not found for {language_name}")

	def save_theme(self, theme_name):
		self.current_theme = theme_name
		self.load_theme(theme_name)
		self.settings.setValue("theme", theme_name)

	def is_yay_installed(self):
		try:
			process = subprocess.run(['yay', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
			return process.returncode == 0
		except FileNotFoundError:
			return False

	def install_linux_lts(self):
		# أمر التثبيت
		cmd = (
			"pkexec bash -c '"
			"pacman -S --needed linux-lts linux-lts-headers && "
			"if pacman -Qs linux-lts > /dev/null; then "
			"echo \"linux-lts installed successfully.\"; "
			"grub-mkconfig -o /boot/grub/grub.cfg; "
			"else "
			"echo \"Failed to install linux-lts.\" >&2; exit 1; "
			"fi'"
		)

		print("Running command:", cmd)  # دي هتطبع الأمر قبل تشغيله

		subprocess.run(cmd, shell=True)

		# نسأل المستخدم بعد انتهاء التثبيت
		reply = QMessageBox.question(
			self,
			_("Set LTS as default"),
			_("Do you want to make the LTS kernel the default boot option?"),
			QMessageBox.Yes | QMessageBox.No
		)

		if reply == QMessageBox.Yes:
			# أمر ضبط الكيرنل الافتراضي
			set_default_cmd = (
				"pkexec bash -c '"
				"grub-set-default \"Advanced options for Arch Linux>Arch Linux, with Linux lts\" && "
				"grub-mkconfig -o /boot/grub/grub.cfg'"
			)

			print("Running command:", set_default_cmd)

			subprocess.run(set_default_cmd, shell=True)





	def install_linux_zen(self):
		# أمر التثبيت
		cmd = (
			"pkexec bash -c '"
			"pacman -S --needed linux-zen linux-zen-headers && "
			"if pacman -Qs linux-zen > /dev/null; then "
			"echo \"linux-zen installed successfully.\"; "
			"grub-mkconfig -o /boot/grub/grub.cfg; "
			"else "
			"echo \"Failed to install linux-zen.\" >&2; exit 1; "
			"fi'"
		)

		print("Running command:", cmd)  # دي هتطبع الأمر قبل تشغيله

		subprocess.run(cmd, shell=True)

		# نسأل المستخدم بعد انتهاء التثبيت
		reply = QMessageBox.question(
			self,
			_("Set LTS as default"),
			_("Do you want to make the zen kernel the default boot option?"),
			QMessageBox.Yes | QMessageBox.No
		)

		if reply == QMessageBox.Yes:
			# أمر ضبط الكيرنل الافتراضي
			set_default_cmd = (
				"pkexec bash -c '"
				"grub-set-default \"Advanced options for Arch Linux>Arch Linux, with Linux zen\" && "
				"grub-mkconfig -o /boot/grub/grub.cfg'"
			)

			print("Running command:", set_default_cmd)

			subprocess.run(set_default_cmd, shell=True)

	def apply_system_language(self):
		selected_lang_name = self.system_language_combobox.currentText()
		lang_code = None
		for code, name in SYSTEM_LANGUAGES.items():
			if name == selected_lang_name:
				lang_code = code
				break

		if not lang_code:
			QMessageBox.critical(self, _("Error"), _("Please select a valid system language."))
			return

		# نتأكد إن lang_code مش فيها .UTF-8 عشان ما نكررهاش
		base_lang_code = lang_code.replace('.UTF-8', '')

		# 🔍 نتحقق من اللغة الحالية باستخدام localectl
		try:
			current_locale_output = subprocess.check_output("localectl status", shell=True).decode()
			if f"LANG={base_lang_code}.UTF-8" in current_locale_output:
				QMessageBox.information(
					self,
					_("No Change Needed"),
					_("The selected language is already active.")
				)
				return
		except Exception as e:
			QMessageBox.warning(self, _("Warning"), _("Could not verify current system language:\n") + str(e))

		locale_line = f"{base_lang_code}.UTF-8 UTF-8"
		cmd = (
			'pkexec bash -c "'
			f"sed -i 's/^#\\s*{locale_line}/{locale_line}/' /etc/locale.gen && "
			"locale-gen && "
			f"localectl set-locale LANG={base_lang_code}.UTF-8"
			'"'
		)

		try:
			process = subprocess.Popen(
				cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
			)
			stdout, stderr = process.communicate()

			if process.returncode == 0:
				QMessageBox.information(
					self,
					_("Success"),
					_("System language changed successfully. Please restart your system to apply changes.")
				)
			else:
				error_message = stderr.decode().strip()
				QMessageBox.critical(self, _("Error"), _("Failed to apply system language:\n") + error_message)

		except FileNotFoundError:
			QMessageBox.critical(self, _("Error"), _("Required system tools not found. Please ensure 'pkexec', 'sed', and 'locale-gen' are installed."))
		except Exception as e:
			QMessageBox.critical(self, _("Error"), _("An unexpected error occurred:\n") + str(e))

	def open_url(self, url):
		webbrowser.open(url)

	def run_terminal_cmd(self, command, title=_("Running Command")):
		try:
			subprocess.Popen([
				"xfce4-terminal",
				"--hold",
				"--title", title,
				"--command",
				f"bash -ic '{command}; echo; echo Press Enter to exit...; read'"
			])
		except FileNotFoundError:
			QMessageBox.critical(self, _("Error"), _("xfce4-terminal is not installed. Please install xfce4-terminal."))

	def _execute_command(self, command, dialog):
		process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = process.communicate()
		dialog.close()
		if process.returncode == 0:
			QMessageBox.information(self, _("Success"), stdout.decode())
		else:
			QMessageBox.critical(self, _("Error"), stderr.decode())

	def check_disk_space(self):
		try:
			total, used, free = shutil.disk_usage("/")
			free_gb = free // (2 ** 30)
			warning_threshold = 10  # GB
			error_threshold = 5  # GB

			self.disk_space_status.setText(f"{free_gb} GB {_('Free')}")
			if free_gb < error_threshold:
				self.disk_space_status.setStyleSheet("font-weight: bold; color: red;")
			elif free_gb < warning_threshold:
				self.disk_space_status.setStyleSheet("font-weight: bold; color: orange;")
			else:
				self.disk_space_status.setStyleSheet("font-weight: bold; color: green;")
		except Exception as e:
			print(f"Error checking disk space: {e}")
			self.disk_space_status.setText(_("N/A"))

	def update_system_info(self):
		processor_info = None
		if platform.system() == "Linux":
			try:
				with open("/proc/cpuinfo", "r") as f:
					for line in f:
						if "model name" in line:
							processor_info = line.split(":")[1].strip()
							break
			except FileNotFoundError:
				print("Error: /proc/cpuinfo not found.")
			except Exception as e:
				print(f"Error reading /proc/cpuinfo: {e}")

		if not processor_info:
			processor_info = platform.processor() or _("N/A")

		self.processor_info.setText(processor_info)

		# Memory Info
		try:
			mem = psutil.virtual_memory()
			total_memory_gb = round(mem.total / (1024 ** 3), 2)
			self.memory_info.setText(f"{total_memory_gb} GB")
		except Exception as e:
			print(f"Error getting memory info: {e}")
			self.memory_info.setText(_("N/A"))

	def retranslate_ui(self):
		self.setWindowTitle(_("Welcome to Helwan Linux"))
		self.tabs.setTabText(0, _("Welcome"))
		self.tabs.setTabText(1, _("System Cleaner"))
		
		# تحديث عنوان تبويب مجموعات البرامج
		if self.tabs.count() > 2: # تأكد أن التبويب موجود
			self.tabs.setTabText(2, _("Software Groups"))

		if self.app_lang_label:
			self.app_lang_label.setText(_("Application Language:"))
		if self.startup_check:
			self.startup_check.setText(_("Show on startup"))
		if self.pacman_btn_bottom:
			self.pacman_btn_bottom.setText(_("Update System (Pacman)"))
		if self.yay_btn_bottom:
			self.yay_btn_bottom.setText(_("Update System (Yay)"))
			if not self.is_yay_installed():
				self.yay_btn_bottom.setToolTip(_("Yay is not installed."))
			else:
				self.yay_btn_bottom.setToolTip("")
		if self.install_lts_btn:
			self.install_lts_btn.setText(_("Install Linux LTS"))
		if self.install_zen_btn:
			self.install_zen_btn.setText(_("Install Linux Zen"))
		if self.sys_lang_label:
			self.sys_lang_label.setText(_("System Language:"))
		if self.apply_lang_btn:
			self.apply_lang_btn.setText(_("Apply System Language"))
		if self.docs_btn:
			self.docs_btn.setText(_("Open Documentation"))
		if self.youtube_btn:
			self.youtube_btn.setText(_("Open YouTube Channel"))
		if self.system_info_group:
			self.system_info_group.setTitle(_("System Information"))
		if self.disk_space_label:
			self.disk_space_label.setText(_("Available Disk Space:"))
		if self.processor_label:
			self.processor_label.setText(_("Processor:"))
		if self.memory_label:
			self.memory_label.setText(_("RAM:"))
		if self.neofetch_btn:
			self.neofetch_btn.setText(_("Show System Info Details"))
		if self.htop_btn:
			self.htop_btn.setText(_("Performance Monitor"))
		if self.theme_label:
			self.theme_label.setText(_("Application Theme:"))
		self.greeting.setText(
			_("Welcome to the world of Helwan Linux! ❤️\nWe are here to help you build your dreams on the strongest foundation!"))
		
		cleaner_group = self.findChild(QGroupBox, "Pacman Cleaner")
		if cleaner_group:
			cleaner_group.setTitle(_("Pacman Cleaner"))
			clean_cache_check = self.findChild(QCheckBox, "clean_pacman_cache_full_check")
			if clean_cache_check:
				clean_cache_check.setText(
					_("Clean Pacman Cache (Full) - Warning! This will remove all downloaded packages."))
			remove_orphan_check = self.findChild(QCheckBox, "remove_orphan_packages_check")
			if remove_orphan_check:
				remove_orphan_check.setText(
					_("Remove Orphan Packages - Packages that are no longer required by any installed package."))
			clean_paccache_keep_check = self.findChild(QCheckBox, "clean_paccache_keep_two_check")
			if clean_paccache_keep_check:
				clean_paccache_keep_check.setText(_("Clean Old Packages (Keep Last 2 Versions)"))
			clean_uninstalled_check = self.findChild(QCheckBox, "clean_paccache_uninstalled_check")
			if clean_uninstalled_check:
				clean_uninstalled_check.setText(_("Remove Uninstalled Packages from Cache"))
			run_cleanup_button = self.findChild(QPushButton, "run_pacman_cleanup_button")
			if run_cleanup_button:
				run_cleanup_button.setText(_("Run Pacman Cleanup"))

		# تحديث عناصر تبويب مجموعات البرامج
		software_group_box = self.findChild(QGroupBox, "Software Groups Installer")
		if software_group_box:
			software_group_box.setTitle(_("Software Groups Installer"))

			# تحديث أزرار تبويب مجموعات البرامج
			dev_btn = self.findChild(QPushButton, "dev_tools_button")
			if dev_btn:
				dev_btn.setText(_("Install Development Tools"))

			prog_btn = self.findChild(QPushButton, "prog_lang_button")
			if prog_btn:
				prog_btn.setText(_("Install Programming Languages"))

			multimedia_btn = self.findChild(QPushButton, "multimedia_suite_button")
			if multimedia_btn:
				multimedia_btn.setText(_("Install Multimedia Suite"))

			internet_btn = self.findChild(QPushButton, "internet_tools_button")
			if internet_btn:
				internet_btn.setText(_("Install Internet Tools"))

			office_btn = self.findChild(QPushButton, "office_suite_button")
			if office_btn:
				office_btn.setText(_("Install Office Suite"))

			gaming_btn = self.findChild(QPushButton, "gaming_tools_button")
			if gaming_btn:
				gaming_btn.setText(_("Install Gaming Tools"))

			docker_btn = self.findChild(QPushButton, "docker_tools_button")
			if docker_btn:
				docker_btn.setText(_("Install Docker Tools"))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = WelcomeApp()
	window.show()
	sys.exit(app.exec_())
