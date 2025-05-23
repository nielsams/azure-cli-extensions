# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import *


class WeightsAndBiasesScenario(ScenarioTest):
    @ResourceGroupPreparer(name_prefix='cli_test_weights_and_biases', location="eastus")
    def test_weights_and_biases_all(self, resource_group):
        self.kwargs.update({
            'name': 'wnb-test-org-5',
            'resource_group': 'jawt-rg'
        })

        # List WeightsAndBiases Organizations
        self.cmd('az weights-and-biases instance list --resource-group {resource_group}',
                 checks=[])

        # Show WeightsAndBiases Organization
        self.cmd('az weights-and-biases instance show --resource-group {resource_group} --instancename {name}',
                 checks=[
                     self.check('name', '{name}'),
                 ])
