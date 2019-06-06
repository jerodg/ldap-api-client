# Installation

## Install

#### Development

    pipenv install sealib_activedirectory --dev
	
#### Production

	pipenv install sealib_activedirectory

## Upgrade

#### Development
	
	pipenv update --dev
	
#### Production

	pipenv update
	
## Firewall

### LAN
|Port|Description|Protocol|
|---|---|---|
|389|LDAP|TCP/UDP|
|636|LDAP Over SSL/TLS|TCP/UDP|
|3268|Global Catalog|TCP/UDP|


## Troubleshooting

* None

## Proxy

* None

## Enviornment Variables

* `{AD_USER}` - ActiveDirectory User With Read Permission
* `{AD_PASS}` - Password
* `{AD_HOST}` - Hostname for AD server to connect to


