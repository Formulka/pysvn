@echo off
rem figure out where we are
for %%I in ( %0\..\.. ) do set WORKDIR=%%~fI

set PY_MAJ=2
if not "%1" == "" set PY_MAJ=%1
set PY_MIN=6
if not "%2" == "" set PY_MIN=%2
if not "%3" == "" set BUILD_TYPE=%3
if not "%4" == "" set SVN_VER_MAJ_MIN=%4

if "%BUILD_TYPE%" == "" set /p BUILD_TYPE="Build type (Release): "
if "%BUILD_TYPE%" == "" set BUILD_TYPE=Release


if "%SVN_VER_MAJ_MIN%" == "" set /p SVN_VER_MAJ_MIN="Build Version (1.6): "
if "%SVN_VER_MAJ_MIN%" == "" set SVN_VER_MAJ_MIN=1.6

if "%SVN_VER_MAJ_MIN%" == "1.4" set SVN_VER_MAJ_DASH_MIN=1-4
if "%SVN_VER_MAJ_MIN%" == "1.5" set SVN_VER_MAJ_DASH_MIN=1-5
if "%SVN_VER_MAJ_MIN%" == "1.6" set SVN_VER_MAJ_DASH_MIN=1-6


rem Save CWD
pushd .

rem in development the version info can be found
rem otherwise the builder will have run it already
if "%PY_MAJ%.%PY_MIN%" == "2.4" set COMPILER=msvc71
if "%PY_MAJ%.%PY_MIN%" == "2.5" set COMPILER=msvc71
if "%PY_MAJ%.%PY_MIN%" == "2.6" set COMPILER=msvc90
if "%PY_MAJ%.%PY_MIN%" == "2.7" set COMPILER=msvc90
if "%PY_MAJ%.%PY_MIN%" == "3.0" set COMPILER=msvc90
if "%PY_MAJ%.%PY_MIN%" == "3.1" set COMPILER=msvc90

if exist ..\..\ReleaseEngineering\win32-%COMPILER%\software-versions-%SVN_VER_MAJ_MIN%.cmd (
    pushd ..\..\ReleaseEngineering\win32-%COMPILER%
    call software-versions-%SVN_VER_MAJ_MIN%.cmd off
    popd
    )

if "%PY_MAJ%" == "2" set PYCXX_VER=%PY2CXX_VER%
if "%PY_MAJ%" == "3" set PYCXX_VER=%PY3CXX_VER%

set PYCXX=%WORKDIR%\Import\pycxx-%PYCXX_VER%
set OPENSSL=%TARGET%\openssl-%OPENSSL_VER%
set SUBVERSION=%TARGET%\subversion-%SVN_VER%
set APR=%SUBVERSION%
set PY=c:\python%PY_MAJ%%PY_MIN%
set PYLIB=python%PY_MAJ%%PY_MIN%
set PYTHONPATH=%WORKDIR%\Source
set PYTHON=%PY%\python.exe
set PYSVNMODULE=_pysvn_%PY_MAJ%_%PY_MIN%.pyd
if "%PY_MAJ%" == "2" set PYSVN_INIT_FUNCTION=init_pysvn
if "%PY_MAJ%" == "3" set PYSVN_INIT_FUNCTION=PyInit__pysvn

rem Need python and SVN on the path
PATH %PY%;%SUBVERSION%\%BUILD_TYPE%\bin;%PATH%

rem prove the python version selected
python -c "import sys;print( 'Info: Python Version %%s' %% sys.version )"

rem restore original CWD
popd
