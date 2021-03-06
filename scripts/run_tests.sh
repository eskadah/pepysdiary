#!/bin/bash
set -e

# You can optionally pass in a test, or test module or class, as an argument.
# e.g.
# ./run_tests.sh tests.appname.test_models.TestClass.test_a_thing
TESTS_TO_RUN=${1:tests}

./manage.py test --settings=pepysdiary.settings.tests $TESTS_TO_RUN
flake8