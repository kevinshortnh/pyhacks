#!/usr/bin/python

import os
import logging
import sys
import stat
import signal

import shutil

#-------------------------------------------------------------------------------
# Define a class for handling %post

class POST:

    #---------------------------------------------------------------------------
    # Filenames
    #
    #   Keep all filenames here, rather than embedding them further in the
    #   script. This will make it a lot easier to review the list of files we
    #   need to inspect during system test.

    FILE_BOOT_GRUB_GRUB_CONF					= '/boot/grub/grub.conf'
    FILE_ETC_AUTO_MASTER					= '/etc/auto.master'
    FILE_ETC_AUTO_NET						= '/etc/auto.net'
    FILE_ETC_CRON_HOURLY_UPDATE_SUDOERS				= '/etc/cron.hourly/update_sudoers'
    FILE_ETC_CUPS_CLASSES_CONF					= '/etc/cups/classes.conf'
    FILE_ETC_CUPS_CUPSD_CONF					= '/etc/cups/cupsd.conf'
    FILE_ETC_CUPS_PPD_HP8150ENG_PPD				= '/etc/cups/ppd/hp8150eng.ppd'
    FILE_ETC_CUPS_PRINTERS_CONF					= '/etc/cups/printers.conf'
    FILE_ETC_DHCLIENT_DATA_CONF					= '/etc/dhclient-data.conf'
    FILE_ETC_EXPORTS						= '/etc/exports'
    FILE_ETC_FSTAB						= '/etc/fstab'
    FILE_ETC_GDM_CUSTOM_CONF					= '/etc/gdm/custom.conf'
    FILE_ETC_HOST_CONF						= '/etc/host.conf'
    FILE_ETC_HOSTS						= '/etc/hosts'
    FILE_ETC_INITTAB						= '/etc/inittab'
    FILE_ETC_KRB5_CONF						= '/etc/krb5.conf'
    FILE_ETC_MODPROBE_CONF					= '/etc/modprobe.conf'
    FILE_ETC_NSSWITCH_CONF					= '/etc/nsswitch.conf'
    FILE_ETC_NTP_CONF						= '/etc/ntp.conf'
    FILE_ETC_NTP_DRIFT_TEMP					= '/etc/ntp/drift.TEMP'
    FILE_ETC_NTP_NTPSERVERS					= '/etc/ntp/ntpservers'
    FILE_ETC_NTP_STEP_TICKERS					= '/etc/ntp/step-tickers'
    FILE_ETC_PAM_D_RSH						= '/etc/pam.d/rsh'
    FILE_ETC_PROFILE_D_SAFARIFUSION_CSH				= '/etc/profile.d/SafariFusion.csh'
    FILE_ETC_PROFILE_D_SAFARIFUSION_SH				= '/etc/profile.d/SafariFusion.sh'
    FILE_ETC_RESOLV_CONF					= '/etc/resolv.conf'
    FILE_ETC_SAMBA_SMB_CONF					= '/etc/samba/smb.conf'
    FILE_ETC_SECURETTY						= '/etc/securetty'
    FILE_ETC_SSH_SSH_CONFIG					= '/etc/ssh/ssh_config'
    FILE_ETC_SUDOERS						= '/etc/sudoers'
    FILE_ETC_SYSCONFIG_I18N					= '/etc/sysconfig/i18n'
    FILE_ETC_SYSCONFIG_NETWORK					= '/etc/sysconfig/network'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_DATA		= '/etc/sysconfig/network-scripts/ifcfg-data'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH0		= '/etc/sysconfig/network-scripts/ifcfg-eth0'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH1		= '/etc/sysconfig/network-scripts/ifcfg-eth1'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH3		= '/etc/sysconfig/network-scripts/ifcfg-eth3'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH4		= '/etc/sysconfig/network-scripts/ifcfg-eth4'
    FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_MGMT		= '/etc/sysconfig/network-scripts/ifcfg-mgmt'
    FILE_ETC_X11_GDM_GDM_CONF					= '/etc/X11/gdm/gdm.conf'
    FILE_ETC_YUM_REPOS_D_CENTOS_BASE_REPO			= '/etc/yum.repos.d/CentOS-Base.repo'
    FILE_ETC_YUM_REPOS_D_FUSION_REPO				= '/etc/yum.repos.d/fusion.repo'
    FILE_ETC_YUM_REPOS_D_VIEW_REPO				= '/etc/yum.repos.d/view.repo'
    FILE_ETC_YUM_REPOS_D_SDE_REPO				= '/etc/yum.repos.d/sde.repo'
    FILE_ROOT_RHOSTS						= '/root/.rhosts'
    FILE_ROOT_SSH_AUTHORIZED_KEYS				= '/root/.ssh/authorized_keys'
    FILE_TMP_ANACONDA_LOG					= '/tmp/anaconda.log'
    FILE_USR_JAVA_JDK						= '/usr/java/jdk'

    #---------------------------------------------------------------------------
    # Directory names
    #
    #   Keep all direcory names here, rather than embedding them further in the
    #   script. This will make it a lot easier to review the list of files we
    #   need to inspect during system test.

    DIR_ETC_NTP		= '/etc/ntp'
    DIR_ETC_SAMBA	= '/etc/samba'
    DIR_ETC_VNC		= '/etc/vnc'
    DIR_ETC_X11_GDM	= '/etc/X11/gdm'
    DIR_ETC_YUM_REPOS_D	= '/etc/yum.repos.d'
    DIR_EXPORT		= '/export'
    DIR_HOME		= '/home'
    DIR_NET		= '/net'
    DIR_ROOT_SSH	= '/root/.ssh'
    DIR_EXPORT		= '/export'
    DIR_EXPORT2		= '/export2'
    DIR_SAFARI_INST	= '/opt'

    #---------------------------------------------------------------------------
    # Linux commands
    #
    #   Keep all Linux commands here, rather than embedding them further in the
    #   script. This will make it a lot easier to review the list of files we
    #   need to inspect during system test.

    CMD_CHMOD     		= '/bin/chmod'
    CMD_CHOWN     		= '/bin/chown'
    CMD_ECHO      		= '/bin/echo'
    CMD_HOSTNAME  		= '/bin/hostname'
    CMD_LN        		= '/bin/ln'
    CMD_LS        		= '/bin/ls'
    CMD_MKDIR     		= '/bin/mkdir'
    CMD_MV        		= '/bin/mv'
    CMD_RM        		= '/bin/rm'
    CMD_SED       		= '/bin/sed'
    CMD_TOUCH     		= '/bin/touch'

    CMD_CHKCONFIG 		= '/sbin/chkconfig'
    CMD_IFCONFIG  		= '/sbin/ifconfig'
    CMD_INIT  			= '/sbin/init'
    CMD_IPTABLES  		= '/sbin/iptables'
    CMD_MODPROBE  		= '/sbin/modprobe'
    CMD_SERVICE   		= '/sbin/service'

    CMD_MYSQL_CLIENT     	= '/usr/bin/mysql'
    CMD_MYSQL_INSTALL_DB	= '/usr/bin/mysql_install_db'

    CMD_EXPORTFS  		= '/usr/sbin/exportfs'

    CMD_ETC_INIT_D_MYSQL	= '/etc/init.d/mysql'

    CMD_ASADMIN   		= '/opt/safari/sailfin/bin/asadmin'


    #---------------------------------------------------------------------------
    # KEEP THESE IN SYNC WITH pre.py SCRIPT !!!

    # These get a SafariFusion configuration

    ENV_FIELD_FUSION		= 'field-fusion'
    ENV_VMFUSION		= 'vmfusion'
    ENV_XBSFUSION		= 'xbsfusion'

    # These get a SafariView configuration

    ENV_FIELD_VIEW		= 'field-view'
    ENV_VMVIEW			= 'vmview'
    ENV_XBSVIEW			= 'xbsview'

    # These get a development configuration

    ENV_DEV			= 'dev'
    ENV_VMDEV			= 'vmdev'
    ENV_MIN			= 'min'
    ENV_SERVER			= 'server'
    ENV_XSOFTMTA		= 'xsoftmta'

    #---------------------------------------------------------------------------
    # These get a SafariFusion configuration

    def isFusionConfig(self):

	return ((self.pre_env == POST.ENV_FIELD_FUSION)
	    or  (self.pre_env == POST.ENV_VMFUSION)
	    or  (self.pre_env == POST.ENV_XBSFUSION))

    #---------------------------------------------------------------------------
    # These get a SafariView configuration

    def isViewConfig(self):

	return ((self.pre_env == POST.ENV_FIELD_VIEW)
	    or  (self.pre_env == POST.ENV_VMVIEW)
	    or  (self.pre_env == POST.ENV_XBSVIEW))

    #---------------------------------------------------------------------------
    # These get a development configuration

    def isDevConfig(self):

	return ((self.pre_env == POST.ENV_DEV)
	    or  (self.pre_env == POST.ENV_VMDEV)
	    or  (self.pre_env == POST.ENV_MIN)
	    or  (self.pre_env == POST.ENV_SERVER)
	    or  (self.pre_env == POST.ENV_XSOFTMTA))

    #---------------------------------------------------------------------------
    # These get a virtual machine configuration

    def isVMConfig(self):

	return ((self.pre_env == POST.ENV_VMDEV)
	    or  (self.pre_env == POST.ENV_VMFUSION)
	    or  (self.pre_env == POST.ENV_VMVIEW))

    #---------------------------------------------------------------------------
    # Run a system command

    def runCommand(self, command):

	self.logger.info('Running: ' + command)

	rc = os.system(command)

	if 0 != rc:

	    self.warn += 1

	    self.logger.warn('Command returned %s' % (rc))

	if '/' != command[0:1]:

	    self.warn += 1

	    self.logger.warn('Command does not begin with "/"')

    #---------------------------------------------------------------------------
    # Initialize object instance

    def __init__(self):

	########################
	# create a custom logger
	########################

	formatter = logging.Formatter(
	    '%(asctime)s %(name)s %(levelname)-8.8s : %(message)s',
	    '%H:%M:%S')

	fh = logging.FileHandler(POST.FILE_TMP_ANACONDA_LOG)
	fh.setFormatter(formatter)

	self.logger = logging.getLogger('xyzzy')
	self.logger.setLevel(logging.DEBUG)
	self.logger.addHandler(fh)
	
	self.logger.info('%post script started')

	self.setPreValues()

	##############
	# Error counts
	##############

	self.critical = 0
	self.warn = 0

    #---------------------------------------------------------------------------
    # Make some directories

    def makeDirectories(self):

	for dir in (

	    POST.DIR_ETC_NTP,
	    POST.DIR_ETC_SAMBA,
	    POST.DIR_ETC_VNC,
	    POST.DIR_ETC_X11_GDM,
	    POST.DIR_ETC_YUM_REPOS_D,
	    POST.DIR_HOME,
	    POST.DIR_NET,
	    POST.DIR_ROOT_SSH,

	    ):

	    self.runCommand(POST.CMD_MKDIR + ' -p ' + dir)

    #---------------------------------------------------------------------------
    # Set hostname
    #
    #   self.hostnameLong  is the FQDN
    #   self.hostnameShort is the hostname, withthe domain name stripped off

    def setHostname(self):

	self.hostnameLong = self.pre_hostname

	########################
	# set the short hostname
	########################

	if self.hostnameLong.find('.') >= 0:

	    self.hostnameShort = self.hostnameLong[0:self.hostnameLong.find('.')]

	else:

	    self.hostnameShort = self.hostnameLong

	#######################################
	# use IP address instead of 'localhost'
	#######################################

	if 'localhost' == self.hostnameShort:

	    f = os.popen(POST.CMD_IFCONFIG)
	    ifconfig = f.readlines()
	    f.close()

	    self.hostnameShort = ifconfig[1].split()[1][5:].replace('.','-')
	    self.hostnameLong  = self.hostnameShort

	##############
	# set hostname
	##############

	self.runCommand(POST.CMD_HOSTNAME + ' ' + self.hostnameLong)

    #---------------------------------------------------------------------------
    # Set /etc/hosts - hosts file

    def setHostsFile(self):

	f = file(POST.FILE_ETC_HOSTS,'w')
	f.write('127.0.0.1\t%s %s localhost\n' % (self.hostnameLong, self.hostnameShort))
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_HOSTS)

    #---------------------------------------------------------------------------
    # Set resolver configuration files

    def setNameResolver(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_HOST_CONF,'w')
	f.write('order hosts, bind\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_HOST_CONF)

	f = file(POST.FILE_ETC_RESOLV_CONF,'w')
	if self.pre_isCorporate:
	    f.write('domain cedarpointcom.com\n')
	    f.write('search cedarpointcom.com\n')
	    f.write('nameserver 192.168.101.201\n')
	    f.write('nameserver 192.168.101.202\n')
	else:
	    f.write('domain sweng.com\n')
	    f.write('search sweng.com cedarpointcom.com\n')
	    f.write('nameserver 172.16.0.7\n')
	    f.write('nameserver 192.168.101.201\n')
	    f.write('nameserver 192.168.101.202\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_RESOLV_CONF)

	f = file(POST.FILE_ETC_DHCLIENT_DATA_CONF,'w')
	f.write('send host-name "%s";\n' % (self.hostnameLong))
	if not self.pre_isCorporate:
	    f.write('prepend domain-name "sweng.com ";\n')
	    f.write('prepend domain-name-servers 172.16.0.7;\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_DHCLIENT_DATA_CONF)

    #---------------------------------------------------------------------------
    # Set /etc/nsswitch.conf - Name Service Switch configuration file

    def setNameServiceSwitchConf(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_NSSWITCH_CONF,'w')
	f.write('''#
# /etc/nsswitch.conf
#
# An example Name Service Switch config file. This file should be
# sorted with the most-used services at the beginning.
#
# The entry '[NOTFOUND=return]' means that the search for an
# entry should stop if the search in the previous entry turned
# up nothing. Note that if the search failed due to some other reason
# (like no NIS server responding) then the search continues with the
# next entry.
#
# Legal entries are:
#
#	nisplus or nis+		Use NIS+ (NIS version 3)
#	nis or yp		Use NIS (NIS version 2), also called YP
#	dns			Use DNS (Domain Name Service)
#	files			Use the local files
#	db			Use the local database (.db) files
#	compat			Use NIS on compat mode
#	hesiod			Use Hesiod for user lookups
#	[NOTFOUND=return]	Stop searching if not found so far
#

# To use db, put the "db" in front of "files" for entries you want to be
# looked up first in the databases
#
# Example:
#passwd:    db files nisplus nis
#shadow:    db files nisplus nis
#group:     db files nisplus nis

passwd:     files nis
shadow:     files nis
group:      files nis

#hosts:     db files nisplus nis dns
hosts:      files dns

# Example - obey only what nisplus tells us...
#services:   nisplus [NOTFOUND=return] files
#networks:   nisplus [NOTFOUND=return] files
#protocols:  nisplus [NOTFOUND=return] files
#rpc:        nisplus [NOTFOUND=return] files
#ethers:     nisplus [NOTFOUND=return] files
#netmasks:   nisplus [NOTFOUND=return] files     

bootparams: nisplus [NOTFOUND=return] files

ethers:     db files
netmasks:   files
networks:   files dns
protocols:  files nis
rpc:        db files
services:   files nis

netgroup:   files nis

publickey:  nisplus

automount:  files nis
aliases:    files nisplus
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_NSSWITCH_CONF)

    #---------------------------------------------------------------------------
    # Set Network Time Protocol server options files

    def setNTP(self):

	##################################
	# Customize these for dev env only
	##################################

	if self.isDevConfig():

	    f = file(POST.FILE_ETC_NTP_CONF,'w')
	    f.write('''# Prohibit general access to this service.
restrict default ignore
restrict 192.168.101.201 mask 255.255.255.255 nomodify notrap noquery

# Permit all access over the loopback interface.  This could
# be tightened as well, but to do so would effect some of
# the administrative functions.
restrict 127.0.0.1 


# -- CLIENT NETWORK -------
# Permit systems on this network to synchronize with this
# time service.  Do not permit those systems to modify the
# configuration of this service.  Also, do not use those
# systems as peers for synchronization.
# restrict 192.168.1.0 mask 255.255.255.0 notrust nomodify notrap


# --- OUR TIMESERVERS ----- 
# or remove the default restrict line 
# Permit time synchronization with our time source, but do not
# permit the source to query or modify the service on this system.

# restrict mytrustedtimeserverip mask 255.255.255.255 nomodify notrap noquery
# server mytrustedtimeserverip



# --- NTP MULTICASTCLIENT ---
#multicastclient			# listen on default 224.0.1.1
# restrict 224.0.1.1 mask 255.255.255.255 notrust nomodify notrap
# restrict 192.168.1.0 mask 255.255.255.0 notrust nomodify notrap



# --- GENERAL CONFIGURATION ---
#
# Undisciplined Local Clock. This is a fake driver intended for backup
# and when no outside source of synchronized time is available. The
# default stratum is usually 3, but in this case we elect to use stratum
# 0. Since the server line does not have the prefer keyword, this driver
# is never used for synchronization, unless no other other
# synchronization source is available. In case the local host is
# controlled by some external source, such as an external oscillator or
# another protocol, the prefer keyword would cause the local host to
# disregard all other synchronization sources, unless the kernel
# modifications are in use and declare an unsynchronized condition.
#
server 192.168.101.201
fudge	127.127.1.0 stratum 10	

#
# Drift file.  Put this in a directory which the daemon can write to.
# No symbolic links allowed, either, since the daemon updates the file
# by creating a temporary in the same directory and then rename()'ing
# it to the file.
#
driftfile /etc/ntp/drift
broadcastdelay	0.008

#
# Authentication delay.  If you use, or plan to use someday, the
# authentication facility you should make the programs in the auth_stuff
# directory and figure out what this number should be on your machine.
#
#authenticate yes

#
# Keys file.  If you want to diddle your server at run time, make a
# keys file (mode 600 for sure) and define the key number to be
# used for making requests.
#
# PLEASE DO NOT USE THE DEFAULT VALUES HERE. Pick your own, or remote
# systems might be able to reset your clock at will. Note also that
# ntpd is started with a -A flag, disabling authentication, that
# will have to be removed as well.
#
keys		/etc/ntp/keys
''')
	    f.close()
	    self.logger.info('Wrote ' + POST.FILE_ETC_NTP_CONF)

	    f = file(POST.FILE_ETC_NTP_STEP_TICKERS,'w')
	    f.write('''corpdc1
''')
	    f.close()
	    self.logger.info('Wrote ' + POST.FILE_ETC_NTP_STEP_TICKERS)

	    f = file(POST.FILE_ETC_NTP_NTPSERVERS,'w')
	    f.write('''corpdc1.cedarpointcom.com
corpdc2.cedarpointcom.com
''')
	    f.close()
	    self.logger.info('Wrote ' + POST.FILE_ETC_NTP_NTPSERVERS)

	######################################
	# Customize these for all environments
	######################################

	commands = [

	    POST.CMD_TOUCH + ' '     + POST.FILE_ETC_NTP_DRIFT_TEMP,
	    POST.CMD_CHMOD + ' 777 ' + POST.FILE_ETC_NTP_DRIFT_TEMP,

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set /etc/auto.* - Automounter files

    def setAutomounter(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_AUTO_NET,'w')
	f.write('''#!/bin/bash

# $Id: auto.net,v 1.8 2005/04/05 13:02:09 raven Exp $

# This file must be executable to work! chmod 755!

# Look at what a host is exporting to determine what we can mount.
# This is very simple, but it appears to work surprisingly well

key="$1"

# add "nosymlink" here if you want to suppress symlinking local filesystems
# add "nonstrict" to make it OK for some filesystems to not mount
opts="-fstype=nfs,hard,intr,nodev"

nismap=`ypcat -k auto.net 2>/dev/null | awk '(\$1 == key)  {print \$2}' key=$key 2>/dev/null`
if [ -n "$nismap" ]
then
	echo "$opts / $nismap"
	exit 0
fi


# # Special cases for XYZZY
# case "$key" in 
# 	local)
# 		echo "$opts \"
# 		echo "        / netstore:/tools/local"
# 		exit 0
# 		;;
# 	logs)
# 		echo "$opts \"
# 		echo "        / logsrv01:/mnt/log"
# 		exit 0
# 		;;
# esac
		
		
# Showmount comes in a number of names and varieties.  "showmount" is
# typically an older version which accepts the '--no-headers' flag
# but ignores it.  "kshowmount" is the newer version installed with knfsd,
# which both accepts and acts on the '--no-headers' flag.
#SHOWMOUNT="kshowmount --no-headers -e $key"
#SHOWMOUNT="showmount -e $key | tail -n +2"

for P in /bin /sbin /usr/bin /usr/sbin
do
	for M in showmount kshowmount
	do
		if [ -x $P/$M ]
		then
			SMNT=$P/$M
			break
		fi
	done
done

[ -x $SMNT ] || exit 1

# Newer distributions get this right
SHOWMOUNT="$SMNT --no-headers -e $key"

$SHOWMOUNT | LC_ALL=C sort -k 1 | 	awk -v key="$key" -v opts="$opts" -- '
	BEGIN	{ ORS=""; first=1 }
		{ if (first) { print opts; first=0 }; print "\\\n\t" $1, key ":" $1 }
	END	{ if (!first) print "\\n"; else exit 1 }
	' | sed 's/#/\#/g'
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_AUTO_NET)

	f = file(POST.FILE_ETC_AUTO_MASTER,'w')
	f.write('/home\typ:auto.home\t--timeout=300\n')
	f.write('/net\t/etc/auto.net\t--timeout=300\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_AUTO_MASTER)

    #---------------------------------------------------------------------------
    # Set /etc/fstab - file system table

    def setFSTab(self):

	commands = [

	    (POST.CMD_SED +
		" -i.bak -e '/tmpfs/d' " +
		POST.FILE_ETC_FSTAB),

	    (POST.CMD_SED +
		" -i.bak -e '$atmpfs\t\t\t/tmp\t\t\ttmpfs\tdefaults\t0 0' " +
		POST.FILE_ETC_FSTAB),

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set GNOME Display Manager configuration

    def setGDM(self):

	if not self.isDevConfig():

	    return

	self.runCommand(POST.CMD_SED +
	    " -i.bak -e '/\[security\]/aDisallowTCP=false' " +
	    POST.FILE_ETC_GDM_CUSTOM_CONF)

	f = file(POST.FILE_ETC_X11_GDM_GDM_CONF,'w')
	f.write('''# GDM Configuration file.  You can use gdmsetup program to graphically
# edit this, or you can optionally just edit this file by hand.  Note that
# gdmsetup does not tweak every option here, just the ones most users
# would care about.  Rest is for special setups and distro specific
# tweaks.  If you edit this file, you should send the HUP or USR1 signal to
# the daemon so that it restarts: (Assuming you have not changed PidFile)
#   kill -USR1 `cat /var/run/gdm.pid`
# (HUP will make gdm restart immediately while USR1 will make gdm not kill
# existing sessions and will only restart gdm after all users log out)
#
# You can also use the gdm-restart and gdm-safe-restart scripts which just
# do the above for you.
#
# For full reference documentation see the gnome help browser under
# GNOME|System category.  You can also find the docs in HTML form
# on http://www.jirka.org/gdm.html
#
# NOTE: Some of these are commented out but still show their default values.
# If you wish to change them you must remove the '#' from the beginning of
# the line.  The commented out lines are lines where the default might
# change in the future, so set them one way or another if you feel
# strongly about it.
#
# Have fun! - George

[daemon]
# Automatic login, if true the first local screen will automatically logged
# in as user as set with AutomaticLogin key.
AutomaticLoginEnable=false
AutomaticLogin=

# Timed login, useful for kiosks.  Log in a certain user after a certain
# amount of time
TimedLoginEnable=false
TimedLogin=
TimedLoginDelay=30

# The gdm configuration program that is run from the login screen, you should
# probably leave this alone
#Configurator=/usr/sbin/gdmsetup --disable-sound --disable-crash-dialog

# The chooser program.  Must output the chosen host on stdout, probably you
# should leave this alone
#Chooser=/usr/bin/gdmchooser

# Greeter for local (non-xdmcp) logins.  Change gdmgreeter to gdmlogin to
# get the standard greeter.
Greeter=/usr/bin/gdmgreeter

# The greeter for xdmcp logins, usually you want a less graphically intensive
# greeter here so it's better to leave this with gdmlogin
#RemoteGreeter=/usr/bin/gdmlogin

# Launch the greeter with an additional list of colon seperated gtk 
# modules. This is useful for enabling additional feature support 
# e.g. gnome accessibility framework. Only "trusted" modules should
# be allowed to minimise security holes
#AddGtkModules=false
# By default these are the accessibility modules
#GtkModulesList=gail:atk-bridge:/usr/lib/gtk-2.0/modules/libdwellmouselistener:/usr/lib/gtk-2.0/modules/libkeymouselistener

# Default path to set.  The profile scripts will likely override this
DefaultPath=/usr/local/bin:/usr/bin:/bin:/usr/X11R6/bin
# Default path for root.  The profile scripts will likely override this
RootPath=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/usr/X11R6/bin

# If you are having trouble with using a single server for a long time and
# want gdm to kill/restart the server, turn this on
#AlwaysRestartServer=false

# User and group that gdm should run as.  Probably should be gdm and gdm and
# you should create these user and group.  Anyone found running this as
# someone too privilaged will get a kick in the ass.  This should have
# access to only the gdm directories and files.
User=gdm
Group=gdm
# To try to kill all clients started at greeter time or in the Init script.
# doesn't always work, only if those clients have a window of their own
#KillInitClients=true
LogDir=/var/log/gdm
# You should probably never change this value unless you have a weird setup
PidFile=/var/run/gdm.pid
# Note that a post login script is run before a PreSession script.
# It is run after the login is successful and before any setup is
# run on behalf of the user
PostLoginScriptDir=/etc/X11/gdm/PostLogin/
PreSessionScriptDir=/etc/X11/gdm/PreSession/
PostSessionScriptDir=/etc/X11/gdm/PostSession/
DisplayInitDir=/etc/X11/gdm/Init
# Distributions:  If you have some script that runs an X server in say
# VGA mode, allowing a login, could you please send it to me?
#FailsafeXServer=
# if X keeps crashing on us we run this script.  The default one does a bunch
# of cool stuff to figure out what to tell the user and such and can
# run an X configuration program.
XKeepsCrashing=/etc/X11/gdm/XKeepsCrashing
# Reboot, Halt and suspend commands, you can add different commands
# separated by a semicolon and gdm will use the first one it can find
#RebootCommand=/sbin/reboot;/sbin/shutdown -r now;/usr/sbin/shutdown -r now;/usr/bin/reboot
#HaltCommand=/sbin/poweroff;/sbin/shutdown -h now;/usr/sbin/shutdown -h now;/usr/bin/poweroff
#SuspendCommand=
# Probably should not touch the below this is the standard setup
ServAuthDir=/var/gdm
# This is our standard startup script.  A bit different from a normal
# X session, but it shares a lot of stuff with that.  See the provided
# default for more information.
BaseXsession=/etc/X11/xdm/Xsession
# This is a directory where .desktop files describing the sessions live
# It is really a PATH style variable since 2.4.4.2 to allow actual
# interoperability with KDM.  Note that <sysconfdir>/dm/Sessions is there
# for backwards compatibility reasons with 2.4.4.x
#SessionDesktopDir=/etc/X11/sessions/:/etc/X11/dm/Sessions/:/usr/share/gdm/BuiltInSessions/:/usr/share/xsessions/
# This is the default .desktop session.  One of the ones in SessionDesktopDir
DefaultSession=default.desktop
# Better leave this blank and HOME will be used.  You can use syntax ~/ below
# to indicate home directory of the user.  You can also set this to something
# like /tmp if you don't want the authorizations to be in home directories.
# This is useful if you have NFS mounted home directories.  Note that if this
# is the home directory the UserAuthFBDir will still be used in case the home
# directory is NFS, see security/NeverPlaceCookiesOnNFS to override this behaviour.
UserAuthDir=
# Fallback if home directory not writable
UserAuthFBDir=/tmp
UserAuthFile=.Xauthority
# The X server to use if we can't figure out what else to run.
StandardXServer=/usr/X11R6/bin/X
# The maximum number of flexible X servers to run.
#FlexibleXServers=5
# And after how many minutes should we reap the flexible server if there is
# no activity and no one logged on.  Set to 0 to turn off the reaping.
# Does not affect Xnest flexiservers.
#FlexiReapDelayMinutes=5
# the X nest command
Xnest=/usr/X11R6/bin/Xnest -audit 0 -name Xnest
# Automatic VT allocation.  Right now only works on Linux.  This way
# we force X to use specific vts.  turn VTAllocation to false if this
# is causing problems.
#FirstVT=7
#VTAllocation=true
# Should double login be treated with a warning (and possibility to change
# vts on linux systems for console logins)
#DoubleLoginWarning=true

# If true then the last login information is printed to the user before
# being prompted for password.  While this gives away some info on what
# users are on a system, it on the other hand should give the user an
# idea of when they logged in and if it doesn't seem kosher to them,
# they can just abort the login and contact the sysadmin (avoids running
# malicious startup scripts)
#DisplayLastLogin=false

# Program used to play sounds.  Should not require any 'daemon' or anything
# like that as it will be run when no one is logged in yet.
#SoundProgram=/usr/bin/play

# These are the languages that the console cannot handle because of font
# issues.  Here we mean the text console, not X.  This is only used
# when there are errors to report and we cannot start X.
# This is the default:
#ConsoleCannotHandle=am,ar,az,bn,el,fa,gu,hi,ja,ko,ml,mr,pa,ta,zh

[security]
# If any distributions ship with this one off, they should be shot
# this is only local, so it's only for say kiosk use, when you
# want to minimize possibility of breakin
AllowRoot=true
# If you want to be paranoid, turn this one off
AllowRemoteRoot=true
# This will allow remote timed login
AllowRemoteAutoLogin=false
# 0 is the most anal, 1 allows group write permissions, 2 allows all write
# permissions
RelaxPermissions=0
# Check if directories are owned by logon user.  Set to false, if you have, for
# example, home directories owned by some other user.
CheckDirOwner=true
# Number of seconds to wait after a bad login
#RetryDelay=1
# Maximum size of a file we wish to read.  This makes it hard for a user to DoS
# us by using a large file.
#UserMaxFile=65536
# If true this will basically append -nolisten tcp to every X command line,
# a good default to have (why is this a "negative" setting? because if
# it is false, you could still not allow it by setting command line of
# any particular server).  It's probably better to ship with this on
# since most users will not need this and it's more of a security risk
# then anything else.
# Note: Anytime we find a -query or -indirect on the command line we do
# not add a "-nolisten tcp", as then the query just wouldn't work, so
# this setting only affects truly local sessions.
#DisallowTCP=true
DisallowTCP=false
# By default never place cookies if we "detect" NFS.  We detect NFS
# by detecting "root-squashing".  It seems bad practice to place
# cookies on things that go over the network by default and thus we
# don't do it by default.  Sometimes you can however use safe remote
# filesystems where this is OK and you may want to have the cookie in your
# home directory.
#NeverPlaceCookiesOnNFS=true

# XDMCP is the protocol that allows remote login.  If you want to log into
# gdm remotely (I'd never turn this on on open network, use ssh for such
# remote usage that).  You can then run X with -query <thishost> to log in,
# or -indirect <thishost> to run a chooser.  Look for the 'Terminal' server
# type at the bottom of this config file.
[xdmcp]
# Distributions: Ship with this off.  It is never a safe thing to leave
# out on the net.  Setting up /etc/hosts.allow and /etc/hosts.deny to only
# allow local access is another alternative but not the safest.
# Firewalling port 177 is the safest if you wish to have xdmcp on.
# Read the manual for more notes on the security of XDMCP.
Enable=false
# Honour indirect queries, we run a chooser for these, and then redirect
# the user to the chosen host.  Otherwise we just log the user in locally.
#HonorIndirect=true
# Maximum pending requests
#MaxPending=4
#MaxPendingIndirect=4
# Maximum open XDMCP sessions at any point in time
#MaxSessions=16
# Maximum wait times
#MaxWait=15
#MaxWaitIndirect=15
# How many times can a person log in from a single host.  Usually better to
# keep low to fend off DoS attacks by running many logins from a single
# host.  This is now set at 2 since if the server crashes then gdm doesn't
# know for some time and wouldn't allow another session.
#DisplaysPerHost=2
# The number of seconds after which a non-responsive session is logged off.
# Better keep this low.
#PingIntervalSeconds=15
# The port.  177 is the standard port so better keep it that way
#Port=177
# Willing script, none is shipped and by default we'll send
# hostname system id.  But if you supply something here, the
# output of this script will be sent as status of this host so that
# the chooser can display it.  You could for example send load,
# or mail details for some user, or some such.
#Willing=/etc/X11/gdm/Xwilling

[gui]
# The specific gtkrc file we use.  It should be the full path to the gtkrc
# that we need.  Unless you need a specific gtkrc that doesn't correspond to
# a specific theme, then just use the GtkTheme key
#GtkRC=/usr/share/themes/Default/gtk/gtkrc

# The GTK+ theme to use for the gui
GtkTheme=Bluecurve
# If to allow changing the GTK+ (widget) theme from the greeter.  Currently
# this only affects the standard greeter as the graphical greeter does
# not yet have this ability
#AllowGtkThemeChange=true
# Comma separated list of themes to allow.  These must be the names of the
# themes installed in the standard locations for gtk themes.  You can
# also specify 'all' to allow all installed themes.  These should be just
# the basenames of the themes such as 'Thinice' or 'LowContrast'.
#GtkThemesToAllow=all

# Maximum size of an icon, larger icons are scaled down
#MaxIconWidth=128
#MaxIconHeight=128

[greeter]
# Greeter has a nice title bar that the user can move
TitleBar=false
# Configuration is available from the system menu of the greeter
ConfigAvailable=false
# Face browser is enabled.  This only works currently for the
# standard greeter as it is not yet enabled in the graphical greeter.
Browser=false
# The default picture in the browser
#DefaultFace=/usr/share/pixmaps/nobody.png
# These are things excluded from the face browser, not from logging in
#Exclude=bin,daemon,adm,lp,sync,shutdown,halt,mail,news,uucp,operator,nobody,gdm,postgres,pvm,rpm,nfsnobody,pcap
# As an alternative to the above this is the minimum uid to show
MinimalUID=500
# If user or user.png exists in this dir it will be used as his picture
#GlobalFaceDir=/usr/share/faces/
# File which contains the locale we show to the user.  Likely you want to use
# the one shipped with gdm and edit it.  It is not a standard locale.alias file,
# although gdm will be able to read a standard locale.alias file as well.
#LocaleFile=/etc/X11/gdm/locale.alias
# Logo shown in the standard greeter
#Logo=/usr/share/pixmaps/gdm-foot-logo.png
Logo=
## nice RH logo for the above line: /usr/share/pixmaps/redhat/shadowman-200.png
# The standard greeter should shake if a user entered the wrong username or
# password.  Kind of cool looking
#Quiver=true
# The Actions menu (formerly system menu) is shown in the greeter, this is the
# menu that contains reboot, shutdown, suspend, config and chooser.  None of
# these is available if this is off.  They can be turned off individually
# however
#SystemMenu=true
# Should the chooser button be shown.  If this is shown, GDM can drop into
# chooser mode which will run the xdmcp chooser locally and allow the user
# to connect to some remote host.  Local XDMCP does not need to be enabled
# however
#ChooserButton=true
# Note to distributors, if you wish to have a different Welcome string
# and wish to have this translated you can have entries such as
# Welcome[cs]=Vitejte na %n
# Just make sure the string is in utf-8
# Welcome is for all console logins and RemoteWelcome is for remote logins
# (through XDMCP).
# The default entries that are shipped are translated inside gdm and
# are as follows:
#Welcome=Welcome
#RemoteWelcome=Welcome to %n
# Don't allow user to move the standard greeter window.  Only makes sense
# if TitleBar is on
#LockPosition=false
# Set a position rather then just centering the window.  If you enter
# negative values for the position it is taken as an offset from the
# right or bottom edge.
#SetPosition=false
#PositionX=0
#PositionY=0
# Xinerama screen we use to display the greeter on.  Not for true
# multihead, currently only works for Xinerama.
#XineramaScreen=0
# Background settings for the standard greeter:
# Type can be 0=None, 1=Image, 2=Color
#BackgroundType=2
#BackgroundImage=
#BackgroundScaleToFit=true
BackgroundColor=#20305a
# XDMCP session should only get a color, this is the sanest setting since
# you don't want to take up too much bandwidth
#BackgroundRemoteOnlyColor=true
# Program to run to draw the background in the standard greeter.  Perhaps
# something like an xscreensaver hack or some such.
#BackgroundProgram=
# if this is true then the background program is run always, otherwise
# it is only run when the BackgroundType is 0 (None)
#RunBackgroundProgramAlways=false
# Show the Failsafe sessions.  These are much MUCH nicer (focus for xterm for
# example) and more failsafe then those supplied by scripts so distros should
# use this rather then just running an xterm from a script.
ShowGnomeFailsafeSession=false
#ShowXtermFailsafeSession=true
# Normally there is a session type called 'Last' that is shown which refers to
# the last session the user used.  If off, we will be in 'switchdesk' mode where
# the session saving stuff is disabled in GDM
ShowLastSession=false
# Always use 24 hour clock no matter what the locale.
#Use24Clock=false
# Use circles in the password field.  Looks kind of cool actually,
# but only works with certain fonts.
#UseCirclesInEntry=false
# These two keys are for the new greeter.  Circles is the standard
# shipped theme
GraphicalTheme=Default
GraphicalThemeDir=/usr/share/gdm/themes/
# If InfoMsgFile points to a file, the greeter will display the contents of the
# file in a modal dialog box before the user is allowed to log in.
#InfoMsgFile=
# If InfoMsgFile is present then InfoMsgFont can be used to specify the font
# to be used when displaying the contents of the file.
#InfoMsgFont=Sans 24
# If SoundOnLogin is true, then the greeter will beep when login is ready
# for user input.  If SoundOnLogin is a file and the greeter finds the
# 'play' executable (see daemon/SoundProgram) it will play that file
# instead of just beeping
#SoundOnLogin=true
SoundOnLogin=false
#SoundOnLoginFile=
SoundOnLoginFile=/usr/share/sounds/KDE_Startup_new.wav

# The chooser is what's displayed when a user wants an indirect XDMCP
# session, or selects Run XDMCP chooser from the system menu
[chooser]
# Default image for hosts
#DefaultHostImg=/usr/share/pixmaps/nohost.png
# Directory with host images, they are named by the hosts: host or host.png
HostImageDir=/usr/share/hosts/
# Time we scan for hosts (well only the time we tell the user we are
# scanning actually, we continue to listen even after this has
# expired)
#ScanTime=4
# A comma separated lists of hosts to automatically add (if they answer to
# a query of course).  You can use this to reach hosts that broadcast cannot
# reach.
Hosts=
# Broadcast a query to get all hosts on the current network that answer
Broadcast=true
# Set it to true if you want to send a multicast query to hosts.
Multicast=false
# It is an IPv6 multicast address.It is hardcoded here and will be replaced when
# officially registered xdmcp multicast address of TBD will be available
#Multicast_Addr=ff02::1
# Allow adding random hosts to the list by typing in their names
#AllowAdd=true

[debug]
# This will enable debugging into the syslog, usually not neccessary
# and it creates a LOT of spew of random stuff to the syslog.  However it
# can be useful in determining when something is going very wrong.
Enable=false

[servers]
# These are the standard servers.  You can add as many you want here
# and they will always be started.  Each line must start with a unique
# number and that will be the display number of that server.  Usually just
# the 0 server is used.
0=Standard
#1=Standard
# Note the VTAllocation and FirstVT keys on linux.  Don't add any vt<number>
# arguments if VTAllocation is on, and set FirstVT to be the first vt
# available that your gettys don't grab (gettys are usually dumb and grab
# even a vt that has already been taken).  Using 7 will work pretty much for
# all linux distributions.  VTAllocation is not currently implemented on
# anything but linux since I don't own any non-linux systems.  Feel free to
# send patches.  X servers will just not get any extra arguments then.
#
# If you want to run an X terminal you could add an X server such as this
#0=Terminal -query serverhostname
# or for a chooser (optionally serverhostname could be localhost)
#0=Terminal -indirect serverhostname
#
# If you wish to run the XDMCP chooser on the local display use the following
# line
#0=Chooser

## Note:
# is your X server not listening to TCP requests?  Perhaps you should look
# at the security/DisallowTCP setting!

# Definition of the standard X server.
[server-Standard]
name=Standard server
command=/usr/X11R6/bin/X -audit 0
flexible=true

# To use this server type you should add -query host or -indirect host
# to the command line
[server-Terminal]
name=Terminal server
# Add -terminate to make things behave more nicely
command=/usr/X11R6/bin/X -audit 0 -terminate
# Make this not appear in the flexible servers (we need extra params
# anyway, and terminate would be bad for xdmcp choosing).  You can
# make a terminal server flexible, but not with an indirect query.
# If you need flexible indirect query server, then you must get rid
# of the -terminate and the only way to kill the flexible server will
# then be by Ctrl-Alt-Backspace
flexible=false
# Not local, we do not handle the logins for this X server
handled=false

# To use this server type you should add -query host or -indirect host
# to the command line
[server-Chooser]
name=Chooser server
command=/usr/X11R6/bin/X -audit 0
# Make this not appear in the flexible servers for now, but if you
# wish to allow a chooser server then make this true.  This is the
# only way to make a flexible chooser server that behaves nicely.
flexible=false
# Run the chooser instead of the greeter.  When the user chooses a
# machine they will get this same server but run with
# "-terminate -query hostname"
chooser=true
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_X11_GDM_GDM_CONF)

    #---------------------------------------------------------------------------
    # Set /etc/pam.d/rsh - Pluggable Authentication Modules file

    def setPAM(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_PAM_D_RSH,'w')
	f.write('''#%PAM-1.0
# For root login to succeed here with pam_securetty, "rsh" must be
# listed in /etc/securetty.
auth       required	pam_nologin.so
auth       required	pam_securetty.so
auth       required	pam_env.so
auth       optional	pam_rhosts_auth.so
account    required	pam_stack.so service=system-auth
session    required	pam_stack.so service=system-auth
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_PAM_D_RSH)

    #---------------------------------------------------------------------------
    # Set /etc/securetty - file which lists ttys from which root can log in

    def setSecureTTY(self):

	f = file(POST.FILE_ETC_SECURETTY,'w')

	f.write('''console
vc/1
vc/2
vc/3
vc/4
vc/5
vc/6
vc/7
vc/8
vc/9
vc/10
vc/11
tty1
tty2
tty3
tty4
tty5
tty6
tty7
tty8
tty9
tty10
tty11
ttyS0
ttyS1
''')

	if self.isDevConfig():

	    f.write('''rlogin
rsh
''')

	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SECURETTY)

    #---------------------------------------------------------------------------
    # Set /etc/ssh/ssh_config - Secure Shell

    def setSSH(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_SSH_SSH_CONFIG,'w')
	f.write('''#	$OpenBSD: ssh_config,v 1.19 2003/08/13 08:46:31 markus Exp $

# This is the ssh client system-wide configuration file.  See
# ssh_config(5) for more information.  This file provides defaults for
# users, and the values can be changed in per-user configuration files
# or on the command line.

# Configuration data is parsed as follows:
#  1. command line options
#  2. user-specific file
#  3. system-wide file
# Any configuration value is only changed the first time it is set.
# Thus, host-specific definitions should be at the beginning of the
# configuration file, and defaults at the end.

# Site-wide defaults for various options

# Host *
#   ForwardAgent no
    ForwardX11 yes
#   RhostsRSAAuthentication no
#   RSAAuthentication yes
#   PasswordAuthentication yes
#   HostbasedAuthentication no
#   BatchMode no
#   CheckHostIP yes
#   AddressFamily any
#   ConnectTimeout 0
#   StrictHostKeyChecking ask
#   IdentityFile ~/.ssh/identity
#   IdentityFile ~/.ssh/id_rsa
#   IdentityFile ~/.ssh/id_dsa
#   Port 22
#   Protocol 2,1
#   Cipher 3des
#   Ciphers aes128-cbc,3des-cbc,blowfish-cbc,cast128-cbc,arcfour,aes192-cbc,aes256-cbc
#   EscapeChar ~
Host *
	GSSAPIAuthentication yes
# If this option is set to yes then the remote X11 clients will have full access
# to the local X11 display. As virtually no X11 client supports the untrusted
# mode correctly we set this to yes.
       ForwardX11Trusted yes
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SSH_SSH_CONFIG)

    #---------------------------------------------------------------------------
    # Set sudoers

    def setSudoers(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_SUDOERS,'w')
	f.write('''# sudoers file.
#
# This file MUST be edited with the 'visudo' command as root.
#
# See the sudoers man page for the details on how to write a sudoers file.
#
Cmnd_Alias SUROOT =! /bin/su "", !/bin/su - , !/bin/su.static "",!/bin//su.static - , /bin/su - [a-z]*, /bin/su [a-z]* , !/bin/su root, !/bin/su - root, !/bin/su -[a-z]*, !/su.static -[a-z]* , !/usr/sbin/visudo, !/usr/bin/passwd root

# Host alias specification

# User alias specification

User_Alias	SDE = byoung, byoung02, mbrunelle, dmerrill
User_Alias	IT = jgraham
User_Alias      EIT = kshort


# Cmnd alias specification

# Defaults specification

# User privilege specification
root    ALL=(ALL) ALL
%clearusers    ALL=ALL, SUROOT

SDE     ALL=ALL, SUROOT
EIT     ALL=ALL, SUROOT
IT      ALL=ALL, SUROOT

# Uncomment to allow people in group wheel to run all commands
# %wheel        ALL=(ALL)       ALL

# Same thing without a password
# %wheel        ALL=(ALL)       NOPASSWD: ALL

# Samples
# %users  ALL=/sbin/mount /cdrom,/sbin/umount /cdrom
# %users  localhost=/sbin/shutdown -h now
Defaults logfile=/var/log/sudolog, insults
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SUDOERS)

	f = file(POST.FILE_ETC_CRON_HOURLY_UPDATE_SUDOERS,'w')
	f.write('''#!/bin/bash

if [ -f /net/local/etc/sudoers ]
then
	src=/net/local/etc/sudoers
elif [ -f /net/netstore/tools/local/etc/sudoers ]
then
	src=/net/netstore/tools/local/etc/sudoers
elif [ -f /nfs/netstore/tools/local/etc/sudoers ]
then
	src=/nfs/netstore/tools/local/etc/sudoers
else
	exit 0
fi

dst=/etc/sudoers

[ -f $src ] || exit 0
[ -f $dst ] || exit 0
[ $src -nt $dst ] && cp -f $src $dst
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_CRON_HOURLY_UPDATE_SUDOERS)

	self.runCommand(POST.CMD_CHMOD + ' 755 ' + POST.FILE_ETC_CRON_HOURLY_UPDATE_SUDOERS)

    #---------------------------------------------------------------------------
    # Set Kerberos5

    def setKerberos5(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_KRB5_CONF,'w')
	f.write('''[logging]
 default = FILE:/var/log/krb5libs.log
 kdc = FILE:/var/log/krb5kdc.log
 admin_server = FILE:/var/log/kadmind.log

[libdefaults]
    default_realm = CEDARPOINTCOM.COM
    dns_lookup_realm = false
    dns_lookup_kdc = false
    	ticket_lifetime = 24h
	forwardable = yes
	default_tgs_enctypes = DES-CBC-CRC DES-CBC-MD5 RC4-HMAC
	default_tkt_enctypes = DES-CBC-CRC DES-CBC-MD5 RC4-HMAC
	preferred_enctypes = DES-CBC-CRC DES-CBC-MD5 RC4-HMAC


[realms]
    CEDARPOINTCOM.COM = {
    kdc = corpdc1.cedarpointcom.com
    kdc = corpdc2.cedarpointcom.com
	admin_server = 192.168.101.201:749 
    default_domain=cedarpointcom.com
 }

[domain_realm]
    .cedarpointcom.com = CEDARPOINTCOM.COM
    cedarpointcom.com = CEDARPOINTCOM.COM

[kdc]
    profile = /var/kerberos/krb5kdc/kdc.conf

[appdefaults]
    pam = {
    debug = false
    ticket_lifetime = 36000
    renew_lifetime = 36000
    forwardable = true
    krb4_convert = false
 }
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_KRB5_CONF)

    #---------------------------------------------------------------------------
    # Set /root/.rhosts - set remote root access file

    def setRootRhosts(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ROOT_RHOSTS,'w')
	f.write('''xmatrix
xkickstart
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ROOT_RHOSTS)

    #---------------------------------------------------------------------------
    # Set /root/.ssh/authorized_keys - set Secure Shell root authorized keys

    def SetRootSshAuthorizedKeys(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ROOT_SSH_AUTHORIZED_KEYS,'w')
	f.write('''ssh-dss AAAAB3NzaC1kc3MAAACBALYwCJEeAZeupB6+l6A0PROjcoY76wLLXMdqeA4ADcDY9l/TUtZ9+T4RpPRqeDv0HNq5/XsaA7lIUsWJNfk7ye5gEz3uAhJzGlKGQt739Amryat9+40+CUQC1/yT1WLkb1VRpR2PLw5SdCNJHsJEuKlPzFAT2fe0dgwp80DDJuhdAAAAFQDblSKLi3o70I2zfA60mp3NfH0adwAAAIAHTLKTNkYzYXk+Cv0sRCSxxLGSGsm3nu+WHO9iEx0CHAB6w9FO8dKn82ceNZzVf6tFx2PSTuqN5TGjZF7OwXmLF/TW42iOqVEQ/CodanXrH0rw/Vp5ulGll8Gj5+Mo7vYWmee5Tp2yL62TXgAkhlv8Yn9mdVmgU9OM18upabje3wAAAIBsVYGZVpuyg1wHwCwrrscGPOsktQVbTSFnKP4Pq2Xvz2jSiQBCxdFJX+umur1Bzef9mtYIX28+rxmILXdnwHrYXdRbQ2m319oUu+91unoapTom4t6uJOdd0GY2JA35XFRWABD2GDRTFNDYxX4p5eOWRZ31XDQJf/BTu8uadWgOtQ== root@xkickstart.cedarpointcom.com
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ROOT_SSH_AUTHORIZED_KEYS)

    #---------------------------------------------------------------------------
    # Set I18N - Internationalization file

    def setI18N(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_SYSCONFIG_I18N,'w')
	f.write('''LANG="en_US"
SUPPORTED="en_US.UTF-8:en_US:en"
SYSFONT="latarcyrheb-sun16"
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_I18N)

    #---------------------------------------------------------------------------
    # Set networking files

    def setNetworking(self):

	if 'dhcp' == self.pre_data:

	    bootProto0 = 'dhcp'
	    ipAddr0 = ''

	else:

	    bootProto0 = 'static'
	    ipAddr0 = self.pre_data

	if 'dhcp' == self.pre_mgmt:

	    bootProto1 = 'dhcp'
	    ipAddr1 = ''

	else:

	    bootProto1 = 'static'
	    ipAddr1 = self.pre_mgmt

	f = file(POST.FILE_ETC_MODPROBE_CONF,'a')
	f.write('# Ethernet bonding\n')
	f.write('alias data bonding\n')
	f.write('alias mgmt bonding\n')
	f.write('options data miimon=100 mode=1\n')
	f.write('options mgmt miimon=100 mode=1\n')
	f.close()
	self.logger.info('Appended ' + POST.FILE_ETC_MODPROBE_CONF)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK,'w')
	f.write('NETWORKING=yes\n')
	f.write('NETWORKING_IPV6=yes\n')
	f.write('HOSTNAME=%s\n' % (self.hostnameLong))
	f.write('DHCP_HOSTNAME=%s\n' % (self.hostnameLong))
	if self.isDevConfig():
	    f.write('NISDOMAIN=cedarpointcom\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_DATA,'w')
	f.write('DEVICE=data\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto0))
	f.write('USERCTL=no\n')
	f.write('IPADDR=%s\n'  % (ipAddr0))
	f.write('NETMASK=%s\n' % (self.pre_netmask0))
	f.write('GATEWAY=%s\n' % (self.pre_gateway0))
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_DATA)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_MGMT,'w')
	f.write('DEVICE=mgmt\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto1))
	f.write('USERCTL=no\n')
	f.write('IPADDR=%s\n'    % (ipAddr1))
	f.write('NETMASK=%s\n'   % (self.pre_netmask1))
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_MGMT)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH0,'w')
	f.write('DEVICE=eth0\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto0))
	f.write('USERCTL=no\n')
	f.write('MASTER=data\n')
	f.write('SLAVE=yes\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH0)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH1,'w')
	f.write('DEVICE=eth1\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto1))
	f.write('USERCTL=no\n')
	f.write('MASTER=mgmt\n')
	f.write('SLAVE=yes\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH1)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH3,'w')
	f.write('DEVICE=eth3\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto0))
	f.write('USERCTL=no\n')
	f.write('MASTER=data\n')
	f.write('SLAVE=yes\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH3)

	f = file(POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH4,'w')
	f.write('DEVICE=eth4\n')
	f.write('ONBOOT=yes\n')
	f.write('BOOTPROTO=%s\n' % (bootProto1))
	f.write('USERCTL=no\n')
	f.write('MASTER=mgmt\n')
	f.write('SLAVE=yes\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SYSCONFIG_NETWORK_SCRIPTS_IFCFG_ETH4)

    #-------------------------------------------------------------------------------
    # Set iptables
    #
    # data comprises eth0 [and eth3]
    #
    #   172.16.x.x  lab "development" networks
    #
    # mgmt comprises eth1 [and eth4]
    #
    #   172.21.x.x  lab "management" networks
    #   192.168.x.x corporate networks
    #
    # ***************************************
    # * NOTE: RULE ORDER IS SIGNIFICANT !!! *
    # ***************************************
    #
    #---------------------------------------------------------------------------
    # Here are the expected results: (numeric)
    #
    #---------------------------------------------------------------------------
    # Here are the expected results: (symbolic)
    #
    #---------------------------------------------------------------------------

    def setIptables(self):

	if not self.isFusionConfig():

	    return

	commands = [

	    # Load required modules

	    POST.CMD_MODPROBE + ' iptable_filter',
	    POST.CMD_MODPROBE + ' ip_tables',
	    POST.CMD_MODPROBE + ' ipt_REJECT',
	    POST.CMD_MODPROBE + ' ipt_state',
	    POST.CMD_MODPROBE + ' ipt_tcp',
	    POST.CMD_MODPROBE + ' ipt_udp',
	    POST.CMD_MODPROBE + ' x_tables',

	    # Flush all current rules from iptables.

	    POST.CMD_IPTABLES + ' -F',

	    ##################
	    # Configure chains
	    ##################

	    # Set default policies for INPUT, FORWARD, and OUTPUT chains.

	    POST.CMD_IPTABLES + ' -P INPUT DROP',
	    POST.CMD_IPTABLES + ' -P FORWARD DROP',
	    POST.CMD_IPTABLES + ' -P OUTPUT ACCEPT',

	    # Delete, then create a user-defined chain

	    POST.CMD_IPTABLES + ' -X',
	    POST.CMD_IPTABLES + ' -N SF-Input',

	    # Chain FORWARD and INPUT to 'SF-Input'

	    POST.CMD_IPTABLES + ' -A FORWARD -j SF-Input',
	    POST.CMD_IPTABLES + ' -A INPUT   -j SF-Input',

	    #####################################################################
	    # Define global rules -- THINK WELL BEFORE YOU CHANGE ANY OF THESE!!!
	    #####################################################################

	    # Allow RFC4303 'ESP' (Encapsulate Security Payload)

	    POST.CMD_IPTABLES + ' -A SF-Input -p 50 -j ACCEPT',

	    # Allow RFC4302 'AH' (Authentication Header)

	    POST.CMD_IPTABLES + ' -A SF-Input -p 51 -j ACCEPT',

	    # Allow all access for loopback interface

	    POST.CMD_IPTABLES + ' -A SF-Input -i lo   -j ACCEPT',

	    # Allow packets belonging to ESTABLISHED and RELATED connections

	    POST.CMD_IPTABLES + ' -A SF-Input -m state --state ESTABLISHED,RELATED -j ACCEPT',

	    # Allow 'ICMP' pings

	    POST.CMD_IPTABLES + ' -A SF-Input -p icmp --icmp-type any -j ACCEPT',

	    # Allow 'mdns' (Multicast DNS)

	    POST.CMD_IPTABLES + ' -A SF-Input -p udp --dport 5353 -d 224.0.0.251 -j ACCEPT',

	    # Allow 'ssh' (The Secure Shell [SSH] Protocol)

	    POST.CMD_IPTABLES + ' -A SF-Input -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT',

	    # Allow 'ipp' (Internet Printing Protocol)

	    # POST.CMD_IPTABLES + ' -A SF-Input -p tcp -m tcp --dport 631 -j ACCEPT',
	    # POST.CMD_IPTABLES + ' -A SF-Input -p udp -m udp --dport 631 -j ACCEPT',

	    ###############################################################
	    # These are required by the Sun Glassfish Communications Server
	    ###############################################################

	    # Allow 'appserv-http' (App Server - Admin HTTP); SGCS:INST_ASADMIN_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 4848 -j ACCEPT',

	    # Allow 'http-alt' (HTTP Alternate) ; SGCS:INST_ASWEB_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 8080 -j ACCEPT',

	    # Allow 'undefined' (undefined) ; SGCS:INST_HTTPS_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 8181 -j ACCEPT',

	    # Allow 'undefined' (undefined) ; SGCS:INST_JMS_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 7676 -j ACCEPT',

	    # Allow 'lrs-paging' (LRS NetPage); SGCS:INST_ORB_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 3700 -j ACCEPT',

	    # Allow 'scp' (Siemens AuD SCP); SGCS:INST_ORB_SSL_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 3820 -j ACCEPT',

	    # Allow 'undefined' (undefined) ; SGCS:INST_ORB_SSL_MUTUALAUTH_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 3920 -j ACCEPT',

	    # Allow 'sun-as-jmxrmi' (Sun App Server - JMX/RMI); SGCS:INST_JMX_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 8686 -j ACCEPT',

	    # Allow 'sip' (SIP); SGCS:INST_SIP_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 5060 -j ACCEPT',
	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m udp -p udp --dport 5060 -j ACCEPT',

	    # Allow 'sip-tls' (SIP-TLS); SGCS:INST_SIPS_PORT

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 5061 -j ACCEPT',

	    # Allow IMS i-cscf

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 4060 -j ACCEPT',
	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m udp -p udp --dport 4060 -j ACCEPT',

	    # Allow IMS s-cscf

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 6060 -j ACCEPT',
	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m udp -p udp --dport 6060 -j ACCEPT',

	    ###############################################################
	    # End of Sun Glassfish Communications Server section
	    ###############################################################

	    ########################################
	    # These are required by the MySQL Server
	    ########################################

	    # Allow 'mysql' (MySQL)

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m tcp -p tcp --dport 3306 -j ACCEPT',

	    #############################
	    # End of MySQL Server section
	    #############################

	    #######################################
	    # These are required by the SNMP Server
	    #######################################

	    # Allow 'snmp' (SNMP)

	    POST.CMD_IPTABLES + ' -A SF-Input -i data -m state --state NEW -m udp -p udp --dport 161 -j ACCEPT',

	    ############################
	    # End of SNMP Server section
	    ############################

	    #########################
	    # Reject everything else!
	    #########################

	    POST.CMD_IPTABLES + ' -A SF-Input -j REJECT --reject-with icmp-host-prohibited',

	    # Save settings.

	    POST.CMD_SERVICE + ' iptables save >/dev/null 2>&1',

	    ]

	for command in commands:

	    self.runCommand(command)

	# List rules

	command = (
	    POST.CMD_IPTABLES +
	    ' -L' +
	    ' -v' +
	    ' -n' +
	    ' --line-number')

	self.logger.info(command)
	self.logger.info('---------------')

	f = os.popen(command)
	for i in f.readlines():

	    self.logger.info(i.rstrip())

	self.logger.info('---------------')
	f.close()

    #---------------------------------------------------------------------------
    # Set services

    def setServices(self):

	if self.isFusionConfig():

	    commands = [

		POST.CMD_CHKCONFIG + ' ntpd       on',
		POST.CMD_CHKCONFIG + ' snmpd      on',
		POST.CMD_CHKCONFIG + ' ipmi       on',

		POST.CMD_CHKCONFIG + ' lm_sensors off',

		]

	elif self.isDevConfig():

	    commands = [

		POST.CMD_CHKCONFIG + ' nfs        on',
		POST.CMD_CHKCONFIG + ' nscd       on',
		POST.CMD_CHKCONFIG + ' ntpd       on',
		POST.CMD_CHKCONFIG + ' rlogin     on',
		POST.CMD_CHKCONFIG + ' rsh        on',
		POST.CMD_CHKCONFIG + ' smb        on',
		POST.CMD_CHKCONFIG + ' snmpd      on',
		POST.CMD_CHKCONFIG + ' telnet     on',

		POST.CMD_CHKCONFIG + ' lm_sensors off',

		]

	else:

	    commands = [

		POST.CMD_CHKCONFIG + ' ntpd       on',

		]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set printers

    def setPrinters(self):

	if not self.isDevConfig():

	    return

	###############################################################################
	# THIS PRINTER HAS BEEN RETIRED, SO THIS CODE SERVES AS A PLACEHOLDER
	# UNTIL WE ADD CONFIGURATION FOR A NEW PRINTER.
	###############################################################################
	# -rw-r--r-- root/root    104553 2008-07-10 10:34:16 etc/cups/ppd/hp8150eng.ppd
	###############################################################################

	f = file(POST.FILE_ETC_CUPS_PPD_HP8150ENG_PPD,'w')
	f.write('''*PPD-Adobe: "4.3"
*% =======================================================
*% Disclaimer:  The above statement indicates
*% that this PPD was written using the Adobe PPD
*% File Format Specification 4.3, but does not
*% intend to imply approval and acceptance by
*% Adobe Systems, Inc.
*% =======================================================
*% Printer Description File
*% Copyright 1992-2003 Hewlett-Packard Company
*%
*% Permission is hereby granted, free of charge, to any person obtaining
*% a copy of this software and associated documentation files (the
*% "Software"), to deal in the Software without restriction, including
*% without limitation the rights to use, copy, modify, merge, publish,
*% distribute, sublicense, and/or sell copies of the Software, and to
*% permit persons to whom the Software is furnished to do so, subject to
*% the following conditions:
*% 
*% The above copyright notice and this permission notice shall be
*% included in all copies or substantial portions of the Software.
*% 
*% THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
*% EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
*% MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
*% NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
*% LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
*% OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
*% WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*% 
*% [this is the MIT open source license -- please see www.opensource.org]
*%

*%========================================================
*% PPD for HP LaserJet 8150 Series
*% For Macintosh
*%========================================================

*%=================================================
*% 		 PPD File Version Information
*%=================================================
*FileVersion: "1.1.2 X"
*FormatVersion: "4.3"
*LanguageEncoding: MacStandard
*LanguageVersion: English
*PCFileName: "HP8150_H.PPD"
*APDialogExtension: "/Library/Printers/hp/PDEs/hpColorOptions.plugin"
*APDialogExtension: "/Library/Printers/hp/PDEs/hpEdgeToEdge.plugin"
*APDialogExtension: "/Library/Printers/hp/PDEs/hpFinishing.plugin"
*APDialogExtension: "/Library/Printers/hp/PDEs/hpImageQuality.plugin"
*APDialogExtension: "/Library/Printers/hp/PDEs/hpProofAndPrint.plugin"
*APPrinterIconPath: "/Library/Printers/hp/Icons/HP LaserJet 8150 Series.icns"

*%=================================================
*% 		 Product Version Information
*%=================================================
*ModelName: "HP LaserJet 8150 Series"
*ShortNickName: "HP LaserJet 8150 Series"
*NickName: "HP LaserJet 8150 Series Postscript (recommended)"
*Product: "(HP LaserJet 8150 Series)"
*Manufacturer: "HP"

*PSVersion: "(3010.107) 0"

*%=================================================
*%		 Device Capabilities
*%=================================================
*ColorDevice:       False
*DefaultColorSpace: Gray
*FileSystem:        True
*?FileSystem: "
   save
     false
     (%disk?%)
     { currentdevparams dup /Writeable known
        { /Writeable get {pop true} if }  { pop } ifelse
     } 100 string /IODevice resourceforall
     {(True)}{(False)} ifelse = flush
   restore
"
*End

*LanguageLevel: "3"
*Throughput:    "32"
*TTRasterizer:  Type42
*?TTRasterizer: "
   save
      42 /FontType resourcestatus
      { pop pop (Type42)} {pop pop (None)} ifelse = flush
   restore
"
*End

*%=================================================
*%		 Emulations and Protocols
*%=================================================
*Protocols: TBCP

*SuggestedJobTimeout:  "0"
*SuggestedWaitTimeout: "120"

*PrintPSErrors: True

*%=== Output Bin ======================
*PageStackOrder Upper: Normal
*PageStackOrder Left: Reverse
*PageStackOrder Stacker: Normal
*PageStackOrder Separator: Normal
*PageStackOrder Collator: Normal
*PageStackOrder UStapler: Normal
*PageStackOrder OutputBin1: Normal
*PageStackOrder OutputBin2: Normal
*PageStackOrder OutputBin3: Normal
*PageStackOrder OutputBin4: Normal
*PageStackOrder OutputBin5: Normal
*PageStackOrder OutputBin6: Normal
*PageStackOrder OutputBin7: Normal
*PageStackOrder OutputBin8: Normal

*%=================================================
*%		 Installable Options
*%=================================================
*OpenGroup: InstallableOptions/Installed Options

*OpenUI *HPOption_Tray4/Tray 4: Boolean
*DefaultHPOption_Tray4: False
*HPOption_Tray4 True/Installed: ""
*HPOption_Tray4 False/Not Installed: ""
*?HPOption_Tray4: "
  save
    currentpagedevice /InputAttributes get dup 5 known
    {5 get null ne {(True)}{(False)} ifelse} {pop (False)} ifelse = flush
  restore
"
*End
*CloseUI: *HPOption_Tray4

*OpenUI *HPOption_Tray5/Tray 5: Boolean
*DefaultHPOption_Tray5: False
*HPOption_Tray5 True/Installed: ""
*HPOption_Tray5 False/Not Installed: ""
*?HPOption_Tray5: "
  save
    currentpagedevice /InputAttributes get dup 6 known
    {6 get null ne {(True)}{(False)} ifelse} {pop (False)} ifelse = flush
  restore
"
*End
*CloseUI: *HPOption_Tray5

*OpenUI *HPOption_Duplexer/Duplex Unit: Boolean
*DefaultHPOption_Duplexer: False
*HPOption_Duplexer True/Installed: ""
*HPOption_Duplexer False/Not Installed: ""
*?HPOption_Duplexer: "
  save
    currentpagedevice /Duplex known
    {(True)}{(False)}ifelse = flush
  restore
"
*End
*CloseUI: *HPOption_Duplexer

*OpenUI *HPOption_Disk/Printer Disk: PickOne
*DefaultHPOption_Disk: None
*HPOption_Disk None/None: ""
*HPOption_Disk RAMDisk/RAM Disk: ""
*HPOption_Disk HardDisk/Hard Disk: ""
*?HPOption_Disk: "
   save
     (HardDisk)
     (RAMDisk)
     (None)
     0
     (%disk?%)
     { currentdevparams dup /Writeable known
        { dup /Writeable get
        	{ /PhysicalSize get 500000 gt {2}{1}ifelse 2 copy lt { exch }if pop }
        	{ pop } ifelse
        } { pop } ifelse
     } 100 string /IODevice resourceforall
     index = flush pop pop pop
   restore
"
*End
*CloseUI: *HPOption_Disk

*OpenUI *HPOption_Envelope_Feeder/Envelope Feeder: Boolean
*DefaultHPOption_Envelope_Feeder: False
*HPOption_Envelope_Feeder True/Installed: ""
*HPOption_Envelope_Feeder False/Not Installed: ""
*?HPOption_Envelope_Feeder: "
  save
    currentpagedevice /InputAttributes get dup 2 known
    {2 get null ne {(True)}{(False)} ifelse} {pop (False)} ifelse = flush
  restore
"
*End
*CloseUI: *HPOption_Envelope_Feeder

*OpenUI *HPOption_MBM_Mixed/Accessory Output Bins: PickOne
*OrderDependency: 10 AnySetup *HPOption_MBM_Mixed
*DefaultHPOption_MBM_Mixed: Standard
*HPOption_MBM_Mixed Standard/Not Installed: ""
*HPOption_MBM_Mixed MBM5S/5 Bin Mailbox with Stapler: ""
*HPOption_MBM_Mixed MBM7/7 Bin Mailbox: ""
*HPOption_MBM_Mixed MBM8/8 Bin Mailbox: ""
*HPOption_MBM_Mixed MBMStaplerStacker/HP 3000-Sheet Stapler-Stacker: "userdict /HPConfigurableStapler 0 put"
*HPOption_MBM_Mixed MBMStacker/HP 3000-Sheet Stacker: ""
*%No PS to reliably determine what output device is attached ###
*%*?HPOption_MBM_Mixed: "(Unknown) = flush"
*CloseUI: *HPOption_MBM_Mixed

*OpenUI *HPOption_MBM_Mode/Multi-Bin Mailbox Mode: PickOne
*DefaultHPOption_MBM_Mode: MailboxModeStacker
*HPOption_MBM_Mode MailboxModeMailbox/Standard Mailbox: ""
*HPOption_MBM_Mode MailboxModeStacker/Stacker-Separator-Collator: ""
*%*?HPOption_MBM: "(Unknown) = flush"
*CloseUI: *HPOption_MBM_Mode


*OpenUI *InstalledMemory/Total Printer Memory: PickOne
*DefaultInstalledMemory: 24-31MB
*InstalledMemory 24-31MB/24 - 31 MB: ""
*InstalledMemory 32-39MB/32 - 39 MB: ""
*InstalledMemory 40-47MB/40 - 47 MB: ""
*InstalledMemory 48-55MB/48 - 55 MB: ""
*InstalledMemory 56-63MB/56 - 63 MB: ""
*InstalledMemory 64-71MB/64 - 71 MB: ""
*InstalledMemory 72MB/72 MB or more: ""
*?InstalledMemory: "
  save
    currentsystemparams /RamSize get
    524288 div ceiling cvi 2 div
    /size exch def
    size 72 ge
      {(72MB)}
       {size 64 ge
          {(64-71MB)}
          {size 56 ge
             {(56-63MB)}
             {size 48 ge
                {(48-55MB)}
                {size 40 ge
                   {(40-47MB)}
                   {size 32 ge
                      {(32-39MB)}
                      {size 24 ge
                      	{(24-31MB)}
                      {(16MB)} ifelse
					} ifelse
                 } ifelse
             } ifelse
          } ifelse
       } ifelse
    } ifelse = flush
  restore
"
*End
*CloseUI: *InstalledMemory

*%=================================================
*%		 Fit to Page
*%=================================================
*OpenUI *HPOption_PaperPolicy/Fit to Page: PickOne
*OrderDependency: 10 AnySetup *HPOption_PaperPolicy
*DefaultHPOption_PaperPolicy: PromptUser
*HPOption_PaperPolicy PromptUser/Prompt User: "
   <</DeferredMediaSelection true>> setpagedevice"
*End
*HPOption_PaperPolicy NearestSizeAdjust/Nearest Size and Scale: "
   <</DeferredMediaSelection false /Policies << /PageSize 3 >> >> setpagedevice"
*End
*HPOption_PaperPolicy NearestSizeNoAdjust/Nearest Size and Crop: "
   <</DeferredMediaSelection false /Policies << /PageSize 5 >> >> setpagedevice"
*End
*CloseUI: *HPOption_PaperPolicy

*CloseGroup: InstallableOptions

*%=================================================
*%		 UI Constraints
*%=================================================
*% If A than not B  (Also include the reverse constraints if appropriate)
*%
*% Constrain output bins that are not available with Standard configuration
*%-------------------------------------------------------------------------
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin Stacker
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin StackerSeparator
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin1
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin2
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin3
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin4
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin5
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin8
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin UStapler

*UIConstraints: *OutputBin Stacker *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin StackerSeparator *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin1 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin2 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin3 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin4 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin5 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin6 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin7 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin OutputBin8 *HPOption_MBM_Mixed Standard
*UIConstraints: *OutputBin UStapler *HPOption_MBM_Mixed Standard


*% High capacity stapler disabled without high capacity output unit
*UIConstraints: *HPOption_MBM_Mixed MBM5S *HPStaplerOptions 1diagonal
*UIConstraints: *HPOption_MBM_Mixed MBM5S *HPStaplerOptions 2parallel
*UIConstraints: *HPOption_MBM_Mixed MBM5S *HPStaplerOptions 3parallel
*UIConstraints: *HPOption_MBM_Mixed MBM5S *HPStaplerOptions 6parallel
*UIConstraints: *HPOption_MBM_Mixed MBM5S *HPStaplerOptions Custom

*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions 1diagonal
*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions 1parallel
*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions 2parallel
*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions 3parallel
*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions 6parallel
*UIConstraints: *HPOption_MBM_Mixed Standard *HPStaplerOptions Custom

*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions 1diagonal
*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions 1parallel
*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions 2parallel
*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions 3parallel
*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions 6parallel
*UIConstraints: *HPOption_MBM_Mixed MBM7 *HPStaplerOptions Custom

*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions 1diagonal
*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions 1parallel
*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions 2parallel
*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions 3parallel
*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions 6parallel
*UIConstraints: *HPOption_MBM_Mixed MBM8 *HPStaplerOptions Custom

*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions 1diagonal
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions 1parallel
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions 2parallel
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions 3parallel
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions 6parallel
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPStaplerOptions Custom

*%Constrain stapling to the stapling bin
*%------------------------------------------------------------------
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions 1diagonal
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions 1parallel
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions 2parallel
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions 3parallel
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions 6parallel
*UIConstraints: *OutputBin PrinterDefault *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *OutputBin PrinterDefault
*UIConstraints: *HPStaplerOptions 1parallel *OutputBin PrinterDefault
*UIConstraints: *HPStaplerOptions 2parallel *OutputBin PrinterDefault
*UIConstraints: *HPStaplerOptions 3parallel *OutputBin PrinterDefault
*UIConstraints: *HPStaplerOptions 6parallel *OutputBin PrinterDefault
*UIConstraints: *HPStaplerOptions Custom *OutputBin PrinterDefault

*UIConstraints: *OutputBin Upper *HPStaplerOptions 1diagonal
*UIConstraints: *OutputBin Upper *HPStaplerOptions 1parallel
*UIConstraints: *OutputBin Upper *HPStaplerOptions 2parallel
*UIConstraints: *OutputBin Upper *HPStaplerOptions 3parallel
*UIConstraints: *OutputBin Upper *HPStaplerOptions 6parallel
*UIConstraints: *OutputBin Upper *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *OutputBin Upper
*UIConstraints: *HPStaplerOptions 1parallel *OutputBin Upper
*UIConstraints: *HPStaplerOptions 2parallel *OutputBin Upper
*UIConstraints: *HPStaplerOptions 3parallel *OutputBin Upper
*UIConstraints: *HPStaplerOptions 6parallel *OutputBin Upper
*UIConstraints: *HPStaplerOptions Custom *OutputBin Upper

*UIConstraints: *OutputBin Left *HPStaplerOptions 1diagonal
*UIConstraints: *OutputBin Left *HPStaplerOptions 1parallel
*UIConstraints: *OutputBin Left *HPStaplerOptions 2parallel
*UIConstraints: *OutputBin Left *HPStaplerOptions 3parallel
*UIConstraints: *OutputBin Left *HPStaplerOptions 6parallel
*UIConstraints: *OutputBin Left *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *OutputBin Left
*UIConstraints: *HPStaplerOptions 1parallel *OutputBin Left
*UIConstraints: *HPStaplerOptions 2parallel *OutputBin Left
*UIConstraints: *HPStaplerOptions 3parallel *OutputBin Left
*UIConstraints: *HPStaplerOptions 6parallel *OutputBin Left
*UIConstraints: *HPStaplerOptions Custom *OutputBin Left

*UIConstraints: *OutputBin Stacker *HPStaplerOptions 1diagonal
*UIConstraints: *OutputBin Stacker *HPStaplerOptions 1parallel
*UIConstraints: *OutputBin Stacker *HPStaplerOptions 2parallel
*UIConstraints: *OutputBin Stacker *HPStaplerOptions 3parallel
*UIConstraints: *OutputBin Stacker *HPStaplerOptions 6parallel
*UIConstraints: *OutputBin Stacker *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *OutputBin Stacker
*UIConstraints: *HPStaplerOptions 1parallel *OutputBin Stacker
*UIConstraints: *HPStaplerOptions 2parallel *OutputBin Stacker
*UIConstraints: *HPStaplerOptions 3parallel *OutputBin Stacker
*UIConstraints: *HPStaplerOptions 6parallel *OutputBin Stacker
*UIConstraints: *HPStaplerOptions Custom *OutputBin Stacker

*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions 1diagonal
*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions 1parallel
*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions 2parallel
*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions 3parallel
*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions 6parallel
*UIConstraints: *OutputBin StackerSeparator *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *OutputBin StackerSeparator
*UIConstraints: *HPStaplerOptions 1parallel *OutputBin StackerSeparator
*UIConstraints: *HPStaplerOptions 2parallel *OutputBin StackerSeparator
*UIConstraints: *HPStaplerOptions 3parallel *OutputBin StackerSeparator
*UIConstraints: *HPStaplerOptions 6parallel *OutputBin StackerSeparator
*UIConstraints: *HPStaplerOptions Custom *OutputBin StackerSeparator


*% Do not staple uncollated documents
*UIConstraints: *Collate False *HPStaplerOptions 1diagonal
*UIConstraints: *Collate False *HPStaplerOptions 1parallel
*UIConstraints: *Collate False *HPStaplerOptions 2parallel
*UIConstraints: *Collate False *HPStaplerOptions 3parallel
*UIConstraints: *Collate False *HPStaplerOptions 6parallel
*UIConstraints: *Collate False *HPStaplerOptions Custom

*UIConstraints: *HPStaplerOptions 1diagonal *Collate False
*UIConstraints: *HPStaplerOptions 1parallel *Collate False
*UIConstraints: *HPStaplerOptions 2parallel *Collate False
*UIConstraints: *HPStaplerOptions 3parallel *Collate False
*UIConstraints: *HPStaplerOptions 6parallel *Collate False
*UIConstraints: *HPStaplerOptions Custom *Collate False

*% high capacity output unit has no mailbox mode
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *HPOption_MBM_Mode MailboxModeMailbox
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *HPOption_MBM_Mode MailboxModeMailbox

*% Do not staple envelopes, all other sizes are supported.
*UIConstraints: *PageSize Env10        *OutputBin UStapler
*UIConstraints: *PageRegion Env10      *OutputBin UStapler
*UIConstraints: *PageSize EnvMonarch   *OutputBin UStapler
*UIConstraints: *PageRegion EnvMonarch *OutputBin UStapler
*UIConstraints: *PageSize EnvDL        *OutputBin UStapler
*UIConstraints: *PageRegion EnvDL      *OutputBin UStapler
*UIConstraints: *PageSize EnvC5        *OutputBin UStapler
*UIConstraints: *PageRegion EnvC5      *OutputBin UStapler
*UIConstraints: *PageSize EnvISOB5     *OutputBin UStapler
*UIConstraints: *PageRegion EnvISOB5   *OutputBin UStapler

*UIConstraints: *OutputBin UStapler *PageSize Env10
*UIConstraints: *OutputBin UStapler *PageRegion Env10
*UIConstraints: *OutputBin UStapler *PageSize EnvMonarch
*UIConstraints: *OutputBin UStapler *PageRegion EnvMonarch
*UIConstraints: *OutputBin UStapler *PageSize EnvDL
*UIConstraints: *OutputBin UStapler *PageRegion EnvDL
*UIConstraints: *OutputBin UStapler *PageSize EnvC5
*UIConstraints: *OutputBin UStapler *PageRegion EnvC5
*UIConstraints: *OutputBin UStapler *PageSize EnvISOB5
*UIConstraints: *OutputBin UStapler *PageRegion EnvISOB5

*% Constrain output bins that are not available with MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin2 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin3 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin4 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin5 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin6 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin7 *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *OutputBin OutputBin8 *HPOption_MBM_Mixed MBMStaplerStacker

*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin2
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin3
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin4
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin5
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin OutputBin8

*% The Stacker-Separator-Collator is not available with the 3000-sheet stacker
*UIConstraints: *OutputBin StackerSeparator *HPOption_MBM_Mixed MBMStaplerStacker
*UIConstraints: *HPOption_MBM_Mixed MBMStaplerStacker *OutputBin StackerSeparator

*% Constrain output bins that are not available with MBMStacker
*UIConstraints: *OutputBin OutputBin2 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin3 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin4 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin5 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin6 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin7 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin OutputBin8 *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin UStapler *HPOption_MBM_Mixed MBMStacker
*UIConstraints: *OutputBin StackerSeparator *HPOption_MBM_Mixed MBMStacker

*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin2
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin3
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin4
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin5
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin OutputBin8
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin UStapler
*UIConstraints: *HPOption_MBM_Mixed MBMStacker *OutputBin StackerSeparator

*%Job Retention not allowed unless printer has a hard disk

*UIConstraints: *HPOption_Disk None *HPJobRetentionOption HPJobRetentionQuickCopy
*UIConstraints: *HPOption_Disk None *HPJobRetentionOption HPJobRetentionProof
*UIConstraints: *HPOption_Disk None *HPJobRetentionOption HPJobRetentionStore
*%UIConstraints: *HPOption_Disk None *HPJobRetentionOption HPJobRetentionPrivate

*UIConstraints: *HPOption_Disk RAMDisk *HPJobRetentionOption HPJobRetentionQuickCopy
*UIConstraints: *HPOption_Disk RAMDisk *HPJobRetentionOption HPJobRetentionStore

*%Cannot Mopy without a disk
*UIConstraints: *HPOption_Disk None *Collate True
*UIConstraints: *Collate True *HPOption_Disk None

*% If optional trays are not installed, disable access to LargeCapacity (Tray 4) and Tray 5.
*UIConstraints: *HPOption_Tray4 False *InputSlot LargeCapacity
*UIConstraints: *HPOption_Tray5 False *InputSlot Tray5

*% If the envelope feeder is not installed disable envelope slot.
*UIConstraints: *HPOption_Envelope_Feeder False *InputSlot Envelope

*% If the duplexer is not installed disable duplex modes.
*%------------------------------------------------------------
*UIConstraints: *HPOption_Duplexer False *Duplex DuplexNoTumble
*UIConstraints: *HPOption_Duplexer False *Duplex DuplexTumble

*% Don't allow these paper sizes/types in the Envelope Feeder
*%------------------------------------------------------------
*UIConstraints: *PageSize Letter         *InputSlot Envelope
*UIConstraints: *PageSize LetterSmall    *InputSlot Envelope
*UIConstraints: *PageSize Executive      *InputSlot Envelope
*UIConstraints: *PageSize Legal          *InputSlot Envelope
*UIConstraints: *PageSize LegalSmall     *InputSlot Envelope
*UIConstraints: *PageSize Tabloid        *InputSlot Envelope
*UIConstraints: *PageSize w842h1274      *InputSlot Envelope
*UIConstraints: *PageSize w612h935       *InputSlot Envelope
*UIConstraints: *PageSize w558h774       *InputSlot Envelope
*UIConstraints: *PageSize w774h1116      *InputSlot Envelope
*UIConstraints: *PageSize A3             *InputSlot Envelope
*UIConstraints: *PageSize A4             *InputSlot Envelope
*UIConstraints: *PageSize A4Small        *InputSlot Envelope
*UIConstraints: *PageSize A5             *InputSlot Envelope
*UIConstraints: *PageSize B4             *InputSlot Envelope
*UIConstraints: *PageSize B5             *InputSlot Envelope
*UIConstraints: *PageSize DoublePostcard *InputSlot Envelope

*UIConstraints: *PageRegion Letter         *InputSlot Envelope
*UIConstraints: *PageRegion LetterSmall    *InputSlot Envelope
*UIConstraints: *PageRegion Executive      *InputSlot Envelope
*UIConstraints: *PageRegion Legal          *InputSlot Envelope
*UIConstraints: *PageRegion LegalSmall     *InputSlot Envelope
*UIConstraints: *PageRegion Tabloid        *InputSlot Envelope
*UIConstraints: *PageRegion w842h1274      *InputSlot Envelope
*UIConstraints: *PageRegion w612h935       *InputSlot Envelope
*UIConstraints: *PageRegion w558h774       *InputSlot Envelope
*UIConstraints: *PageRegion w774h1116      *InputSlot Envelope
*UIConstraints: *PageRegion A3             *InputSlot Envelope
*UIConstraints: *PageRegion A4             *InputSlot Envelope
*UIConstraints: *PageRegion A4Small        *InputSlot Envelope
*UIConstraints: *PageRegion A5             *InputSlot Envelope
*UIConstraints: *PageRegion B4             *InputSlot Envelope
*UIConstraints: *PageRegion B5             *InputSlot Envelope
*UIConstraints: *PageRegion DoublePostcard *InputSlot Envelope

*UIConstraints: *MediaType Transparency    *InputSlot Envelope
*UIConstraints: *MediaType Labels          *InputSlot Envelope

*% If selected page size is an envelope, executive, A5, B5 (JIS),
*% 11x17 (Oversize 11.7x17.7), Asian, or DoublePostcard
*%    disable access to paper trays 2, 4.
*%------------------------------------------------------------
*UIConstraints: *PageSize Env10       *InputSlot Middle
*UIConstraints: *PageSize Env10       *InputSlot LargeCapacity
*UIConstraints: *PageSize EnvMonarch  *InputSlot Middle
*UIConstraints: *PageSize EnvMonarch  *InputSlot LargeCapacity
*UIConstraints: *PageSize EnvDL       *InputSlot Middle
*UIConstraints: *PageSize EnvDL       *InputSlot LargeCapacity
*UIConstraints: *PageSize EnvC5       *InputSlot Middle
*UIConstraints: *PageSize EnvC5       *InputSlot LargeCapacity
*UIConstraints: *PageSize EnvISOB5    *InputSlot Middle
*UIConstraints: *PageSize EnvISOB5    *InputSlot LargeCapacity

*UIConstraints: *PageSize A5              *InputSlot Middle
*UIConstraints: *PageSize A5              *InputSlot LargeCapacity
*UIConstraints: *PageSize B5              *InputSlot Middle
*UIConstraints: *PageSize B5              *InputSlot LargeCapacity
*UIConstraints: *PageSize Executive       *InputSlot Middle
*UIConstraints: *PageSize Executive       *InputSlot LargeCapacity
*UIConstraints: *PageSize w842h1274       *InputSlot Middle
*UIConstraints: *PageSize w842h1274       *InputSlot LargeCapacity
*UIConstraints: *PageSize DoublePostcard  *InputSlot Middle
*UIConstraints: *PageSize DoublePostcard  *InputSlot LargeCapacity
*UIConstraints: *PageSize w612h935        *InputSlot Middle
*UIConstraints: *PageSize w612h935        *InputSlot LargeCapacity
*UIConstraints: *PageSize w558h774        *InputSlot Middle
*UIConstraints: *PageSize w558h774        *InputSlot LargeCapacity
*UIConstraints: *PageSize w774h1116       *InputSlot Middle
*UIConstraints: *PageSize w774h1116       *InputSlot LargeCapacity

*% If selected page region is an envelope, executive, A5, B5 (JIS),
*% 11x17 (Oversize 11.7x17.7), Asian, or DoublePostcard
*%    disable access to paper trays 2, 3, 4 and 5
*%------------------------------------------------------------
*UIConstraints: *PageRegion Env10       *InputSlot Middle
*UIConstraints: *PageRegion Env10       *InputSlot LargeCapacity
*UIConstraints: *PageRegion EnvMonarch  *InputSlot Middle
*UIConstraints: *PageRegion EnvMonarch  *InputSlot LargeCapacity
*UIConstraints: *PageRegion EnvDL       *InputSlot Middle
*UIConstraints: *PageRegion EnvDL       *InputSlot LargeCapacity
*UIConstraints: *PageRegion EnvC5       *InputSlot Middle
*UIConstraints: *PageRegion EnvC5       *InputSlot LargeCapacity
*UIConstraints: *PageRegion EnvISOB5    *InputSlot Middle
*UIConstraints: *PageRegion EnvISOB5    *InputSlot LargeCapacity

*UIConstraints: *PageRegion A5              *InputSlot Middle
*UIConstraints: *PageRegion A5              *InputSlot LargeCapacity
*UIConstraints: *PageRegion B5              *InputSlot Middle
*UIConstraints: *PageRegion B5              *InputSlot LargeCapacity
*UIConstraints: *PageRegion Executive       *InputSlot Middle
*UIConstraints: *PageRegion Executive       *InputSlot LargeCapacity
*UIConstraints: *PageRegion w842h1274       *InputSlot Middle
*UIConstraints: *PageRegion w842h1274       *InputSlot LargeCapacity
*UIConstraints: *PageRegion DoublePostcard  *InputSlot Middle
*UIConstraints: *PageRegion DoublePostcard  *InputSlot LargeCapacity
*UIConstraints: *PageRegion w612h935        *InputSlot Middle
*UIConstraints: *PageRegion w612h935        *InputSlot LargeCapacity
*UIConstraints: *PageRegion w558h774        *InputSlot Middle
*UIConstraints: *PageRegion w558h774        *InputSlot LargeCapacity
*UIConstraints: *PageRegion w774h1116       *InputSlot Middle
*UIConstraints: *PageRegion w774h1116       *InputSlot LargeCapacity

*% Don't allow 11x17 or A3 in tray 2
*%------------------------------------------------------------
*UIConstraints: *PageSize Tabloid   *InputSlot Middle
*UIConstraints: *PageRegion Tabloid *InputSlot Middle
*UIConstraints: *PageSize A3        *InputSlot Middle
*UIConstraints: *PageRegion A3      *InputSlot Middle

*% Don't allow DoublePostcard, envelopes, transparencies or labels to be duplexed
*%------------------------------------------------------------
*UIConstraints: *PageSize DoublePostcard *Duplex DuplexNoTumble
*UIConstraints: *PageSize Env10          *Duplex DuplexNoTumble
*UIConstraints: *PageSize EnvMonarch     *Duplex DuplexNoTumble
*UIConstraints: *PageSize EnvDL          *Duplex DuplexNoTumble
*UIConstraints: *PageSize EnvC5          *Duplex DuplexNoTumble
*UIConstraints: *PageSize EnvISOB5       *Duplex DuplexNoTumble

*UIConstraints: *MediaType Transparency *Duplex DuplexNoTumble
*UIConstraints: *MediaType Labels       *Duplex DuplexNoTumble

*UIConstraints: *PageRegion DoublePostcard *Duplex DuplexNoTumble
*UIConstraints: *PageRegion Env10          *Duplex DuplexNoTumble
*UIConstraints: *PageRegion EnvMonarch     *Duplex DuplexNoTumble
*UIConstraints: *PageRegion EnvDL          *Duplex DuplexNoTumble
*UIConstraints: *PageRegion EnvC5          *Duplex DuplexNoTumble
*UIConstraints: *PageRegion EnvISOB5       *Duplex DuplexNoTumble

*UIConstraints: *PageSize DoublePostcard *Duplex DuplexTumble
*UIConstraints: *PageSize Env10          *Duplex DuplexTumble
*UIConstraints: *PageSize EnvMonarch     *Duplex DuplexTumble
*UIConstraints: *PageSize EnvDL          *Duplex DuplexTumble
*UIConstraints: *PageSize EnvC5          *Duplex DuplexTumble
*UIConstraints: *PageSize EnvISOB5       *Duplex DuplexTumble

*UIConstraints: *MediaType Transparency *Duplex DuplexTumble
*UIConstraints: *MediaType Labels       *Duplex DuplexTumble

*UIConstraints: *PageRegion DoublePostcard *Duplex DuplexTumble
*UIConstraints: *PageRegion Env10          *Duplex DuplexTumble
*UIConstraints: *PageRegion EnvMonarch     *Duplex DuplexTumble
*UIConstraints: *PageRegion EnvDL          *Duplex DuplexTumble
*UIConstraints: *PageRegion EnvC5          *Duplex DuplexTumble
*UIConstraints: *PageRegion EnvISOB5       *Duplex DuplexTumble

*% Cannot duplex custom page sizes
*NonUIConstraints: *CustomPageSize True *Duplex DuplexNoTumble
*NonUIConstraints: *CustomPageSize True *Duplex DuplexTumble

*NonUIConstraints: *Duplex DuplexNoTumble *CustomPageSize True
*NonUIConstraints: *Duplex DuplexTumble   *CustomPageSize True

*% Output bin UI Constraints
*% If optional Multi-Bin Mailbox is not installed,
*% disable Multi-Bin Mailbox output destinations.
*%------------------------------------------------------------
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin UStapler
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin Stacker
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin1
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin2
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin3
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin4
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin5
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mixed Standard *OutputBin OutputBin8

*% Constrain output bins that are not available.
*%------------------------------------------------------------
*UIConstraints: *HPOption_MBM_Mixed MBM5S *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mixed MBM5S *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mixed MBM5S *OutputBin OutputBin8
*UIConstraints: *HPOption_MBM_Mixed MBM5S *OutputBin Stacker

*UIConstraints: *HPOption_MBM_Mixed MBM7 *OutputBin UStapler
*UIConstraints: *HPOption_MBM_Mixed MBM7 *OutputBin OutputBin8
*UIConstraints: *HPOption_MBM_Mixed MBM7 *OutputBin Stacker

*UIConstraints: *HPOption_MBM_Mixed MBM8 *OutputBin UStapler
*UIConstraints: *HPOption_MBM_Mixed MBM8 *OutputBin Stacker

*% If an output accessory is not selected then disable the mailbox modes except mailbox.
*%------------------------------------------------------------
*% *UIConstraints: *HPOption_MBM_Mixed Standard *HPOption_MBM_Mode MailboxModeStacker

*% If Multi-Bin Mailbox mode is Mailbox, disable Stacker-Separator-Collator.
*%------------------------------------------------------------
*UIConstraints: *HPOption_MBM_Mode MailboxModeMailbox *OutputBin Stacker
*UIConstraints: *HPOption_MBM_Mode MailboxModeMailbox *OutputBin StackerSeparator

*% If Multi-Bin Mailbox mode is Stacker-Separator-Collator disable Individual Mailboxes
*%------------------------------------------------------------
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin1
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin2
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin3
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin4
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin5
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin6
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin7
*UIConstraints: *HPOption_MBM_Mode MailboxModeStacker *OutputBin OutputBin8

*% Limit support to Letter, A4  to the MBM5 stapler bin.
*% Note: These are included for informational purposes only
*% This is actually a 3-way constraint handled by a ppdA resource
*%------------------------------------------------------------
*UIConstraints: *PageSize Env10   *OutputBin UStapler
*UIConstraints: *PageRegion Env10 *OutputBin UStapler

*UIConstraints: *PageSize EnvMonarch   *OutputBin UStapler
*UIConstraints: *PageRegion EnvMonarch *OutputBin UStapler

*UIConstraints: *PageSize EnvDL   *OutputBin UStapler
*UIConstraints: *PageRegion EnvDL *OutputBin UStapler

*UIConstraints: *PageSize EnvC5   *OutputBin UStapler
*UIConstraints: *PageRegion EnvC5 *OutputBin UStapler

*UIConstraints: *PageSize EnvISOB5   *OutputBin UStapler
*UIConstraints: *PageRegion EnvISOB5 *OutputBin UStapler

*UIConstraints: *PageSize Executive   *OutputBin UStapler
*UIConstraints: *PageRegion Executive *OutputBin UStapler

*UIConstraints: *PageSize Legal   *OutputBin UStapler
*UIConstraints: *PageRegion Legal *OutputBin UStapler

*UIConstraints: *PageSize LegalSmall   *OutputBin UStapler
*UIConstraints: *PageRegion LegalSmall *OutputBin UStapler

*UIConstraints: *PageSize Tabloid   *OutputBin UStapler
*UIConstraints: *PageRegion Tabloid *OutputBin UStapler

*UIConstraints: *PageSize w842h1274   *OutputBin UStapler
*UIConstraints: *PageRegion w842h1274 *OutputBin UStapler

*UIConstraints: *PageSize A3   *OutputBin UStapler
*UIConstraints: *PageRegion A3 *OutputBin UStapler

*UIConstraints: *PageSize B4   *OutputBin UStapler
*UIConstraints: *PageRegion B4 *OutputBin UStapler

*UIConstraints: *PageSize w612h935   *OutputBin UStapler
*UIConstraints: *PageRegion w612h935 *OutputBin UStapler

*UIConstraints: *PageSize w558h774   *OutputBin UStapler
*UIConstraints: *PageRegion w558h774 *OutputBin UStapler

*UIConstraints: *PageSize w774h1116   *OutputBin UStapler
*UIConstraints: *PageRegion w774h1116 *OutputBin UStapler

*%These paper sizes cannot be stapled
*UIConstraints: *PageSize B5   *OutputBin UStapler
*UIConstraints: *PageRegion B5 *OutputBin UStapler
*UIConstraints: *PageSize A5   *OutputBin UStapler
*UIConstraints: *PageRegion A5 *OutputBin UStapler
*UIConstraints: *PageSize DoublePostcard   *OutputBin UStapler
*UIConstraints: *PageRegion DoublePostcard *OutputBin UStapler

*UIConstraints: *OutputBin UStapler *PageSize B5
*UIConstraints: *OutputBin UStapler *PageRegion B5
*UIConstraints: *OutputBin UStapler *PageSize A5
*UIConstraints: *OutputBin UStapler *PageRegion A5
*UIConstraints: *OutputBin UStapler *PageSize DoublePostcard
*UIConstraints: *OutputBin UStapler *PageRegion DoublePostcard

*%These media types make no sense to staple
*UIConstraints: *MediaType Transparency *OutputBin UStapler
*UIConstraints: *MediaType Card_Stock *OutputBin UStapler
*UIConstraints: *MediaType Labels *OutputBin UStapler

*UIConstraints: *OutputBin UStapler *MediaType Transparency
*UIConstraints: *OutputBin UStapler *MediaType Card_Stock
*UIConstraints: *OutputBin UStapler *MediaType Labels

*% Disable feeding Asian, 11x17 (Oversize), A5, B5 (JIS), DoublePostcard,
*% and envelopes to the output bins
*%------------------------------------------------------------
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin1
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin2
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin3
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin4
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin5
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin6
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin7
*UIConstraints: *PageSize w612h935 *OutputBin OutputBin8

*UIConstraints: *PageSize w558h774 *OutputBin OutputBin1
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin2
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin3
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin4
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin5
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin6
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin7
*UIConstraints: *PageSize w558h774 *OutputBin OutputBin8

*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin1
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin2
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin3
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin4
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin5
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin6
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin7
*UIConstraints: *PageSize w774h1116 *OutputBin OutputBin8

*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin1
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin2
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin3
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin4
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin5
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin6
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin7
*UIConstraints: *PageSize w842h1274 *OutputBin OutputBin8

*UIConstraints: *PageSize A5 *OutputBin UStapler
*UIConstraints: *PageSize A5 *OutputBin Stacker
*UIConstraints: *PageSize A5 *OutputBin OutputBin1
*UIConstraints: *PageSize A5 *OutputBin OutputBin2
*UIConstraints: *PageSize A5 *OutputBin OutputBin3
*UIConstraints: *PageSize A5 *OutputBin OutputBin4
*UIConstraints: *PageSize A5 *OutputBin OutputBin5
*UIConstraints: *PageSize A5 *OutputBin OutputBin6
*UIConstraints: *PageSize A5 *OutputBin OutputBin7
*UIConstraints: *PageSize A5 *OutputBin OutputBin8

*UIConstraints: *PageSize B5 *OutputBin UStapler
*UIConstraints: *PageSize B5 *OutputBin Stacker
*UIConstraints: *PageSize B5 *OutputBin OutputBin1
*UIConstraints: *PageSize B5 *OutputBin OutputBin2
*UIConstraints: *PageSize B5 *OutputBin OutputBin3
*UIConstraints: *PageSize B5 *OutputBin OutputBin4
*UIConstraints: *PageSize B5 *OutputBin OutputBin5
*UIConstraints: *PageSize B5 *OutputBin OutputBin6
*UIConstraints: *PageSize B5 *OutputBin OutputBin7
*UIConstraints: *PageSize B5 *OutputBin OutputBin8

*UIConstraints: *PageSize DoublePostcard *OutputBin UStapler
*UIConstraints: *PageSize DoublePostcard *OutputBin Stacker
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin1
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin2
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin3
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin4
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin5
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin6
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin7
*UIConstraints: *PageSize DoublePostcard *OutputBin OutputBin8

*UIConstraints: *PageSize Env10 *OutputBin Stacker
*UIConstraints: *PageSize Env10 *OutputBin OutputBin1
*UIConstraints: *PageSize Env10 *OutputBin OutputBin2
*UIConstraints: *PageSize Env10 *OutputBin OutputBin3
*UIConstraints: *PageSize Env10 *OutputBin OutputBin4
*UIConstraints: *PageSize Env10 *OutputBin OutputBin5
*UIConstraints: *PageSize Env10 *OutputBin OutputBin6
*UIConstraints: *PageSize Env10 *OutputBin OutputBin7
*UIConstraints: *PageSize Env10 *OutputBin OutputBin8

*UIConstraints: *PageSize EnvMonarch *OutputBin Stacker
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin1
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin2
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin3
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin4
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin5
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin6
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin7
*UIConstraints: *PageSize EnvMonarch *OutputBin OutputBin8

*UIConstraints: *PageSize EnvDL *OutputBin Stacker
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin1
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin2
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin3
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin4
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin5
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin6
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin7
*UIConstraints: *PageSize EnvDL *OutputBin OutputBin8

*UIConstraints: *PageSize EnvC5 *OutputBin Stacker
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin1
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin2
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin3
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin4
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin5
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin6
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin7
*UIConstraints: *PageSize EnvC5 *OutputBin OutputBin8

*UIConstraints: *PageSize EnvISOB5 *OutputBin Stacker
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin1
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin2
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin3
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin4
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin5
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin6
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin7
*UIConstraints: *PageSize EnvISOB5 *OutputBin OutputBin8

*% Disable feeding Asian, 11x17 (Oversize), A5, B5 (JIS), DoublePostcard,
*% and envelopes to the output bins
*%------------------------------------------------------------
*UIConstraints: *PageRegion w612h935 *OutputBin Stacker
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin1
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin2
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin3
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin4
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin5
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin6
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin7
*UIConstraints: *PageRegion w612h935 *OutputBin OutputBin8

*UIConstraints: *PageRegion w558h774 *OutputBin Stacker
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin1
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin2
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin3
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin4
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin5
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin6
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin7
*UIConstraints: *PageRegion w558h774 *OutputBin OutputBin8

*UIConstraints: *PageRegion w774h1116 *OutputBin Stacker
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin1
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin2
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin3
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin4
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin5
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin6
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin7
*UIConstraints: *PageRegion w774h1116 *OutputBin OutputBin8

*UIConstraints: *PageRegion w842h1274 *OutputBin Stacker
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin1
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin2
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin3
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin4
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin5
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin6
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin7
*UIConstraints: *PageRegion w842h1274 *OutputBin OutputBin8

*UIConstraints: *PageRegion A5 *OutputBin UStapler
*UIConstraints: *PageRegion A5 *OutputBin Stacker
*UIConstraints: *PageRegion A5 *OutputBin OutputBin1
*UIConstraints: *PageRegion A5 *OutputBin OutputBin2
*UIConstraints: *PageRegion A5 *OutputBin OutputBin3
*UIConstraints: *PageRegion A5 *OutputBin OutputBin4
*UIConstraints: *PageRegion A5 *OutputBin OutputBin5
*UIConstraints: *PageRegion A5 *OutputBin OutputBin6
*UIConstraints: *PageRegion A5 *OutputBin OutputBin7
*UIConstraints: *PageRegion A5 *OutputBin OutputBin8

*UIConstraints: *PageRegion B5 *OutputBin UStapler
*UIConstraints: *PageRegion B5 *OutputBin Stacker
*UIConstraints: *PageRegion B5 *OutputBin OutputBin1
*UIConstraints: *PageRegion B5 *OutputBin OutputBin2
*UIConstraints: *PageRegion B5 *OutputBin OutputBin3
*UIConstraints: *PageRegion B5 *OutputBin OutputBin4
*UIConstraints: *PageRegion B5 *OutputBin OutputBin5
*UIConstraints: *PageRegion B5 *OutputBin OutputBin6
*UIConstraints: *PageRegion B5 *OutputBin OutputBin7
*UIConstraints: *PageRegion B5 *OutputBin OutputBin8

*UIConstraints: *PageRegion DoublePostcard *OutputBin UStapler
*UIConstraints: *PageRegion DoublePostcard *OutputBin Stacker
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin1
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin2
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin3
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin4
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin5
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin6
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin7
*UIConstraints: *PageRegion DoublePostcard *OutputBin OutputBin8

*UIConstraints: *PageRegion Env10 *OutputBin Stacker
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin1
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin2
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin3
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin4
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin5
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin6
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin7
*UIConstraints: *PageRegion Env10 *OutputBin OutputBin8

*UIConstraints: *PageRegion EnvMonarch *OutputBin Stacker
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin1
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin2
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin3
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin4
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin5
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin6
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin7
*UIConstraints: *PageRegion EnvMonarch *OutputBin OutputBin8

*UIConstraints: *PageRegion EnvDL *OutputBin Stacker
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin1
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin2
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin3
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin4
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin5
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin6
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin7
*UIConstraints: *PageRegion EnvDL *OutputBin OutputBin8

*UIConstraints: *PageRegion EnvC5 *OutputBin Stacker
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin1
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin2
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin3
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin4
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin5
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin6
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin7
*UIConstraints: *PageRegion EnvC5 *OutputBin OutputBin8

*UIConstraints: *PageRegion EnvISOB5 *OutputBin Stacker
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin1
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin2
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin3
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin4
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin5
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin6
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin7
*UIConstraints: *PageRegion EnvISOB5 *OutputBin OutputBin8


*%=== Proof and Hold =======================
*% The UserName setting is obtained from the print job. This may not work on non-Mac drivers.
*OpenUI *HPJobRetentionOption/Job Retention: PickOne
*OrderDependency: 14 Prolog *HPJobRetentionOption
*DefaultHPJobRetentionOption: HPJobRetentionOff
*HPJobRetentionOption HPJobRetentionQuickCopy/Quick Copy: "
	<< /Collate true /CollateDetails
		<< /Type 8 /Hold 1 >>
	>> setpagedevice
"
*End
*HPJobRetentionOption HPJobRetentionProof/Proof and Hold: "
	<< /Collate true /CollateDetails
		<< /Type 8 /Hold 3 >>
	>> setpagedevice
"
*End
*HPJobRetentionOption HPJobRetentionStore/Stored Job: "
	<< /Collate true /CollateDetails
		<< /Type 8 /Hold 2 >>
	>> setpagedevice
"
*End

*%HPJobRetention HPJobRetentionPrivate/Private Job: "
*%	<< /Collate true /CollateDetails
*%		<< /Type 8 /Hold 1 /HoldType 1 >>
*%	>> setpagedevice
*%"
*%End

*HPJobRetentionOption HPJobRetentionOff/Off: "
	<< /CollateDetails
	<< /Type 8 /Hold 0 >> >> setpagedevice
"
*End
*CloseUI: *HPJobRetentionOption



*OpenUI *HPUserName/User Name: PickOne
*% The UserName setting is obtained from the print job. This will not work unchanged on non-Mac drivers.
*% The PS code has been written to put in default user and job names if they are not available from the job.
*% User specification of UserName works only with LW 8.5.1 or later. It will not work with non-Mac drivers.
*% If the driver does not support text entry UI the UserName will always be obtained from the print job.
*% The user is allowed to set the user name to allow organization of jobs in the printer.
*% For example, all forms could be stored under UserName "Forms".
*OrderDependency: 15 Prolog *HPUserName
*DefaultHPUserName: FileSharingName
*HPUserName FileSharingName/Use file sharing name: "
	<< /CollateDetails
		<< /Type 8
			/UserName /dscInfo where
				{ /dscInfo get dup /For known
					{/For get}
					{pop (No User Name)} ifelse}
				{(No User Name)}ifelse
			dup length 80 gt { 0 80 getinterval } if
			dup true exch { 32 eq not { false exch pop } if } forall
			{ pop (No User Name) } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End
*HPUserName Forms/Forms: "
	<< /CollateDetails
		<< /Type 8
			/UserName (Forms)
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End
*HPUserName Set/Custom user name: "
	<< /CollateDetails
		<< /Type 8
			/UserName /dscInfo where
				{ /dscInfo get dup /For known
					{/For get}
					{pop (No User Name)} ifelse}
				{(No User Name)}ifelse
			dup length 80 gt { 0 80 getinterval } if
			dup true exch { 32 eq not { false exch pop } if } forall
			{ pop (No User Name) } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End
*CloseUI: *HPUserName
*% Allows LW 8.5.1 and above to use custom strings
*RBISetHPUserName Data: "() 80"
*RBISetHPUserName Code: "
	<< /CollateDetails
		<< /Type 8 /UserName 7 -1 roll
			dup true exch { 32 eq not { false exch pop } if } forall
			{ pop (No User Name) } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End

*OpenUI *HPJobName/Job Name: PickOne
*% The JobMgrName setting is obtained from the print job. This may not work on non-Mac drivers.
*% User specification of Jobname works only with LW 8.5.1 or later. It will not work with non-Mac drivers.
*% If the driver does not support text entry UI the JobMgrName will always be obtained from the print job.
*OrderDependency: 16 Prolog *HPJobName
*DefaultHPJobName: DocName
*HPJobName DocName/Use Document Name: "
	<< /CollateDetails
		<< /Type 8
			/JobMgrName /dscInfo where
				{ /dscInfo get dup /Title known
					{/Title get}
					{pop ()} ifelse}
				{()}ifelse
			/dscInfo where
				{ /dscInfo get dup /Creator known
					{
						/Creator get dup 0 exch
						{ dup 32 eq exch dup 64 gt exch 122 le and or { 1 add } { exit } ifelse } forall
						0 exch getinterval anchorsearch { pop } if
					}
					{pop} ifelse
				} if
			{ (:) search
				{ pop pop }
				{ exit }
				ifelse
			} loop
			dup 0 exch { false ( -) { 2 index eq or } forall exch pop { 1 add } { exit } ifelse } forall
			dup 0 eq { pop } { dup 2 index length exch sub getinterval } ifelse
			dup length 80 gt { 0 80 getinterval } if
			dup true exch { 32 eq not { false exch pop } if } forall
			{ pop () } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End
*HPJobName Set/User Specified Job Name: "
	<< /CollateDetails
		<< /Type 8
			/JobMgrName /dscInfo where
				{ /dscInfo get dup /Title known
					{/Title get}
					{pop ()} ifelse}
				{()}ifelse
			/dscInfo where
				{ /dscInfo get dup /Creator known
					{
						/Creator get dup 0 exch
						{ dup 32 eq exch dup 64 gt exch 122 le and or { 1 add } { exit } ifelse } forall
						0 exch getinterval anchorsearch { pop } if
					}
					{pop} ifelse
				} if
			{ (:) search
				{ pop pop }
				{ exit }
				ifelse
			} loop
			dup 0 exch { false ( -) { 2 index eq or } forall exch pop { 1 add } { exit } ifelse } forall
			dup 0 eq { pop } { dup 2 index length exch sub getinterval } ifelse
			dup length 80 gt { 0 80 getinterval } if
			dup true exch { 32 eq not { false exch pop } if } forall
			{ pop () } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End
*CloseUI: *HPJobName
*% Allows LW 8.5.1 and above to use custom strings
*RBISetHPJobName Data: "() 80"
*RBISetHPJobName Code: "
	<< /CollateDetails
		<< /Type 8 /JobMgrName 7 -1 roll
			{ (:) search
				{ pop pop
					{ ( ) anchorsearch
						{ pop }
						{ exit }
						ifelse
					} loop
				}
				{ exit }
				ifelse
			} loop dup true exch { 32 eq not { false exch pop } if } forall
			{ pop () } if
			0 1 2 index length 1 sub
			{ dup 2 index exch get dup 97 ge 1 index 122 le and
				{ 32 sub 2 index 3 1 roll put }
				{ pop pop } ifelse
			} for
		>>
	>> setpagedevice
"
*End

*%================================
*%    Media Output Destination
*%================================
*OpenUI *OutputBin/Output Destination: PickOne
*OrderDependency: 100 AnySetup *OutputBin
*DefaultOutputBin: PrinterDefault
*OutputBin PrinterDefault/Printer's Current Setting: ""
*OutputBin Upper/Top Bin: "<</Staple 0 /OutputType (TOP OUTPUT BIN)>> setpagedevice"
*OutputBin Left/Left Bin (Face Up): "
   currentpagedevice /OutputAttributes get
   4 known
         {<</Staple 0 /OutputType (FACE UP BIN)>> setpagedevice}
         {<</Staple 0 /OutputType (LEFT OUTPUT BIN)>> setpagedevice}
       ifelse
"
*End
*OutputBin Stacker/Stacker: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 2)>> setpagedevice"
*%*OutputBin Collator/Collator: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 2)>> setpagedevice"
*%*OutputBin Separator/Job Separator: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 2)>> setpagedevice"
*OutputBin StackerSeparator/Stacker-Separator-Collator: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 2)>> setpagedevice"
*OutputBin UStapler/Stapler: "
  userdict /HPStapleOption known {HPStapleOption}{<</Staple 2>> setpagedevice} ifelse
  /currentdistillerparams 0 def
  /setpagedevice { dup /Orientation known
    { dup dup /Orientation get 2 mod 0 eq /StapleDetails << /Type 8 /Portrait 6 -1 roll >> put }if
    systemdict /setpagedevice get exec
  } bind def"
*End
*OutputBin OutputBin1/Bin 1: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 2)>> setpagedevice"
*OutputBin OutputBin2/Bin 2: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 3)>> setpagedevice"
*OutputBin OutputBin3/Bin 3: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 4)>> setpagedevice"
*OutputBin OutputBin4/Bin 4: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 5)>> setpagedevice"
*OutputBin OutputBin5/Bin 5: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 6)>> setpagedevice"
*OutputBin OutputBin6/Bin 6: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 7)>> setpagedevice"
*OutputBin OutputBin7/Bin 7: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 8)>> setpagedevice"
*OutputBin OutputBin8/Bin 8: "<</Staple 0 /OutputType (OPTIONAL OUTBIN 9)>> setpagedevice"
*?OutputBin:"
save
 currentpagedevice /OutputAttributes get dup
 5 known
 {/Priority get 0 get
    [(Upper) (Left) (Reserved1) (Reserved2) (OutputBin1)
     (OutputBin2) (OutputBin3) (OutputBin4) (OutputBin5) (OutputBin6) (OutputBin7) (OutputBin8)] exch get = flush}
 {/Priority get 0 get
    [(Upper) (Left)  (Reserved1) (Reserved2) (Stacker)] exch get = flush} ifelse
