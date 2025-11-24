[app]
title = SGA Agents
package.name = sga
package.domain = org.nabil

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,xlsx,xls,db

version = 1.0
requirements = python3,kivy==2.1.0,pandas==1.3.5,openpyxl==3.0.9,xlrd==2.0.1,tabulate==0.8.9

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

orientation = portrait

[buildozer]
log_level = 2

[app]
android.api = 33
android.minapi = 21
android.sdk = 28
android.ndk = 25b

# Python configuration
python.version = 3
python.requirements = ${app:requirements}

# Buildozer configuration
buildozer.init = true
