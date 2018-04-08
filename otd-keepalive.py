connect ('weblogic','','t3://otd-adminServer:7001')
listRoutes1 ='abc'
configname              = 'https-config'
props = {}
props['configuration'] = configname
props['virtual-server'] = configname
listRoutes=otd_listRoutes(props)

for i in listRoutes:
        edit()
        startEdit()
        print "Value: ------------------------------------------------------------------->"+ i
        props = {}
        props['configuration'] = configname
        props['virtual-server'] = configname
        props['route']=str(i)
        props['use-keep-alive']='false'
        otd_setRouteProperties(props)
        activate(200000, block='true') 
