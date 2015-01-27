from datetime import datetime, timedelta
from snmp_helper import snmp_get_oid_v3, snmp_extract
from email_helper import send_mail
from creds import a_user, auth_key, encrypt_key, IP, email
import pickle
import os

def getRunningLastChangedV3 (devListTuple, snmpAuthTuple):
    '''
    Given a tuple of device tuples if the format (<IP>, <port>) and an SNMPv3 authentication tuple
    in the format (<username>, <authentication key>, <encryption key>), return a dictionary where
    the key is a device name and the value is a tuple in the format (lastChangeOid, sysUptimeOid).
    '''

    sysNameOid = '1.3.6.1.2.1.1.5.0'
    lastChangeOid = '1.3.6.1.4.1.9.9.43.1.1.1.0'
    sysUptimeOid = '1.3.6.1.2.1.1.3.0'
    rtnDict = dict()

    for aDev in devListTuple:
        devName = snmp_extract(snmp_get_oid_v3(aDev, snmp_user, oid=sysNameOid))
        lastChange = snmp_extract(snmp_get_oid_v3(aDev, snmp_user, oid=lastChangeOid))
        uptime = snmp_extract(snmp_get_oid_v3(aDev, snmp_user, oid=sysUptimeOid))
        rtnDict[devName] = (lastChange, uptime)

    return rtnDict

def saveResults (resultObject, resultsFile):
    '''
    Given an object resultObject and a filename resultsFile, cut the second item in
    the result tuple from each key and pickle the resulting object into the file.
    '''
    newResult = dict()
    for aDev in result:
        newResult[aDev] = resultObject[aDev][0] #Chop off system uptime to save space
    resultFile = open(resultsFile, "wb")
    pickle.dump(newResult, resultFile)
    resultFile.close()



if __name__ == "__main__":

    snmp_user = (a_user, auth_key, encrypt_key)
    pynet_rtr1 = (IP, 7961)
    pynet_rtr2 = (IP, 8061)
    devList = (pynet_rtr1, pynet_rtr2)
    result = getRunningLastChangedV3 (devList, snmp_user)
    savedResult = None
    fileName = "results.p"

    if os.path.isfile(fileName):
        resultFile = open(fileName, "rb")
        savedResult = pickle.load(resultFile)
        resultFile.close()

    # Uncomment these lines and increment the 106068741 value to test
    # result['pynet-rtr1.twb-tech.com'] = list(result['pynet-rtr1.twb-tech.com'])
    # result['pynet-rtr1.twb-tech.com'][0] = 106068741


    if savedResult:
        changesSeen = ''
        for aDev in savedResult:
            if savedResult[aDev] < result[aDev][0]:
                changeSeen = True
                sysUptime = int(result[aDev][1])
                lastChange = int(result[aDev][0])
                lastReboot = datetime.today() - timedelta(microseconds = (sysUptime * 10000))
                changeTime = lastReboot + timedelta(microseconds = (lastChange * 10000))
                changesSeen += "Config for device %s last changed: %s\n" % (aDev, changeTime)

        if changesSeen:
            send_mail(email, "Network changes", changesSeen, "pynet@pynet.org")
            saveResults(result, fileName)

    else: # File doesn't exist, create it.
        saveResults(result, fileName)
