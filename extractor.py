import requests
import wget
import os
import tarfile
from bs4 import BeautifulSoup

# Esploro le prime 50 pagine delle vulnerabilità Linux 2021 del sito https://www.cvedetails.com/
# e catturo i link per la patch del sito https://git.kernel.org/
'''
URL = "https://www.cvedetails.com/vulnerability-list/vendor_id-33/product_id-47/year-2021/Linux-Linux-Kernel.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="vulnslisttable")

url = soup.find_all("td", nowrap=True)
link = ""
git_url = ""
for text in url:
    title = text.getText()
    link = "https://www.cvedetails.com/cve/"+title

    # Esploro la singola pagina della vulnerabilità
    new_URL = link
    page = requests.get(new_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="vulnrefstable")

    new_urls = soup.find_all("td", class_="r_average")
    
    # catturo i link di git.kernel.org
    for new_element in new_urls:
        if "https://git.kernel.org" in new_element.getText():
            git_url = new_element.getText()

# pulizia del link URL
git_divide = git_url.split(" ")
url = git_divide[0].strip("\n")
request = requests.get(url)
'''
git_kernel_url = "https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=298a58e165e447ccfaae35fe9f651f9d7e15166f"
request = requests.get(git_kernel_url)

# catturo i link del commit parent e del figlio
soup = BeautifulSoup(request.content, "html.parser")
diff_results = soup.find_all("div", class_="head")
parent_result = soup.find_all("td", class_="sha1")
part1_parent_url = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/snapshot/linux-"
part2_parent_url = ""
extrac_paths = []
for element in parent_result:
    if "diff" in element.getText():
        part2_parent_url = element.text.removesuffix(" (diff)")
        print("\n")

#print(part1_parent_url+part2_parent_url)

# Catturo il/i path del/dei file da estrarre
for element in diff_results:
    extrac_paths.append(element.text.split(" ")[2].removeprefix("a"))


print(*extrac_paths, sep="\n")

### Scarica cartelle ###
dlinks = soup.find_all("a", href=True)
link_child = ""
for element in dlinks:
    if ".tar.gz" in element.text:
        link_child = "https://git.kernel.org" + element["href"]

folder_index = 1
folder_name = "Cartella " + str(folder_index)
os_path = "C:/Users/migue/Desktop/Universita/Magistrale/2_anno/Tesi/Tesi_Magistrale/patches/"
dir = os.path.join("C://", "Users/migue/Desktop/Universita/Magistrale/2_anno/Tesi/Tesi_Magistrale/patches", folder_name)
link_parent = part1_parent_url+part2_parent_url+".tar.gz"

if not os.path.exists(dir):
    os.mkdir(dir)

#wget.download(link_child, out=os_path+folder_name) ## Scarico prima il figlio
child_name = link_child.split('/')[-1]
parent_name = link_parent.split('/')[-1]
print(child_name)
print(parent_name)
#wget.download(link_parent, out=os_path+folder_name) ## Scarico il padre
folder_index += 1

# Estraggo i file
file_child = tarfile.open(os_path+folder_name+"/"+child_name)
file_parent = tarfile.open(os_path+folder_name+"/"+parent_name)

for path in extrac_paths:
    try:
        file_child.extract(child_name.removesuffix(".tar.gz")+path, os_path+folder_name)
        file_parent.extract(parent_name.removesuffix(".tar.gz")+path, os_path+folder_name)
    except:
        print("Error, file doesn't exist")


file_child.close()
file_parent.close()

#for path in extrac_paths:







