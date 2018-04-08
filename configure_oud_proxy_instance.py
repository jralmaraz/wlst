PRODUCT_HOME=%PRODUCT_HOME%
DOMAIN_HOME=%OUD_DOMAIN_HOME%
oud_createInstance(scriptName='oud-proxy-setup', instanceName='%PROXY_INSTANCE_NAME%', hostname='%OUD_PROXY_HOSTNAME%', ldapPort=%PROXY_LDAP_PORT%, rootUserDN='cn=Directory\ Manager',rootUserPasswordFile='%PROXY_ROOT_PW_FILE%', adminConnectorPort=%PROXY_LDAP_ADMIN_PORT%)