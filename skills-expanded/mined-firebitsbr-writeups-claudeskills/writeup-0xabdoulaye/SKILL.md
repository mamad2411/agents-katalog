<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xabdoulaye
description: CTF writeups and security challenges by 0xabdoulaye.
---

# Writeups by 0xabdoulaye

Source repository: `/repos/0xabdoulaye`

## Repository Index

- CyberTalents-Blue-Team-Scholarship-Writeups/README.md
- CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/Brut3Forc3.md
- CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/Missey.md
- CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/README.md
- CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/activeattack.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/README.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/WithIncode.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/YaraMagic.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/55H-Access/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Backdoor/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Bean-Detector/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Bean/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/CVE-Number/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Competition/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Creepy-DNS/README.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/FourOFour/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/MEGO/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Pass-Reset/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Phisher/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Remote-Hacker/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/SIEM-Port/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Smart-Role/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/USB-Case/Readme.md
- CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/WormSeen/README.md

## Writeup Content


### File: CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/README.md

- encode challenge:
first use capinfos ARP+Storm.pcap 
Number of pa
packets:   68
i used thsark 
tshark -r chall.pcap -Y arp 
also 
tshark -r ARP+Storm.pcap -Y "arp.dst.proto_ipv4 == 11.0.0.100" 
then i add 
tshark -r ARP+Storm.pcap -Y "arp.dst.proto_ipv4 == 11.0.0.100"  -T fields -e arp.opcode -E separator =, > encode.txt
make in one line and with spaces
sed ':a;N;$!ba;s/\n/ /g' encode.txt > enc0de.txt

i get these number and then  i made them in inline 
90 109 120 104 90 51 116 110 99 107 66 48 100 87 108 48 77 72 86 122 88 122 66 119 89 48 57 107 90 86 56 120 99 49 57 66 98 72 100 65 101 88 78 102 81 84 90 49 85 50 86 107 88 51 81 119 88 51 65 119 77 88 77 119 98 110 48 61 
decode it from decimal and i got 
ZmxhZ3tnckB0dWl0MHVzXzBwY09kZV8xc19BbHdAeXNfQTZ1U2VkX3QwX3AwMXMwbn0= 
base64 decode from terminale and got the flag.

- Refresher chall :
found many images then have extract them using wireshark
take first character of any 200 success images by writing a script name seded.py
then i got the 
iamsupersecretpasswordgood4uthefinding 

now look at the wireshark ftp you''
i see a zip file now extract it as raw 
now extract it using 7z x 
flag : flag{y0u_c0m3_f0r_fl1g_1nd_h3r3_1t_1s_2000}

worm challenge
crack zip and find .exe
i use pyinstxtractor to extract worm file 
foun
found worm.pyc it's interesting file
i think i need to convert that .pyc to .py 
found : https://acrosby.bitbucket.io/2018/06/28/pycdc/
extract it 
└─# ./pycdc /home/kali/Desktop/Learning/Bluteam/worm.exe_extracted/worm.pyc

flag : flag{192.168.1.0/24:22:85}

splunk
learning splunk
Splunk can be used as a single instance or as a distributed deployment. The latter would be a typical scenario for security usage in organizations, where data needs to be collected from multiple assets and sent to a centralized solution. 
SOC analysts need to make correlations and search the data, typically at different times and different physical locations.

Search Processing Language is a language designed by Splunk for use with Splunk software. It encompasses all the search commands and their functions, arguments, and clauses. 
Ressources: https://tryhackme.com/room/splunkexploringspl
Introduction to SIEM : https://tryhackme.com/room/introtosiem

SIEM stands for Security Information and Event Management system. It is a tool that collects data from various endpoints/network devices across the network, stores them at a centralized place, and performs correlation on them. This room will cover the basic concepts required to understand SIEM and how it works.
1) Host-Centric Log Sources

These are log sources that capture events that occurred within or related to the host. Some log sources that generate host-centric logs are Windows Event logs, Sysmon, Osquery, etc. Some examples of host-centric logs are:

    A user accessing a file
    A user attempting to authenticate.
    A process Execution Activity
    A process adding/editing/deleting a registry key or value.
    Powershell execution

    SOC Analyst Responsibilities

SOC Analysts utilize SIEM solutions in order to have better visibility of what is happening within the network. Some of their responsibilities include:

    Monitoring and Investigating.
    Identifying False positives.
    Tuning Rules which are causing the noise or False positives.
    Reporting and Compliance.
    Identifying blind spots in the network visibility and covering them.


    55H-access
    We observed a huge traffic towards our SSH Server 
X: How many source IPs attempting to connect  → Number
Y: The Source IP with the most connections → x.x.x.x
Z: The Source IP with the most connections country → xxxxxxx
W: The Firewall action taken from the security control → xxxxxxx
Flag format: flag{X:Y:Z:W}

search for ssh service in search filter it all time
then 
answer is 
X = src_ip = 19
Y = src_ip = top 10 : 91.224.160.108
Z = finland by googling the IPs  "https://iplocation.co.uk/ip-address/91.224.160.108"
W = blocked  : found on action value

flag{19:91.224.160.108:finland:blocked}

- FourOFour 
Massive web bruteforce attack observed on our IIS server, Your lead has informed you to initiate some investigation to identify the following :
X: The highest number of non existent URLs request sent by the attacker → Number
Y: The Source IP → x.x.x.x
Z: The attacker source country → xxx

first : IIS server all time
c_ip="40.80.148.42" sc_status="404"
X: 2009
Y = 40.80.148.42
Z = usa

flag{1315:40.80.148.42:usa} not work

x i think not correct


- usb case:
first i check provided link : https://lantern.splunk.com/Security/Use_Cases
search for usb
found : Removable devices connected to a machine

search query : sourcetype=winregistry friendlyname filter in all time

Expand the result and look at the registry_value_data field. 
X: Date and time when the USB plugged on device  (YYYY-MM-DD:HH:MM:SS)
Y: The Machine name 
Z: Name of the USB device
flag{2016-08-24:10:42:17:we8105desk:MIRANDA_PRI}


- Chall:  Remote Hacker
desc: 

Our SoC L1 reported that she received alert of suspicious login detected by company user “Kvasir” on 13/06/2022. 
Please do check and return by your analysis: 

X: Session Duration spent by the attacker on the system (HH:MM:SS) 

Y: The application used by the user after login (xxxx.exe) 

Z: Identify the SHA256 of this application W: Attacker IP address 
A: Attacker Machine host name 

