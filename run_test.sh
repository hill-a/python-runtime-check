#!/bin/bash
coverage run -m pytest test.py
echo ""
coverage report
coverage xml
echo ""
python-codacy-coverage -r coverage.xml