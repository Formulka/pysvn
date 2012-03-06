#
#	pysvn_test_common
#
#	include this mak file after defining the variables it needs
#
KNOWN_GOOD_VERSION=py$(PY_VERSION_MAJ)-svn$(SVN_VERSION_MAJ_MIN)
all: test-01.unix.new.log.clean test-04.unix.new.log test-05.unix.new.log test-06.unix.new.log test-07.unix.new.log

# the extra tests rely on having a repos over HTTP.
extratests: test-03.unix.new.log

help:
	@echo "make clean         - clean all tests"
	@echo "make all           - run all tests"
	@echo "make clean-01      - clean test 01"
	@echo "make diff-01       - run wb-diff on the outcome of test 01"
	@echo "make new-01        - use the new log as the known-good log of test 01"

clean: clean-01 clean-03 clean-04 clean-05 clean-06 clean-07

#
#	Helpers while developing and verifying tests
#
test-01.unix.new.log: test-01.sh test-01.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-01
	PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-01.sh >test-01.unix.new.log 2>&1

test-01.unix.new.log.clean: test-01.unix.new.log
	$(PYTHON) benchmark_diff.py test-01.unix.known_good-$(KNOWN_GOOD_VERSION).log test-01.unix.new.log

clean-01:
	-rm -f test-01.unix.new.log
	-rm -f test-01.unix.new.log.clean
	-rm -rf testroot-01

diff-01: test-01.unix.new.log.clean
	wb-diff test-01.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-01.unix.new.log.clean

new-01: test-01.unix.new.log
	cp  test-01.unix.new.log test-01.unix.known_good-$(KNOWN_GOOD_VERSION).log

test-03.unix.new.log: test-03.sh test-03.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-03
	PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-03.sh >test-03.unix.new.log 2>&1
	$(PYTHON) benchmark_diff.py test-03.unix.known_good-$(KNOWN_GOOD_VERSION).log test-03.unix.new.log

clean-03:
	-rm -f test-03.unix.new.log
	-rm -f test-03.unix.new.log.clean
	-rm -rf testroot-03

diff-03: test-03.unix.new.log
	wb-diff test-03.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-03.unix.new.log.clean

new-03: test-03.unix.new.log
	cp  test-03.unix.new.log test-03.unix.known_good-$(KNOWN_GOOD_VERSION).log

test-04.unix.new.log: test-04.sh test-04.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-04
	PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-04.sh >test-04.unix.new.log 2>&1
	$(PYTHON) benchmark_diff.py test-04.unix.known_good-$(KNOWN_GOOD_VERSION).log test-04.unix.new.log

clean-04:
	-rm -f test-04.unix.new.log
	-rm -f test-04.unix.new.log.clean
	-rm -rf testroot-04

diff-04: test-04.unix.new.log
	wb-diff test-04.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-04.unix.new.log.clean

new-04: test-04.unix.new.log
	cp  test-04.unix.new.log test-04.unix.known_good-$(KNOWN_GOOD_VERSION).log

test-05.unix.new.log: test-05.sh test-05.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-05
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 2 1; then PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-05.sh >test-05.unix.new.log 2>&1; fi
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 2 1; then $(PYTHON) benchmark_diff.py test-05.unix.known_good-$(KNOWN_GOOD_VERSION).log test-05.unix.new.log; fi

clean-05:
	-rm -f test-05.unix.new.log
	-rm -f test-05.unix.new.log.clean
	-rm -rf testroot-05

diff-05: test-05.unix.new.log
	wb-diff test-05.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-05.unix.new.log.clean

new-05: test-05.unix.new.log
	cp  test-05.unix.new.log test-05.unix.known_good-$(KNOWN_GOOD_VERSION).log

test-06.unix.new.log: test-06.sh test-06.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-06
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 3 0; then PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-06.sh >test-06.unix.new.log 2>&1; fi
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 3 0; then $(PYTHON) benchmark_diff.py test-06.unix.known_good-$(KNOWN_GOOD_VERSION).log test-06.unix.new.log; fi

clean-06:
	-rm -f test-06.unix.new.log
	-rm -f test-06.unix.new.log.clean
	-rm -rf testroot-06

diff-06: test-06.unix.new.log
	wb-diff test-06.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-06.unix.new.log.clean

new-06: test-06.unix.new.log
	cp  test-06.unix.new.log test-06.unix.known_good-$(KNOWN_GOOD_VERSION).log

test-07.unix.new.log: test-07.sh test-07.unix.known_good-$(KNOWN_GOOD_VERSION).log
	-rm -rf testroot-07
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 5 0; then PATH=$(SVN_BIN_DIR):$(PATH) PYTHON=$(PYTHON) ./test-07.sh >test-07.unix.new.log 2>&1; fi
	if PYTHONPATH=../Source $(PYTHON) svn_min_version.py 1 5 0; then $(PYTHON) benchmark_diff.py test-07.unix.known_good-$(KNOWN_GOOD_VERSION).log test-07.unix.new.log; fi

clean-07:
	-rm -f test-07.unix.new.log
	-rm -f test-07.unix.new.log.clean
	-rm -rf testroot-07

diff-07: test-07.unix.new.log
	wb-diff test-07.unix.known_good-$(KNOWN_GOOD_VERSION).log.clean test-07.unix.new.log.clean

new-07: test-07.unix.new.log
	cp  test-07.unix.new.log test-07.unix.known_good-$(KNOWN_GOOD_VERSION).log
