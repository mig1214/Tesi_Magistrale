# Suite of programs
This programs have the goal to download a list of vulnerabilities described in the website https://www.cvedetails.com/ and download them using the website https://git.kernel.org.
Extractor.py download two files:

- child file
- parent file

So it's possibile to create the diff -u file between these files. After download it will be create folders where are stored all the vulnerabilities and the patches.
After that it is possibile run ApplyPatch.py that search in the new folders the parent and patch files and apply this one at the parent file.
Finally the file "AP_xxx" with the applied patch is generated. 
Next, with the program CallOfFunctions, the functions modified in the patches are saved in a text file separeting them in two classes: functions derived from parent file (no patched) and function derived from child file (patched).
After that with the patches are unified in a single text file with the program UnionPatches so it's possible for the program HunterFunctions to understand the most frequent called to functions in the functions text files.
With that information it's possible modified the program VectorsConveter and obtain the set of vectors that can be studied from the automatic learning model SVM.
