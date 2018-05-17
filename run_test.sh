#!/bin/bash
coverage run -m pytest test.py
echo ""
coverage report
coverage xml
echo ""
mypy .
echo ""
python-codacy-coverage -r coverage.xml