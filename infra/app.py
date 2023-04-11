#!/usr/bin/env python3

import aws_cdk as cdk

from infra.infra_stack import InfraStack


app = cdk.App()
InfraStack(app, "infra")

app.synth()
