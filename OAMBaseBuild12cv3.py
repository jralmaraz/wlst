loadProperties("buildOAM.properties") 

redirect(logOutputPath)

allOAMServers=["wls_oam1","wls_oam2"]
allAMAServers=["wls_ama1","wls_ama2"]
allAPPServers=["wls_app1","wls_app2"]
allOAMServersAddresses=["ip-172-30-0-167.ap-southeast-2.compute.internal","ip-172-30-0-237.ap-southeast-2.compute.internal"]
allAMAServersAddresses=["ip-172-30-0-167.ap-southeast-2.compute.internal","ip-172-30-0-237.ap-southeast-2.compute.internal"]
allAPPServersAddresses=["ip-172-30-0-167.ap-southeast-2.compute.internal","ip-172-30-0-237.ap-southeast-2.compute.internal"]
allMachinesNames=["ip-172-30-0-167.ap-southeast-2.compute.internal","ip-172-30-0-237.ap-southeast-2.compute.internal"]
allMachinesAddresses=["ip-172-30-0-167.ap-southeast-2.compute.internal","ip-172-30-0-237.ap-southeast-2.compute.internal"]

def createServer(server):
        cd('/')
        try:
                create(server, 'Server')
        except:
                print "Create Server " + server + " failed, check the logs"
                dumpStack()

def cloneServer(originalServer,newServer):
        cd('/')
        try:
                clone(originalServer,newServer,'Server')
        except:
                print "Clone server " + newServer + "failed..."
                dumpStack()

def createCluster(cluster):
        cd('/')
        try:
                create(cluster, 'Cluster')
        except:
                print "Create Cluster " + cluster + " failed, check the logs"
                dumpStack()

def createMachine(machine):
        cd('/')
        try:
                create(machine, 'Machine')
        except:
                print "Create Machine " + machine + " failed, check the logs"
                dumpStack()
        try:
                cd('/Machines/' + machine)
                create(machine, 'NodeManager')
        except:
                print "Create Node Manager for machine " + machine + " failed, check the logs"
                dumpStack()

def configureNodeManager(machine,ListenAddress):
        cd('/Machines/'+ machine+ '/NodeManager/' + machine)
        try:
                set('NMType', 'SSL')
        except:
                print "Set NMType to SSL Failed"
                dumpStack()
        try:
                set('ListenAddress', ListenAddress)
        except:
                print "Set ListenAddress failed"
                dumpStack()

        try:
                set('DebugEnabled', 'false')
        except:
                print "Set Debug failed"
                dumpStack()

def assignServertoMachine(server,machine):
        print('Assigning servers to machine')
        try:
                assign('Server', server, 'Machine', machine)
        except:
                print "Assign " + server + " to " + machine + " failed"
                dumpStack()

def setDomainNodeManager(Password):

        cd("/SecurityConfiguration/base_domain")
        try:
                set('NodeManagerUsername', 'weblogic')
        except:
                print "Set NodeManagerUsername failed"
                dumpStack()
        try:
                cmo.setNodeManagerPasswordEncrypted(Password)
        except:
                print "Set NodeManager PasswordEncrypted failed"
                dumpStack()

def enableWeblogicPlugin(cluster):
        cd('/Cluster/'+cluster)
        try:
                set('WeblogicPluginEnabled', 'true')
        except:
                print "Set Weblogic Plugin on " + cluster + " failed"
                dumpStack()

def assignServerToCluster(server,cluster):
        cd('/')
        try:
                assign('Server', server,'Cluster',cluster)
        except:
                print "Assign " + server + " to " + cluster + " failed"
                dumpStack()

def configServerBase(server,address,plainPort):

        print('Updating '+ server + ': ')
        cd('/Servers/' + server)
        try:
                set('ListenAddress', address)
        except:
                print "Set Listen Address to " + server + " failed"
                dumpStack()
        try:
                set('ListenPort', int(plainPort))
        except:
                print "Set the Listen Port to " + server + " failed"
                dumpStack()

#Setup Identity and Trust Store for each server

# Enable SSL. Attach the keystore later.