restore
"
*End
*CloseUI: *OutputBin

*%=== 3000 Sheet Stacker/Stapler Stapler Options =========================
*OpenUI *HPStaplerOptions/Stapler Option: PickOne
*OrderDependency: 45 AnySetup *HPStaplerOptions
*DefaultHPStaplerOptions: PrintersDefault
*HPStaplerOptions PrintersDefault/Printer's Current Setting: ""
*HPStaplerOptions 1diagonal/1 Staple, diagonal: "
  userdict /HPConfigurableStapler known
  { userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (ONEANGLED)>> >> setpagedevice} put }
  if"
*End
*HPStaplerOptions 1parallel/1 Staple, parallel: "
  userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (ONE)>> >> setpagedevice} put"
*End
*HPStaplerOptions 2parallel/2 Staples, parallel: "
  userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (TWO)>> >> setpagedevice} put"
*End
*HPStaplerOptions 3parallel/3 Staples, parallel: "
  userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (THREE)>> >> setpagedevice} put"
*End
*HPStaplerOptions 6parallel/6 Staples, parallel: "
  userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (SIX)>> >> setpagedevice} put"
*End
*HPStaplerOptions Custom/Custom: "
  userdict /HPStapleOption {<</Staple 2 /StapleDetails <</Type 8 /StapleOption (CUSTOM)>> >> setpagedevice} put"
