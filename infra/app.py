#!/usr/bin/env python3

import aws_cdk as cdk
import cdk_nag
from infra.infra_stack import InfraStack

app = cdk.App()
InfraStack(app, "infra")

# cdk.Aspects.of(app).add(cdk_nag.AwsSolutionsChecks())
app.synth()