transform it on xml 
evtxtract Microsoft-Windows-Sysmon_4Operational.evtx > Microsoft-Windows-Sysmon_4Operational.xml
INFO:root:recovered 20044 complete records
INFO:root:recovered 0 incomplete records

evtxtract Security.evtx > Security.xml  
INFO:root:recovered 6178 complete records
INFO:root:recovered 0 incomplete records

CTRL+F 
find 2022-06-13
<Computer>DESKTOP-9BBI1VE</Computer>
04:51:36s and 4:51:28. for kvasir
SearchIndexer.exe
autochk.exe
smss.exe
00:02:40
<Data Name="LogonType">3</Data>
<TimeCreated SystemTime="2022-06-05 13:03:18.636375"></TimeCreated>
<Data Name="IpAddress">192.168.1.58</Data>

</System>
<EventData><Data Name="RuleName">technique_id=T1204,technique_name=User Execution</Data>
<Data Name="UtcTime">2022-06-13 05:03:21.855</Data>
<Data Name="ProcessGuid">{9beb5cef-c519-62a6-1301-000000000b00}</Data>
<Data Name="ProcessId">5172</Data>
<Data Name="Image">C:\Windows\System32\win32calc.exe</Data>
<Data Name="FileVersion">10.0.17763.1 (WinBuild.160101.0800)</Data>
<Data Name="Description">Windows Calculator</Data>
<Data Name="Product">Microsoft&#174; Windows&#174; Operating System</Data>
<Data Name="Company">Microsoft Corporation</Data>
<Data Name="OriginalFileName">WIN32CALC.EXE</Data>
<Data Name="CommandLine">"C:\Windows\system32\win32calc.exe" </Data>
<Data Name="CurrentDirectory">C:\Windows\system32\</Data>
<Data Name="User">DESKTOP-9BBI1VE\kvasir</Data>
<Data Name="LogonGuid">{9beb5cef-c2f9-62a6-0c6e-040000000000}</Data>
<Data Name="LogonId">0x0000000000046e0c</Data>
<Data Name="TerminalSessionId">1</Data>
<Data Name="IntegrityLevel">High</Data>
<Data Name="Hashes">SHA1=EC73FCAB989C8D525FE3BBCC3736BC3E6192A112,MD5=46CDCA3D2EB9B837EC3C4CDA60D0D0D9,SHA256=3E2300394C15B59A964EAB45D9EB96D317650E2F7448FD1B4AE825A134402B7A,IMPHASH=BDE48881DABC2774907583E3DE072A63</Data>
<Data Name="ParentProcessGuid">{9beb5cef-c2fb-62a6-3b00-000000000b00}</Data>

flag{05:03:21:win32calc.exe:3E2300394C15B59A964EAB45D9EB96D317650E2F7448FD1B4AE825A134402B7A:192.168.1.58:Nitro}
flag{00:02:40:win32calc.exe:3E2300394C15B59A964EAB45D9EB96D317650E2F7448FD1B4AE825A134402B7A:192.168.1.58:Nitro}


chall yara Magic and WithIn Code:
YARA is the name of a tool primarily used in malware research and detection. It provides a rule-based approach to create descriptions of malware families based on textual or binary patterns
Yara Use Cases:

1. Identify Malware samples.

2. Detect Malware infection

3. Perform Incident Response and Threat Hunting activities.

- For yara first challenge :
https://support.knowbe4.com/hc/en-us/articles/360013116053-How-to-Write-YARA-Rules
I run ls:
root@nenandjabhata:/home/files/Yara Magic# ls
Folder  rule2.yara  rule.yara
i found a yara rule .
now i execute it
root@nenandjabhata:/home/files/Yara Magic# yara -f rule.yara Folder/
MySuperCoolRule Folder//12776

