[app]

title = TR Martins Jarvis
package.name = trmartinsjarvis
package.domain = org.trmartins

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,CAMERA

android.api = 35
android.minapi = 23
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]

log_level = 2
warn_on_root = 1
