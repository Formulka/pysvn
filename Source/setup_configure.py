#
# ====================================================================
# Copyright (c) 2005-2010 Barry A Scott.  All rights reserved.
#
# This software is licensed as described in the file LICENSE.txt,
# which you should have received as part of this distribution.
#
# ====================================================================
#
#
#   setup_configure.py
#
#   make it easy to build pysvn outside of svn
#
import sys
import os
import distutils
import distutils.sysconfig
import distutils.util

import xml.dom.minidom
import xml.sax

class SetupError(Exception):
    pass

# version of PyCXX that we require
pycxx_version = (6, 2, 2)


all_options_info = {
    '--arch':               (2, '<arch>'),
    '--apr-inc-dir':        (1, '<dir>'),
    '--apr-lib-dir':        (1, '<dir>'),
    '--define':             (2, '<define-string>'),
    '--enable-debug':       (0, None),
    '--fixed-module-name':  (0, None),
    '--norpath':            (0, None),
    '--platform':           (1, '<platform-name>'),
    '--pycxx-dir':          (1, '<dir>'),
    '--pycxx-src-dir':      (1, '<dir>'),
    '--svn-inc-dir':        (1, '<dir>'),
    '--svn-lib-dir':        (1, '<dir>'),
    '--svn-bin-dir':        (1, '<dir>'),
    '--svn-root-dir':       (1, '<dir>'),
    '--verbose':            (0, None),
    }

def cmd_configure( argv ):
    if sys.platform == 'win32':
        print( 'Error: Works for Unix like systems only' )
        return 1

    try:
        creater = MakeFileCreater()
        return creater.createMakefile( argv )

    except SetupError as e:
        print( 'Error:',str(e) )
        return 1

def cmd_help( argv ):
    progname = os.path.basename( argv[0] )
    print( '''    Create a makefile for this python and platform

        python %(progname)s configure <options>

    where <options> is one or more of:
''' % {'progname': progname} )
    for option, num_value in sorted( all_options_info.items() ):
        num, value = num_value
        if num == 0:
            print( '        %s' % (option,) )
        else:
            print( '        %s=%s' % (option,value) )

    return 1