- Within code challenge:
I write a rule 
Flag into base64 RmxhZw= and base64 to hex 526d78685a773d3d
root@nenandjabhata:/home/files# cat rule.yara 
rule Finder
{
    strings:

            $encode = "RmxhZw=="
            $hex = "526d78685a773d3d"

        condition:
            $encode or $hex
}
root@nenandjabhata:/home/files#
when i execute it i find : root@nenandjabhata:/home/files# yara -f rule.yara Code
Finder Code/6645
 we’re going to use the -s option which will give us the offset location of the string in the matched file (for more
explanation about the Yara options use the command ($yara - - help) 
root@nenandjabhata:/home/files# yara -s -f rule.yara Code
Finder Code/6645
0x2460:$encode: RmxhZw==
we need now to decode the 0x2460 into decimal and we got 9312 as flag

- Powershell Hunting:
1. What is Powershell?
2. Powershell Hunting Commands
3. Baselines
4. Hunting Web Shells
5. Powershell Hunting Tools
6. Hunting Windows Processes

Compare :
Comparing Baselines

    $baseline = Get-Content .\baseline-services.txt
    $current = Get-Content .\current-services.txt
    Compare-Object $baseline $current
Arson:
a pcap file
i opened it using wireshark and i follwed tcp stream by http request 
i find : a powershell script in hots.ps1 
i save it as
i found this : $key = "llm0xB8WOfv9Ssq9+f0sIMFK6OyQHOzhdenMzRInqXA="
$ip = "192.168.1.11"
$port = "7788"
$implant_name = "razer"
$sleep_time = 5

i think it's a cipher AES and i found his key
i continued in the response of that request and i found this :
result=irbYP4XxfwuTlCbMxv4CE9KdquYNczFCMziT5VTG6aS%2B%2BMDZiChw3YJbtbrvt4FKO2WmdKwVBqjdX4xDguV7slrxsNNLqVbSOCceAURzkhNDvaMOIg8a0tPx3G7U%2BPUH
here is an url encryption i need to decode it : irbYP4XxfwuTlCbMxv4CE9KdquYNczFCMziT5VTG6aS++MDZiChw3YJbtbrvt4FKO2WmdKwVBqjdX4xDguV7slrxsNNLqVbSOCceAURzkhNDvaMOIg8a0tPx3G7U+PUH
This not work for our powershell script
clean all function in the script; i need decryption function:
i found this last which have razer in his post : IN3DZMA9y5D0q5y4Pe3Uv%2FVE3mA4EZY55XHJJIdLc29WAK73bE2DzB7ae%2Fmpy4CW
decode url : IN3DZMA9y5D0q5y4Pe3Uv/VE3mA4EZY55XHJJIdLc29WAK73bE2DzB7ae/mpy4CW
when i execute the powershell script i found :
 flag{2C_p0w3r_Chi11}

- Wireshark: Exodus challenge
Using http filter i get the key GET /?KEY=STAR
Now i filter icmp and i got data values :
from hex i xor these value using cyberchef and key STAR
and then from base64 i decode and find zip file 

What will you learn?
1- What is Security Onion
2- Security Onion Use Cases
3- Security Onion Platform
4- Security Onion Workflows
5- Deploying Security Onion
6- Security Onion Console
7- Security Onion Network Visibility
8- Security Onion Host Visibility
What is Security Onion?

Security Onion is a free and open platform for threat hunting, enterprise security monitoring, and log management. It includes our own tools for Alerts, Dashboards, Hunt, PCAP, and Cases as well as other tools such as Playbook, FleetDM, osquery, CyberChef, Elasticsearch, Logstash, Kibana, Suricata, Zeek, and Wazuh.
Security Onion Platform
Analysis Tools

    SOC
    Kibana
    CyberChef

Network and Host Tools
    Wazuh
    Suricata
    Zeek

Infrastructure
    Docker
    Redis
    Salt
Operating System

    Ubunto
    CentOS

    Filebeat -  Used to collect Log files and send them to logstash.
    Logstach – Used to aggregate logs.
    Redis – In memory Storage for the query for fast retrieval of the logstash.
    Elasticsearch – Indexing and Storage of logs.
    Curator – for managing Elasticsearch indexing.
Security Onion Host Visibility

Host logs can be sent to Security Onion through:

    Wazuh EDR
    Syslog
    Osquery
    Beats
    Sysmon

What will you learn?
1. Window Processes
2. Famous Windows Processes
3. Hunting Tips

Windows is the most targeted operating system by attackers, and various types of processes run in Windows, including the operating system processes and different applications processes, as a threat hunter you need to know windows processes to be able to locate abnormal behavior.
smss.exe

Responsible for starting user sessions. This process is started by the main system thread and is responsible for various activities such as starting Winlogon and Win32 (Csrss.exe) processes and setting system variables.

    Image Path: %SystemRoot%\System32\smss.exe
    Parent Process: System
    Session 0 starts csrss.exe and wininet.exe and session 1 starts csrss.exe for the user and winlogon.exe.
Mandiant RedLine

Mandiant Redline is a free tool that provides host investigative capabilities to users and uncovers signs of malicious activity through memory and file analysis to develop a threat assessment profile.

Hunting Tips:

    The most targeted process from malware authors is svchost.exe because it has multiple instances hence malware running as svchost.exe can be easily undetected.
    Malware authors tend to use a name similar to windows processes and misspell it such as:

- 1sass.exe

- svchot.exe

- cssrss.exe

    Always check the image path of the process that you suspect.
    Some malware authors use process injection techniques to inject their code inside legitimate process, you can detect process injection by checking the memory for the processes for any READ_WRITE_EXECUTE sections.

- W4nna Fl4g challenge
i use volatility 
scan pslist









Hunting Windows Events
Hunting Windows Event IDs
Hunting Accounts:

    4720: Account created
    4722: Account Enabled
    4724: reset password
    4728: user added to global group
    4756: user added to universal group

Logon Types
2
Physical login to the computer
3
A login from the network
4
Used by batch servers
5
A service started by the SCM
7
The workstation was unlocked
8
Network credentials were sent in cleartext
9
A caller specified new creds
10
A user logged in using terminal service or RDP
11
A user logged in using stored network credentials


Hunting Password Attacks

    4625: failed login.
    Logon Type 3: Network login.
Hunting Scheduled Tasks and Services

    4698: a scheduled task was created.
    200, 201: Task Monitoring and Control.
    4697: a service was installed in the system
Hunting RDP Sessions:

    4624: An account was successfully logged on.
    4778: A session was reconnected to a Window Station.

Scanner challenge
Our web server at 192.168.250.20 is being scanned by a famous vulnerability scanner, can you investigate the logs and tell us: 

    X: the vulnerability scanner name
    Y: The Source IP → x.x.x.x

Flag format: flag{X:Y}

Credentials: cybertalents/cybertalents 

I use this on splunk : 192.168.250.20 
| stats count by http_user_agent
found : Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0) 961
Nessus  36 and i now nessus is a vulnerability scanner.
I load it to see the src_ip and i found 192.168.2.50 and this 192.168.250.20
flag{Nessus:192.168.2.50} and it's correct

New account 
an attacker after compromising the machine added a new account as admin. can you find the name of the new account? 
flag format : flag{md5 of string} 

using evtxtract to extract it to xml
└─# python3 /root/environment/myenv/bin/evtxtract Security436509324654726509.evtx > security.xml

Now for hunting account we need : Hunting Accounts:

    4720: Account created
    4722: Account Enabled
    4724: reset password
    4728: user added to global group
    4756: user added to universal group

so we found <EventID Qualifiers="">4720</EventID>
and the name <EventData><Data Name="TargetUserName">Sam</Data>
we need to make this name as md5
I use md5hash generator
flag{ba0e0cde1bf72c28d435c89a66afc61a}


### File: CyberTalents-Blue-Team-Scholarship-Writeups/README.md

# CyberTalents Blue Team Scholarship Writeups

Hey there! During my three-month learning journey, I'll be diving into the exciting world of cybersecurity with CyberTalents. I'll be taking two advanced courses on their platform, where I'll gain hands-on experience and learn from some of the best instructors in the field.

The first course is called "CyberTalents Certified SOC Analyst," where I'll be honing my skills in handling security incidents and managing a Security Operations Center (SOC). It's all about detecting and responding to cyber threats effectively.

The second course, "CyberTalents Certified Threat Hunter," sounds even more thrilling! I'll be learning the art of proactive hunting for cyber threats, seeking out those sneaky adversaries before they can cause any harm.

I can't wait to explore these courses, take on challenges, and share my progress with you all. Join me on this cybersecurity adventure, and together, we'll become skilled defenders of the digital world! Let's go! 🚀💻🔒

follow me on my Hacking Journey blog here : https://blackcybersec.xyz


## Certified SOC ANALYST

