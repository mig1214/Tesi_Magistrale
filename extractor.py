import requests
import wget
import os
import tarfile
import shutil
import difflib
import sys
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup

# Esploro le prime 50 pagine delle vulnerabilità Linux 2021 del sito https://www.cvedetails.com/
# e catturo i link per la patch del sito https://git.kernel.org/

URL = "https://www.cvedetails.com/vulnerability-list/vendor_id-33/product_id-47/year-2021/Linux-Linux-Kernel.html"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
results = soup.find(id="vulnslisttable")

url = soup.find_all("td", nowrap=True)
link = ""
git_url = ""
folder_index = 1
for text in url:
    title = text.getText()
    link = "https://www.cvedetails.com/cve/"+title

    # Esploro la singola pagina della vulnerabilità
    new_URL = link
    page = requests.get(new_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="vulnrefstable")

    new_urls = soup.find_all("td", class_="r_average")
    # Controllo che ci sia un link git.kernel.org altrimenti passo alla prossima iterazione
    check = False
    for element in new_urls:
        if "https://git.kernel.org" in element.getText():
            check = True
    if not check:
        continue

    # catturo i link di git.kernel.org
    for new_element in new_urls:
        if "https://git.kernel.org" in new_element.getText():
            git_url = new_element.getText()


    # pulizia del link URL
    git_divide = git_url.split(" ")
    git_kernel_url = git_divide[0].strip("\n")
    # salto quei link diversi da quelli standard
    if "linux.git/log/" in git_kernel_url:
        continue
    request = requests.get(git_kernel_url)

    #git_kernel_url = "https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit/?id=298a58e165e447ccfaae35fe9f651f9d7e15166f"
    #request = requests.get(git_kernel_url)

    # catturo i link del commit parent e del figlio
    soup = BeautifulSoup(request.content, "html.parser")
    diff_results = soup.find_all("div", class_="head")
    parent_result = soup.find_all("td", class_="sha1")
    # Controllo che sia nella pagina standard
    if len(diff_results) == 0 or len(parent_result) == 0:
        continue
    part1_parent_url = "https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/snapshot/linux-"
    part2_parent_url = ""
    extrac_paths = []
    for element in parent_result:
        if "diff" in element.getText():
            part2_parent_url = element.text.removesuffix(" (diff)")
            print("\n")
        if "net-" in element.getText():
            part1_parent_url = "https://git.kernel.org/pub/scm/linux/kernel/git/netdev/net.git/snapshot/net-"
        elif "bpf-" in element.getText():
            part1_parent_url = "https://git.kernel.org/pub/scm/linux/kernel/git/bpf/bpf.git/snapshot/bpf-"
        elif "ext4-" in element.getText():
            part1_parent_url = "https://git.kernel.org/pub/scm/linux/kernel/git/tytso/ext4.git/snapshot/ext4-"

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

    folder_name = "Vulnerabilita " + str(folder_index)
    os_path = "./list_vulnerabilities/"
    dir = os.path.join(os_path, folder_name)
    link_parent = part1_parent_url+part2_parent_url+".tar.gz"
    child_name = ""
    parent_name = ""

    if not os.path.exists(dir):
        os.mkdir(dir)
        child_name = link_child.split('/')[-1]
        print("Download file: " + child_name)
        wget.download(link_child, out=os_path+folder_name) ## Scarico prima il figlio
        parent_name = link_parent.split('/')[-1]
        print("Scaricato file: " + child_name)
        print("Download file: " + parent_name)
        wget.download(link_parent, out=os_path+folder_name) ## Scarico il padre
        print("Scaricato file: " + parent_name)
        folder_index += 1

    # Estraggo i file
    if not (child_name == "") and not (parent_name == ""):
        file_child = tarfile.open(os_path+folder_name+"/"+child_name)
        file_parent = tarfile.open(os_path+folder_name+"/"+parent_name)
        child_lines_txt = []
        parent_lines_txt = []
        index = 1

        for path in extrac_paths:
            # Creo una cartella per le singole vulnerabilità e patch
            name_patch = "Patch "+str(index)
            name_file_extract = path.split('/')[-1]
            dir2 = os.path.join(os_path+folder_name+"/", name_patch)
            if not os.path.exists(dir2):
                os.mkdir(dir2)
            try:
                print("Estrazione file: " + name_file_extract)
                # Estraggo i file child e parent necessari
                file_child.extract(child_name.removesuffix(".tar.gz") + path, os_path+folder_name)
                file_parent.extract(parent_name.removesuffix(".tar.gz") + path, os_path+folder_name)

                # memorizzo il percorso dei file estratti
                file_extract_c = os.path.join(os_path + folder_name + "/" + name_patch, "c_" + name_file_extract)
                file_extract_p = os.path.join(os_path + folder_name + "/" + name_patch, "p_" + name_file_extract)

                # Creo file dove copiare i file child e parent
                file_c = open(file_extract_c, "w")
                file_p = open(file_extract_p, "w")

                # Copio file figlio
                src_c = os_path+folder_name + "/" + child_name.removesuffix(".tar.gz") + path
                dst_c = file_extract_c

                shutil.copyfile(src_c, dst_c)

                # Copio file padre
                src = os_path + folder_name + "/" + parent_name.removesuffix(".tar.gz") + path
                dst = file_extract_p

                shutil.copyfile(src, dst)
                file_c.close()
                file_p.close()

                # Comparo i file child e parent
                patchfile = os.path.join(os_path + folder_name + "/" + name_patch, "patchfile.patch")
                file_patch = open(patchfile, "w")
                with open(src_c) as sc:
                    c_text = sc.readlines()
                with open(src) as sp:
                    p_text = sp.readlines()
                #print(*c_text, sep="\n")
                for line in difflib.unified_diff(p_text, c_text, fromfile=src, tofile=src_c, lineterm="\n"):
                    print(line)
                    file_patch.write(line)
                file_patch.close()
                index += 1
                print("Fine estrazione file.")
            except:
                print("Error, file doesn't exist")
                if os.path.exists(dir2):
                    os.rmdir(dir2)

        file_child.close()
        file_parent.close()