class MakeFileCreater:
    def __init__( self ):
        self.verbose = False
        self.is_mac_os_x = False
        self.is_mac_os_x_fink = False
        self.is_mac_os_x_darwin_ports = False
        self.mac_os_x_version = None
        self.mac_os_x_arch = False
        self.mac_os_x_sdk = None
        self.platform = sys.platform

        self.__all_options = {}
        self.__used_options = set()

    def node_text( self, all_nodes ):
        all_text = []
        for node in all_nodes:
            if node.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                all_text.append( node.data )
        return ''.join( all_text )

    def is_atleast_mac_os_x_version( self, version ):
        return self.mac_os_x_version[0:len(version)] >= list(version)

    def detectMacVersion( self ):
        if os.path.exists( '/System/Library/CoreServices/SystemVersion.plist' ):
            dom = xml.dom.minidom.parse( open( '/System/Library/CoreServices/SystemVersion.plist' ) )
            plist = dom.getElementsByTagName( 'plist' )[0]
            plist_dict = plist.getElementsByTagName( 'dict' )[0]
            for key_or_value in plist_dict.childNodes:
                if key_or_value.nodeName == 'key' and self.node_text( key_or_value.childNodes ) == 'ProductVersion':
                    value_node = key_or_value.nextSibling
                    while value_node.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                        value_node = value_node.nextSibling

                    self.mac_os_x_version_string = self.node_text( value_node.childNodes )
                    if self.verbose:
                        print( 'Info: Mac OS X Version %s' % self.mac_os_x_version_string )
                    self.mac_os_x_version = [int(s) for s in self.mac_os_x_version_string.split('.')]
                    self.is_mac_os_x = True

                    # look for the universal SDK
                    for mac_ver in ['10.5', '%d.%d' % (self.mac_os_x_version[0], self.mac_os_x_version[1])]:
                        self.mac_os_x_sdk = '/Developer/SDKs/MacOSX%s.sdk' % mac_ver
                        if os.path.exists( self.mac_os_x_sdk ):
                            print( 'Info: Mac OS X Universal SDKs found (%s)' % self.mac_os_x_sdk )
                            break

    def parseOptions( self, argv ):
        for option in argv:
            option_parts = option.split( '=', 1 )
            option_name = option_parts[0]
            if option_name not in all_options_info:
                print( 'Error: Unknown option %s' % option )
                return False

            repeat_count, value = all_options_info[ option_name ]
            if repeat_count == 0:
                if len(option_parts) != 1:
                    print( 'Error: Option %s does not take a value' % (option_name,) )
                    return False

                self.__all_options[ option_name ] = None

            elif repeat_count == 1:
                if len(option_parts) != 2:
                    print( 'Error: Option %s requires a value' % (option_name,) )
                    return False

                if option_name in self.__all_options:
                    print( 'Error: only one %s is allowed' % (option_name,) )
                    return False

                self.__all_options[ option_name ] = option_parts[1]

            elif repeat_count == 2:
                if len(option_parts) != 2:
                    print( 'Error: Option %s requires a value' % (option_name,) )
                    return False

                self.__all_options.setdefault( option_name, [] ).append( option_parts[1] )

        return True

    def hasOption( self, option_name ):
        self.__used_options.add( option_name )
        return option_name in self.__all_options

    def getOption( self, option_name ):
        self.__used_options.add( option_name )
        return self.__all_options[ option_name ]

    def checkAllOptionsUsed( self ):
        all_options = set( self.__all_options )
        unused_options = all_options - self.__used_options
        if len(unused_options) > 0:
            print( 'Error: Unused options: %s' % (', '.join( unused_options ),) )
            return False

        return True

    def createMakefile( self, _argv ):
        if not self.parseOptions( _argv[2:] ):
            return 1

        if self.hasOption( '--platform' ):
            self.platform = self.getOption( '--platform' )
            print( 'Info: Platform overridden as %s' % self.platform )

        self.verbose = self.hasOption( '--verbose' )
        self.detectMacVersion()

        if self.is_mac_os_x and self.hasOption( '--arch' ):
            print( 'Info: Building for arch %s' % ', '.join( self.getOption( '--arch' ) ) )
            self.mac_os_x_arch = ' '.join( ['-arch %s' % (arch,) for arch in self.getOption( '--arch' )] )
        else:
            self.mac_os_x_arch = ''

        if self.verbose:
            print( 'Info: Creating makefile for python %r on %s' % (sys.version_info, self.platform) )

        debug_cflags_list = []
        if self.hasOption( '--enable-debug' ):
            print( 'Info: Enabling debug' )
            debug_cflags_list.append( '-g' )

        include_dir_list = []

        # add pycxx include
        pycxx_dir = self.find_pycxx()
        include_dir_list.append( pycxx_dir )
        # add pycxx source
        pycxx_src_dir = self.find_pycxx_src( pycxx_dir )
        include_dir_list.append( pycxx_src_dir )

        # must add python after pyxx because some distributions have pycxx inside of the
        # python include dir

        # add python include dirs
        include_dir_list.append( distutils.sysconfig.get_python_inc() )
        if distutils.sysconfig.get_python_inc() != distutils.sysconfig.get_python_inc( True ):
            include_dir_list.append( distutils.sysconfig.get_python_inc( True ) )
        print( 'Info: Found Python include in %s' % ' '.join( include_dir_list ) )

        # add SVN include
        svn_include = self.find_svn_inc()
        include_dir_list.append( svn_include )
        # add APR include
        include_dir_list.append( self.find_apr_inc() )

        # add source dir
        include_dir_list.append( '.' )

        # get the python CFLAGS
        py_cflags_python_list = distutils.sysconfig.get_config_var('CFLAGS').split()
        # we only want the -D flags, other flags have broken pysvn
        py_cflags_list = []
        for flag in py_cflags_python_list:
            if flag.startswith( '-D' ):
                py_cflags_list.append( flag )

        # add platform specific defines
        if self.is_mac_os_x:
            py_cflags_list.append( '-DDARWIN' )

        # need PyCXX to 2TO3 backwards compatibility mode
        py_cflags_list.append( '-DPYCXX_PYTHON_2TO3' )

        # get user supplied defines
        if self.hasOption( '--define' ):
            for define in self.getOption( '--define' ):
                py_cflags_list.append( '-D%s' % (define,) )

        module_type = '.so'
        if self.platform == 'cygwin':
            module_type = '.dll'

        if self.hasOption( '--fixed-module-name' ):
            print( 'Info: Using fixed module name' )
            pysvn_module_name = '_pysvn'+ module_type

        else:
            # name of the module including the python version to help
            # ensure that only a matching _pysvn.so for the version of
            # python is imported
            pysvn_module_name = '_pysvn_%d_%d%s' % (sys.version_info[0], sys.version_info[1], module_type)
            if sys.version_info[0] >= 3:
                py_cflags_list.append( '-DPyInit__pysvn=PyInit__pysvn_%d_%d' % sys.version_info[:2] )
                py_cflags_list.append( '-DPyInit__pysvn_d=PyInit__pysvn_%d_%d_d' % sys.version_info[:2] )
            else:
                py_cflags_list.append( '-Dinit_pysvn=init_pysvn_%d_%d' % sys.version_info[:2] )
                py_cflags_list.append( '-Dinit_pysvn_d=init_pysvn_%d_%d_d' % sys.version_info[:2] )


        pysvn_version_info = {}
        f = open( '../Builder/version.info', 'r' )
        for line in f:
            key, value = line.strip().split('=')
            pysvn_version_info[ key ] = value

        template_values = {
            'pysvn_module_name': pysvn_module_name,

            # python executable
            'python_exe':       sys.executable,

            # includes
            'svn_include':      svn_include,
            'includes':         ' '.join( ['-I%s' % include_dir for include_dir in include_dir_list] ),

            # debug_cflags
            'debug_cflags':     ' '.join( debug_cflags_list ),
            
            # py_cflags
            'py_cflags':        ' '.join( py_cflags_list ),

            # add svn bin dir
            'svn_bin_dir':      self.find_svn_bin(),

            # add svn lib dir
            'svn_lib_dir':      self.find_svn_lib(),

            # add apr lib dir
            'apr_lib_dir':      self.find_apr_lib(),

            'lib_apr':          self.lib_apr,    # set as a side effect of find_apr_lib

            # pycxx src dir
            'pycxx_dir':        pycxx_dir,

            # pycxx src dir
            'pycxx_src_dir':    pycxx_src_dir,

            # python version:
            'python_version':   '%d.%d' % (sys.version_info[0], sys.version_info[1]),

            # python platform:
            'python_platform':  distutils.util.get_platform(),

            # pysvn version:
            'pysvn_version':    '%(MAJOR)s.%(MINOR)s.%(PATCH)s' % pysvn_version_info,

            # mac arch options
            'mac_os_x_arch':    self.mac_os_x_arch
            }

        if not self.checkAllOptionsUsed():
            return 1

        print( 'Info: Creating Makefile for Source' )

        major, minor, patch = self.getSvnVersion( svn_include )
        template_values[ 'svn_version_maj_min' ] = '%d.%d' % (major, minor)
        template_values[ 'py_version_maj' ] = '%d' % (sys.version_info[0],)

        makefile = open( 'Makefile', 'w' )
        if self.platform == 'darwin' and self.is_mac_os_x:
            # need to figure out the framework dir to use otherwise the latest
            # python framework will be used and not the one matching this python
            var_prefix = distutils.sysconfig.get_config_var('prefix')
            var_ldlibrary = distutils.sysconfig.get_config_var('LDLIBRARY')
            framework_lib = os.path.join( var_prefix, os.path.basename( var_ldlibrary ) )

            if self.is_atleast_mac_os_x_version( (10,5) ) >= 0:
                if self.verbose:
                    print( 'Info: Using Mac OS X 10.5 makefile template' )

                template_values['extra_libs'] = ''
                template_values['frameworks'] = '-framework System %s -framework CoreFoundation -framework Kerberos -framework Security' % framework_lib

            elif self.is_atleast_mac_os_x_version( (10,4) ) >= 0:
                if self.verbose:
                    print( 'Info: Using Mac OS X 10.4 makefile template' )

                # 10.4 needs the libintl.a but 10.3 does not
                template_values['extra_libs'] = '%(svn_lib_dir)s/libintl.a' % template_values
                template_values['frameworks'] = '-framework System %s -framework CoreFoundation -framework Kerberos -framework Security' % framework_lib

            else:
                if self.verbose:
                    print( 'Info: Using Mac OS X 10.3 makefile template' )

                template_values['extra_libs'] = ''
                template_values['frameworks'] = '-framework System %s -framework CoreFoundation' % framework_lib

            if self.is_mac_os_x_fink:
                makefile.write( self.makefile_template_macosx_fink % template_values )

            elif self.is_mac_os_x_darwin_ports:
                makefile.write( self.makefile_template_macosx_darwin_ports % template_values )

            else:
                if sys.version_info[0] >= 3:
                    makefile.write( self.makefile_template_macosx_one_arch_py3 % template_values )
                else:
                    makefile.write( self.makefile_template_macosx_one_arch_py2 % template_values )

        elif self.platform.startswith('aix'):
            if self.verbose:
                print( 'Info: Using AIX makefile template' )
            for path in sys.path:
                python_exp = os.path.join(path, 'config', 'python.exp')
                if os.path.exists(python_exp):
                    template_values['python_exp'] = python_exp
                    break
            else:
                python_exp = os.path.abspath(os.path.join(sys.executable, os.path.pardir, os.path.pardir, 
                                                          'lib', 'python2.4', 'config', 'python.exp'))
                if os.path.exists(python_exp):
                    template_values['python_exp'] = python_exp
                else:
                    template_values['python_exp'] = 'python.exp'
            makefile.write( self.makefile_template_aix % template_values )

        elif self.platform.startswith('sunos5'):
            if self.verbose:
                print( 'Info: Using Sun OS 5 makefile template' )
            makefile.write( self.makefile_template_sunos5 % template_values )

        elif self.platform.startswith('linux'):
            if self.verbose:
                print( 'Info: Using Linux makefile template' )
            if self.hasOption( '--norpath' ):
                makefile.write( self.makefile_template_linux_norpath % template_values )
            else:
                makefile.write( self.makefile_template_linux % template_values )

        elif self.platform.startswith('freebsd'):
            if self.verbose:
                print( 'Info: Using FreeBSD makefile template' )
            makefile.write( self.makefile_template_freebsd % template_values )

        elif self.platform == 'cygwin':
            if self.verbose:
                print( 'Info: Using Cygwin makefile template' )
            makefile.write( self.makefile_template_cygwin % template_values )


        else:
            if self.verbose:
                print( 'Info: Using unix makefile template' )
            makefile.write( self.makefile_template % template_values )

        f = open( 'pysvn_common.mak', 'r' )
        makefile.write( f.read() % template_values )
        f.close()
        makefile.close()

        print( 'Info: Creating Makefile for Tests' )

        makefile = open( '../Tests/Makefile', 'w' )
        makefile.write( self.makefile_tests_template % template_values )
        f = open( '../Tests/pysvn_test_common.mak', 'r' )
        makefile.write( f.read() )
        f.close()
        makefile.close()


    makefile_tests_template = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_tests_template --
