#!/bin/echo Usage: . $0

# default to highest version we can find if no value in $1 and $2
if [ ! -z "$1" ]
then
    PREF_VER=$1.$2
else
    PREF_VER=2.7
fi

for PY_VER in ${PREF_VER} 2.7 2.6
do
    # used in pick python to use in Builder driver makefile
    export PYTHON=$( which python${PY_VER} )
    if [ -e "${PYTHON}" ]
    then
        break
    fi
done
unset PREF_VER

if [ -e "${PYTHON}" ]
then
    # prove the python version selected is as expected
    ${PYTHON} -c "import sys;print( 'Info: Python Version %r' % sys.version )"
else
    echo "Error: Cannot find python${PREF_VER} on the PATH"
fi