*End
*CloseUI: *HPStaplerOptions

*% Fills not allowed with overlays
*%------------------------------------------------------------
*UIConstraints: *HPwmSwitch Overlay *HPwmTextStyle Fill
*UIConstraints: *HPwmTextStyle Fill *HPwmSwitch Overlay

*% Halo style does not work with Watermarks
*%------------------------------------------------------------
*UIConstraints: *HPwmSwitch Watermark *HPwmTextStyle Halo
*UIConstraints: *HPwmTextStyle Halo *HPwmSwitch Watermark

*% =================================
*%  Watermark Printing
*% =================================
*OpenUI *HPwmSwitch/Watermark/Overlay:  PickOne
*OrderDependency: 10000 AnySetup *HPwmSwitch
*DefaultHPwmSwitch: Off
*HPwmSwitch Off/None: ""
*HPwmSwitch Watermark/Watermark: "
% Copyright (c) Hewlett-Packard Co 1997
/HPwm where { pop }{
  userdict begin
  true setglobal /HPwm 5 dict dup begin /HPwmOn true def end def false setglobal
  userdict /HPwmLocation known not {/HPwmLocation true def} if
  userdict /HPwmText known not {/HPwmText (Draft) def} if
  FontDirectory /HPwmFont known not {
    /Helvetica-Bold findfont dup length dict begin
    {1 index /FID ne {def} {pop pop} ifelse} forall
    /MacEncoding where
    { pop /Encoding MacEncoding def }
    { /Encoding ISOLatin1Encoding def } ifelse
    currentdict
    end
    /HPwmFont exch definefont pop
  } if
  userdict /HPwmSize known not {/HPwmSize 48 def} if
  userdict /HPwmAngle known not {/HPwmAngle 45 def} if
  userdict /HPwmSaturation known not
  { /HPwmSaturation
    { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .55 mul } forall setcolor } def
  } if
  userdict /HPwmColor known not
  { /HPwmColor { 0 setgray HPwmSaturation } def
  } if
  userdict /HPwmStyle known not
  {/HPwmStyle { HPwmText false charpath HPwmColor .48 setlinewidth stroke } def
  } if
  end

  /HPwminitialize
	{ HPwm /HPwmOn get
	    { gsave
	      initmatrix
	      0 setgray 1 setlinewidth true setstrokeadjust 0 setlinejoin 0 setlinecap [] 0 setdash
	      currentpagedevice /PageSize get aload pop 2 div exch 2 div exch translate
	      HPwmAngle rotate
	      /normland where {
	      	pop /normland load dup type /booleantype eq { { 90 rotate } if } if
	      } if
	      /HPwmFont HPwmSize selectfont
	      HPwmText stringwidth 2 div neg exch 2 div neg exch HPwmSize .25 mul sub moveto
	      HPwmStyle HPwmLocation not {true setglobal HPwm /HPwmOn false put false setglobal} if
	      grestore
	    } if
   } bind def
  /md where {
  	pop /initializepage where {
  		/LWinitializepage /initializepage load def
  		/initializepage { HPwminitialize LWinitializepage } put
  	}if
  } if

  /LWinitializepage where { pop }{
  <<
  /BeginPage
  { pop HPwminitialize } bind
  >> setpagedevice
  } ifelse
} ifelse"
*End
*HPwmSwitch Overlay/Overlay: "
% Copyright (c) Hewlett-Packard Co 1997
/HPwm where { pop }{
  userdict begin
  true setglobal /HPwm 5 dict dup begin /HPwmOn true def end def false setglobal
  userdict /HPwmLocation known not {/HPwmLocation true def} if
  userdict /HPwmText known not {/HPwmText (Draft) def} if
  FontDirectory /HPwmFont known not {
    /Helvetica-Bold findfont dup length dict begin
    {1 index /FID ne {def} {pop pop} ifelse} forall
    /MacEncoding where
    { pop /Encoding MacEncoding def }
    { /Encoding ISOLatin1Encoding def } ifelse
    currentdict
    end
    /HPwmFont exch definefont pop
  } if
  userdict /HPwmSize known not {/HPwmSize 48 def} if
  userdict /HPwmAngle known not {/HPwmAngle 45 def} if
  userdict /HPwmSaturation known not
  { /HPwmSaturation
    { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .55 mul } forall setcolor } def
  } if
  userdict /HPwmColor known not
  { /HPwmColor { 0 setgray HPwmSaturation } def
  } if
  userdict /HPwmStyle known not
  {/HPwmStyle { HPwmText false charpath HPwmColor .48 setlinewidth stroke } def
  } if
 end
  <<
  /EndPage
    {
  	  2 eq { pop false }{
  		pop HPwm /HPwmOn get
	    { gsave
	      initmatrix
	      0 setgray 1 setlinewidth true setstrokeadjust 0 setlinejoin 0 setlinecap [] 0 setdash
	      currentpagedevice /PageSize get aload pop 2 div exch 2 div exch translate
	      HPwmAngle rotate
	      /normland where {
	      	pop /normland load dup type /booleantype eq { { 90 rotate } if } if
	      } if
	      /HPwmFont HPwmSize selectfont
	      HPwmText stringwidth 2 div neg exch 2 div neg exch HPwmSize .25 mul sub moveto
	      HPwmStyle HPwmLocation not {true setglobal HPwm /HPwmOn false put false setglobal} if
	      grestore
	    } if
	    true
	  } ifelse
    } bind
  >> setpagedevice
} ifelse"
*End
*CloseUI: *HPwmSwitch