| Challenges | Difficulty |                                                Tags                                                | Completed |
|:-------------:|:----------:|:--------------------------------------------------------------------------------------------------:|:---------:|
|               |            |                                                                                                    |           |
|     [CVE-Number](./Soc-analyst/CVE-Number/Readme.md)      |    Basic    |                                       EternalBlue, Searchsploit                                       | Completed |
|   [Backdoor](./Soc-analyst/Backdoor/Readme.md)   |   Medium   |                                            Tshark, Wireshark, vsFTPD                                            |        Completed   |
|    [Bean Detector](./Soc-analyst/Bean-Detector/Readme.md)    |    Medium    |                                 Log analysis, Forensic, Web                               | Completed |
|     Bean    |    Easy    |                                     LFI, Web                                     | Completed |
|    55H-Access    |    Easy    |                              Splunk, Forensic, SSH                             |  Completed|
|      [Competition](./Soc-analyst/Competition/Readme.md)     |    Basic    |                                 CTF, Hacking, Google                                  | Completed |
|     [Creepy-DNS](./Soc-analyst/Creepy-DNS/README.md)    |   Easy   |                               DNS, DNS Zone Transfer, Google                              |      Completed     |
|    FourOFour    |   Easy   |                                   Splunk,  Log, IIS Server,Microsoft                                   |      Completed     |
|     MEGO     |    Medium    |                                       Forensic, Volatility, Disc                                      | Completed |
|   Pass-Reset  |   Easy   |                                     File Misconfiguration, Web                                     |       Completed    |
|    Phisher    |    Medium    |                                     Foresic, Disc, Volatility                                     |        Completed   |
|      [Remote Hacker](./Soc-analyst/Remote-Hacker/Readme.md)     |   Medium   |                           Forensic, Logs Analysis, Windows logs                          |   Completed        |
|   [SIEM Port](./Soc-analyst/SIEM-Port/Readme.md)   |    Basic    |                                        SIEM, TLS                                       | Completed |
|     [Smart-Role](./Soc-analyst/Smart-Role/Readme.md)    |   Basic   |                                 Soc, CTI, Analyst                                 |         Completed  |
|     USB-Case    |    Easy    |                                   Splunk, USB Device                                   | Completed          |
|  [WormSeen](./Soc-analyst/WormSeen/README.md) |   Medium   |                                     Exe Analysis, Forensic, Python                                    |       Completed    |


## Certified Threat Hunter

| Challenges | Difficulty |                                                Tags                                                | Completed |
|:-------------:|:----------:|:--------------------------------------------------------------------------------------------------:|:---------:|
|               |            |                                                                                                    |           |
|     [APT](./Threat-hunter)      |    Easy    |                                       Hacking groups,  OSINT                                     | Completed |
|   [Kill Chain](./Threat-hunter)   |   Basic   |                                            Mittre attack                                            |        Completed   |
|    [CTI Analyst](./Threat-hunter)    |    Easy    |                                Malware hash                               | Completed |
|     [Yara Magic](./Threat-hunter/YaraMagic.md)    |    Easy    |                                     yara, rules, Basic                                     | Completed |
|    [Within Code](./Threat-hunter/WithIncode.md)    |    Medium    |                              yara, rules, conditions, strings                             |  Completed|
|      [Falcon Hunt](./Threat-hunter)     |    Medium    |                                 hunting,                                   | Completed |
|     Enc0de   |   Easy   |                               Arp, network analysis                              |      Completed     |
|    Refresher    |   Medium   |                                   Wireshark hunting                                   |      Completed     |
|     Ex0dus     |    Medium    |                                       Forensic, Wireshark, ICMP                                      | Completed |
|   Missey  |   Easy   |                                     Wireshark,                                     |       Completed    |
|    Baseline    |    Easy    |                                     Powershell, Hunting                                     |        Completed   |
|      [Arson](./Threat-hunter)     |   Medium   |                           Powershell, Ps1, Wireshark                          |   Completed        |
|   [Process](./Threat-hunter)   |    Basic    |                                        Windows, Process                                     | Completed |
|     [W4nna-Flag](./Threat-hunter)    |   Medium   |                                 Forensic, Volatility                                 |         Completed  |
|     Masqur4d3    |    Medium    |                                   Memory                                   | Completed          |
|  Scanner |   Easy   |                                     Logs Analysis, Attacker                                   |       Completed    |
|   [New account](./Threat-hunter)   |    Easy    |                Completed                                                             | Completed |
|     [Active Attacks](./Threat-hunter)    |   Medium   |            Completed                                                      |         Completed  |
|     Brut3 Forc3    |    Medium    |                                   Completed                                   | Completed          |



### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Creepy-DNS/README.md

Our NMS detect a suspected traffic, your task is to investigate the captured traffic and find the anomaly reason

# solution

i have used tshark to see what's on the dns 
`└─# tshark -Y 'dns' -r dns.pcapng`
in the dns, i see like subdomains,
```
m.cybertalents.com
Z.cybertalents.com
```
i think i need to fetch these first char on the dns. now i will ask GPT
i make the dns on a file, then i just used :
`└─# cat dns.output | grep -E '\b[a-zA-Z0-9_-]+\.cybertalents\.com\b' | awk '{print $12}'  | tee -a output2.txt`
Now i will use sublime text to remove all char i don't want.

remove spaces: `sed -i '/^[[:space:]]*$/d' output2.txt`

Now i have Repeated character i will remove them:
it's like this 
`ZZmmxxhhZZ33tt00cc22hhBBccmmttffSSXXNNffQQXXddllcczzBBttZZVV99OOZZXXRR33MMHHJJrraaWW55nnXX33RRvvMMGGxx99`
Now i make a small script:
```python
with open('output2_single_line.txt', 'r') as file:
    content = file.read()

unique_content = ''.join(char for i, char in enumerate(content) if char != content[i - 1])

with open('output2_single_line_cleaned.txt', 'w') as file:
    file.write(unique_content)

```

Now when i open the ouput: `└─# cat output2_single_line_cleaned.txt 
ZmxhZ3t0c2hBcmtfSXNfQXdlczBtZV9OZXR3MHJraW5nX3RvMGx9   `
Now i will just decoded it as base64 

```
└─# echo "ZmxhZ3t0c2hBcmtfSXNfQXdlczBtZV9OZXR3MHJraW5nX3RvMGx9" | base64 -d
flag{tshArk_Is_Awes0me_Netw0rking_to0l}
```


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/WormSeen/README.md

OOur EDR has flagged suspicious traffic from production endpoint, after reviewing the respective process generating the traffic and another alert has been alerted “Worm Detected” in our SIEM

You decided to escalate the case to IR team to further investigate and answer the below questions 

 

Questions:

What is the range of worm spreading (x.x.x.x/xx) ?