#
PYTHON=%(python_exe)s
SVN_VERSION_MAJ_MIN=%(svn_version_maj_min)s
PY_VERSION_MAJ=%(py_version_maj)s
SVN_BIN_DIR=%(svn_bin_dir)s
#include pysvn_test_common.mak
'''

    makefile_template = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s -Wl,--rpath -Wl,%(svn_lib_dir)s \
-lsvn_client-1 \
-lsvn_diff-1 \
-lsvn_repos-1 \
 -lcom_err -lresolv -lexpat -lneon

#include pysvn_common.mak
'''

    makefile_template_sunos5 = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s -Wl,--rpath -Wl,%(svn_lib_dir)s \
-lsvn_client-1 \
-lsvn_diff-1 \
-lsvn_repos-1 \
 -lresolv -lexpat -lneon

#include pysvn_common.mak
'''

    makefile_template_linux = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_linux --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s -Wl,--rpath -Wl,%(svn_lib_dir)s \
-lsvn_client-1 \
-lsvn_diff-1 \
-lsvn_repos-1 \
-lcom_err -lresolv -lexpat -lssl
PYSVN_CREATE_INIT_OPTION=%(pysvn_module_name)s

#include pysvn_common.mak
'''

    makefile_template_linux_norpath = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_linux --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s \