*% =================================
*%  Watermark Pages
*% =================================
*OpenUI *HPwmPages/Watermark Pages:  PickOne
*OrderDependency: 67 AnySetup *HPwmPages
*DefaultHPwmPages: AllPages
*HPwmPages AllPages/All: "userdict /HPwmLocation true put"
*HPwmPages FirstPage/First Only: "userdict /HPwmLocation false put"
*CloseUI: *HPwmPages

*% =================================
*%  Watermark Text
*% =================================
*OpenUI *HPwmTextMessage/Watermark Text:  PickOne
*OrderDependency: 65 AnySetup *HPwmTextMessage
*DefaultHPwmTextMessage: Draft
*HPwmTextMessage Draft/Draft: "userdict /HPwmText (Draft) put"
*HPwmTextMessage CompanyConfidential/Company Confidential: "userdict /HPwmText (Company Confidential) put"
*HPwmTextMessage CompanyProprietary/Company Proprietary: "userdict /HPwmText (Company Proprietary) put"
*HPwmTextMessage CompanyPrivate/Company Private: "userdict /HPwmText (Company Private) put"
*HPwmTextMessage Confidential/Confidential: "userdict /HPwmText (Confidential) put"
*HPwmTextMessage Copy/Copy: "userdict /HPwmText (Copy) put"
*HPwmTextMessage Copyright/Copyright: "userdict /HPwmText (Copyright) put"
*HPwmTextMessage FileCopy/File Copy: "userdict /HPwmText (File Copy) put"
*HPwmTextMessage Final/Final: "userdict /HPwmText (Final) put"
*HPwmTextMessage ForInternalUse/For Internal Use Only: "userdict /HPwmText (For Internal Use Only) put"
*HPwmTextMessage Preliminary/Preliminary: "userdict /HPwmText (Preliminary) put"
*HPwmTextMessage Proof/Proof: "userdict /HPwmText (Proof) put"
*HPwmTextMessage ReviewCopy/Review Copy: "userdict /HPwmText (Review Copy) put"
*HPwmTextMessage Sample/Sample: "userdict /HPwmText (Sample) put"
*HPwmTextMessage TopSecret/Top Secret: "userdict /HPwmText (Top Secret) put"
*HPwmTextMessage Urgent/Urgent: "userdict /HPwmText (Urgent) put"
*HPwmTextMessage Set/Custom: "userdict /HPwmText (Custom) put"
*CloseUI: *HPwmTextMessage

