# AWS Security Assessment Tool

This solution allows for users to create and run unit tests against their AWS infrastructure and their CloudFormation templates.

## Requirements:
 - python 2.x
 - Boto

## Command Line Syntax

```

Usage: securitychecker --template <CF-Template> --config <Test Config> [ --unit-test ] --output <outputfile>

Options:
  --version             			show program version number and exit
  -h, --help            			show this help message and exit
  -t TEMPLATE, --template=TEMPLATE		CloudFormation template to test
  -u TEST, --unit-test=TEST			Unittest, if specifying a single unit test file
  -c CONFIG, --config=CONFIG			Config file, if specifying a test config file for multiple tests
  -o OUTFILE, --output=OUTFILE			Output file
  -l CONFIGTYPE, --list-config=CONFIGTYPE	List configurations available with this install
```

## Usage Examples

To run a single unit test against a CF template: 

	securitychecker --template stack2.json --unit-test CF-ELBHealthCheck

To run a test config of multiple tests against a CF template:

	securitychecker --template stack2.json --config csm-level34

## Linux Installation
Tested on Ubuntu and Amazon Linux:

```
pip install https://s3.amazonaws.com/cf-templates-awsmikedix/security-check/securitychecker-0.2.tar.gz
```

## Directory Structure
```
dist/ contains the distributable package (same as in S3 link below)
securitychecker/  
    ComplianceTest.py --> where a lot of the original script was put into a separate class
    __init__.py
    __main__.py
    securitychecker --> entry point of the script, can be run on its own if not installed
    data/
        compliance --> Directories for config files and UnitTests
        UnitTests --> when installed end up in /usr/local/lib/<module install dir>/data
setup.py    package setup script
OriginalFiles/ --> Original Scripts & Documentation
```

## Misc Info

Sample UnitTests can be found in the UnitTest folder.  Tests that begin with API go against the AWS infrastructure directly, while tests that begin with CF are meant for CloudFormation templates.

Additional documentation around this application can be found within the Documentation folder.