-lsvn_client-1 \
-lsvn_diff-1 \
-lsvn_repos-1 \
-lcom_err -lresolv -lexpat -lneon -lssl
PYSVN_CREATE_INIT_OPTION=%(pysvn_module_name)s

#include pysvn_common.mak
'''

    makefile_template_freebsd = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_freebsd --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s -Wl,--rpath -Wl,/usr/lib:/usr/local/lib:%(svn_lib_dir)s \
-lsvn_client-1 \
-lsvn_diff-1 \
-lsvn_repos-1

.if exists(/usr/lib/libkrb5.so)
LDLIBS+=-lkrb5
.endif
LDLIBS+=-lcom_err -lexpat -lneon

#include pysvn_common.mak
'''

    makefile_template_cygwin = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_cygwin --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s \
-L/usr/lib/python2.5/config -lpython2.5.dll \
-lsvn_client-1   \
-lsvn_repos-1    \
-lsvn_subr-1     \
-lsvn_delta-1    \
-lsvn_fs_fs-1    \
-lsvn_fs-1       \
-lsvn_ra_svn-1   \
-lsvn_repos-1    \
-lsvn_ra_local-1 \
-lsvn_diff-1     \
-lsvn_ra-1       \
-lsvn_wc-1       \
-lapr-1          \
-laprutil-1      \
-liconv          \
-lexpat          \
-lpthread        \
-lz              \