*% Allows LW 8.5.1 to use custom strings
*RBISetHPwmTextMessage Data: "(Custom) 50"
*RBISetHPwmTextMessage Code: "userdict /HPwmText 3 -1 roll put"

*% =================================
*%  Watermark Font
*% =================================
*OpenUI *HPwmFontName/Watermark Font:  PickOne
*OrderDependency: 65 AnySetup *HPwmFontName
*DefaultHPwmFontName: HelveticaB
*HPwmFontName CourierB/Courier Bold: "
  /Courier-Bold findfont dup length dict begin
    {1 index /FID ne {def} {pop pop} ifelse} forall
    /MacEncoding where
    { pop /Encoding MacEncoding def }
    { /Encoding ISOLatin1Encoding def } ifelse
    currentdict
  end
  /HPwmFont exch definefont pop"
*End
*HPwmFontName HelveticaB/Helvetica Bold: "
  /Helvetica-Bold findfont dup length dict begin
    {1 index /FID ne {def} {pop pop} ifelse} forall
    /MacEncoding where
    { pop /Encoding MacEncoding def }
    { /Encoding ISOLatin1Encoding def } ifelse
    currentdict
  end
  /HPwmFont exch definefont pop"
*End
*HPwmFontName TimesB/Times Bold: "
  /Times-Bold findfont dup length dict begin
    {1 index /FID ne {def} {pop pop} ifelse} forall
    /MacEncoding where
    { pop /Encoding MacEncoding def }
    { /Encoding ISOLatin1Encoding def } ifelse
    currentdict
  end
  /HPwmFont exch definefont pop"
