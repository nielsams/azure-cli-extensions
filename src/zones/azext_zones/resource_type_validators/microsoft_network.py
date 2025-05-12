# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from .._resourceTypeValidation import ZoneRedundancyValidationResult, register_resource_type
from knack.log import get_logger


@register_resource_type('microsoft.network')
class microsoft_network:

    @staticmethod
    def validate(resource):
        resourceType = resource['type']
        resourceSubType = resourceType[resourceType.index('/') + 1:]

        _logger = get_logger("microsoft_network")
        _logger.debug(
            "Validating Microsoft.Network resource type: %s",
            resourceSubType)

        # Application gateways
        if resourceSubType == 'applicationgateways':
            zones = resource.get('zones') or []
            if len(zones) > 1:
                return ZoneRedundancyValidationResult.Yes
            else:
                return ZoneRedundancyValidationResult.No
                
        # Azure firewalls
        if resourceSubType == 'azurefirewalls':
            zones = resource.get('zones') or []
            if len(zones) > 1 and resource['sku']['capacity'] > 1:
                return ZoneRedundancyValidationResult.Yes
            else:
                return ZoneRedundancyValidationResult.No
                
        # Load balancers
        if resourceSubType == 'loadbalancers':
            frontend_ip_configs = resource['properties'].get('frontendIPConfigurations') or []
            zones = frontend_ip_configs[0].get('zones') or []
            if len(zones) > 1:
                return ZoneRedundancyValidationResult.Yes
            else:
                return ZoneRedundancyValidationResult.No
                
        # Public IP addresses
        if resourceSubType == 'publicipaddresses':
            zones = resource.get('zones') or []
            if resource['sku']['name'] in ['Standard'] and len(zones) > 1:
                return ZoneRedundancyValidationResult.Yes
            else:
                return ZoneRedundancyValidationResult.No
                
        # Virtual network gateways
        if resourceSubType == 'virtualnetworkgateways':
            sku = resource['properties']['sku']['name']
            if sku.endswith('AZ'):
                return ZoneRedundancyValidationResult.Yes
            else:
                return ZoneRedundancyValidationResult.No
            
        # Network connections
        if resourceSubType == 'connections':
            # Network connections depend on the configuration of the Virtual Network Gateway
            return ZoneRedundancyValidationResult.Dependent
                
        # Network interfaces
        if resourceSubType == 'networkinterfaces':
            return ZoneRedundancyValidationResult.Dependent
            
        # Local Network Gateways
        if resourceSubType == 'localnetworkgateways':
            return ZoneRedundancyValidationResult.Dependent

        # Resources that are always zone redundant
        if resourceSubType in (
            'dnszones',
            'frontdoors',
            'networksecuritygroups',
            'networkwatchers',
            'networkwatchers/flowlogs',
            'networkwatchers/packetcaptures',
            'privatednszones',
            'privatednszones/virtualnetworklinks',
            'privateendpoints',
            'virtualnetworks'
        ):
            return ZoneRedundancyValidationResult.Always

        return ZoneRedundancyValidationResult.Unknown
