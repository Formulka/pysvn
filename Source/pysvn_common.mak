#
#	pysvn_common.mak
#
#	include this mak file after defining the variables it needs
#
CXX_OBJECTS=cxxsupport.o cxx_extensions.o cxxextensions.o IndirectPythonInterface.o
PYSVN_OBJECTS=pysvn.o pysvn_callbacks.o pysvn_client.o pysvn_static_strings.o \
	pysvn_enum_string.o \
	pysvn_client_cmd_add.o \
	pysvn_client_cmd_changelist.o \
	pysvn_client_cmd_checkin.o \
	pysvn_client_cmd_copy.o \
	pysvn_client_cmd_diff.o \
	pysvn_client_cmd_export.o \
	pysvn_client_cmd_info.o \
	pysvn_client_cmd_list.o \
	pysvn_client_cmd_lock.o \
	pysvn_client_cmd_merge.o \
	pysvn_client_cmd_prop.o \
	pysvn_client_cmd_revprop.o \
	pysvn_client_cmd_switch.o \
	pysvn_transaction.o pysvn_revision.o pysvn_docs.o pysvn_path.o \
	pysvn_arg_processing.o pysvn_converters.o pysvn_svnenv.o pysvn_profile.o
PYSVN_INCLUDES=pysvn.hpp pysvn_docs.hpp pysvn_svnenv.hpp pysvn_static_strings.hpp
all: pysvn/__init__.py pysvn/%(pysvn_module_name)s

pysvn/__init__.py : pysvn/__init__.py.template generate_svn_error_codes/generate_svn_error_codes
	$(PYTHON) -u create__init__.py pysvn/__init__.py.template pysvn/__init__.py generate_svn_error_codes/generate_svn_error_codes %(pysvn_module_name)s

generate_svn_error_codes/generate_svn_error_codes: generate_svn_error_codes/generate_svn_error_codes.cpp generate_svn_error_codes/create_svn_error_codes_hpp.py
	$(PYTHON) -u generate_svn_error_codes/create_svn_error_codes_hpp.py $(SVN_INCLUDE)
	$(CCC) $(CCCFLAGS) generate_svn_error_codes/generate_svn_error_codes.cpp -o generate_svn_error_codes/generate_svn_error_codes

pysvn/%(pysvn_module_name)s: $(PYSVN_OBJECTS) $(CXX_OBJECTS)
	@echo Compile $@
	$(LDSHARED) -o $@ $(PYSVN_OBJECTS) $(CXX_OBJECTS) $(LDLIBS)

pysvn.o: pysvn.cpp $(PYSVN_INCLUDES) pysvn_version.hpp
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_version.hpp: pysvn_version.hpp.template
	@echo Compile $@
	$(PYTHON) -u ../Builder/brand_version.py ../Builder/version.info pysvn_version.hpp.template

pysvn_docs.hpp: pysvn_docs.cpp
	@echo Compile $@
	touch pysvn_docs.hpp

pysvn_docs.cpp: ../Docs/pysvn_prog_ref.html ../Docs/generate_cpp_docs_from_html_docs.py
	@echo Compile $@
	$(PYTHON) -u ../Docs/generate_cpp_docs_from_html_docs.py $(SVN_INCLUDE) ../Docs/pysvn_prog_ref.html pysvn_docs.hpp pysvn_docs.cpp

pysvn_callbacks.o: pysvn_callbacks.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client.o: pysvn_client.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_static_strings.o: pysvn_static_strings.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_add.o: pysvn_client_cmd_add.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_changelist.o: pysvn_client_cmd_changelist.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_checkin.o: pysvn_client_cmd_checkin.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_copy.o: pysvn_client_cmd_copy.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_diff.o: pysvn_client_cmd_diff.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_export.o: pysvn_client_cmd_export.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_info.o: pysvn_client_cmd_info.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_list.o: pysvn_client_cmd_list.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_lock.o: pysvn_client_cmd_lock.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_merge.o: pysvn_client_cmd_merge.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_prop.o: pysvn_client_cmd_prop.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_revprop.o: pysvn_client_cmd_revprop.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_client_cmd_switch.o: pysvn_client_cmd_switch.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_transaction.o: pysvn_transaction.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_enum_string.o: pysvn_enum_string.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_docs.o: pysvn_docs.cpp
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_path.o: pysvn_path.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_revision.o: pysvn_revision.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_arg_processing.o: pysvn_arg_processing.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_converters.o: pysvn_converters.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_svnenv.o: pysvn_svnenv.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

pysvn_profile.o: pysvn_profile.cpp $(PYSVN_INCLUDES)
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

cxxsupport.o: $(PYCXXSRC)/cxxsupport.cxx
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

cxx_extensions.o: $(PYCXXSRC)/cxx_extensions.cxx
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $<

cxxextensions.o: $(PYCXXSRC)/cxxextensions.c
	@echo Compile $@
	$(CC) -c $(CCFLAGS) -o $@ $<

IndirectPythonInterface.o: $(PYCXXSRC)/IndirectPythonInterface.cxx
	@echo Compile $@
	$(CCC) -c $(CCCFLAGS) -o $@ $< 

clean:
	rm -f pysvn_version.hpp
	rm -f pysvn_docs.hpp pysvn_docs.cpp
	rm -f *.o
	rm -f pysvn/__init__.py
	rm -f pysvn/__init__.pyc
	rm -f pysvn/*.so
	rm -f generate_svn_error_codes/generate_svn_error_codes
	rm -f generate_svn_error_codes/generate_svn_error_codes.hpp
	rm -f generate_svn_error_codes/generate_svn_error_codes.o

test: pysvn/__init__.py pysvn/%(pysvn_module_name)s
	PYTHONPATH=. $(PYTHON) -c "import pysvn;print( pysvn );print( pysvn.version );print( pysvn.svn_version );print( pysvn.Client() )"

DISTDIR=$(shell python -c "import os; print os.path.abspath(os.path.join(os.curdir, '..', 'dist'))")
egg: pysvn/%(pysvn_module_name)s
	mkdir -p dist/EGG-INFO
	mkdir -p $(DISTDIR)
	cp -rvf pysvn dist
	cp -rvf ../pysvn.egg-info/* dist/EGG-INFO
	find dist/ | sed 's:dist/::' > dist/EGG-INFO/SOURCES.txt
	rm -f $(DISTDIR)/pysvn-%(pysvn_version)s-py%(python_version)s-%(python_platform)s.egg
	(cd dist ; zip -r $(DISTDIR)/pysvn-%(pysvn_version)s-py%(python_version)s-%(python_platform)s.egg *)
	rm -rf dist