*End
*CloseUI: *HPwmFontName

*% =================================
*%  Watermark Size
*% =================================
*OpenUI *HPwmFontSize/Watermark Size (points):  PickOne
*OrderDependency: 65 AnySetup *HPwmFontSize
*DefaultHPwmFontSize: pt48
*HPwmFontSize pt24/24: "userdict /HPwmSize 24 put"
*HPwmFontSize pt30/30: "userdict /HPwmSize 30 put"
*HPwmFontSize pt36/36: "userdict /HPwmSize 36 put"
*HPwmFontSize pt42/42: "userdict /HPwmSize 42 put"
*HPwmFontSize pt48/48: "userdict /HPwmSize 48 put"
*HPwmFontSize pt54/54: "userdict /HPwmSize 54 put"
*HPwmFontSize pt60/60: "userdict /HPwmSize 60 put"
*HPwmFontSize pt66/66: "userdict /HPwmSize 66 put"
*HPwmFontSize pt72/72: "userdict /HPwmSize 72 put"
*HPwmFontSize pt78/78: "userdict /HPwmSize 78 put"
*HPwmFontSize pt84/84: "userdict /HPwmSize 84 put"
*HPwmFontSize pt90/90: "userdict /HPwmSize 90 put"
*CloseUI: *HPwmFontSize

*% =================================
*%  Watermark Angle
*% =================================
*OpenUI *HPwmTextAngle/Watermark Angle:  PickOne
*OrderDependency: 65 AnySetup *HPwmTextAngle
*DefaultHPwmTextAngle: Deg45
*HPwmTextAngle Deg90/90<A1>: "userdict /HPwmAngle 90 put"
*HPwmTextAngle Deg75/75<A1>: "userdict /HPwmAngle 75 put"
*HPwmTextAngle Deg60/60<A1>: "userdict /HPwmAngle 60 put"
*HPwmTextAngle Deg45/45<A1>: "userdict /HPwmAngle 45 put"
*HPwmTextAngle Deg30/30<A1>: "userdict /HPwmAngle 30 put"
*HPwmTextAngle Deg15/15<A1>: "userdict /HPwmAngle 15 put"
*HPwmTextAngle Deg0/0<A1>: "userdict /HPwmAngle 0 put"
*HPwmTextAngle DegN15/15<A1>: "userdict /HPwmAngle -15 put"
*HPwmTextAngle DegN30/30<A1>: "userdict /HPwmAngle -30 put"
*HPwmTextAngle DegN45/45<A1>: "userdict /HPwmAngle -45 put"
*HPwmTextAngle DegN60/60<A1>: "userdict /HPwmAngle -60 put"
*HPwmTextAngle DegN75/75<A1>: "userdict /HPwmAngle -75 put"
*HPwmTextAngle DegN90/90<A1>: "userdict /HPwmAngle -90 put"
*CloseUI: *HPwmTextAngle

*% =================================
*%  Watermark Style
*% =================================
*OpenUI *HPwmTextStyle/Watermark Style:  PickOne
*OrderDependency: 65 AnySetup *HPwmTextStyle
*DefaultHPwmTextStyle: Medium
*HPwmTextStyle Thin/Thin Outline: "userdict /HPwmStyle { HPwmText false charpath HPwmColor .24 setlinewidth stroke } bind put"
*HPwmTextStyle Medium/Medium Outline: "userdict /HPwmStyle { HPwmText false charpath HPwmColor .48 setlinewidth stroke } bind put"
*HPwmTextStyle Thick/Thick Outline: "userdict /HPwmStyle { HPwmText false charpath HPwmColor .96 setlinewidth stroke } bind put"
*HPwmTextStyle Halo/Thick Outline with Halo: "userdict /HPwmStyle
     { HPwmText false charpath gsave /DeviceGray setcolorspace 1 setgray 1.8 setlinewidth stroke grestore
     HPwmColor .96 setlinewidth stroke } bind put"
*End
*HPwmTextStyle Fill/Filled: "userdict /HPwmStyle { HPwmColor HPwmText show } bind put"
*CloseUI: *HPwmTextStyle

*% =================================
*%  WaterMark Brightness
*% =================================
*OpenUI *HPwmBrightness/Watermark Intensity:  PickOne
*OrderDependency: 63 AnySetup *HPwmBrightness
*DefaultHPwmBrightness: Medium
*HPwmBrightness Darkest/Darkest:          "userdict /HPwmSaturation { null pop } put"
*HPwmBrightness Darker/Darker:            "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .88 mul } forall setcolor } put"
*HPwmBrightness Dark/Dark:                "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .77 mul } forall setcolor } put"
*HPwmBrightness MediumDark/Medium Dark:   "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .66 mul } forall setcolor } put"
*HPwmBrightness Medium/Medium:            "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .55 mul } forall setcolor } put"
*HPwmBrightness MediumLight/Medium Light: "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .44 mul } forall setcolor } put"
*HPwmBrightness Light/Light:              "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .33 mul } forall setcolor } put"
*HPwmBrightness Lighter/Lighter:          "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .22 mul } forall setcolor } put"
*HPwmBrightness Lightest/Lightest:        "userdict /HPwmSaturation { [ currentcmykcolor ] /DeviceCMYK setcolorspace { .11 mul } forall setcolor } put"
*CloseUI: *HPwmBrightness

*%=================================================
*%		 Enable/Disable Collate via PostScript
*%=================================================
*OpenUI *Collate/Collate:  Boolean
*OrderDependency: 12 AnySetup *Collate
*DefaultCollate: False
*Collate True/On (turn off in application): "<</Collate true>> setpagedevice"
*Collate False/Off: "<</Collate false>> setpagedevice"
*?Collate: "
   save
      currentpagedevice /Collate get
      {(True)}{(False)}ifelse = flush
   restore
"
*End
*CloseUI: *Collate

*%=================================================
*%        Resolution Enhancement
*%=================================================
*OpenUI *Smoothing/Resolution Enhancement:  PickOne
*OrderDependency: 20 DocumentSetup *Smoothing
*DefaultSmoothing: PrinterDefault
*Smoothing PrinterDefault/Printer's Current Setting: ""
*Smoothing None/Off: "
<< /PostRenderingEnhance true
    /PostRenderingEnhanceDetails << /REValue 0 /Type 8 >>
>>  setpagedevice"
*End
*Smoothing Light/Light: "
<< /PostRenderingEnhance true
    /PostRenderingEnhanceDetails << /REValue 1 /Type 8 >>
>>  setpagedevice"
*End
*Smoothing Medium/Medium: "
<< /PostRenderingEnhance true
    /PostRenderingEnhanceDetails << /REValue 2 /Type 8 >>
>>  setpagedevice"
*End
*Smoothing Dark/Dark: "
<< /PostRenderingEnhance true
    /PostRenderingEnhanceDetails << /REValue 3 /Type 8 >>
>> setpagedevice"
*End
*?Smoothing: "
  save
    currentpagedevice /PostRenderingEnhanceDetails get /REValue get
    [(Off) (Light) (Medium) (Dark)]  exch get print
  restore
"
*End
*CloseUI: *Smoothing

*FreeVM: "7500000"
*VMOption 24-31MB/24 - 31 MB: "7500000"
*VMOption 32-39MB/32 - 39 MB: "14500000"
*VMOption 40-47MB/40 - 47 MB: "21500000"
*VMOption 48-55MB/48 - 55 MB: "28500000"
*VMOption 56-63MB/56 - 63 MB: "35500000"
*VMOption 64-71MB/64 - 71 MB: "42500000"
*VMOption 72MB/72 MB or more: "50000000"

*%=================================================
*%		 Paper Sizes
*%=================================================
*OpenUI *PageSize: PickOne
*OrderDependency: 30 AnySetup *PageSize
*DefaultPageSize: Letter
*PageSize Letter/Letter: "
  <</PageSize [612 792] /ImagingBBox null>> setpagedevice"
*End
*PageSize LetterSmall/Letter (Small): "
	<</PageSize [612 792] /ImagingBBox null>> setpagedevice"
*End
*PageSize Executive/Executive: "
  <</PageSize [522 756] /ImagingBBox null>> setpagedevice"
*End
*PageSize Legal/Legal: "
  <</PageSize [612 1008] /ImagingBBox null>> setpagedevice"
*End
*PageSize LegalSmall/Legal (Small): "
	<</PageSize [612 1008] /ImagingBBox null>> setpagedevice"
*End
*PageSize Tabloid/11x17: "
  <</PageSize [792 1224] /ImagingBBox null>> setpagedevice"
*End
*PageSize w842h1274/11x17 (Oversize 11.7x17.7): "
  <</PageSize [842 1274] /ImagingBBox null>> setpagedevice"
*End
*PageSize A3/A3: "
  <</PageSize [842 1191] /ImagingBBox null>> setpagedevice"
*End
*PageSize A4/A4: "
  <</PageSize [595 842] /ImagingBBox null>> setpagedevice"
*End
*PageSize A4Small/A4 (Small): "
	<</PageSize [595 842] /ImagingBBox null>> setpagedevice"
*End
*PageSize A5/A5: "
  <</PageSize [420 595] /ImagingBBox null>> setpagedevice"
*End
*PageSize B4/JIS B4: "
  <</PageSize [729 1032] /ImagingBBox null>> setpagedevice"
*End
*PageSize B5/JIS B5: "
  <</PageSize [516 729] /ImagingBBox null>> setpagedevice"
*End
*PageSize DoublePostcard/Double Postcard (JIS): "
  <</PageSize [419.5 567] /ImagingBBox null>> setpagedevice"
*End
*PageSize w612h935/Executive (JIS): "
  <</PageSize [612 935] /ImagingBBox null>> setpagedevice"
*End
*PageSize w558h774/16K: "
  <</PageSize [558 774] /ImagingBBox null>> setpagedevice"
*End
*PageSize w774h1116/8K: "
  <</PageSize [774 1116] /ImagingBBox null>> setpagedevice"
*End
*PageSize Env10/Env Comm10: "
  <</PageSize [297 684] /ImagingBBox null>> setpagedevice"
*End
*PageSize EnvMonarch/Env Monarch: "
  <</PageSize [279 540] /ImagingBBox null>> setpagedevice"
*End
*PageSize EnvDL/Env DL: "
  <</PageSize [312 624] /ImagingBBox null>> setpagedevice"
*End
*PageSize EnvC5/Env C5: "
  <</PageSize [459 649] /ImagingBBox null>> setpagedevice"
*End
*PageSize EnvISOB5/Env ISO B5: "
  <</PageSize [499 709] /ImagingBBox null>> setpagedevice"
*End
*?PageSize: "
   save
   currentpagedevice /PageSize get aload pop
   2 copy gt {exch} if
   (Unknown)
   19 dict
   dup [612 792]  (Letter) put
   dup [522 756]  (Executive) put
   dup [612 1008] (Legal) put
   dup [792 1224] (Tabloid) put
   dup [842 1274] (w842h1274) put
   dup [842 1191] (A3) put
   dup [595 842]  (A4) put
   dup [420 595]  (A5) put
   dup [729 1032] (B4) put
   dup [516 729]  (B5) put
   dup [419.5 567]  (DoublePostcard) put
   dup [612 935] (w612h935) put
   dup [558 774] (w558h774) put
   dup [774 1116] (w774h1116) put
   dup [297 684]  (Env10) put
   dup [279 540]  (EnvMonarch) put
   dup [312 624]  (EnvDL) put
   dup [459 649]  (EnvC5) put
   dup [499 709]  (EnvISOB5) put
   { exch aload pop 4 index sub abs 5 le exch
      5 index sub abs 5 le and
      {exch pop exit} {pop} ifelse
   } bind forall
   = flush pop pop
   restore
"
*End
*CloseUI: *PageSize

*OpenUI *PageRegion: PickOne
*OrderDependency: 40 AnySetup *PageRegion
*DefaultPageRegion: Letter
*PageRegion Letter/Letter: "
  <</PageSize [612 792] /ImagingBBox null>> setpagedevice"
*End
*PageRegion LetterSmall/Letter (Small): "
	<</PageSize [612 792] /ImagingBBox null>> setpagedevice"
*End
*PageRegion Executive/Executive: "
  <</PageSize [522 756] /ImagingBBox null>> setpagedevice"
*End
*PageRegion Legal/Legal: "
  <</PageSize [612 1008] /ImagingBBox null>> setpagedevice"
*End
*PageRegion LegalSmall/Legal (Small): "
	<</PageSize [612 1008] /ImagingBBox null>> setpagedevice"
*End
*PageRegion Tabloid/11x17: "
  <</PageSize [792 1224] /ImagingBBox null>> setpagedevice"
*End
*PageRegion w842h1274/11x17 (Oversize 11.7x17.7): "
  <</PageSize [842 1274] /ImagingBBox null>> setpagedevice"
*End
*PageRegion A3/A3: "
  <</PageSize [842 1191] /ImagingBBox null>> setpagedevice"
*End
*PageRegion A4/A4: "
  <</PageSize [595 842] /ImagingBBox null>> setpagedevice"
*End
*PageRegion A4Small/A4 (Small): "
	<</PageSize [595 842] /ImagingBBox null>> setpagedevice"
*End
*PageRegion A5/A5: "
  <</PageSize [420 595] /ImagingBBox null>> setpagedevice"
*End
*PageRegion B4/JIS B4: "
  <</PageSize [729 1032] /ImagingBBox null>> setpagedevice"
*End
*PageRegion B5/JIS B5: "
  <</PageSize [516 729] /ImagingBBox null>> setpagedevice"
*End
*PageRegion DoublePostcard/Double Postcard (JIS): "
  <</PageSize [419.5 567] /ImagingBBox null>> setpagedevice"
*End
*PageRegion w612h935/Executive (JIS): "
  <</PageSize [612 935] /ImagingBBox null>> setpagedevice"
*End
*PageRegion w558h774/16K: "
  <</PageSize [558 774] /ImagingBBox null>> setpagedevice"
*End
*PageRegion w774h1116/8K: "
  <</PageSize [774 1116] /ImagingBBox null>> setpagedevice"
*End
*PageRegion Env10/Env Comm10: "
  <</PageSize [297 684] /ImagingBBox null>> setpagedevice"
*End
*PageRegion EnvMonarch/Env Monarch: "
  <</PageSize [279 540] /ImagingBBox null>> setpagedevice"
*End
*PageRegion EnvDL/Env DL: "
  <</PageSize [312 624] /ImagingBBox null>> setpagedevice"
*End
*PageRegion EnvC5/Env C5: "
  <</PageSize [459 649] /ImagingBBox null>> setpagedevice"
*End
*PageRegion EnvISOB5/Env ISO B5: "
  <</PageSize [499 709] /ImagingBBox null>> setpagedevice"
*End
*CloseUI: *PageRegion

*DefaultImageableArea: Letter
*ImageableArea Letter/Letter:							"4.00 3.00 606.00 786.00"
*ImageableArea LetterSmall/Letter (Small):				"30.00 31.00 582.00 761.00"
*ImageableArea Executive/Executive:						"3.00 3.00 516.00 750.00"
*ImageableArea Legal/Legal:								"64.00 54.00 606.00 1002.00"
*ImageableArea LegalSmall/Legal (Small):				"3.00 3.00 548.00 954.00"
*ImageableArea Tabloid/11x17:							"3.00 3.00 786.00 1218.00"
*ImageableArea w842h1274/11x17 (Oversize 11.7x17.7):	"3.00 3.00 836.00 1268.00"
*ImageableArea A3/A3:									"3.00 3.00 836.00 1185.00"
*ImageableArea A4/A4:									"4.00 3.00 586.00 836.00"
*ImageableArea A4Small/A4 (Small):						"28.00 30.00 566.00 811.00"
*ImageableArea A5/A5:									"3.00 3.00 414.00 589.00"
*ImageableArea B4/JIS B4:								"3.00 3.00 723.00 1026.00"
*ImageableArea B5/JIS B5:								"3.00 3.00 510.00 723.00"
*ImageableArea DoublePostcard/Double Postcard (JIS):	"3.00 3.00 413.50 561.00"
*ImageableArea w612h935/Executive (JIS):				"3.00 3.00 606.00 929.00"
*ImageableArea w558h774/16K:							"3.00 3.00 552.00 768.00"
*ImageableArea w774h1116/8K:							"3.00 3.00 768.00 1110.00"
*ImageableArea Env10/Env Comm10:						"3.00 3.00 291.00 678.00"
*ImageableArea EnvMonarch/Env Monarch:					"3.00 3.00 273.00 534.00"
*ImageableArea EnvDL/Env DL:							"3.00 3.00 306.00 618.00"
*ImageableArea EnvC5/Env C5:							"3.00 3.00 453.00 643.00"
*ImageableArea EnvISOB5/Env ISO B5:						"3.00 3.00 493.00 703.00"

*?ImageableArea: "
   save
   /cvp { (                ) cvs print ( ) print } bind def
   /upperright {10000 mul floor 10000 div} bind def
   /lowerleft {10000 mul ceiling 10000 div} bind def
   newpath clippath pathbbox
   4 -2 roll exch 2 {lowerleft cvp} repeat
   exch 2 {upperright cvp} repeat flush
   restore
"
*End

*DefaultPaperDimension: Letter
*PaperDimension Letter/Letter:							"612 792"
*PaperDimension LetterSmall/Letter (Small):				"612 792"
*PaperDimension Executive/Executive:					"522 756"
*PaperDimension Legal/Legal:							"612 1008"
*PaperDimension LegalSmall/Legal (Small):				"612 1008"
*PaperDimension Tabloid/11x17:							"792 1224"
*PaperDimension w842h1274/11x17 (Oversize 11.7x17.7):	"842 1274"
*PaperDimension A3/A3:									"842 1191"
*PaperDimension A4/A4:									"595 842"
*PaperDimension A4Small/A4 (Small):						"595 842"
*PaperDimension A5/A5:									"420 595"
*PaperDimension B4/JIS B4:								"729 1032"
*PaperDimension B5/JIS B5:								"516 729"
*PaperDimension DoublePostcard/Double Postcard (JIS):	"419.5 567"
*PaperDimension w612h935/Executive (JIS):				"612 935"
*PaperDimension w558h774/16K:							"558 774"
*PaperDimension w774h1116/8K:							"774 1116"
*PaperDimension Env10/Env Comm10:						"297 684"
*PaperDimension EnvMonarch/Env Monarch:					"279 540"
*PaperDimension EnvDL/Env DL:							"312 624"
*PaperDimension EnvC5/Env C5:							"459 649"
*PaperDimension EnvISOB5/Env ISO B5:					"499 709"

*LandscapeOrientation: Plus90

*%=================================================
*%		 Custom Paper Support
*%=================================================
*%Orientation and Margin (offsets) values are not utilized

*VariablePaperSize: True

*LeadingEdge PreferLong: ""
*DefaultLeadingEdge: PreferLong

*% Smallest = 3.67x7.5, Largest = 11.7 x 17.7
*MaxMediaWidth:  "842"
*MaxMediaHeight: "1274"
*HWMargins:      12 12 12 12
*CustomPageSize True: "
  pop pop pop
  <</DeferredMediaSelection true /PageSize [ 7 -2 roll ] /ImagingBBox null >>
  setpagedevice
"
*End

*ParamCustomPageSize Width:        1 points 264 842
*ParamCustomPageSize Height:       2 points 540 1274
*ParamCustomPageSize WidthOffset:  3 points 0 0
*ParamCustomPageSize HeightOffset: 4 points 0 0
*ParamCustomPageSize Orientation:  5 int 0 0

*RequiresPageRegion All: True

*%=================================================
*%		 Paper Sources
*%=================================================
*OpenUI *InputSlot: PickOne
*OrderDependency: 20 AnySetup *InputSlot
*DefaultInputSlot: Middle
*InputSlot Upper/Tray 1: "<</ManualFeed false /MediaPosition 3>> setpagedevice"
*InputSlot Middle/Tray 2: "<</ManualFeed false /MediaPosition 0>> setpagedevice"
*InputSlot Lower/Tray 3: "<</ManualFeed false /MediaPosition 1>> setpagedevice"
*InputSlot LargeCapacity/Tray 4: "<</ManualFeed false /MediaPosition 5>> setpagedevice"
*InputSlot Tray5/Tray 5: "<</ManualFeed false /MediaPosition 6>> setpagedevice"
*InputSlot Envelope/Envelope Feeder: "<</ManualFeed false /MediaPosition 2>> setpagedevice"
*?InputSlot: "
 save
   [(Middle) (Lower) (Envelope) (Upper) (LargeCapacity) (Tray5)]
   statusdict /papertray get exec
   {get exec} stopped { pop pop (Unknown) } if =
   currentpagedevice /InputAttributes get dup
   /Priority get 0 get get /MediaType get = flush
 restore
"
*End
*CloseUI: *InputSlot

*% Enable/Disable Manual Feed
*OpenUI *ManualFeed/Tray 1 (Manual): Boolean
*OrderDependency: 20 AnySetup *ManualFeed
*DefaultManualFeed: False
*ManualFeed True/True: "
	<</ManualFeed true>> setpagedevice"
*End
*ManualFeed False/False: "
	<</ManualFeed false>> setpagedevice"
*End
*?ManualFeed: "
	save
		currentpagedevice /ManualFeed get
		{(True)}{(False)}ifelse = flush
	restore
"
*End
*CloseUI: *ManualFeed

*%==========================================
*%		Media Type
*%=========================================
*OpenUI *MediaType/Media Type: PickOne
*OrderDependency: 20 AnySetup *MediaType
*DefaultMediaType: Plain
*MediaType Plain/Plain:  "
    <</MediaType (Plain)>> setpagedevice"
