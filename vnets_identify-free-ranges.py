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

        vNetRange = IPSet()
        for prefix in addressPrefixes:
            vNetRange.add(prefix)

        subnetInfos = []
        subnets = properties['subnets']
        for subnet in subnets:
            subnetProperties = subnet['properties']
            subnetInfo = {
                'name': subnet['name'],
            }
            subnetPrefixes = []
            if not subnetProperties.get('addressPrefix') is None:
                subnetPrefixes.append(subnetProperties['addressPrefix'])
            elif not subnetProperties.get('addressPrefixes') is None:
                subnetPrefixes.extend(subnetProperties['addressPrefixes'])
            else:
                print(f"ERROR: No addressPrefix or addressPrefixes found in subnet {subnet['name']}.")
                exit(1)
            for addressPrefix in subnetPrefixes:
                vNetRange.remove(addressPrefix)
            subnetInfo['addressPrefixes'] = subnetPrefixes
            subnetInfos.append(subnetInfo)
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