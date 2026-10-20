<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ayeshx
description: CTF writeups and security challenges by ayeshx.
---

# Writeups by ayeshx

Source repository: `/repos/ayeshx`

## Repository Index

- external_pentester/README.md

## Writeup Content


### File: external_pentester/README.md

<h1>Installing the API to a Local Machine</h1>
<ol>
    <li>
        <h3>Initial Installation</h3>
        <ul>
            <li>Ensure you are installing on a Kali Linux Machine.</li>
            <li>Download the zip file or clone directly to your preferred directory.</li>
            <li>Make sure there is internet connection on the Kali Machine at all times.</li>
            <li>After downloading, go to the downloaded directory (i.e., inside the new downloaded directory.</li>
            <li>Make sure you have <em>extensions.txt, fasttrack.txt, metasploit, pswds.lst, url.txt and user.txt</em>
                in the downloaded directory.</li>
            <li>
                <strong>Nmap-Vulners Installation:</strong> 
                <ul>
                    <li>Go to this link: <a href="https://github.com/vulnersCom/nmap-vulners">Nmap-Vulners</a></li>
                    <li>Download the repository locally.</li>
                    <li>Follow the steps in the Installation section, it's simple and straightforward.</li>
                    <li>You will need to locate the hidden <em>.nmap</em> directory on the Kali machine. If you cannot find this directory then it is probably in <em>/usr/share/nmap/scripts</em> directory.</li>
                    <li>Copy the <em>nmap-vulners.nse</em> script here. </li>
                </ul>   
            </li>
            <li>
                <strong>Vulscan Installation</strong>
                <ul>
                    <li>Go to this link: <a href="https://github.com/scipag/vulscan">Vulscan</a></li>
                    <li>Follow the steps in the <em>Installation</em> section.</li>
                    <li>This should take place in the same nmap scripts directory as above in nmap-vulners.</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>
        <h3>Pre-run Configurations</h3>
        <ul>
            <li>Inside the API directory, open a terminal and enter <strong><em>npm install</em></strong>. This will
                install all node dependencies required.</li>
            <li><strong>DO NOT MODIFY THE <em>.env</em> FILE </strong> with any of your own paths.</li>
            <li>Any of the <em>passwordlists and extension files</em> inside the API can be modified to reflect what you
                want. However it is <strong>recommended to not do so</strong>
                because they already contain good estimates of what is required.</li>
            <li>Finally, inside the API in a terminal, enter <strong>node pentestApi.js</strong> and hit enter.</li>
            <li>Make sure the console output says <em>Server has started</em>, this means that The API has now started,
                and is waiting for connections.</li>
            <li><strong>NOTE:</strong> The API runs on port 3005, and normally you shouldn't have anything running on
                this port. If you do get an error, make sure that
                there is no process running on port 3005 and kill such a process!</li>
        </ul>
    </li>
    <li>
        <h3>Sending Requests to the API</h3>
        <ul>
            <li>A request can be sent from anywhere in the form of an HTTP request, i.e., from inside code, from a
                platform or simply from a terminal in the form of
                <strong>http://hostaddress:port/starttest/192.168.1/startIP/endIP/phases</strong>.</li>
            <li>A sample request looks like the following - <br> <strong>curl
                    http://localhost:3005/starttest/192.168.1/212/212/ivd</strong> <br>
                <ol>
                    <li>
                        In this example we used the curl command to send a request to a RESTful HTTP route. We used
                        <em>localhost</em> because we sent the request from the
                        same machine, in other cases acquire the IP Address of the Kali Machine and send a request to
                        that IP, followed by the port.
                    </li>
                    <li>
                        The route parameters include the <em>startest</em> keyword followed by the local subnet which is
                        <em>192.168.1</em> in most cases.
                    </li>
                    <li>
                        This is followed by a start IP address, in this case start from 192.168.1.212. The next
                        parameter is the end IP Address. In this case its the same
                        device. This means it only pen-tests one device. <br>
                        The last parameter is to specify the phases of testing, which for now need to include all 3
                        phases, <br>
                        i -> Information Gathering <br>
                        v -> Vulnerabililty Assessment <br>
                        d -> Dictionary Attacks
                    </li>
                </ol>
            </li>
            <li>A request can also be sent from anywhere in the form of an MQTT request, i.e., from inside code or from
                a platform by the following simple steps:
                <ol>
                    <li>Publishing a message on the <strong><em>pentest/start</em></strong> topic.</li>
                    <li>This message needs to be a JSON of the following format: <br>
                        <strong>{</strong>
                        <br>
                        <strong>ip: []</strong>
                        <br>
                        <strong>domain: ''</strong>
                        <br>
                        <strong>}</strong>
                    </li>
                    <li>The message <strong>has to be <em>stringified</em> using JSON.stringify()</strong> method.</li>
                    <li>A sample method of publishing this message is shown in the <strong><em>portal.html</em></strong>
                        file in this directory.</li>
                    <li>The <em>ip</em> array in the message is an array of various IP Addresses to run the test on,
                        only the last 8 bits, eg: if you want to test the IP addresses 192.168.1.1 and 192.168.1.13,
                        then you would only pass the "1" and the "13" as elements of this array!</li>
                    <li>The domain field in the JSON message is the beginning 24 bits of the IP address <strong>without
                            the trailing "."</strong>.</li>
                    <li>Once the message is published, the client should also subscribe to 2 topics which are
                        <strong><em>pentest/updates</em> and the <em>pentest/complete</em></strong></li>
                    <li>After this process, the user just has to wait for results and they will appear once the tests
                        are complete.</li>
                    <li>To further analyze the results, parsing is required which is explained the below section on
                        Report Generation.</li>
                    <li>
                        <h4>NOTE:</h4>
                        Even though the setup for MQTT can be longer than HTTP, the benefits are more than simple HTTP.
                        <ul>
                            <li>It is an asynchronous pattern which is more intuitive.</li>
                            <li>More variety of IP Addresses can be tested.</li>
                            <li>It is lightweight and can be requested from anywhere in the code.</li>
                        </ul>
                    </li>
                </ol>
            </li>
        </ul>
    </li>
</ol>
<h1>Report Generation</h1>
<ol>
    <li>
        <h3>Structure of the report generated</h3>
        <ul>
            <li>Report is in <strong>JSON structure</strong> with fields for various results of tools used in the
                security test.</li>
            <li>
                <h4>Sample Report JSON -></h4>
                <br>
                <img src="./API_JSON_template1.png" alt="">
                <br>
                <img src="./API_JSON_template2.png" alt="">
                <br>
                <img src="./API_JSON_template3.png" alt="">
            </li>
            <br>
            <li>The fields of the JSON are as shown in the template and each device tested comes in the <em>devices</em>
                array which is the <strong>top level field</strong> of the report.</li>
            <li>A sample code in plain HTML/JS is shown in the <strong><em>portal.html</em></strong> file provided in
                the directory.</li>
            <li>The 2 methods in the html file show different ways of sending the request which are <em>MQTT based or
                    HTTP based</em>.</li>
            <li>
                <h4>NOTE</h4>
                <ul>
                    <li>HTTP Based request only allows an IP address range sequentially, so different addresses cannot
                        be tested in the same domain, eg: 192.168.1.1 -> 192.168.1.10 in order.</li>
                    <li>MQTT Based request allows any random IP address within the same LAN/domain, eg: 192.168.1.1 &
                        192.168.1.37 & 192.168.1.14</li>
                    <li>HTTP Based request takes time to get a response because the tests take time to complete, however
                        MQTT Based requests are asynchronous by nature and non-blocking so they are recommended!</li>
                    <li>Parsing the json in typescript or JS is a simple one liner -> <strong>var res =
                            JSON.parse(msg);</strong>.</li>
                </ul>
            </li>
        </ul>
    </li>
</ol>

