@echo off

set x=None

@for /f "usebackq tokens=1,*" %%i in (`netsh WLAN show interfaces`) do (

  if [%%i]==[SSID] set x=%%j

)

set x=%x: =%
echo %x%