def configBaseSSL(server,SSLPort):

        cd('/Servers/' + server)
        create(server,'SSL')
        cd('SSL/'+ server)

        try:
                set('Enabled', 'True')
                set('ListenPort', int(SSLPort))
                set('HostnameVerificationIgnored', 'True')
        except:
                print "Set " + server + " SSL properties failed, check logs"
                dumpStack()

        cd('/Servers/'+server)
        try:
                set('KeyStores','CustomIdentityAndCustomTrust')
                set('CustomIdentityKeyStoreType', KeyStoreType)
                set('CustomIdentityKeyStoreFileName', IdentityKeyStorePath)
                cmo.setCustomIdentityKeyStorePassPhraseEncrypted(IdentityKeyStorePassword)

                set('CustomTrustKeyStoreType', KeyStoreType)
                set('CustomTrustKeyStoreFileName', trustKeyStorePath)
                cmo.setCustomTrustKeyStorePassPhraseEncrypted(trustKeyStorePassword)
        except:
                print "Set " + server + " SSL Keystores failed, check logs"
                dumpStack()



        cd('/Servers/'+str(server)+'/SSL/'+str(server))
        try:
                set('ServerPrivateKeyAlias',SSLPrivateKeyAlias)
                cmo.setServerPrivateKeyPassPhraseEncrypted(IdentityKeyStorePassword)
        except:
                print "Set " + server + " Private Key Alias failed, check logs"
                dumpStack()
# Direct stdout and stderr.

def setLogging(server):
        cd('/Servers/' + server)
        create(server,'Log')
        cd('/Servers/' + server + '/Log/' + server)
        set('RedirectStderrToServerLogEnabled', 'True')
        set('RedirectStdoutToServerLogEnabled', 'True')

# setup node manager startup username and password

def setServerNodeManager(server):

        cd('/Servers/'+ server)
        try:
                create(server, 'ServerStart')
        except:
                print "Create ServerStart for " + server + " failed"
                dumpStack()

        cd('/Servers/'+server+'/ServerStart/'+server)
        try:
                set('Username', 'weblogic')
        except:
                print "Set username for " + server + " failed"
        try:
                cmo.setPasswordEncrypted(weblogicPassword)
        except:
                print "Set Password for " + server + " failed"
                dumpStack()

def setServerStart (server,JVMArgs):
        cd('/Servers/'+server)
        create(server, 'ServerStart')
        cd('/Servers/'+server+'/ServerStart/'+server)
        set('Arguments', JVMArgs)

def updateServerName(originalName,newName):
        print('Updating Managed Server: ' + originalName + " to " + newName )
        cd('/Servers/' + originalName)
        try:
                cmo.setName(newName)
        except:
                print "Set server name to " + newName + " failed"
                dumpStack()

def updateJDBC():

        allDS = ["WLSSchemaDataSource","LocalSvcTblDataSource","opss-data-source","opss-audit-viewDS","opss-audit-DBDS","oamDS"]

        for tmpDS in allDS:
          dsName=tmpDS
          print "Setting URL for JDBC Driver"
          cd('/JDBCSystemResource/'+dsName+'/JdbcResource/'+dsName+'/JDBCDriverParams/NO_NAME_0')
          try:
                set('URL', dbURL)
          except:
                print "Set DB URL failed for " + dsName
                dumpStack()

          print "Updating Database Scheme Username"
          cd('/JDBCSystemResource/'+dsName+'/JdbcResource/'+dsName+'/JDBCDriverParams/NO_NAME_0/Properties/NO_NAME_0/Property/user')
          originalSchemeName=get('Value')
          schemeSufix=originalSchemeName.split('_', 1)[-1]
          try:
                set("Value", rcuPrefix+ "_" +schemeSufix)
          except:
                print "Set Prefix for " + dsName + " failed "
                dumpStack()

          print  "Updating Password for, " + dsName
          cd('/JDBCSystemResource/'+dsName+'/JdbcResource/'+dsName+'/JDBCDriverParams/NO_NAME_0')
          try:
                set('PasswordEncrypted', dsPassword)
          except:
                print "Set password for " + dsName + " failed"
                dumpStack()

          cd('/JDBCSystemResource/'+dsName+'/JdbcResource/'+dsName+'/JDBCConnectionPoolParams/NO_NAME_0')

          try:
                set("CapacityIncrement", 1)
                set("TestFrequencySeconds", 120)
                set("InitialCapacity", 0)
                set("TestConnectionsOnReserve", "true")
                set("MaxCapacity", 200)
                set("TestTableName", "SQL ISVALID")
                set("ConnectionCreationRetryFrequencySeconds", 10)
                set("SecondsToTrustAnIdlePoolConnection", 0)
                set("ShrinkFrequencySeconds", 60)
                set("SecondsToTrustAnIdlePoolConnection", 1)
          except:
                print "Config of JDBCConnectionPoolParams for " + dsName + " failed"
                dumpStack()
          #Check Targets
          #print "Setting DataSource targets"
          #dsTarget=datasourceTargets(dsName)
          #cd('/JDBCSystemResource/'+dsName)
          #set('Target', dsTarget)