#include pysvn_common.mak
'''

    makefile_template_aix = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_aix --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -shared %(debug_cflags)s
LDLIBS=-L%(svn_lib_dir)s \
-lsvn_client-1   \
-lsvn_repos-1    \
-lsvn_subr-1     \
-lsvn_delta-1    \
-lsvn_fs_fs-1    \
-lsvn_fs-1       \
-lsvn_ra_svn-1   \
-lsvn_repos-1    \
-lsvn_ra_local-1 \
-lsvn_diff-1     \
-lsvn_ra-1       \
-lsvn_wc-1       \
-lsvn_fs_util-1  \
-lsvn_ra_neon-1  \
-lapr-1          \
-lneon           \
-laprutil-1      \
-liconv          \
-lexpat          \
-lintl           \
-lpthread        \
-lz              \
-Wl,-bI:%(python_exp)s

#include pysvn_common.mak
'''

    makefile_template_macosx_one_arch_py2 = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_macosx_one_arch --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -no-long-double -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s %(mac_os_x_arch)s
CC=gcc
CCFLAGS=-Wall -no-long-double -fPIC %(includes)s %(debug_cflags)s %(mac_os_x_arch)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -bundle %(debug_cflags)s -u _PyMac_Error %(frameworks)s %(mac_os_x_arch)s
LDLIBS=-L%(svn_lib_dir)s \
-L%(apr_lib_dir)s \
-lsvn_client-1 \
-lsvn_repos-1 \
-lsvn_wc-1 \
-lsvn_fs-1 \
-lsvn_subr-1 \
-lsvn_diff-1 \
-l%(lib_apr)s
#include pysvn_common.mak
'''

    makefile_template_macosx_one_arch_py3 = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_macosx_one_arch --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -no-long-double -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s %(mac_os_x_arch)s
CC=gcc
CCFLAGS=-Wall -no-long-double -fPIC %(includes)s %(debug_cflags)s %(mac_os_x_arch)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -bundle %(debug_cflags)s %(frameworks)s %(mac_os_x_arch)s
LDLIBS=-L%(svn_lib_dir)s \
-L%(apr_lib_dir)s \
-lsvn_client-1 \
-lsvn_repos-1 \
-lsvn_wc-1 \
-lsvn_fs-1 \
-lsvn_subr-1 \
-lsvn_diff-1 \
-l%(lib_apr)s
#include pysvn_common.mak
'''

    makefile_template_macosx_fink = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_macosx_fink --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -Wno-long-double -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -Wno-long-double -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -bundle %(debug_cflags)s -u _PyMac_Error %(frameworks)s
