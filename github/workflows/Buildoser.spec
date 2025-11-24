[app]
title = SGA Agents
package.name = sga
package.domain = org.nabil

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt,xlsx,xls,db

version = 1.0
requirements = python3,kivy,pandas,openpyxl,xlrd,tabulate

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

orientation = portrait

[buildozer]
log_level = 2
