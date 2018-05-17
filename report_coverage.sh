#!/bin/bash
coverage report
coverage xml
echo ""
python-codacy-coverage -r coverage.xml