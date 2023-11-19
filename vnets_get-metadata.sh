#!/bin/bash
az graph query --graph-query 'resources | where type == "microsoft.network/virtualnetworks"' > vnets.json