*End
*MediaType Preprinted/Preprinted:  "
    <</MediaType (Preprinted)>> setpagedevice"
*End
*MediaType Letterhead/Letterhead:  "
    <</MediaType (Letterhead)>> setpagedevice"
*End
*MediaType Transparency/Transparency:  "
    <</MediaType (Transparency)>> setpagedevice"
*End
*MediaType Prepunched/Prepunched:  "
    <</MediaType (Prepunched)>> setpagedevice"
*End
*MediaType Labels/Labels:  "
    <</MediaType (Labels)>> setpagedevice"
*End
*MediaType Bond/Bond:  "
    <</MediaType (Bond)>> setpagedevice"
*End
*MediaType Recycled/Recycled:  "
    <</MediaType (Recycled)>> setpagedevice"
*End
*MediaType Color/Color:  "
    <</MediaType (Color)>> setpagedevice"
*End
*MediaType Card_Stock/Card_Stock:  "
    <</MediaType (Card Stock)>> setpagedevice"
*End
*MediaType Rough/Rough:  "
    <</MediaType (Rough)>> setpagedevice"
*End
*?MediaType: "
  save
    currentpagedevice /InputAttributes get dup
    /Priority get
    0 get get
    /MediaType get
    (Card Stock) anchorsearch
      {pop pop (Card_Stock)} if
    = flush
  restore
"
*End
*CloseUI: *MediaType

*%=================================================
*%		 Halftone Information
*%=================================================
*ScreenFreq:  "106.0"
*ScreenAngle: "45.0"

*ResScreenFreq 300dpi/300 dpi:  "60.0"
*ResScreenAngle 300dpi/300 dpi: "45.0"
*ResScreenFreq 600dpi/600 dpi:  "106.0"
*ResScreenAngle 600dpi/600 dpi: "45.0"

*DefaultScreenProc: Dot
*ScreenProc HPEnhanced: "
	{ /EnhancedHalftone /Halftone findresource }"
*End
*ScreenProc Dot: "
        {abs exch abs 2 copy add 1 gt {1 sub dup mul exch 1 sub dup mul add 1
        sub }{dup mul exch dup mul add 1 exch sub }ifelse }
"
*End
*ScreenProc Line: "{ pop }"
*ScreenProc Ellipse: "{ dup 5 mul 8 div mul exch dup mul exch add sqrt 1 exch sub }"

*DefaultTransfer: Null
*Transfer Null: "{ }"
*Transfer Null.Inverse: "{ 1 exch sub }"

*DefaultHalftoneType:    9
*AccurateScreensSupport: False

*OpenUI *HPHalftone/Levels of Gray: PickOne
*OrderDependency: 10 DocumentSetup *HPHalftone
*DefaultHPHalftone: PrinterDefault
*HPHalftone PrinterDefault/Printer's Current Setting: ""
*HPHalftone Enhanced/Enhanced: "
   << /Install {
     currentpagedevice /HWResolution get
     dup 0 get 600 eq exch 1 get 600 eq and
     { /EnhancedColorRendering600 } { /EnhancedColorRendering } ifelse
     /ColorRendering findresource setcolorrendering
     /EnhancedHalftone /Halftone findresource sethalftone
     { } settransfer false setstrokeadjust
   }
   >> setpagedevice
   currentpagedevice /HWResolution get dup 0 get 600 eq exch 1 get 600 eq and
   {
       << /PostRenderingEnhance true
            /PostRenderingEnhanceDetails << /REValue 0 /Type 8 >>
       >> setpagedevice
   } if
   /setscreen { pop pop pop } def
   /setcolorscreen { pop pop pop pop pop pop pop pop pop pop pop pop } def
   /sethalftone { pop } def
"
*End
*HPHalftone Standard/Standard: "
   << /Install {
     currentpagedevice /HWResolution get
     dup 0 get 600 eq exch 1 get 600 eq and dup
     currentpagedevice /PostRenderingEnhance get
     currentpagedevice /PostRenderingEnhanceDetails get /REValue get 0 ne and
     { {/DefaultColorRenderingRE600} {/DefaultColorRenderingRE} ifelse}
     { {/DefaultColorRendering600} {/DefaultColorRendering} ifelse} ifelse
     /ColorRendering findresource setcolorrendering
     { /DefaultHalftone600 } {/DefaultHalftone} ifelse
     /Halftone findresource sethalftone
     {} settransfer false setstrokeadjust
   } >> setpagedevice
   currentpagedevice /HWResolution get dup 0 get 600 eq exch 1 get 600 eq and
   {
     << /PostRenderingEnhance true /PostRenderingEnhanceDetails
     << /REValue 0 /Type 8 >> >> setpagedevice
   } if
"
*End
*?HPHalftone: "
   save
      currenthalftone /HalftoneType get 9 eq
     {(Enhanced)} {(Standard)} ifelse = flush
   restore
"
*End
*CloseUI: *HPHalftone

*%=================================================
*%		Resolution
*%=================================================
*% Select Printer Resolution
*OpenUI *Resolution/Printer Resolution: PickOne
*DefaultResolution: 600x600x2dpi
*OrderDependency: 5 DocumentSetup  *Resolution
*Resolution 300x300dpi/300 dpi: "
    <</HWResolution [300 300] /PreRenderingEnhance false>> setpagedevice"
*End
*Resolution 600x600dpi/600 dpi: "
    <</HWResolution [600 600] /PreRenderingEnhance false>> setpagedevice"
*End
*Resolution 600x600x2dpi/FastRes 1200: "
	<</HWResolution [600 600] /PreRenderingEnhance true>> setpagedevice"
*End
*?Resolution: "
  save
    currentpagedevice /HWResolution get
    0 get
    (          ) cvs print
    (dpi)
    = flush
  restore
"
*End
*CloseUI: *Resolution

*%=================================================
*%          HPEconoMode
*%=================================================
*OpenUI *HPEconoMode/EconoMode: PickOne
*DefaultHPEconoMode: PrinterDefault
*OrderDependency: 10 AnySetup *HPEconoMode
*HPEconoMode PrinterDefault/Printer's Current Setting: ""
*HPEconoMode True/Save Toner: "
    <</EconoMode true>> setpagedevice"
*End
*HPEconoMode False/Highest Quality: "
    <</EconoMode false>> setpagedevice"
*End
*?HPEconoMode: "
  save
    currentpagedevice /EconoMode get
    {(True)}{(False)}ifelse = flush
  restore
"
*End
*CloseUI: *HPEconoMode

*%=================================================
*%		 Edge-to-Edge Printing
*%=================================================
*OpenUI *HPEdgeToEdge/Edge-To-Edge Printing: Boolean
*OrderDependency: 10 AnySetup *HPEdgeToEdge
*DefaultHPEdgeToEdge: False
*HPEdgeToEdge False/Off: "<</EdgeToEdge false>> setpagedevice"
*HPEdgeToEdge True/On: "<</EdgeToEdge true>> setpagedevice"
*?HPEdgeToEdge: "
  save
    currentpagedevice /EdgeToEdge get
      {(True)}{(False)}ifelse = flush
  restore
"
*End
*CloseUI: *HPEdgeToEdge


*%=================================================
*%		 Duplex
*%=================================================
*OpenUI *Duplex/Duplex:  PickOne
*OrderDependency: 50 AnySetup *Duplex
*DefaultDuplex: None
*Duplex None/Off (1-Sided): "
  <</Duplex false>> setpagedevice"
*End
*Duplex DuplexNoTumble/Flip on Long Edge (Standard): "
  <</Duplex true /Tumble false>> setpagedevice"
*End
*Duplex DuplexTumble/Flip on Short Edge: "
  <</Duplex true /Tumble true>> setpagedevice"
*End
*?Duplex: "
   save
   currentpagedevice /Duplex known
   false ne
     { currentpagedevice /Duplex get
        { currentpagedevice /Tumble get
            {(DuplexTumble)}{(DuplexNoTumble)}ifelse
        } { (None)}    ifelse
     }{(None)}  ifelse = flush
   restore
"
*End
*CloseUI: *Duplex

*%=================================================
*%		 Color Control
*%=================================================
*DefaultColorSep: ProcessBlack.106lpi.600dpi/106 lpi / 600 dpi
*InkName: ProcessBlack/Process Black
*InkName: CustomColor/Custom Color
*InkName: ProcessCyan/Process Cyan
*InkName: ProcessMagenta/Process Magenta
*InkName: ProcessYellow/Process Yellow

*%  For 60 lpi / 300 dpi  =========================
*ColorSepScreenAngle ProcessBlack.60lpi.300dpi/60 lpi / 300 dpi: "45"
*ColorSepScreenAngle CustomColor.60lpi.300dpi/60 lpi / 300 dpi: "45"
*ColorSepScreenAngle ProcessCyan.60lpi.300dpi/60 lpi / 300 dpi: "15"
*ColorSepScreenAngle ProcessMagenta.60lpi.300dpi/60 lpi / 300 dpi: "75"
*ColorSepScreenAngle ProcessYellow.60lpi.300dpi/60 lpi / 300 dpi: "0"

*ColorSepScreenFreq ProcessBlack.60lpi.300dpi/60 lpi / 300 dpi: "60"
*ColorSepScreenFreq CustomColor.60lpi.300dpi/60 lpi / 300 dpi: "60"
*ColorSepScreenFreq ProcessCyan.60lpi.300dpi/60 lpi / 300 dpi: "60"
*ColorSepScreenFreq ProcessMagenta.60lpi.300dpi/60 lpi / 300 dpi: "60"
*ColorSepScreenFreq ProcessYellow.60lpi.300dpi/60 lpi / 300 dpi: "60"

*%  For 85 lpi / 600 dpi  (5,5,2,6,6,2,20/3,0) ====
*ColorSepScreenAngle ProcessBlack.85lpi.600dpi/85 lpi / 600 dpi: "45.0"
*ColorSepScreenAngle CustomColor.85lpi.600dpi/85 lpi / 600 dpi: "45.0"
*ColorSepScreenAngle ProcessCyan.85lpi.600dpi/85 lpi / 600 dpi: "71.5651"
*ColorSepScreenAngle ProcessMagenta.85lpi.600dpi/85 lpi / 600 dpi: "18.4349"
*ColorSepScreenAngle ProcessYellow.85lpi.600dpi/85 lpi / 600 dpi: "0.0"

*ColorSepScreenFreq ProcessBlack.85lpi.600dpi/85 lpi / 600 dpi: "84.8528"
*ColorSepScreenFreq CustomColor.85lpi.600dpi/85 lpi / 600 dpi: "84.8528"
*ColorSepScreenFreq ProcessCyan.85lpi.600dpi/85 lpi / 600 dpi: "94.8683"
*ColorSepScreenFreq ProcessMagenta.85lpi.600dpi/85 lpi / 600 dpi: "94.8683"
*ColorSepScreenFreq ProcessYellow.85lpi.600dpi/85 lpi / 600 dpi: "30.0"
*ColorSepScreenProc ProcessYellow.85lpi.600dpi/85 lpi / 600 dpi: "
{1 add 2 div 3 mul dup floor sub 2 mul 1 sub exch
1 add 2 div 3 mul dup floor sub 2 mul 1 sub exch
abs exch abs 2 copy add 1 gt {1 sub dup mul exch 1 sub dup mul add 1
sub }{dup mul exch dup mul add 1 exch sub }ifelse }"
*End

*%  For 106 lpi /300 dpi  =========================
*ColorSepScreenAngle ProcessBlack.106lpi.300dpi/106 lpi /300 dpi: "45.0"
*ColorSepScreenAngle CustomColor.106lpi.300dpi/106 lpi /300 dpi: "45.0"
*ColorSepScreenAngle ProcessCyan.106lpi.300dpi/106 lpi /300 dpi: "71.5651"
*ColorSepScreenAngle ProcessMagenta.106lpi.300dpi/106 lpi /300 dpi: "18.4349"
*ColorSepScreenAngle ProcessYellow.106lpi.300dpi/106 lpi /300 dpi: "0.0"

*ColorSepScreenFreq ProcessBlack.106lpi.300dpi/106 lpi /300 dpi: "106.066"
*ColorSepScreenFreq CustomColor.106lpi.300dpi/106 lpi /300 dpi: "106.066"
*ColorSepScreenFreq ProcessCyan.106lpi.300dpi/106 lpi /300 dpi: "94.8683"
*ColorSepScreenFreq ProcessMagenta.106lpi.300dpi/106 lpi /300 dpi: "94.8683"
*ColorSepScreenFreq ProcessYellow.106lpi.300dpi/106 lpi /300 dpi: "100.0"

*%  For 106 lpi /600 dpi  =========================

*ColorSepScreenAngle ProcessBlack.106lpi.600dpi/106 lpi /600 dpi: "45.0"
*ColorSepScreenAngle CustomColor.106lpi.600dpi/106 lpi /600 dpi: "45.0"
*ColorSepScreenAngle ProcessCyan.106lpi.600dpi/106 lpi /600 dpi: "71.5651"
*ColorSepScreenAngle ProcessMagenta.106lpi.600dpi/106 lpi /600 dpi: "18.4349"
*ColorSepScreenAngle ProcessYellow.106lpi.600dpi/106 lpi /600 dpi: "0.0"

*ColorSepScreenFreq ProcessBlack.106lpi.600dpi/106 lpi /600 dpi: "106.066"
*ColorSepScreenFreq CustomColor.106lpi.600dpi/106 lpi /600 dpi: "106.066"
*ColorSepScreenFreq ProcessCyan.106lpi.600dpi/106 lpi /600 dpi: "94.8683"
*ColorSepScreenFreq ProcessMagenta.106lpi.600dpi/106 lpi /600 dpi: "94.8683"
*ColorSepScreenFreq ProcessYellow.106lpi.600dpi/106 lpi /600 dpi: "100.0"

*%=================================================
*%		 Font Information
*%=================================================
*DefaultFont: Courier
*Font AvantGarde-Book: Standard "(001.006S)" Standard ROM
*Font AvantGarde-BookOblique: Standard "(001.006S)" Standard ROM
*Font AvantGarde-Demi: Standard "(001.007S)" Standard ROM
*Font AvantGarde-DemiOblique: Standard "(001.007S)" Standard ROM
*Font Bookman-Demi: Standard "(001.004S)" Standard ROM
*Font Bookman-DemiItalic: Standard "(001.004S)" Standard ROM
*Font Bookman-Light: Standard "(001.004S)" Standard ROM
*Font Bookman-LightItalic: Standard "(001.004S)" Standard ROM
*Font Courier: Standard "(002.004S)" Standard ROM
*Font Courier-Bold: Standard "(002.004S)" Standard ROM
*Font Courier-BoldOblique: Standard "(002.004S)" Standard ROM
*Font Courier-Oblique: Standard "(002.004S)" Standard ROM
*Font Helvetica: Standard "(001.006S)" Standard ROM
*Font Helvetica-Bold: Standard "(001.007S)" Standard ROM
*Font Helvetica-BoldOblique: Standard "(001.007S)" Standard ROM
*Font Helvetica-Narrow: Standard "(001.006S)" Standard ROM
*Font Helvetica-Narrow-Bold: Standard "(001.007S)" Standard ROM
*Font Helvetica-Narrow-BoldOblique: Standard "(001.007S)" Standard ROM
*Font Helvetica-Narrow-Oblique: Standard "(001.006S)" Standard ROM
*Font Helvetica-Oblique: Standard "(001.006S)" Standard ROM
*Font NewCenturySchlbk-Bold: Standard "(001.009S)" Standard ROM
*Font NewCenturySchlbk-BoldItalic: Standard "(001.007S)" Standard ROM
*Font NewCenturySchlbk-Italic: Standard "(001.006S)" Standard ROM
*Font NewCenturySchlbk-Roman: Standard "(001.007S)" Standard ROM
*Font Palatino-Bold: Standard "(001.005S)" Standard ROM
*Font Palatino-BoldItalic: Standard "(001.005S)" Standard ROM
*Font Palatino-Italic: Standard "(001.005S)" Standard ROM
*Font Palatino-Roman: Standard "(001.005S)" Standard ROM
*Font Symbol: Special "(001.007S)" Special ROM
*Font Times-Bold: Standard "(001.007S)" Standard ROM
*Font Times-BoldItalic: Standard "(001.009S)" Standard ROM
*Font Times-Italic: Standard "(001.007S)" Standard ROM
*Font Times-Roman: Standard "(001.007S)" Standard ROM
*Font ZapfChancery-MediumItalic: Standard "(001.007S)" Standard ROM
*Font ZapfDingbats: Special "(001.004S)" Special ROM
*Font Albertus-ExtraBold: Standard "(001.008S)" Standard ROM
*Font Albertus-Medium: Standard "(001.008S)" Standard ROM
*Font AntiqueOlive: Standard "(001.008S)" Standard ROM
*Font AntiqueOlive-Bold: Standard "(001.008S)" Standard ROM
*Font AntiqueOlive-Italic: Standard "(001.008S)" Standard ROM
*Font Arial: Standard "(001.008S)" Standard ROM
*Font Arial-Bold: Standard "(001.008S)" Standard ROM
*Font Arial-BoldItalic: Standard "(001.008S)" Standard ROM
*Font Arial-Italic: Standard "(001.008S)" Standard ROM
*Font CGOmega: Standard "(001.008S)" Standard ROM
*Font CGOmega-Bold: Standard "(001.008S)" Standard ROM
*Font CGOmega-BoldItalic: Standard "(001.008S)" Standard ROM
*Font CGOmega-Italic: Standard "(001.008S)" Standard ROM
*Font CGTimes: Standard "(001.008S)" Standard ROM
*Font CGTimes-Bold: Standard "(001.008S)" Standard ROM
*Font CGTimes-BoldItalic: Standard "(001.008S)" Standard ROM
*Font CGTimes-Italic: Standard "(001.008S)" Standard ROM
*Font Clarendon-Condensed-Bold: Standard "(001.008S)" Standard ROM
*Font Coronet: Standard "(001.008S)" Standard ROM
*Font CourierHP: Standard "(001.008S)" Standard ROM
*Font CourierHP-Bold: Standard "(001.008S)" Standard ROM
*Font CourierHP-BoldItalic: Standard "(001.008S)" Standard ROM
*Font CourierHP-Italic: Standard "(001.008S)" Standard ROM
*Font Garamond-Antiqua: Standard "(001.008S)" Standard ROM
*Font Garamond-Halbfett: Standard "(001.008S)" Standard ROM
*Font Garamond-Kursiv: Standard "(001.008S)" Standard ROM
*Font Garamond-KursivHalbfett: Standard "(001.008S)" Standard ROM
*Font LetterGothic: Standard "(001.008S)" Standard ROM
*Font LetterGothic-Bold: Standard "(001.008S)" Standard ROM
*Font LetterGothic-Italic: Standard "(001.008S)" Standard ROM
*Font Marigold: Standard "(001.008S)" Standard ROM
*Font SymbolMT: Standard "(001.008S)" Standard ROM
*Font TimesNewRoman: Standard "(001.008S)" Standard ROM
*Font TimesNewRoman-Bold: Standard "(001.008S)" Standard ROM
*Font TimesNewRoman-BoldItalic: Standard "(001.008S)" Standard ROM
*Font TimesNewRoman-Italic: Standard "(001.008S)" Standard ROM
*Font Univers-Bold: Standard "(001.008S)" Standard ROM
*Font Univers-BoldItalic: Standard "(001.008S)" Standard ROM
*Font Univers-Condensed-Bold: Standard "(001.008S)" Standard ROM
*Font Univers-Condensed-BoldItalic: Standard "(001.008S)" Standard ROM
*Font Univers-Condensed-Medium: Standard "(001.008S)" Standard ROM
*Font Univers-Condensed-MediumItalic: Standard "(001.008S)" Standard ROM
*Font Univers-Medium: Standard "(001.008S)" Standard ROM
*Font Univers-MediumItalic: Standard "(001.008S)" Standard ROM
*Font Wingdings-Regular: Standard "(001.008S)" Standard ROM
*?FontQuery: "
   save
   { count 1 gt
      { exch dup 127 string cvs (/) print print (:) print
      /Font resourcestatus {pop pop (Yes)} {(No)} ifelse =
      } { exit } ifelse
   } bind loop
   (*) = flush
   restore
"
*End

*?FontList: "
   save
     (*) {cvn ==} 128 string /Font resourceforall
     (*) = flush
   restore
"
*End

*%=================================================
*%		 Printer Messages (verbatim from printer):
*%=================================================
*Message: "%%[ exitserver: permanent state may be changed ]%%"
*Message: "%%[ Flushing: rest of job (to end-of-file) will be ignored ]%%"
*Message: "\FontName\ not found, using Courier"

*% Status (format: %%[ status: <one of these> ] %%)
*Status: "warming up"/warming up
*Status: "idle"/idle
*Status: "busy"/busy
*Status: "waiting"/waiting
*Status: "printing"/printing
*Status: "initializing"/initializing
*Status: "printing test page"/printing test page
*Status: "PrinterError: cover open or no toner cartridge"/cover open or no toner cartridge
*Status: "PrinterError: cover open"/cover open
*Status: "PrinterError: needs attention"/needs attention
*Status: "PrinterError: no toner cartridge"/no toner cartridge
*Status: "PrinterError: warming up"/warming up
*Status: "PrinterError: manual feed"/manual feed
*Status: "PrinterError: out of paper"/out of paper
*Status: "PrinterError: Paper Jam"/Paper Jam
*Status: "PrinterError: paper jam"/paper jam
*Status: "PrinterError: page protect needed"/page protect needed
*Status: "PrinterError: out of memory"/out of memory
*Status: "PrinterError: output bin full"/output bin full
*Status: "PrinterError: resetting printer"/resetting printer
*Status: "PrinterError: toner is low"/toner is low
*Status: "PrinterError: off line"/off line

*% Printer Error (format: %%[ PrinterError: <one of these> ]%%)
*PrinterError: "cover open or no toner cartridge"/cover open or no toner cartridge
*PrinterError: "cover open"/cover open
*PrinterError: "needs attention"/needs attention
*PrinterError: "no toner cartridge"/no toner cartridge
*PrinterError: "warming up"/warming up
*PrinterError: "manual feed"/manual feed
*PrinterError: "out of paper"/out of paper
*PrinterError: "Paper Jam"/Paper Jam
*PrinterError: "paper jam"/paper jam
*PrinterError: "page protect needed"/page protect needed
*PrinterError: "out of memory"/out of memory
*PrinterError: "output bin full"/output bin full
*PrinterError: "resetting printer"/resetting printer
*PrinterError: "toner is low"/toner is low
*PrinterError: "off line"/off line

*% Input Sources (format: %%[ status: <stat>; source: <one of these> ]%% )
*Source: "BiTronics"/BiTronics
*Source: "other I/O"/other I/O
*Source: "AppleTalk"/AppleTalk
*Source: "APPLETALK"/AppleTalk
*Source: "ATALK"/AppleTalk
*Source: "LocalTalk"/LocalTalk
*Source: "Parallel"/Parallel
*Source: "EtherTalk"/EtherTalk
*Source: "NOVELL"/NOVELL
*Source: "DLC/LLC"/DLC/LLC
*Source: "ETALK"/EtherTalk
*Source: "TCP/IP"/TCP/IP

*Password: "()"
*ExitServer: "
 count 0 eq
 { false } { true exch startjob } ifelse
 not {
     (WARNING: Cannot modify initial VM.) =
     (Missing or invalid password.) =
     (Please contact the author of this software.) = flush quit
     } if
"
*End
*Reset: "
  count 0 eq { false } { true exch startjob } ifelse
  not {
    (WARNING: Cannot reset printer.) =
    (Missing or invalid password.) =
    (Please contact the author of this software.) = flush quit
    } if
  systemdict /quit get exec
  (WARNING : Printer Reset Failed.) = flush
"
*End

