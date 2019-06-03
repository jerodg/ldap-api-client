     ___  ___    _    _  _  _          _        _    _            ___   _                _                   
    / __|| __|  /_\  | |(_)| |__      /_\   __ | |_ (_)__ __ ___ |   \ (_) _ _  ___  __ | |_  ___  _ _  _  _ 
    \__ \| _|  / _ \ | || || '_ \    / _ \ / _||  _|| |\ V // -_)| |) || || '_|/ -_)/ _||  _|/ _ \| '_|| || |
    |___/|___|/_/ \_\|_||_||_.__/___/_/ \_\\__| \__||_| \_/ \___||___/ |_||_|  \___|\__| \__|\___/|_|   \_, |
                                |___|                                                                   |__/ 
                              
![platform](https://img.shields.io/badge/platform-Linux-blue.svg)
![python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![license](https://img.shields.io/badge/license-Proprietary-red.svg)
![88%](https://img.shields.io/badge/coverage-88%25-yellowgreen.svg)

## Purpose                                  
ActiveDirectory REST client API module.

## Owner
Manager of Security, Engineering, and Automation

    jerod.gawne@53.com
    holly.fox@53.com

## Accounts
All files/folders are owned by functional account 'infosecintegration'.

    /home/infosecintegration
    
### Configuration
#### Development
    /home/infosecintegration/.dev_config/
        .sealib_base.sh
        .sealib_activedirectory.sh

#### Production
None

## Backup
Code is stored in version control (Github Enterprise) and as such no specific DR environment is required.

## Installation
### Development
    pipenv install sealib_activedirectory --dev
    
### Production
    pipenv install sealib_activedirectory

## Upgrade
### Development
    pipenv update --dev
    
### Prodution
    pipenv update
    
## Firewall
### LAN
|Port|Description|Protocol|
|---|---|---|
|389|LDAP|TCP/UDP|
|636|LDAP Over SSL/TLS|TCP/UDP|
|3268|Global Catalog|TCP/UDP|

### WAN
None

## Troubleshooting
None

## Proxy
None

## Environment Variables
AD_USER -> ActiveDirectory User With Read Permission
AD_PASS -> Password
AD_HOST -> Hostname for AD server to connect to

## Location

### Development
    slgramihqaims90.info53.com
        /sea_dev/sea_lib_activedirectory
        
### Production
None

### Source
https://github.info53.com/Fifth-Third/sea_lib_activedirectory

### PyPi
#### Development
    [[source]]
    name = "sea_pypi"
    url = "http://slgramihqaims90.info53.com:3030/simple"
    verify_ssl = false

#### Production
TBD

## Tests
### Development
    pytest --cov /sea_dev/sea_lib_activedirectory/sealib_activedirectory/

### Production
None

## Project layout
    docs/
        index.md  # The documentation homepage.
    sealib_base/  # Module folder.
        tests/
            test.py
        __init__.py
        mcafee_epo_api.py
    .gitignore
    LICENSE
    MANIFEST.in
    mkdocs.yml    # The configuration file.
    Pipfile
    README.md
    setup.cfg
    setup.py
