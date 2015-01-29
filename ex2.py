from snmp_helper import snmp_get_oid_v3, snmp_extract
from creds import a_user, auth_key, encrypt_key, IP, email
import pygal
import time

dict1 = {
    "Bytes In":[5269, 5011, 6705, 5987, 5011, 5071, 6451, 5011, 5011, 6181, 5281, 5011],
    "Bytes Out":[5725, 5783, 7670, 6783, 5398, 5783, 9219, 3402, 5783, 6953, 5668, 5783]
}

dict2 = {
    "Packets In":[24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24, 21],
    "Packets Out":[24, 21, 40, 32, 21, 21, 49, 9, 21, 34, 24, 21]
}

pynet_rtr1 = (IP, 7961)
snmp_user = (a_user, auth_key, encrypt_key)

def makeChart(dictOfListsToGraph, timeIncrement, title, fileName):
    '''
    Given a dictionary of lists with graph values, the time increment over which the values
    were gathered, the title of the graph and the fileName, generate a line graph of the values using
    the dictionary keys as Titles for each line.
    '''

    line_chart = pygal.Line()
    line_chart.title = title

    longest = 0
    for anItem in dictOfListsToGraph:
        if len(dictOfListsToGraph[anItem]) > longest:
            longest = len(dictOfListsToGraph[anItem])
    longest *= timeIncrement
    longest += 1
    labelRange = range(int(timeIncrement), longest, int(timeIncrement))
    labelRange = map(str, labelRange)
    # print labelRange
    # strLabelRange = []
    # for aLabel in labelRange:
    #     print str(labelRange[aLabel])
        # strLabelRange.append(str(labelRange[aLabel]))
    line_chart.x_labels = labelRange
    for anItem in dictOfListsToGraph:
        line_chart.add(anItem, dictOfListsToGraph[anItem])
    line_chart.render_to_file(fileName)

# def getBytesAndPacketsV3 (device, snmpAuthTuple, waitBetweenPollsInMinutes, numberOfPolls):
#     '''
#     Given a tuple of device tuples if the format (<IP>, <port>) and an SNMPv3 authentication tuple
#     in the format (<username>, <authentication key>, <encryption key>), return a dictionary where
#     the key is the text definition of the value, and the value is a list of measurements gathered.
#
#     Measurements taken at each poll interval are Bytes In/Out and Packets In/Out.
#     '''
#
#     snmp_oids = {
#         'sysName':'1.3.6.1.2.1.1.5.0',
#         'sysUptime':'1.3.6.1.2.1.1.3.0',
#         'ifDescr_fa4':'1.3.6.1.2.1.2.2.1.2.5',
#         'ifInOctets_fa4':'1.3.6.1.2.1.2.2.1.10.5',
#         'ifInUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.11.5',
#         'ifOutOctets_fa4':'1.3.6.1.2.1.2.2.1.16.5',
#         'ifOutUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.17.5',
#         }
#
#     rtnDict = dict()
#     rtnDict["Bytes In"] = []
#     rtnDict["Bytes Out"] = []
#     rtnDict["Packets In"] = []
#     rtnDict["Packets Out"] = []
#
#     for anInteration in range(numberOfPolls):
#         rtnDict["Bytes In"].append(snmp_extract(snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifInOctets_fa4'])))
#         rtnDict["Bytes Out"].append(snmp_extract(snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifOutOctets_fa4'])))
#         rtnDict["Packets In"].append(snmp_extract(snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifInUcastPkts_fa4'])))
#         rtnDict["Packets Out"].append(snmp_extract(snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifOutUcastPkts_fa4'])))
#
#         time.sleep(waitBetweenPollsInMinutes * 60)
#
#     return rtnDict

if __name__ == "__main__":
    numberOfPolls = 12
    waitBetweenPollsInMinutes = 5
    snmp_oids = {
        'sysName':'1.3.6.1.2.1.1.5.0',
        'sysUptime':'1.3.6.1.2.1.1.3.0',
        'ifDescr_fa4':'1.3.6.1.2.1.2.2.1.2.5',
        'ifInOctets_fa4':'1.3.6.1.2.1.2.2.1.10.5',
        'ifInUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.11.5',
        'ifOutOctets_fa4':'1.3.6.1.2.1.2.2.1.16.5',
        'ifOutUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.17.5',
        }

    bytesDict = dict()
    pktsDict = dict()
    bytesDict["Bytes In"] = []
    bytesDict["Bytes Out"] = []
    pktsDict["Packets In"] = []
    pktsDict["Packets Out"] = []


    for anInteration in range(numberOfPolls):
        bytesDict["Bytes In"].append(int(snmp_extract
                                        (snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifInOctets_fa4']))))
        bytesDict["Bytes Out"].append(int(snmp_extract
                                         (snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifOutOctets_fa4']))))
        pktsDict["Packets In"].append(int(snmp_extract
                                         (snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifInUcastPkts_fa4']))))
        pktsDict["Packets Out"].append(int(snmp_extract
                                          (snmp_get_oid_v3(pynet_rtr1, snmp_user, oid=snmp_oids['ifOutUcastPkts_fa4']))))
        print bytesDict

        time.sleep(waitBetweenPollsInMinutes * 60)

    makeChart(bytesDict, 1, "Input/Output Bytes", "bytes.svg")
    makeChart(pktsDict, 1, "Input/Output Packets", "pkts.svg")
