PRODUCT_HOME=%PRODUCT_HOME%
DOMAIN_HOME=%OUD_DOMAIN_HOME%
oud_createInstance(scriptName='oud-setup', instanceName='%OUD_INSTANCE_NAME%1', hostname='%OUD_HOSTNAME%', ldapPort=%OUD_LDAP_PORT%, rootUserDN='cn=Directory\ Manager',rootUserPasswordFile='/home/oracle/scripts/oud_password.txt',baseDN='%BASE_DN%', sampleData=5, adminConnectorPort=%OUD_LDAP_ADMIN_PORT%)


oud_createInstance(scriptName='oud-setup', instanceName='oud1', hostname='fmw.lab.deloitte.co.nz', ldapPort=3389, rootUserDN='cn=Directory\ Manager',rootUserPasswordFile='/home/oracle/scripts/oud_password.txt',baseDN='dc=lab,dc=deloitte,dc=co,dc=nz', sampleData=5, adminConnectorPort=6444)