LDLIBS= \
%(svn_lib_dir)s/libsvn_client-1.a \
%(svn_lib_dir)s/libsvn_subr-1.a \
%(svn_lib_dir)s/libsvn_wc-1.a \
%(svn_lib_dir)s/libsvn_ra-1.a \
%(svn_lib_dir)s/libsvn_ra_dav-1.a \
%(svn_lib_dir)s/libsvn_ra_local-1.a \
%(svn_lib_dir)s/libsvn_ra_svn-1.a \
%(svn_lib_dir)s/libsvn_delta-1.a \
%(svn_lib_dir)s/libsvn_repos-1.a \
%(svn_lib_dir)s/libsvn_fs-1.a \
%(svn_lib_dir)s/libsvn_fs_fs-1.a \
%(svn_lib_dir)s/libsvn_fs_base-1.a \
%(svn_lib_dir)s/libsvn_diff-1.a \
%(apr_lib_dir)s/libaprutil-0.a \
%(apr_lib_dir)s/libapr-0.a \
%(svn_lib_dir)s/libneon.a \
%(svn_lib_dir)s/libssl.a \
%(svn_lib_dir)s/libcrypto.a \
%(svn_lib_dir)s/libexpat.a \
%(svn_lib_dir)s/libxml2.a \
%(svn_lib_dir)s/libdb-4.3.a \
 -lintl.3 -liconv.2 -lz

#include pysvn_common.mak
'''

    makefile_template_macosx_darwin_ports = '''#
#	Created by pysvn Extension/Source/setup.py
#       -- makefile_template_macosx_darwin_ports --
#
PYTHON=%(python_exe)s
SVN_INCLUDE=%(svn_include)s
CCC=g++
CCCFLAGS=-Wall -Wno-long-double -fPIC -fexceptions -frtti %(includes)s %(py_cflags)s %(debug_cflags)s
CC=gcc
CCFLAGS=-Wall -Wno-long-double -fPIC %(includes)s %(debug_cflags)s
PYCXX=%(pycxx_dir)s
PYCXXSRC=%(pycxx_src_dir)s
LDSHARED=g++ -bundle %(debug_cflags)s -u _PyMac_Error %(frameworks)s
LDLIBS= \
%(svn_lib_dir)s/libsvn_client-1.a \
%(svn_lib_dir)s/libsvn_subr-1.a \
%(svn_lib_dir)s/libsvn_wc-1.a \
%(svn_lib_dir)s/libsvn_ra-1.a \
%(svn_lib_dir)s/libsvn_ra_dav-1.a \
%(svn_lib_dir)s/libsvn_ra_local-1.a \
%(svn_lib_dir)s/libsvn_ra_svn-1.a \
%(svn_lib_dir)s/libsvn_delta-1.a \
%(svn_lib_dir)s/libsvn_fs-1.a \
%(svn_lib_dir)s/libsvn_fs_fs-1.a \
%(svn_lib_dir)s/libsvn_fs_base-1.a \
%(svn_lib_dir)s/libsvn_repos-1.a \
%(svn_lib_dir)s/libsvn_diff-1.a \
%(apr_lib_dir)s/libaprutil-1.a \
%(svn_lib_dir)s/libneon.a \
%(svn_lib_dir)s/libssl.a \
%(svn_lib_dir)s/libcrypto.a \
%(svn_lib_dir)s/libexpat.a \
%(svn_lib_dir)s/libiconv.a \
%(svn_lib_dir)s/libdb-4.3.a \
%(extra_libs)s \
-L%(apr_lib_dir)s \
-l%(lib_apr)s \
-lz

