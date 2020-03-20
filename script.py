# -*- coding: utf-8 -*-
from __future__ import print_function
import libvirt
import sys
import os

def displayMenu():
    print("**************** WELCOME TO THE VM MANAGER ****************")
    choice = raw_input("*** 0- Get hypervisor machine name\n"
                       "*** 1- List stopped virtual machines\n"
                       "*** 2- List active virtual machines\n"
                       "*** 3- Start a machine\n"
                       "*** 4- Stop a machine\n"
                       "*** 5- Show a machine\n"
                       "*** 6- IP address of a machine\n"
                       "*** 7- Quit\n\n"
                       " Enter your choice below: ")

    if choice == "0":
        nameHypervisor()
    elif choice == "1":
        stoppedVMs()
    elif choice == "2":
        activeVMs()
    elif choice == "3":
        startVM()
    elif choice == "4":
        stopVM()
    elif choice == "5":
        showVM()
    elif choice == "6":
        ipAddrVM()
    elif choice == "7":
        conn.close()
        sys.exit
    else:
        print("The number you entred is not valid !")
        again()


#Nom de l'hyperviseur
def nameHypervisor():
    print()
    host = conn.getHostname()
    print('Hostname : '+host)
    print()
    again()

#List des machines eteintes
def stoppedVMs():
    print()
    if len(conn.listDefinedDomains()) == 0:
        print('There are no stopped virtual machine')
    else:
        print('The stopped machines are : ')
        print(conn.listDefinedDomains())
    print()
    again()

#List des machines actives
def activeVMs():
    print()
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('There are no active virtual machine ')
    else:
        print('Active machines : ')
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domain.name(),' ')
    print()
    again()

#Démarrer une machine
def startVM():
    print()
    if len(conn.listDefinedDomains()) == 0:
        print('No stopped virtual machine')
        print()
    else:
        print('Stopped machines : ')
        for i in range(0,len(conn.listDefinedDomains())):
            print (i,": ",conn.listDefinedDomains()[i])
        num = input("Which machine do you want to start ? Enter number: ")
        if (num < len(conn.listDefinedDomains())):
            vm = conn.lookupByName(conn.listDefinedDomains()[num])
            vm.create()
	    os.system("virt-viewer "+vm.name()+"&")
            print("The VM has been successfully started!")
            print()
    again()

#Arreter une machine
def stopVM():
    print()
    print("Active virtual machines : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do u want to stop? Enter ID ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            vm = conn.lookupByName(domain.name())
            vm.destroy()
            print("The VM has been successfully stopped")
            print()
    again()

def ipAddrVM():
    print()
    print("The active virtual machines : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('There are no active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do you want to show its interface address ? Enter ID: ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            vm = conn.lookupByName(domain.name())
	    try:
		    ifaces = vm.interfaceAddresses(libvirt.VIR_DOMAIN_INTERFACE_ADDRESSES_SRC_AGENT, 0)
		    print("The interface IP addresses:")
		    for (name, val) in ifaces.iteritems():
		        if val['addrs']:
		            for ipaddr in val['addrs']:
		                if ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV4:
		                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV4")
		                elif ipaddr['type'] == libvirt.VIR_IP_ADDR_TYPE_IPV6:
		                    print(ipaddr['addr'] + " VIR_IP_ADDR_TYPE_IPV6")
		        print()
	    except:
		    print("Can't get the address! Try installing qemu-guest-tools on the VM")
    again()

#Afficher la machine 
def showVM():
    print()
    print("The active virtual machines are : ")
    domainIDs = conn.listDomainsID()
    if domainIDs == None:
        print('Failed to get a list of domain IDs', file=sys.stderr)
    if len(domainIDs) == 0:
        print('No active virtual machine ')
        print()
    else:
        for domainID in domainIDs:
            domain = conn.lookupByID(domainID)
            print(domainID,': ', domain.name())
        num = input("Which machine do u want to show? Enter ID ")
        if num in domainIDs:
            domain = conn.lookupByID(num)
            os.system("virt-viewer "+ domain.name()+ " &")
            print()
    again()

def again():
    c = raw_input("Try something else ? Tap (y/n) ")
    if c == "y":
        os.system('clear')
        displayMenu()
    else:
        sys.exit

conn = libvirt.open('qemu:///system')
if conn == None:  
    print("A problem has occurred! Connexion failed",file=sys.stderr)
    exit(1)
displayMenu()