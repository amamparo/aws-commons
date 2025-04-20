# aws-commons

Shared infrastructure components for a hobby AWS account.

## Overview
This repository contains foundational infrastructure components for a hobby AWS account. It uses AWS CDK to define and deploy infrastructure as code, focusing on cost-effective solutions for personal projects.

## Getting Started

### Prerequisites
* Python 3.13+
    * [pyenv](https://github.com/pyenv/pyenv) recommended for version management
* [Poetry](https://python-poetry.org/docs/#installation) for dependency management
* AWS CDK CLI (`npm install -g aws-cdk`)
* Configured AWS credentials

### Setup
1. Install dependencies:
   ```shell
   make install
   ```

2. Review and customize `config.toml` with your AWS account details

3. Deploy infrastructure:
   ```shell
   make deploy
   ```

## Development
* `make check` - Run code quality checks and CDK synthesis validation
* `make diff` - Preview infrastructure changes
* `make deploy` - Apply changes to AWS

## Architecture
This project provides basic AWS infrastructure components including networking, DNS, and monitoring.
Deployment decisions prioritize cost efficiency for hobbyist use cases.
See individual modules in `src/` for specific components.

## Configuration
All deployment settings are centralized in `config.toml` for easy customization.
