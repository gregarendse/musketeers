C:\DevTools\apache-jmeter-5.5\bin\jmeter -n -t "test.jmx" -e -l log.jtl -o .data\jmeter -f

& 'C:\Program Files\Zulu\zulu-17\bin\java' -agentpath:C:/DevTools/visualvm/visualvm_214/visualvm_214/visualvm/lib/deployed/jdk16/windows-amd64/profilerinterface.dll=C:\DevTools\visualvm\visualvm_214\visualvm_214\visualvm\lib,5140 -jar .\target\musketeers-0.0.1-SNAPSHOT.jar