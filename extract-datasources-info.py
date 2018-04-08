import re
import jarray
import traceback
domain = 'intosbd'

def quote(text):
    if text or text == '':
        return "\"" + str(text).replace("\"", "\"\"") + "\""
    else:
        return ""

def retrieve_target_list(wlst_name):
    cd(wlst_name)
    nn = ls('Targets', returnMap='true')
    target = []
    target_type = []
    for token_target in nn:
        target.append(token_target)
        cd(wlst_name + '/Targets/' + token_target)
        target_type.append(get('Type'))
    return target, target_type

def add_index_entry(file_handle, values):
    print >>file_handle, ";".join(map(quote, values))


m = ls('/JDBCSystemResources',returnMap='true')

f = open("/tmp/DataSources.out", "w")
for token in m:
    print '___'+token+'___'
    cd('/JDBCSystemResources/'+token + '/JDBCResource/' + token)

    # check for MultiDatasource
    cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDataSourceParams/' + token )
    dataSourceList = get('DataSourceList')
    if dataSourceList is None:

        cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDriverParams/' + token )
        url      = get('Url')
        driver   = get('DriverName')
        usexa    = str(get('UseXaDataSourceInterface'))

        cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCConnectionPoolParams/' + token )
        maxcapacity     = get('MaxCapacity')
        initialcapacity = get('InitialCapacity')
        if not (initialcapacity):
           initialcapacity = '0'
        mincapacity     = get('MinCapacity')
        if not (mincapacity):
           mincapacity  = '0'
        statementcachesize  = get('StatementCacheSize')
        if not (statementcachesize):
           statementcachesize   = '0'
        testconnectionsonreserve = str(get('TestConnectionsOnReserve'))

        inactiveconnectiontimeoutseconds = get('InactiveConnectionTimeoutSeconds')
        if not (inactiveconnectiontimeoutseconds):
          inactiveconnectiontimeoutseconds = '0'

        connectionreservetimeoutseconds = get('ConnectionReserveTimeoutSeconds')
        if not (connectionreservetimeoutseconds):
          connectionreservetimeoutseconds = '0'

        shrinkfrequencyseconds = str(get('ShrinkFrequencySeconds'))
        secondstotrustidlepoolconnection = str(get('SecondsToTrustAnIdlePoolConnection'))
        testfrequency = get('TestFrequencySeconds')
        connectioncreationretryfrequency = str(get('ConnectionCreationRetryFrequencySeconds'))
        initsql = str(get('InitSql'))

        if get('WrapTypes'):
          wrapdatatypes = '1'
        else:
          wrapdatatypes = '0'

        if get('RemoveInfectedConnections'):
          removeinfectedconnections = '1'
        else:
          removeinfectedconnections = '0'

        cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDataSourceParams/' + token )
        jndinames = get('JNDINames')
        rowprefetchenabled = str(get('RowPrefetch'))
        rowprefetchsize = str(get('RowPrefetchSize'))

        cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCConnectionPoolParams/' + token )
        testTableName = get('TestTableName')

        try:
          cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDriverParams/' + token + '/Properties/' + token + '/Properties/user')
          user = get('Value')
        except:
          user = ''

        cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDataSourceParams/' + token)
        globalTransactionsProtocol = get('GlobalTransactionsProtocol')


        try:
            cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCOracleParams/' + token )
            fanenabled = str(get('FanEnabled'))
            onsnodelist = get('OnsNodeList')
        except:
            # In Case any Datasource Type does not include JDBCOracleParams
            fanenabled = '0'
            onsnodelist = ''

        p = ls('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDriverParams/' + token + '/Properties/' + token + '/Properties',returnMap='true')
        properties     = []
        for token3 in p:
            if not token3 == 'user':
               cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCDriverParams/' + token + '/Properties/' + token + '/Properties/'+token3)
               properties.append(token3+"="+str(get('Value')))

        if usexa == '1':
            xapropertiesCur = ''

            cd('/JDBCSystemResources/' + token + '/JDBCResource/' + token + '/JDBCXAParams/' + token)
            xapropertiesarray = ls('', returnMap='true')

            for xaproperty in xapropertiesarray:

                try:
                    val = str(get(xaproperty))

                    if xaproperty == 'isSet' or xaproperty == 'unSet':
                        break
                    elif len(xapropertiesCur) == len(xapropertiesarray) -1:
                        xapropertiesCur += xaproperty + '=' + val
                    else:
                        xapropertiesCur += xaproperty + '=' + val + ','

                except AttributeError:
                    print "%s is not a valid attribute type" % (xaproperty)

        else:
            xapropertiesCur = ''

        target, targetType = retrieve_target_list('/SystemResources/'+token)

        tagged = []
        i = ls('/Servers/', returnMap='true')

        for token4 in i:
            notes = get('/Servers/'+token4+'/Notes')
            if notes:
                if token in notes:
                    for i in ls('/Clusters/', returnMap='true'):
                        if i in notes:
                            tagged.append(i)
                        else:
                            tagged.append(token4)

            add_index_entry(f, [domain+'/'+token,','.join(target),','.join(targetType),driver,','.join(jndinames),url,user,testTableName,','.join(properties)])
f.close()