Destination target port of the attack (XX)?

How many hosts might be affected by the worm (XX)?

 

Flag format: flag{Answer1:Answer2:Answer3}.

# Solution
i will unzip it
```
└─# unzip worm.zip
Archive:  worm.zip
   skipping: worm.exe                unsupported compression method 99
   ```

Not work i will use 7z 
```    
Enter password (will not be echoed):

```                      
it's asking me password, i will crack it
cracked

```
┌──(root㉿kali)-[/home/…/Desktop/Learning/Bluteam/Repeat]
└─# zip2john worm.zip > worm.hash
                                                                                                           
┌──(root㉿kali)-[/home/…/Desktop/Learning/Bluteam/Repeat]
└─# john worm.hash 
Using default input encoding: UTF-8
Loaded 1 password hash (ZIP, WinZip [PBKDF2-SHA1 128/128 AVX 4x])
Cost 1 (HMAC size) is 9191957 for all loaded hashes
Will run 4 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Proceeding with wordlist:/usr/share/wordlists/rockyou.txt
infected         (worm.zip/worm.exe)     
1g 0:00:00:04 DONE 2/3 (2023-09-26 15:13) 0.2252g/s 11516p/s 11516c/s 11516C/s 280690..spongebob9
Use the "--show" option to display all of the cracked passwords reliably
Session completed. 

```
Password : infected

I got an .exe file, i will analyze it

i will try to decompile it into a `pyc` file then i will into a `.py` using `pycdc`
To do That i will use this 
Link :https://github.com/extremecoders-re/pyinstxtractor
Done:
```
└─# python3 pyinstxtractor.py /home/kali/Desktop/Learning/Bluteam/Repeat/worm.exe  
[+] Processing /home/kali/Desktop/Learning/Bluteam/Repeat/worm.exe
[+] Pyinstaller version: 2.1+
[+] Python version: 3.10
[+] Length of package: 9051050 bytes
[+] Found 39 files in CArchive
[+] Beginning extraction...please standby
[+] Possible entry point: pyiboot01_bootstrap.pyc
[+] Possible entry point: pyi_rth_inspect.pyc
[+] Possible entry point: worm.pyc
[!] Warning: This script is running in a different Python version than the one used to build the executable.
[!] Please run this script in Python 3.10 to prevent extraction errors during unmarshalling
[!] Skipping pyz extraction
[+] Successfully extracted pyinstaller archive: /home/kali/Desktop/Learning/Bluteam/Repeat/worm.exe

```
Now i will just use the `pycdc`
`└─# ./pycdc worm.exe_extracted/worm.pyc > worm.py 
Unsupported opcode: GEN_START
Unsupported opcode: JUMP_IF_NOT_EXC_MATCH
`

Now just open the worm.py
```
└─# cat worm.py                 
# Source Generated with Decompyle++
# File: worm.pyc (Python 3.10)

''' Implementation of simple worm that spreads via SSH connection.
'''
import logging
import paramiko
import scp
import sys

class Worm:
    ''' This class represents implementation of worm that spreads via SSH
    connections.
    '''
    
    def __init__(self, network_address):
        self._network = network_address

    
    def network(self):
        ''' Network, on which the worm spreads. '''
        return self._network

    network = property(network)
    
    def network(self, new_network):
        self._network = new_network

    network = network.setter(network)
    
    def credentials(self):
        ''' Possible SSH credentials of the victim. '''
        return (('root', 'root'), ('msfadmin', 'msfadmin'))

    credentials = property(credentials)
    
    def generate_addresses_on_network(self):
        ''' Generate addresses of hosts on the given network.
        For simplicity is expected the following mask:
        255.255.255.0
        '''
        pass
    # WARNING: Decompyle incomplete

    
    def spread_via_ssh(self):
        ''' Spread the worm on the network via SSH connections.
        To establish SSH connection try selected user-password
        combinations. When the connection is established, copy
        the worm to the remote host.
        '''
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # WARNING: Decompyle incomplete


if __name__ == '__main__':
    worm = Worm('192.168.1.0')
    worm.spread_via_ssh()
    return None
               ```



flag : flag{192.168.1.0/24:22:85}
























### File: CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/README.md

## Certified Threat Hunter

Here you will find all **Threat Hunter** Units WriteUPs

follow me on my Hacking Journey Blog here : https://blackcybersec.xyz


## Certified Threat Hunter

| Challenges | Difficulty |                                                Tags                                                | Completed |
|:-------------:|:----------:|:--------------------------------------------------------------------------------------------------:|:---------:|
|               |            |                                                                                                    |           |
|     [APT](./Threat-hunter)      |    Easy    |                                       Hacking groups,  OSINT                                     | Completed |
|   [Kill Chain](./Threat-hunter)   |   Basic   |                                            Mittre attack                                            |        Completed   |
|    [CTI Analyst](./Threat-hunter)    |    Easy    |                                Malware hash                               | Completed |
|     [Yara Magic](./Threat-hunter/YaraMagic.md)    |    Easy    |                                     yara, rules, Basic                                     | Completed |
|    [Within Code](./Threat-hunter/WithIncode.md)    |    Medium    |                              yara, rules, conditions, strings                             |  Completed|
|      [Falcon Hunt](./Threat-hunter)     |    Medium    |                                 hunting,                                   | Completed |
|     Enc0de   |   Easy   |                               Arp, network analysis                              |      Completed     |
|    Refresher    |   Medium   |                                   Wireshark hunting                                   |      Completed     |
|     Ex0dus     |    Medium    |                                       Forensic, Wireshark, ICMP                                      | Completed |
|   Missey  |   Easy   |                                     Wireshark,                                     |       Completed    |
|    Baseline    |    Easy    |                                     Powershell, Hunting                                     |        Completed   |
|      [Arson](./Threat-hunter)     |   Medium   |                           Powershell, Ps1, Wireshark                          |   Completed        |
|   [Process](./Threat-hunter)   |    Basic    |                                        Windows, Process                                     | Completed |
|     [W4nna-Flag](./Threat-hunter)    |   Medium   |                                 Forensic, Volatility                                 |         Completed  |
|     Masqur4d3    |    Medium    |                                   Memory                                   | Completed          |
|  Scanner |   Easy   |                                     Logs Analysis, Attacker                                   |       Completed    |
|   [New account](./Threat-hunter)   |    Easy    |                Completed                                                             | Completed |
|     [Active Attacks](./Threat-hunter)    |   Medium   |            Completed                                                      |         Completed  |
|     Brut3 Forc3    |    Medium    |                                   Completed                                   | Completed          |