# Select the WebLogic domain template and WebServices for JAX-RPC template, and
# then load them
print('Creating OAM Domain ...')
selectTemplate('Basic WebLogic Server Domain')
selectTemplate('Oracle Access Management Suite')
loadTemplates()

# Set the domain password for the WebLogic Server administration user
#weblogicPassword = "".join(java.lang.System.console().readPassword("%s", ["Please enter the weblogic user password:"]))

#dsPassword = "".join(java.lang.System.console().readPassword("%s", ["Please enter the RCU schemas password:"]))

#IdentityKeyStorePassword = "".join(java.lang.System.console().readPassword("%s", ["Please enter the Identity Key Store password:"]))

#trustKeyStorePassword = "".join(java.lang.System.console().readPassword("%s", ["Please enter the Trust Store password:"]))

cd('/Security/base_domain/User/weblogic')
cmo.setPassword(weblogicPassword)

# If the domain already exists, overwrite the domain
setOption('OverwriteDomain', 'false')

#Application directory
setOption('AppDir', appDir)

#Production Mode
setOption('ServerStartMode','prod')

#AdminServer
configServerBase(asName,asAddress,asPort)
configBaseSSL(asName,asSSLPort)
setLogging(asName)

setServerStart(asName,asJVMArguments)

setServerNodeManager(asName)

updateServerName('oam_server1',oamms1Name)
updateServerName('oam_policy_mgr1',amams1Name)

print('Creating Cluster: ' + oamClusterName)
createCluster(oamClusterName)
enableWeblogicPlugin(oamClusterName)

print('Creating Cluster: ' + policyManagerClusterName)
createCluster(policyManagerClusterName)
enableWeblogicPlugin(policyManagerClusterName)

print('Creating Cluster: ' + customClusterName)
createCluster(customClusterName)
enableWeblogicPlugin(customClusterName)

createServer(appms1Name)

index=0
for oamServer in allOAMServers:

    currentoamServerName = oamServer
    currentamaServerName = allAMAServers[index]
    currentappServerName = allAPPServers[index]
     
    currentoamServerAddress = allOAMServersAddresses[index]
    currentamaServerAddress = allAMAServersAddresses[index]
    currentappServerAddress = allAPPServersAddresses[index]

      
    configServerBase(currentoamServerName,currentoamServerAddress,oamms1Port)
    configServerBase(currentamaServerName,currentamaServerAddress,amams1Port)
    configServerBase(currentappServerName,currentappServerAddress,appms1Port)
    
    # Enable SSL. Attach the keystore later.

    configBaseSSL(currentoamServerName,oamms1SSLPort)
    configBaseSSL(currentamaServerName,amams1SSLPort)
    configBaseSSL(currentappServerName,appms1SSLPort)

    # Direct stdout and stderr.

    setLogging(currentoamServerName)
    setLogging(currentamaServerName)
    setLogging(currentappServerName)


    setServerStart(currentoamServerName,msJVMArguments)
    setServerStart(currentamaServerName,msJVMArguments)
    setServerStart(currentappServerName,msJVMArguments)
    # setup node manager startup username and password

    setServerNodeManager(currentoamServerName)
    setServerNodeManager(currentamaServerName)
    setServerNodeManager(currentappServerName)

    assignServerToCluster(currentoamServerName,oamClusterName)
    assignServerToCluster(currentamaServerName,policyManagerClusterName)
    assignServerToCluster(currentappServerName,customClusterName)

    currentMachineName = allMachinesNames[index]

    currentMachineListenAddress = allMachinesAddresses[index]

    createMachine(currentMachineName)
    print "Setting up Machine and NodeManager"
    configureNodeManager(currentMachineName,currentMachineListenAddress)
    assignServertoMachine(asName,machine1Name)
    assignServertoMachine(currentoamServerName,currentMachineName)
    assignServertoMachine(currentamaServerName,currentMachineName)
    assignServertoMachine(currentappServerName,currentMachineName)


    if (int(clusterSize) > 1 and index+1 < len(allOAMServers)):
        print "cloning servers"
        cloneServer(oamms1Name,allOAMServers[index+1])
        cloneServer(amams1Name,allAMAServers[index+1])
        cloneServer(appms1Name,allAPPServers[index+1])

    index += 1

#update jdbc

print('Updating Data Source')
updateJDBC()

#setup node manager

setDomainNodeManager(weblogicPassword)

# write the domain and close the templates

print('Writing domain ..' + domainDir)
try:

        writeDomain(domainDir)
except:
        print "write Domain failed"
        dumpStack()

try:

        closeTemplate()
except:
        print "closeTemplate failed"
        dumpStack()

print('OAM Domain created')
stopRedirect()
exit()