*% =======================================
*% For HP LaserJet 8150 Series
*% =======================================
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_CUPS_PPD_HP8150ENG_PPD)

	commands = [

	    POST.CMD_CHMOD + ' 644 '       + POST.FILE_ETC_CUPS_PPD_HP8150ENG_PPD,
	    POST.CMD_CHOWN + ' root.root ' + POST.FILE_ETC_CUPS_PPD_HP8150ENG_PPD,

	    ]

	for command in commands:

	    self.runCommand(command)

	###########################################################################
	# -rw------- root/lp         333 2008-07-10 10:53:28 etc/cups/printers.conf
	###########################################################################

	f = file(POST.FILE_ETC_CUPS_PRINTERS_CONF,'w')
	f.write('''# Printer configuration file for CUPS v1.2.4
# Written by cupsd on 2008-07-10 10:53
<DefaultPrinter hp8150eng>
Info
Location Bldg3
DeviceURI socket://192.168.2.5:9100
State Idle
StateTime 1215700546
Accepting Yes
Shared Yes
JobSheets none none
QuotaPeriod 0
PageLimit 0
KLimit 0
OpPolicy default
ErrorPolicy stop-printer
</Printer>
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_CUPS_PRINTERS_CONF)

	commands = [
	
	    POST.CMD_CHMOD + ' 600 '     + POST.FILE_ETC_CUPS_PRINTERS_CONF,
	    POST.CMD_CHOWN + ' root.lp ' + POST.FILE_ETC_CUPS_PRINTERS_CONF,

	    ]

	for command in commands:

	    self.runCommand(command)

	##########################################################################
	# -rw------- root/lp          82 2008-07-10 10:53:28 etc/cups/classes.conf
	##########################################################################

	f = file(POST.FILE_ETC_CUPS_CLASSES_CONF,'w')
	f.write('''# Class configuration file for CUPS v1.2.4
# Written by cupsd on 2008-07-10 10:53
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_CUPS_CLASSES_CONF)

	commands = [
	
	    POST.CMD_CHMOD + ' 600 '     + POST.FILE_ETC_CUPS_CLASSES_CONF,
	    POST.CMD_CHOWN + ' root.lp ' + POST.FILE_ETC_CUPS_CLASSES_CONF,

	    ]

	for command in commands:

	    self.runCommand(command)

	########################################################################
	# -rw-r----- root/lp        2472 2007-03-14 08:36:16 etc/cups/cupsd.conf
	########################################################################

	f = file(POST.FILE_ETC_CUPS_CUPSD_CONF,'w')
	f.write('''#
# "$Id: cupsd.conf.in 5454 2006-04-23 21:46:38Z mike $"
#
#   Sample configuration file for the Common UNIX Printing System (CUPS)
#   scheduler.  See "man cupsd.conf" for a complete description of this
#   file.
#
MaxLogSize 2000000000

# Log general information in error_log - change "info" to "debug" for
# troubleshooting...
LogLevel info

# Administrator user group...
SystemGroup sys root

# Only listen for connections from the local machine.
Listen localhost:631
Listen /var/run/cups/cups.sock

# Show shared printers on the local network.
Browsing On
BrowseOrder allow,deny
# (Change '@LOCAL' to 'ALL' if using directed broadcasts from another subnet.)
BrowseAllow @LOCAL

# Default authentication type, when authentication is required...
DefaultAuthType Basic

# Restrict access to the server...
<Location />
  Order allow,deny
  Allow localhost
</Location>

# Restrict access to the admin pages...
<Location /admin>
  Encryption Required
  Order allow,deny
  Allow localhost
</Location>

# Restrict access to configuration files...
<Location /admin/conf>
  AuthType Basic
  Require user @SYSTEM
  Order allow,deny
  Allow localhost
</Location>

# Set the default printer/job policies...
<Policy default>
  # Job-related operations must be done by the owner or an adminstrator...
  <Limit Send-Document Send-URI Hold-Job Release-Job Restart-Job Purge-Jobs Set-Job-Attributes Create-Job-Subscription Renew-Subscription Cancel-Subscription Get-Notifications Reprocess-Job Cancel-Current-Job Suspend-Current-Job Resume-Job CUPS-Move-Job>
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  # All administration operations require an adminstrator to authenticate...
  <Limit Pause-Printer Resume-Printer Set-Printer-Attributes Enable-Printer Disable-Printer Pause-Printer-After-Current-Job Hold-New-Jobs Release-Held-New-Jobs Deactivate-Printer Activate-Printer Restart-Printer Shutdown-Printer Startup-Printer Promote-Job Schedule-Job-After CUPS-Add-Printer CUPS-Delete-Printer CUPS-Add-Class CUPS-Delete-Class CUPS-Accept-Jobs CUPS-Reject-Jobs CUPS-Set-Default>
    AuthType Basic
    Require user @SYSTEM
    Order deny,allow
  </Limit>

  # Only the owner or an administrator can cancel or authenticate a job...
  <Limit Cancel-Job CUPS-Authenticate-Job>
    Require user @OWNER @SYSTEM
    Order deny,allow
  </Limit>

  <Limit All>
    Order deny,allow
  </Limit>
</Policy>

#
# End of "$Id: cupsd.conf.in 5454 2006-04-23 21:46:38Z mike $".
#
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_CUPS_CUPSD_CONF)

	commands = [
	
	    POST.CMD_CHMOD + ' 640 '     + POST.FILE_ETC_CUPS_CUPSD_CONF,
	    POST.CMD_CHOWN + ' root.lp ' + POST.FILE_ETC_CUPS_CUPSD_CONF,

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set VNC

    def setVNC(self):

	if not self.isDevConfig():

	    return

	self.runCommand(POST.CMD_LN + ' -f -s ../X11/xinit/xinitrc /etc/vnc/xstartup')

    #---------------------------------------------------------------------------
    # Set Yum Repositories

    def setYumRepos(self):

	if self.pre_isDerry:

	    # Create Derry repo's

	    f = file(POST.FILE_ETC_YUM_REPOS_D_CENTOS_BASE_REPO,'w')
	    f.write('''# CentOS-Base.repo
#
# This file uses a new mirrorlist system developed by Lance Davis for CentOS.
# The mirror system uses the connecting IP address of the client and the
# update status of each mirror to pick mirrors that are updated to and
# geographically close to the client.  You should use this for CentOS updates
# unless you are manually picking other mirrors.
#
# If the mirrorlist= does not work for you, as a fall back you can try the 
# remarked out baseurl= line instead.
#
#

[base]
name=CentOS-$releasever - Base
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=os
baseurl=http://xkickme.sweng.com/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5

#released updates 
[updates]
name=CentOS-$releasever - Updates
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=updates
baseurl=http://xkickme.sweng.com/centos/$releasever/updates/$basearch/
gpgcheck=1
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5

#packages used/produced in the build but not released
[addons]
name=CentOS-$releasever - Addons
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=addons
#baseurl=http://mirror.centos.org/centos/$releasever/addons/$basearch/
baseurl=http://xkickme.sweng.com/centos/$releasever/addons/$basearch/
gpgcheck=1
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5

#additional packages that may be useful
[extras]
name=CentOS-$releasever - Extras
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=extras
#baseurl=http://mirror.centos.org/centos/$releasever/extras/$basearch/
baseurl=http://xkickme.sweng.com/centos/$releasever/extras/$basearch/
gpgcheck=1
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5

#additional packages that extend functionality of existing packages
[centosplus]
name=CentOS-$releasever - Plus
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=centosplus
#baseurl=http://mirror.centos.org/centos/$releasever/centosplus/$basearch/
baseurl=http://xkickme.sweng.com/centos/$releasever/centosplus/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5

#contrib - packages by Centos Users
[contrib]
name=CentOS-$releasever - Contrib
# mirrorlist=http://mirrorlist.centos.org/?release=$releasever&arch=$basearch&repo=contrib
#baseurl=http://mirror.centos.org/centos/$releasever/contrib/$basearch/
baseurl=http://xkickme.sweng.com/centos/$releasever/contrib/$basearch/
gpgcheck=1
enabled=0
gpgkey=http://xkickme.sweng.com/centos/5/os/i386/RPM-GPG-KEY-CentOS-5
''')
	    f.close()
	    self.logger.info('Wrote ' + POST.FILE_ETC_YUM_REPOS_D_CENTOS_BASE_REPO)

	    if self.isFusionConfig():

		f = file(POST.FILE_ETC_YUM_REPOS_D_FUSION_REPO,'w')
		f.write('''[fusion-latest]
name=Safari Fusion - Latest Promoted Build
mirrorlist=http://xkickme.sweng.com/cgi-bin/fusion_latest_packages.pl
enabled=1
gpgcheck=0
[fusion-base]
name=Safari Fusion - Base Packages
baseurl=http://xkickme.sweng.com/fusion/$basearch/
enabled=1
gpgcheck=0
''')
		f.close()
		self.logger.info('Wrote ' + POST.FILE_ETC_YUM_REPOS_D_FUSION_REPO)

	    elif self.isViewConfig():

		f = file(POST.FILE_ETC_YUM_REPOS_D_VIEW_REPO,'w')
		f.write('''[view-latest]
name=Safari View - Latest Promoted Build
mirrorlist=http://xkickme.sweng.com/cgi-bin/view_latest_packages.pl
enabled=1
gpgcheck=0
[view-base]
name=Safari View - Base Packages
baseurl=http://xkickme.sweng.com/view/$basearch/
enabled=1
gpgcheck=0
''')
		f.close()
		self.logger.info('Wrote ' + POST.FILE_ETC_YUM_REPOS_D_VIEW_REPO)

	    else:

		f = file(POST.FILE_ETC_YUM_REPOS_D_SDE_REPO,'w')
		f.write('''[sde]
name=SDE
baseurl=http://xkickme.sweng.com/sde/global
enabled=1
[sdelocal]
name=SDE packages for $releasever
baseurl=http://xkickme.sweng.com/sde/$releasever
gpgcheck=0
enabled=1
''')
		f.close()
		self.logger.info('Wrote ' + POST.FILE_ETC_YUM_REPOS_D_SDE_REPO)

	else:

	    # Create a non-Derry repo

	    f = file(POST.FILE_ETC_YUM_REPOS_D_CENTOS_BASE_REPO,'w')
	    f.write('''TBD
''')

    #---------------------------------------------------------------------------
    # Set Exports

    def setExports(self):

	if not self.isDevConfig():

	    return

	self.runCommand(POST.CMD_SED + " -i.bak -e '/\/export[ \t]/d' " + POST.FILE_ETC_EXPORTS)

	f = file(POST.FILE_ETC_EXPORTS,'a')
	f.write(POST.DIR_EXPORT + '\t*(rw)\n')
	f.close()
	self.logger.info('Appended ' + POST.FILE_ETC_EXPORTS)

	commands = [

	    POST.CMD_MKDIR + ' -p '     + POST.DIR_EXPORT,
	    POST.CMD_CHOWN + ' 0:1003 ' + POST.DIR_EXPORT,	# 1003 is 'clearusers'
	    POST.CMD_CHMOD + ' 775 '    + POST.DIR_EXPORT,

	    POST.CMD_EXPORTFS + ' >/dev/null 2>&1',

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set network mounts

    def setNetMounts(self):

	if not self.isDevConfig():

	    return

	commands = [

	    POST.CMD_MV + ' /usr/local /usr/local.rpmsave',

	    POST.CMD_LN + ' -f -s /net/netstore/images      /images',
	    POST.CMD_LN + ' -f -s /net/netstore/tools/local /usr/local',
	    POST.CMD_LN + ' -f -s /net/netstore/tools       /tools',
	    POST.CMD_LN + ' -f -s /net/xview04/viewstore1   /viewstore1',
	    POST.CMD_LN + ' -f -s /net/xview04/viewstore2   /viewstore2',
	    POST.CMD_LN + ' -f -s /net/xview05/viewstore3   /viewstore3',
	    POST.CMD_LN + ' -f -s /net/xview05/viewstore4   /viewstore4',

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set /tftpboot mount

    def setTftpbootMount(self):

	if not self.isDevConfig():

	    return

	commands = [

	    POST.CMD_RM + ' -f -r /tftpboot',
	    POST.CMD_LN + ' -f -s /net/netstore/tftpboot /',

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Set Samba

    def setSamba(self):

	if not self.isDevConfig():

	    return

	f = file(POST.FILE_ETC_SAMBA_SMB_CONF,'w')
	f.write('''# This is the main Samba configuration file. You should read the
# smb.conf(5) manual page in order to understand the options listed
# here. Samba has a huge number of configurable options (perhaps too
# many!) most of which are not shown in this example
#
# Any line which starts with a ; (semi-colon) or a # (hash) 
# is a comment and is ignored. In this example we will use a #
# for commentry and a ; for parts of the config file that you
# may wish to enable
#
# NOTE: Whenever you modify this file you should run the command "testparm"
# to check that you have not made any basic syntactic errors. 
#
#======================= Global Settings =====================================
[global]
	log file = /var/log/samba/%m.log
	idmap gid = 10000-20000
	socket options = TCP_NODELAY SO_RCVBUF=8192 SO_SNDBUF=8192
	encrypt passwords = yes
	realm = cedarpointcom.com
	winbind use default domain = no
	template shell = /bin/false
	max xmit = 65535
	dns proxy = no 
	server string = 
	idmap uid = 10000-20000
	password server = 192.168.101.201
	workgroup = CEDARPOINTCOM
	os level = 20
	syslog = 0
	security = ads
	preferred master = no
	getwd cache = yes
	max log size = 50
	log level = 0

[export]
	force create mode = 775
	valid users = ccdoc,clearadm,clearcase_albd,@clearcase,@clearusers,@clearglobal
	writeable = yes
	create mode = 775
	path = /export
	force directory mode = 775
	directory mode = 775
[view]
	force create mode = 775
        valid users = ccdoc,clearadm,clearcase_albd,@clearcase,@clearusers,@clearglobal
        writeable = yes
        create mode = 775
        path = /view
        force directory mode = 775
        directory mode = 775
''')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_SAMBA_SMB_CONF)

    #---------------------------------------------------------------------------
    # Set environment variables

    def setEnvVars(self):

	#######################
	# Discover the JDK path
	#######################

	f = os.popen(POST.CMD_LS + ' -d ' + POST.FILE_USR_JAVA_JDK + '*')
	self.javaHome = f.readlines()[0].rstrip()
	f.close()

	##############################################
	# Create a profile for the Bourne-style shells
	##############################################

	f = file(POST.FILE_ETC_PROFILE_D_SAFARIFUSION_SH,'w')
	f.write('export JAVA_HOME=%s\n' % (self.javaHome))
	f.write('export  JAVAHOME=%s\n' % (self.javaHome))
	f.write('export PATH=${JAVA_HOME}/bin:${PATH}\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_PROFILE_D_SAFARIFUSION_SH)

	self.runCommand(POST.CMD_CHMOD + ' 755 ' + POST.FILE_ETC_PROFILE_D_SAFARIFUSION_SH)

	#########################################
	# Create a profile for the C-style shells
	#########################################

	f = file(POST.FILE_ETC_PROFILE_D_SAFARIFUSION_CSH,'w')
	f.write('setenv JAVA_HOME %s\n' % (self.javaHome))
	f.write('setenv  JAVAHOME %s\n' % (self.javaHome))
	f.write('set path = ( ${JAVA_HOME}/bin $path )\n')
	f.close()
	self.logger.info('Wrote ' + POST.FILE_ETC_PROFILE_D_SAFARIFUSION_CSH)

	self.runCommand(POST.CMD_CHMOD + ' 755 ' + POST.FILE_ETC_PROFILE_D_SAFARIFUSION_CSH)

    #---------------------------------------------------------------------------
    # Enable serial port login

    def enableSerialPortLogin(self):

	if self.isVMConfig():

	    return

	f = file(POST.FILE_ETC_INITTAB,'a')
	f.write('20:2345:respawn:/sbin/agetty -L ttyS0 115200 vt100\n')
	f.close()
	self.logger.info('Appended ' + POST.FILE_ETC_INITTAB)

	self.runCommand(POST.CMD_INIT + ' q')

	os.kill(1, signal.SIGHUP)

	self.logger.info('Did a "kill -s SIGHUP 1" using os.kill()')

    #---------------------------------------------------------------------------
    # Customizations for Virtual Machines

    def configVM(self):

	if not self.isVMConfig():

	    return

	commands = [

	    (POST.CMD_SED +
		" -i.bak -e '/kernel \/vmlinuz/s/$/ divider=10 notsc/' " +
		POST.FILE_BOOT_GRUB_GRUB_CONF),

	    ]

	for command in commands:

	    self.runCommand(command)

    #---------------------------------------------------------------------------
    # Setup MySQL
    #

    def setMySql(self):

	if not self.isFusionConfig():

	    return

	if ((self.pre_env != POST.ENV_VMFUSION)
	and (self.pre_env != POST.ENV_XBSFUSION)):

	    return

	#######################################################################
	#   For our Virtual Machine and Blade Server test environments, we wish
	# to allow 'root' logins from any remote host.
	#######################################################################

	sqlCommand = "grant all privileges on *.* to 'root'@'%' identified by 'passwd' with grant option;"

	command = (
	    POST.CMD_MYSQL_CLIENT +
	    ' --user=root' +
	    ' --password=passwd' +
	    ' --execute=' +
	    '"' +
	    sqlCommand +
	    '"')

	self.runCommand(command)

    #---------------------------------------------------------------------------
    # Customize the domain.xml for test platforms
    #
    #   For our Virtual Machine and Blade Server test environments, we wish to
    #   customize the domain.xml file.

    def setDomainXml(self):

	if not self.isFusionConfig():

	    return

	if ((self.pre_env != POST.ENV_VMFUSION)
	and (self.pre_env != POST.ENV_XBSFUSION)):

	    return

	commands = [

	    #-------------------------------------------------------------------
	    # Start the AppServer for our domain

	    (POST.CMD_ASADMIN +
		' start-domain' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' safariap' +
		' >/dev/null 2>&1'),

	    #-------------------------------------------------------------------
	    # Delete, then re-Create, an <auth-realm>

	    (POST.CMD_ASADMIN +
		' delete-auth-realm' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' imscore.net' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-auth-realm' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --classname com.sun.enterprise.security.auth.realm.jdbc.JDBCRealm' +
		' --property ' +
		    'assign-groups=imsusergroup:' +
		    'datasource-jndi=jdbc/Mysql_node1:' +
		    'db-password=passwd:' +
		    'db-user=root:' +
		    'debug=true:' +
		    'digest-algorithm=md5:' +
		    'encoding=HASHED:' +
		    'group-name-column=groupid:' +
		    'group-table=subscriber:' +
		    'jaas-context=jdbcDigestRealm:' +
		    'password-column=md5password:' +
		    'user-name-column=authusername:' +
		    'user-table=subscriber' +
		' imscore.net' +
		' >/dev/null 2>&1'),

	    #-------------------------------------------------------------------
	    # Delete, then re-Create, an <auth-trust-config>

	    (POST.CMD_ASADMIN +
		' delete-trust-config' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' trust-id_config' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-trust-config' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --isdefault=true' +
		' --trusthandler org.jvnet.glassfish.comms.security.auth.impl.TrustHandlerImpl' +
		' trust-id_config' +
		' >/dev/null 2>&1'),

	    #-------------------------------------------------------------------
	    # Delete, then re-Create, several <sip-listener>
	    #              one with a  nested <ssl>

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-1' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-5060' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --enabled=true' +
		' --siplisteneraddress=%s' % (self.pre_data) +
		' --siplistenerport=5060' +
		' --siplistenertype=default' +
		' --transport=udp_tcp' +
		' sip-listener-5060' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-2' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-5061' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --enabled=true' +
		' --siplisteneraddress=%s' % (self.pre_data) +
		' --siplistenerport=5061' +
		' --siplistenertype=default' +
		' --transport=udp_tcp' +
		' sip-listener-5061' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-ssl' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --certname=s1as' +
		' --clientauthenabled=false' +
		' --ssl2enabled=false' +
		' --ssl3enabled=false' +
		' --tlsenabled=true' +
		' --tlsrollbackenabled=true' +
		' --type=sip-listener' +
		' sip-listener-5061' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-4060' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --enabled=true' +
		' --externalsipaddress=%s' % (self.pre_data) +
		' --externalsipport=4060' +
		' --siplisteneraddress=%s' % (self.pre_data) +
		' --siplistenerport=4060' +
		' --siplistenertype=external' +
		' --transport=udp_tcp' +
		' sip-listener-4060' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' delete-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' sip-listener-6060' +
		' >/dev/null 2>&1'),

	    (POST.CMD_ASADMIN +
		' create-sip-listener' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' --enabled=true' +
		' --externalsipaddress=%s' % (self.pre_data) +
		' --externalsipport=6060' +
		' --siplisteneraddress=%s' % (self.pre_data) +
		' --siplistenerport=6060' +
		' --siplistenertype=external' +
		' --transport=udp_tcp' +
		' sip-listener-6060' +
		' >/dev/null 2>&1'),

	    #-------------------------------------------------------------------
	    # Stop the AppServer for our domain

	    (POST.CMD_ASADMIN +
		' stop-domain' +
		' safariap' +
		' >/dev/null 2>&1'),

	    #-------------------------------------------------------------------
	    # Start the AppServer for our domain

	    (POST.CMD_ASADMIN +
		' start-domain' +
		' --user admin' +
		' --passwordfile %s/safari/sailfin/sailfinpwd' % (self.DIR_SAFARI_INST) +
		' safariap' +
		' >/dev/null 2>&1'),

	    ]

	for command in commands:

	    self.runCommand(command)

#----------------------------------------------------------
# These values are passed from the %pre to the %post

    def setPreValues(self):
        self.pre_arch="x86_64"
        self.pre_data="172.16.150.123"
        self.pre_mgmt="dhcp"
        self.pre_cmdLine="initrd=initrd.img BOOT_IMAGE=vmlinuz ksdevice=eth0 ks=http://xkickme/rhel-5.5-x86_64.cfg xyzzy=private,vcs,hostname:xkstest.sweng.com,data:172.16.150.123"
        self.pre_critical="0"
        self.pre_device="eth0"
        self.pre_drives="['sda']"
        self.pre_env="field-fusion"
        self.pre_firewall="--enabled"
        self.pre_gateway0="172.16.0.254"
        self.pre_gateway1=""
        self.pre_hostname="xkstest.sweng.com"
        self.pre_isCorporate="False"
        self.pre_isDerry="False"
        self.pre_isPrivateRepo="True"
        self.pre_nameserver="172.16.0.7"
        self.pre_netmask0="255.255.0.0"
        self.pre_netmask1=""
        self.pre_osName="rhel"
        self.pre_osRel="5.5"
        self.pre_packages="['@Core', '@editors', '@ftp-server', '@mail-server', '@system-tools', 'FusionDomain', 'MySQL-client-community', 'OpenIPMI', 'OpenIPMI-libs', 'OpenIPMI-tools', 'VCS', 'bash', 'bind-utils', 'bzip2', 'compat-libstdc++-33-3.2.3', 'dos2unix', 'dosfstools', 'emacs', 'expect', 'ftp', 'gcc', 'gdb', 'kernel-devel', 'ksh', 'libuser', 'mailx', 'man', 'net-snmp-libs', 'ntp', 'openldap', 'openldap-clients', 'openldap-devel', 'openldap-servers', 'openldap-servers-sql', 'openssh-clients', 'openssh-server', 'redhat-release', 'sailfin', 'sas_snmp', 'snmpsa', 'strace', 'sysstat', 'system-config-date', 'tclx', 'tcpdump', 'tcsh', 'telnet', 'telnet-server', 'tftp', 'traceroute', 'unixODBC', 'vim-X11', 'vixie-cron', 'wireshark', 'wireshark-gnome', 'xterm', 'yum', 'zlib', 'zlib-devel', '-dovecot', '-mysql']"
        self.pre_products="['vcs']"
        self.pre_selinux="--permissive"
        self.pre_warn="0"

    #---------------------------------------------------------------------------
    # Main %post routine

    def post(self):

	self.makeDirectories()			# make required directories

	self.setHostname()			# set the hostname

	######################
	# Update files in /etc
	######################

	self.setHostsFile()
	self.setNameResolver()
	self.setNameServiceSwitchConf()
	self.setNTP()
	self.setAutomounter()
	self.setFSTab()
	self.setGDM()

	#######################
	# Update security files
	#######################

	self.setPAM()
	self.setSecureTTY()
	self.setSSH()
	self.setSudoers()
	self.setKerberos5()

	#######################
	# Update files in /root
	#######################

	self.setRootRhosts()
	self.SetRootSshAuthorizedKeys()

	################################
	# Update files in /etc/sysconfig
	################################

	self.setI18N()
	self.setNetworking()
	self.setIptables()

	####################
	# Configure services
	####################

	self.setServices()			# enable / disable services
	self.setPrinters()
	self.setVNC()
	self.setYumRepos()

	############################
	# Configure network services
	############################

	self.setExports()
	self.setNetMounts()
	self.setTftpbootMount()
	self.setSamba()

	########################
	# Configure SafariFusion
	########################

	self.setEnvVars()
	self.enableSerialPortLogin()

	#####################################
	# Customizations for Virtual Machines
	#####################################

	self.configVM()

	###################################
	# Customizations for test platforms
	###################################

	self.setMySql()
	self.setDomainXml()			# customize AppServer's domain.xml

	self.logger.info('%' + 'post script completed: %s warnings, %s critical errors' % (self.warn, self.critical))

#-------------------------------------------------------------------------------
# Start here for %post script

POST().post()

# End of %post script
