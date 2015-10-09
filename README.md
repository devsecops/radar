# Radar

Radar helps teams to solve for common mistakes found in infrastructure templates that can expose a Full Stack deployment to Security and Compliance defects.  It is intended to be a harness that can be used by individuals and teams to support error checking and validation against their own requirements and provide a common means for writing these checks so they can be exchanged.

Radar is an extension of the AWS Security Assessment tool to create functionality for DevOps and Security teams to check baseline requirements and configurations in Infrastructure templates, such as CloudFormation. This solution currently allows for teams to process CloudFormation against requirements to ensure that it meets specific criteria before it is included in a Full Stack workload.

The initial code came from a contribution and provides for users to develop unit tests for AWS CloudFormation templates in order to check these templates as part of a deployment configuration.

Radar will be extended to support an API front-end that can be deployed as a common tool from initial desktop checks during development through automated deployment via a CICD pipeline.

## Requirements 
Radar is developed using:
 - python 2.x
 - Boto

## Repository
The repository is being set up to support an API endpoint, the infrastructure templates to support it, and tools that are useful.
```
|- docs
|- infrastructure
|- source
|--- aws-securitychecker
|- tests
```

## Roadmap
We're working on understanding and developing the vision for where this tool could go.  We believe it needs an API and other test harnesses to run through different resources, templates, and components within a Full Stack workload.

### Crawl
We are planning to build an API capability to allow Radar to be run as part of the CICD pipeline.  And we'll be adding tests to run against CloudFormation templates from the CLI in order to support DevOps teams consumption.

### Walk 
Radar is planned for expansion to allow for other resources to be tested and integrations with other tools, such as Gauntlt.

### Run
Radar needs to allow for tests to be run against thousands of accounts, allow for real-time test development, and posting of results into Forecast.