### File: CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/Brut3Forc3.md

we suspect that one of our server at 192.168.250.70  was attacked by a web brute forcing attack, we need to identify:

 

    X:  What is the attacker’s IP address.
    Y: The Average password length (decimal number).

Credentials: cybertalents/cybertalents

in the lessons Hunting for HTTP brute forcing attempts by counting the connections from an IP to our web server.
index=* sourcetype="stream:http" | stats count by src_ip 
first i go to the search bar and i typed
index=* sourcetype="stream:http" 
then i add the dest_ip for our server
index=* sourcetype="stream:http" dest_ip="192.168.250.70"
now i set the http method to post for logins
index=* sourcetype="stream:http" dest_ip="192.168.250.70" http_method=POST 
count it by src_IP
index=* sourcetype="stream:http" dest_ip="192.168.250.70" http_method=POST 
|  stats count by src_ip
23.22.63.114    412
40.80.148.42    12844

we found these two IPs now we will see the data for these 2 IPs
i begin with the second who have a lot of packets
for the first: index=* sourcetype="stream:http" dest_ip="192.168.250.70" http_method=POST src_ip="40.80.148.42"
and in form_data i haven't found any bruteforce.
Now for second : index=* sourcetype="stream:http" dest_ip="192.168.250.70" http_method=POST src_ip="23.22.63.114"
i found here 
username=admin&0960d493674eb04861bd64da9b662118=1&task=login&return=aW5kZXgucGhw&option=com_login&passwd=arthur
and it's the attacker IP: 23.22.63.114 
password batman length 6
flag{23.22.63.114_6}


### File: CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/Missey.md

I see Hex data but separated now i need to automate that

└─# tshark -r Missey.pcap -Y "tcp.analysis.push_bytes_sent==6" -x > hexpush.txt

found this :
70505176335852577a75324b5a4f556a4a563877344363486f72786836716b30397c464c41477b4d31355345445f494e425937247d
it's hex and i found : pPQv3XRWzu2KZOUjJV8w4CcHorxh6qk09|FLAG{M15SED_INBY7$}


### File: CyberTalents-Blue-Team-Scholarship-Writeups/AllInOne/activeattack.md

can use also https://github.com/WithSecureLabs/chainsaw
i got a file log ../logs.evtx

Our network got compromised two days ago by an unknown attacker, and we need to get an answer for the following questions:

1. What is the domain's SID?
2. The attacker failed to login to some accounts, What is the attacker's machine IP address?
3. What is the workstation's name that the attacker was using to authenticate with the administrator account?

Flag format: Flag{ANS1_ANS2_ANS3}

I will use evtxtract to extract it to .xml file 

└─# python3 /root/environment/myenv/bin/evtxtract logs.evtx > logs.xml

Now have extracted,
i know the attaccker failled login and i searched on google
Look for event ID 4625 which is triggered when a failed logon is registered. Open Event Viewer in Active Directory and navigate to Windows Logs> Security. The pane in the center lists all the events that have been setup for auditing. You will have to go through events registered to look for failed logon attempts.

and i found :
`<Data Name="TargetUserName">pbarker</Data>
<Data Name="TargetDomainName">marvel.local</D
<Data Name="IpAddress">192.168.80.128</Data>
<Data Name="IpPort">44236</Data>
</EventData>`
user pbarker and found IP. now i need the SID and for fcastle also
: but these SID was same 
`<Data Name="TargetUserSid">S-1-5-21-271597537-2992796785-3713134209-1105</Data> pbarker
`
 `<Data Name="TargetUserSid">S-1-5-21-271597537-2992796785-3713134209-1103</Data> fcastle`
 in this case the domain SID will be
S-1-5-21-271597537-2992796785-3713134209 the last four number is not on it 
for the login as admin i search for event id 4776
Introduction. Event ID 4776 is logged whenever a domain controller (DC) attempts to validate the credentials of an account using NTLM over Kerberos. 
then i found :
`
<Data Name="TargetUserName">fcastle</Data>
<Data Name="Workstation">KALI</Data>
<Data Name="Status">0x00000000</Data>
but logged as fcastle
and then i found
<Data Name="TargetUserName">administrator</Data>
<Data Name="Workstation">THEPUNISHER</Data>`
Flag{S-1-5-21-271597537-2992796785-3713134209_192.168.80.128_THEPUNISHER}


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/55H-Access/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Backdoor/Readme.md

### Description
Our server compromised due to known vulnerability introduced from many years, Kindly check and identify this flow 

X: Attack source → EX. “Internal/External” <br>
Y: The Source IP → x.x.x.x <br>
Z: CVE Num of the attack → xxx <br>
W: Destination Mac Address <br>
Flag format: flag{X:Y:Z:w} <br>

### Solution
First I used capinfos to see informations of the file
```
$ capinfos backdoor.pcap 
File name:           backdoor.pcap
File type:           Wireshark/tcpdump/... - pcap
File encapsulation:  Ethernet
File timestamp precision:  microseconds (6)
Packet size limit:   file hdr: 96 bytes
Packet size limit:   inferred: 96 bytes
Number of packets:   739
File size:           71 kB
Data size:           134 kB
Capture duration:    72.785513 seconds
First packet time:   2022-04-26 18:07:31.244931
Last packet time:    2022-04-26 18:08:44.030444
Data byte rate:      1,850 bytes/s
Data bit rate:       14 kbps
Average packet size: 182.21 bytes
Average packet rate: 10 packets/s
SHA256:              91a780295b31dac44d5357bf63bfe2cfddb990f447fd60a9048eb16ec5c7ec15
RIPEMD160:           01a55a5fe78f4db4ae13d90b031b6d5e5c8845fd
SHA1:                6a8a80c755676757b2a77b01f0282c46b4f87f9d
Strict time order:   True
Number of interfaces in file: 1
Interface #0 info:
                     Encapsulation = Ethernet (1 - ether)
                     Capture length = 96
                     Time precision = microseconds (6)
                     Time ticks per second = 1000000
                     Number of stat entries = 0
                     Number of packets = 739

```
I see number of packets is 739. now i proceed with Tshark, i used tshark to search if this pcap have a http request but not. Then i try to search for FTP.
```
$ tshark -r backdoor.pcap -Y ftp
Running as user "root" and group "root". This could be dangerous.
  165  10.000115 192.168.1.80 → 192.168.1.58 FTP 86 Response: 220 (vsFTPd 2.3.4)
  167  10.000865 192.168.1.58 → 192.168.1.80 FTP 78 Request: USER zH9:)
  169  10.000901 192.168.1.80 → 192.168.1.58 FTP 100 Response: 331 Please specify the passwor
  171  10.001580 192.168.1.58 → 192.168.1.80 FTP 77 Request: PASS utEt

```
I got only 4 request. So, in the first request i see vsFTPD 2.3.4 and it's the vulnerability that allowed the attacker to hack the machine.
I search that on Google and i got CVE-2011-2523. <br>
Also, you can see that in these FTP request, you will see the source IP, that's 192.168.1.58,  and destination IP : 192.168.1.80.
Now if you use wireshark and filter using FTP. you will find the Destination Mac address. <br>
or use this wireshark command 

