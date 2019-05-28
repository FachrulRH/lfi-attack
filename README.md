# LFI Attacker
Local File Inclusion attack in file download query web application
- Found LFI directory in website
- get the file on directory has been found

<b><h1>How To Use: </h1></b>
- Set the target
  - python lfi.py -u http://example.com/example.php?example=
- Set the target OS linux or windows it's different directory
  - python lfi.py -u http://example.com/example.php?example= --type linux
- Set if you have own path
  - python lfi.py -u http://example.com/example.php?example= --path yourownpath
  
 <b><h1>Module required: </h1></b>
 - urlparse
 - requests
