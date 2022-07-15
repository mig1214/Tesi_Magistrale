# ApplyPatch and Extractor.py
This two program have the goal to download a list of vulnerabilities described in the website https://www.cvedetails.com/ and download them using the website https://git.kernel.org.
Extractor.py download two files:

- child file
- parent file

So it's possibile to create the diff -u file between these files. After download it will be create folders where are stored all the vulnerabilities and the patches.
After that it is possibile run ApplyPatch.py that search in the new folders the parent and patch files and apply this one at the parent file.
Finally the file "AP_xxx" with the applied patch is generated. 
