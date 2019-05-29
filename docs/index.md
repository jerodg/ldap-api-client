     ___  ___    _    _  _  _        __  __        _     __               ___  ___   ___  
    / __|| __|  /_\  | |(_)| |__    |  \/  | __   /_\   / _| ___  ___    | __|| _ \ / _ \ 
    \__ \| _|  / _ \ | || || '_ \   | |\/| |/ _| / _ \ |  _|/ -_)/ -_)   | _| |  _/| (_) |
    |___/|___|/_/ \_\|_||_||_.__/___|_|  |_|\__|/_/ \_\|_|  \___|\___|___|___||_|   \___/ 
                                |___|                                |___|                                                
![platform](https://img.shields.io/badge/platform-Linux-blue.svg)
![python](https://img.shields.io/badge/python-3.7%2B-blue.svg)
![license](https://img.shields.io/badge/license-Proprietary-red.svg)
![88%](https://img.shields.io/badge/coverage-88%25-yellowgreen.svg)

## Purpose                                  
McAfee EPO REST client API module.

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
        .base.sh
        .mcafee_epo.sh

#### Production
    /home/infosecintegration/.prod_config/
        .base.sh
        .mcafee_epo.sh

## Backup
Code is stored in version control (Github Enterprise) and as such no specific DR environment is required.

## Installation
### Development
    pipenv install sealib_mcafee_epo --dev
    
### Production
    pipenv install sealib_mcafee_epo

## Upgrade
### Development
    pipenv update --dev
    
### Prodution
    pipenv update
    
## Firewall
Outbound LAN on port 8443 (https)

## Troubleshooting
None

## Proxy
None

## Environment Variables
MC_URI -> Base McAfee EPO URI
MC_URU_NEW -> Base McAfee EPO URI for New Server
MC_USER -> Username
MC_PASS -> Password

## Location

### Development
    slgramihqaims90.info53.com
        /sea_dev/sealib_mcafee_epo
        
### Production
    slgramihqaims90.info53.com
        /sea_prod/sealib_mcafee_epo

### Source
https://github.info53.com/Fifth-Third/SEA-Lib_McAfee_EPO

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
    pytest --cov /sea_dev/sealib_mcafee_epo/sealib_mcafee_epo/

### Production
    pytest --cov /sea_prod/sealib_mcafee_epo/sealib_mcafee_epo/

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
