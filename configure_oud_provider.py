#!/usr/bin/python
import os, sys
 
adminUser="weblogic"
adminPassword=""
adminServerHost="adminserver.host.com"
adminServerPort="7001"
domainName="YourDomainName"
LDAPProviderName="OUDAuthenticator"
LDAPHost="oudserver.host.com"
LDAPPort="1389"
LDAPAdmin="cn=Directory Manager,cn=Root DNs,cn=config"
LDAPAdminPassword="password"
LDAPGroupBase="cn=Groups,dc=your,dc=company,dc=com"
LDAPUserBase="cn=Users,dc=your,dc=company,dc=com"
 
connect (adminUser,adminPassword,'t3://'+adminServerHost+':'+adminServerPort)
edit()
startEdit()
cd('/SecurityConfiguration/'+domainName+'/Realms/myrealm')
# In the following command, substitute the appropriate class type
cmo.createAuthenticationProvider(LDAPProviderName,'weblogic.security.providers.authentication.IPlanetAuthenticator')
cd('/SecurityConfiguration/'+domainName+'/Realms/myrealm/AuthenticationProviders/'+LDAPProviderName)
cmo.setControlFlag('SUFFICIENT')
cd('/SecurityConfiguration/'+domainName+'/Realms/myrealm/AuthenticationProviders/'+LDAPProviderName)
cmo.setHost(LDAPHost)
cmo.setPort(LDAPPort)
cmo.setPrincipal(LDAPAdmin)
set("Credential",LDAPAdminPassword)
cmo.setGroupBaseDN(LDAPGroupBase)
cmo.setUserBaseDN(LDAPUserBase)
cmo.setUserNameAttribute('uid')
cmo.setAllUsersFilter('(&(uid=*)(objectclass=person))')
cmo.setStaticMemberDNAttribute('uniquemember')
cmo.setStaticGroupDNsfromMemberDNFilter('(&(uniquemember=%M)(objectclass=groupofuniquenames))')
cmo.setDynamicGroupNameAttribute('cn')
cmo.setDynamicGroupObjectClass('groupOfURLs')
cmo.setUserFromNameFilter('(&(uid=%u)(objectclass=person))')
cmo.setDynamicMemberURLAttribute('memberURL')
cmo.setStaticGroupObjectClass('groupofuniquenames')
cmo.setUserObjectClass('inetOrgPerson')
cmo.setGuidAttribute('entryuuid')
cd('/SecurityConfiguration/'+domainName+'/Realms/myrealm/AuthenticationProviders/DefaultAuthenticator')
cmo.setControlFlag('SUFFICIENT')
cd('/SecurityConfiguration/'+domainName+'/Realms/myrealm')
set('AuthenticationProviders',jarray.array([ObjectName('Security:Name=myrealm'+LDAPProviderName), ObjectName('Security:Name=myrealmDefaultAuthenticator'),ObjectName('Security:Name=myrealmDefaultIdentityAsserter')], ObjectName))
save()
activate()
disconnect()
exit()