```
$ tshark -r backdoor.pcap -Y ftp -V | less
Frame 165: 86 bytes on wire (688 bits), 86 bytes captured (688 bits)
    Encapsulation type: Ethernet (1)
    Arrival Time: Apr 26, 2022 18:07:41.245046000 EDT
    [Time shift for this packet: 0.000000000 seconds]
    Epoch Time: 1651010861.245046000 seconds
    [Time delta from previous captured frame: 0.005825000 seconds]
    [Time delta from previous displayed frame: 0.000000000 seconds]
    [Time since reference or first frame: 10.000115000 seconds]
    Frame Number: 165
    Frame Length: 86 bytes (688 bits)
    Capture Length: 86 bytes (688 bits)
    [Frame is marked: False]
    [Frame is ignored: False]
    [Protocols in frame: eth:ethertype:ip:tcp:ftp]
Ethernet II, Src: PcsCompu_66:e3:8b (08:00:27:66:e3:8b), Dst: IntelCor_c5:20:65 (4c:1d:96:c5:20:65)

```
You will find the Destination Mac address: 08:00:27:66:e3:8b <br>
<li>
	<details>
		<summary>Flag</summary>
flag{Internal:192.168.1.58:CVE-2011-2523:08:00:27:66:e3:8b}</details>
</li>



### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Bean-Detector/Readme.md

### Description
 You have received the alert in your company WAF that web attack happened recently. Please check and identify the below details <br>
X : Attacker IP <br> 
Y : Name of Vulnerability Scanner used by the Attacker <br>
Z : number of bytes in the sensitive files Leaked <br>
W : Date and time of the Sucessful attack (xx/xx/xxxx:xx:xx:xx) <br>
### Solution
To solve this challenge also, you need just  to know some  command line tool usage like: grep and cat

```
$ cat beansdetectorlogs | grep -e "flag.txt" -e "200 " 
172.17.0.1 - - [12/Jun/2022:11:04:11 +0000] "GET /files/skel/ HTTP/1.1" 200 184 "-" "Wfuzz/2.2" "-"
172.17.0.1 - - [12/Jun/2022:11:04:11 +0000] "GET /files/skel/.bashrc HTTP/1.1" 200 3526 "-" "Wfuzz/2.2" "-"
172.17.0.1 - - [12/Jun/2022:11:04:11 +0000] "GET /files/skel/.profile HTTP/1.1" 200 675 "-" "Wfuzz/2.2" "-"
172.17.0.1 - - [12/Jun/2022:11:04:11 +0000] "GET /files/skel/200 HTTP/1.1" 404 169 "-" "Wfuzz/2.2" "-"
172.17.0.1 - - [12/Jun/2022:11:04:15 +0000] "GET / HTTP/1.1" 200 404 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0" "-"
172.17.0.1 - - [12/Jun/2022:11:04:31 +0000] "GET /files../ HTTP/1.1" 200 2482 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0" "-"
172.17.0.1 - - [12/Jun/2022:11:04:38 +0000] "GET /files../home/ HTTP/1.1" 200 302 "http://localhost/files../" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0" "-"
172.17.0.1 - - [12/Jun/2022:11:05:12 +0000] "GET /files../home/flag.txt HTTP/1.1" 200 49 "-" "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0" "-"

```
I launch this command and in the last line i got the sensitive file flag.txt and it response successfuly with a 200 response. <br>
Now we need to answer the challenge Questions: <br>
We see that The attacker IP is 172.17.0.1, and the tool that used by the attacker is Wfuzz. <br>
The Date and time of Sucessfull attck is also in that 200 last response. and it's 12/Jun/2022:11:05:12.  We need to transform June by number, that will be 12/06/2022. <br>
The number of bytes in that sensitive files will be found near 200 response and it's "49". <br>

<li>
	<details>
		<summary>Flag</summary>
Bro, read all the Writeup and solve the challenge: the flag format is : flag{X:Y:Z:W}</details>
</li>





### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Bean/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/CVE-Number/Readme.md

## Solution
### Description: What is the CVE ID that is related to EternalBlue
##### Flag Format: XXX-XXXX-XXXX

To Solve this challenge Just google it and i found this article, https://cve.mitre.org/cgi-bin/cvename.cgi?name=cve-2017-0144 
```
The SMBv1 server in Microsoft Windows Vista SP2; Windows Server 2008 SP2 and R2 SP1; Windows 7 SP1; Windows 8.1; Windows Server 2012 Gold and R2; Windows RT 8.1; and Windows 10 Gold, 1511, and 1607; and Windows Server 2016 allows remote attackers to execute arbitrary code via crafted packets, aka "Windows SMB Remote Code Execution Vulnerability." This vulnerability is different from those described in CVE-2017-0143, CVE-2017-0145, CVE-2017-0146, and CVE-2017-0148. 
```

<li>
	<details>
		<summary>Flag</summary>
		cve-2017-0144
	</details>
</li>


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Competition/Readme.md

## Solution :
### Description : Special kind of cybersecurity competition designed to challenge its participants to solve computer security problems

To solve this Challenge, I Copy the description of the Challenge and I submit it on Google.
Then it's return: 

### <code> A capture the flag (CTF) competition is a special kind of cybersecurity competition designed to challenge its participants to solve cyber security problems and/or capture and defend computer systems.</code>


<li>
	<details>
		<summary>Flag</summary>
		CTF
	</details>
</li>


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/FourOFour/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/MEGO/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Pass-Reset/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Phisher/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Remote-Hacker/Readme.md

### Description 
Our SoC L1 reported that she received alert of suspicious login detected by company user “Kvasir” on 13/06/2022. <br>
Please do check and return by your analysis: <br>