#include pysvn_common.mak
'''

    def find_pycxx( self ):
        pycxx_dir = self.find_dir(
                    'PyCXX include',
                    '--pycxx-dir',
                    None,
                    [
                        '../Import/pycxx-%d.%d.%d' % pycxx_version,
                        distutils.sysconfig.get_python_inc() # typical Linux
                    ],
                    'CXX/Version.hxx' )

        major_match = False
        minor_match = False
        f = open( os.path.join( pycxx_dir, 'CXX/Version.hxx' ) )
        for line in f:
            words = line.split()
            if 'PYCXX_VERSION_MAJOR' in words:
                major_match = int( words[2] ) == pycxx_version[0]
            if 'PYCXX_VERSION_MINOR' in words:
                minor_match = int( words[2] ) == pycxx_version[1]

        if not major_match and not minor_match:
            raise SetupError( 'PyCXX version not as required.' )

        return pycxx_dir

    def find_pycxx_src( self, pycxx_dir ):
        return self.find_dir(
                    'PyCXX Source',
                    '--pycxx-src-dir',
                    None,
                    [
                        '%s/Src' % pycxx_dir,
                        '/usr/share/python%s/CXX' % distutils.sysconfig.get_python_version() # typical Linux
                    ],
                    'cxxsupport.cxx' )

    def find_svn_inc( self ):
        return self.find_dir(
                    'SVN include',
                    '--svn-inc-dir',
                    'include/subversion-1',
                    [
                        '/opt/local/include/subversion-1',      # Darwin - darwin ports
                        '/sw/include/subversion-1',             # Darwin - Fink
                        '/usr/include/subversion-1',            # typical Linux
                        '/usr/local/include/subversion-1',      # typical *BSD
                        '/usr/pkg/include/subversion-1',        # netbsd
                    ],
                    'svn_client.h' )

    def find_svn_bin( self ):
        return self.find_dir(
                    'SVN bin',
                    '--svn-bin-dir',
                    'bin',
                    [
                        '/opt/local/bin',      # Darwin - darwin ports
                        '/sw/bin',             # Darwin - Fink
                        '/usr/bin',            # typical Linux
                        '/usr/local/bin',      # typical *BSD
                        '/usr/pkg/bin',        # netbsd
                    ],
                    'svnadmin' )

    def find_svn_lib( self ):
        dir = self.find_dir(
                    'SVN library',
                    '--svn-lib-dir',
                    'lib',
                    [
                        '/opt/local/lib',                       # Darwin - darwin ports
                        '/sw/lib',                              # Darwin - Fink
                        '/usr/lib64',                           # typical 64bit Linux
                        '/usr/lib',                             # typical Linux
                        '/usr/local/lib64',                     # typical 64bit Linux
                        '/usr/local/lib',                       # typical *BSD
                        '/usr/pkg/lib',                         # netbsd
                    ],
                    self.get_lib_name_for_platform( 'libsvn_client-1' ) )
        # if we are using the Fink SVN then remember this
        self.is_mac_os_x_fink = dir.startswith( '/sw/' )
        self.is_mac_os_x_darwin_ports = dir.startswith( '/opt/local/' )
        return dir

    def find_apr_inc( self ):
        last_exception = None
        for apr_ver in ['apr-1', 'apr-0']:
            try:
                return self.find_dir(
                    'APR include',
                    '--apr-inc-dir',
                    'include/%s' % apr_ver,
                    [
                    ],
                    'apr.h' )
            except SetupError:
                pass

        for apr_ver in ['apr-1.0', 'apr-1', 'apr-0']:
            try:
                return self.find_dir(
                    'APR include',
                    '--apr-inc-dir',
                    None,
                    [
                        '/opt/local/include/%s' % apr_ver,      # Darwin - darwin ports
                        '/sw/include/%s' % apr_ver,             # Darwin - fink
                        '/usr/include/%s' % apr_ver,            # typical Linux
                        '/usr/local/apr/include/%s' % apr_ver,  # Mac OS X www.metissian.com
                        '/usr/pkg/include/%s' % apr_ver,        # netbsd
                        '/usr/include/apache2',                 # alternate Linux
                        '/usr/include/httpd',                   # alternate Linux
                        '/usr/local/include/apr0',              # typical *BSD
                        '/usr/local/include/apache2',           # alternate *BSD
                    ],
                    'apr.h' )
            except SetupError as e:
                last_exception = e
        raise last_exception

    def find_apr_lib( self ):
        last_exception = None
        lib_list = [(self.get_lib_name_for_platform( 'libapr-1' ), 'apr-1'),
                    (self.get_lib_name_for_platform( 'libapr-0' ), 'apr-0')]

        for apr_libname, self.lib_apr in lib_list:
            try:
                return self.find_dir(
                    'APR library',
                    '--apr-lib-dir',
                    'lib',
                    [],
                    apr_libname )
            except SetupError:
                pass

        for apr_libname, self.lib_apr in lib_list:
            try:
                return self.find_dir(
                    'APR library',
                    '--apr-lib-dir',
                    None,
                    [
                        '/opt/local/lib',                       # Darwin - darwin ports
                        '/sw/lib',                              # Darwin - fink
                        '/usr/lib64',                           # typical 64bit Linux
                        '/usr/lib',                             # typical Linux
                        '/usr/local/lib64',                     # typical 64bit Linux
                        '/usr/local/lib',                       # typical *BSD
                        '/usr/local/apr/lib',                   # Mac OS X www.metissian.com
                        '/usr/pkg/lib',                         # netbsd
                    ],
                    apr_libname )
            except SetupError as e:
                last_exception = e
        raise last_exception


    def get_lib_name_for_platform( self, libname ):
        if self.is_mac_os_x:
            return '%s.dylib' % libname
        elif self.platform == 'cygwin':
            return '%s.dll.a' % libname
        else:
            return '%s.so' % libname

    def find_dir( self, name, kw, svn_root_suffix, base_dir_list, check_file ):
        dirname = self.__find_dir( name, kw, svn_root_suffix, base_dir_list, check_file )
        print( 'Info: Found %14.14s in %s' % (name, dirname) )
        return dirname

    def __find_dir( self, name, kw, svn_root_suffix, base_dir_list, check_file ):
        # override the base_dir_list from the command line kw
        svn_root_dir = None

        if self.hasOption( kw ):
            base_dir_list = [self.getOption( kw )]

        elif( self.hasOption( '--svn-root-dir' )
        and svn_root_suffix is not None ):
            base_dir_list = ['%s/%s' % (self.getOption( '--svn-root-dir' ), svn_root_suffix)]

        # expect to find check_file in one of the dir
        for dirname in base_dir_list:
            full_check_file = os.path.join( dirname, check_file )
            if self.verbose:
                print( 'Info: Checking for %s in %s' % (name, full_check_file) )
            if os.path.exists( full_check_file ):
                return os.path.abspath( dirname )

        raise SetupError( 'cannot find %s %s - use %s' % (name, check_file, kw) )

    def getSvnVersion( self, svn_include ):
        all_svn_version_lines = open( os.path.join( svn_include, 'svn_version.h' ) ).readlines()
        major = None
        minor = None
        patch = None
        for line in all_svn_version_lines:
            words = line.strip().split()
            if len(words) > 2 and words[0] == '#define':
                if words[1] == 'SVN_VER_MAJOR':
                    major = int(words[2])
                elif words[1] == 'SVN_VER_MINOR':
                    minor = int(words[2])
                elif words[1] == 'SVN_VER_PATCH':
                    patch = int(words[2])
 
        print( 'Info: Building against SVN %d.%d.%d' % (major, minor, patch) )
        return (major, minor, patch)
