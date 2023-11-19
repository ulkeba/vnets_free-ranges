from netaddr import *
import json

vNetToFreeSubnets = []

# Read and parse vnets.json
with open('vnets.json') as json_file:
    jsonContent = json.load(json_file)
    for vnet in jsonContent['data']:
        vnetName = vnet['name']
        properties = vnet['properties']
        addressPrefixes = properties['addressSpace']['addressPrefixes']

        vNetInfos = {
            'name': vnetName,
            'id': vnet['id'],
            'addressPrefixes': addressPrefixes,
        }
        vNetToFreeSubnets.append(vNetInfos)

        #TODO: Generalize to support multiple address prefixes.
        if (len(addressPrefixes) == 1):
            vNetRange = IPSet([addressPrefixes[0]])
        else:
            vNetRange = IPSet()
            for prefix in addressPrefixes:
                vNetRange.add(prefix)

        subnetInfos = []
        subnets = properties['subnets']
        for subnet in subnets:
            subnetProperties = subnet['properties']
            addressPrefix = subnetProperties['addressPrefix']
            subnetInfos.append({
                'name': subnet['name'],
                'addressPrefix': addressPrefix
            })
            vNetRange.remove(addressPrefix)
        vNetInfos['subnets'] = subnetInfos

        freeRangeInfos = []
        for range in vNetRange.iter_cidrs():
            freeRangeInfos.append({
                'addressPrefix': str(range),
                'size': range.size
            })
        vNetInfos['freeRanges'] = freeRangeInfos

jsonContent = json.dumps(vNetToFreeSubnets, indent=4)
with open("vnets_free-ranges.json", "w") as outfile:
    outfile.write(jsonContent)