X: Session Duration spent by the attacker on the system (HH:MM:SS) <br>

Y: The application used by the user after login (xxxx.exe) <br>

Z: Identify the SHA256 of this application W: Attacker IP address <br>

A: Attacker Machine host name <br>

Flag format: flag{X:Y:Z:A}<br>


### Solution
To solve this challenge, Many people used Windows OS to analyze this file. I used Linux to Solve it and here is how i proceed. <br>

On github, i found a tool named evtxtract, that can help me to transform my evtx into xml file. Then i install it. <br>
Now i proceed for conversion for evtx files .<br>
```
$ evtxtract Microsoft-Windows-Sysmon_4Operational.evtx > Windows-Sysmon_4Operational.xml
INFO:root:recovered 20044 complete records
INFO:root:recovered 0 incomplete records
```
```
$ evtxtract Security.evtx > Security.xml  
INFO:root:recovered 6178 complete records
INFO:root:recovered 0 incomplete records
```
Now, on the description i see that the supscious login was detected on 13/06/2022. I click on CTRL+F and try to find that date on the Security.xml file. <br>
Then , I found the computer name on a date 2022-06-13 <br>
```
<Computer>DESKTOP-9BBI1VE</Computer> <br> 
```
For the Session Duration spent by the attacker on the system, You need to identify the login then also check the logoff and calculate it. <br>
I found also the IP adress in the XML code, and this LogonType <br>
In Windows, LogonType codes are used to identify different types of logon events for security auditing purposes. The value "3" for "LogonType" typically indicates a network logon, which means a user has connected to a remote system (over the network) and logged in with their credentials. <br>
```
<Data Name="LogonType">3</Data>
<Data Name="LogonProcessName">NtLmSsp </Data>
<Data Name="AuthenticationPackageName">NTLM</Data>
<Data Name="WorkstationName">Nitro</Data>
<Data Name="TransmittedServices">-</Data>
<Data Name="LmPackageName">-</Data>
<Data Name="KeyLength">0</Data>
<Data Name="ProcessId">0x0000000000000000</Data>
<Data Name="ProcessName">-</Data>
<Data Name="IpAddress">192.168.1.58</Data>
<Data Name="IpPort">0</Data>
<br> 
```
Find IP address and Workstation Name.
To find the Application used by the attacker, we should look for a process created by a user. <br>
In Sysmon (System Monitor), a process creation event with an ID of "1" refers to the process creation event type. Sysmon is a Windows system service and device driver that monitors and logs various system activities to help detect and investigate potential security threats. <br>
So now, we need to return and look at when the user logged into the system and then read the events by date <br>
We will find sethc.exe, Win32calc.exe and then identify which one of these applications is started by the ParentUser. You will find that application Sha256. <br>

<li>
	<details>
		<summary>Flag</summary>
Tryharder bro.. If you don't understand all of these step. ping me on Discord: blomann#3219. for some explanation. Thanks...</details>
</li>



### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/SIEM-Port/Readme.md

## Description
Your company planning to use Qradar as SIEM tool and you planning to receives logs from different different devices like routers, switches and some other devices, What Is The Default TLS Syslog Port That QRadar Listens On?

## Solution
To solve this, Very easy because the only tool you need to know how to use is google
Just Copy the Description and Past in Google or ChatGPT
I found this Questions Links : ```https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjjxc-surmAAxVaXvEDHeDUB6wQFnoECBIQAQ&url=https%3A%2F%2Fstackoverflow.com%2Fquestions%2F66268845%2Fqradar-no-listening-on-514-port&usg=AOvVaw2PckjPqaX_0gaSf7RKEx6g&opi=89978449```

<li>
	<details>
		<summary>Flag</summary>
		flag{514}
	</details>
</li>


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/Smart-Role/Readme.md

## Description

skills of collecting information out of cyberspace that has been previously analysed and shared between organisations about different attack scenarios and vectors.What is the role name of the above definition 
## Solution
In the Lessons and introductions of Soc Analayst there is :
##### Cyber Threat Intelligence
### <code>Cyber threat intelligence is the skill of collecting information out of cyberspace that has been previously analyzed and shared between organizations about different attack scenarios and vectors. </code>


<li>
	<details>
		<summary>Flag</summary>
		flag{Threat Intelligence}
	</details>
</li>


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Soc-analyst/USB-Case/Readme.md




### File: CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/WithIncode.md

# Description
Flag rises within the code. Our developer thinks encoding is safe, try to find the location
flag format: Flag{location}

# Solution
In this challenge, we need to know some knowledge about writing Yara rules.
i will write a yara rule for word `Flag`, Because in the challenge description it say: `Flag rises within the code.`
first i will encode the `Flag` word into `base64`, 
i will got this : `RmxhZw==` and then encode this also into `hex`, i got `526d78685a773d3d`

Now writing the rule:
Here is the Documentation: https://yara.readthedocs.io/en/stable/writingrules.html
```
rule unknown
{
	strings:
		$hex = {526d78685a773d3d}
	condition:
		$hex
}

```
When i execute it:
```terminal
root@nenandjabhata:/home/files# yara -f rule.yara Code/
unknown Code//6645
```
We got the `Code//6645` but it's not the location.
to get our location, we need to use the `-s` flag to print matching strings.

```terminal
root@nenandjabhata:/home/files# yara -s -f rule3.yara Code/
unknown Code//6645
0x2460:$hex: 52 6D 78 68 5A 77 3D 3D
```
Now we need just to decode the `0x2460` from hex to Decimal to get our location
Links : https://www.rapidtables.com/convert/number/hex-to-decimal.html
Flag{9312}


### File: CyberTalents-Blue-Team-Scholarship-Writeups/Threat-hunter/YaraMagic.md

# Description
Help us!Here is a copy of a folder of ours, 
we need to scan this folder with this Yara rule and check if we have any matches!,
 scan this folder with the rule and provide us with the matched filename.
Flag format: FLAG{filename}

# SOlution
The challenge provide us a yara rule, we need only to run it on this folder
here is the rule:
```
root@nenandjabhata:/home/files/Yara Magic# cat rule.yara 
rule MySuperCoolRule
{
    strings:
       
        $my_hex_string = { 54 4f 4b 41 }

    condition:
         $my_hex_string 
}

```
I just run
```terminal
root@nenandjabhata:/home/files/Yara Magic# yara -f rule.yara Folder/
MySuperCoolRule Folder//12776
```

`FLAG{12776}`
