import os
from natsort import os_sorted


def delete_same_functions(path: str):
    functions_list = os_sorted(os.listdir(path))
    i = 0
    while i + 1 < len(functions_list):
        with open(path + "/" + functions_list[i]) as e1:
            e1_lines = e1.readlines()
        with open(path + "/"+functions_list[i+1]) as e2:
            e2_lines = e2.readlines()
        if e1_lines == e2_lines:
            del_path = path + "/"+functions_list[i]
            os.remove(path + "/"+functions_list[i])
        i += 1


def find_indexs(index: int, codelist: list):
    found_up = False
    list_index = []
    try:
        while not found_up and index > 0:
            if codelist[index].startswith("{\n"):
                found_up = True
                list_index.append(index-1)
            else:
                index -= 1
        found_down = False
        while not found_down and index > 0:
            if codelist[index].startswith("}\n"):
                found_down = True
                list_index.append(index)
            else:
                index += 1
        return list_index
    except:
        return []


# Indici delle funzioni
func_index_p = 1
func_index_c = 1
# Indice della cartella Vulnerabilita X
vul_index = 1
# Cerco le cartelle Vulnerabilità X
path_vulnerabilities = os.path.join("./list_vulnerabilities/", "Vulnerabilita " + str(vul_index))
while os.path.exists(path_vulnerabilities):
    path_vulnerabilities = os.path.join("./list_vulnerabilities/", "Vulnerabilita " + str(vul_index))
    # Cerco le cartelle Patch X
    index_patches = 1
    path_patches = os.path.join(path_vulnerabilities, "Patch " + str(index_patches))
    while os.path.exists(path_patches):
        path_patches = os.path.join(path_vulnerabilities, "Patch " + str(index_patches))
        parentFile = ""
        childFile = ""
        patchFile = ""
        if os.path.exists(path_patches):
            files = os.listdir(path_patches)
            # Memorizzo i percorsi dei file parent e patchfile
            for file in files:
                if not file.endswith(".c") and not file.endswith(".patch"):
                    index_patches += 1
                    break
                if "p_" in file:
                    parentFile = os.path.join(path_patches, file)
                if "c_" in file:
                    childFile = os.path.join(path_patches, file)
                if ".patch" in file:
                    patchFile = os.path.join(path_patches, file)
            if parentFile == "" or childFile == "" or patchFile == "":
                continue
            # Catturo indice patch
            parent_indexs = []
            child_indexs = []
            with open(parentFile) as paf:
                with open(childFile) as cf:
                    parent_lines = paf.readlines()
                    child_lines = cf.readlines()
            # Catturo gli indici delle funzioni tramite la patch
            with open(patchFile) as ptf:
                patch_lines = ptf.readlines()
                count = 2
                while count < len(patch_lines):
                    if patch_lines[count].startswith("@"):  # Individuazione inizio cambiamenti
                        start_del = patch_lines[count].split()[1]
                        start_add = patch_lines[count].split()[2]
                        index_remove = int(start_del.split(",")[0].removeprefix("-"))    # Indice per eliminare elementi
                        index_add = int(start_add.split(",")[0].removeprefix("+"))
                                                                # Indice per raggiungere il blocco istruzioni interessate
                        child_indexs.append(index_add)
                        parent_indexs.append(index_remove)
                    count += 1

            # Salvo nella cartella "functions" le diverse funzioni su file.txt differenti provenienti dal parent file
            for index in parent_indexs:
                lista = find_indexs(index, parent_lines)
                if len(lista) > 0:
                    start = lista[0]
                    end = lista[1]
                    file_name = "p_function" + str(func_index_p) + ".txt"
                    func_path = os.path.join("./functions/functions_p", file_name)
                    func_file = open(func_path, "w")
                    for i in range(start, end+1):
                        func_file.write(parent_lines[i])
                        print(parent_lines[i])
                    func_file.close()
                    func_index_p += 1

            # Salvo nella cartella "functions" le diverse funzioni su file.txt differenti provenienti dal child file

            for index in child_indexs:
                lista = find_indexs(index, child_lines)
                if len(lista) > 0:
                    start = lista[0]
                    end = lista[1]
                    file_name = "c_function" + str(func_index_c) + ".txt"
                    func_path = os.path.join("./functions/functions_c", file_name)
                    func_file = open(func_path, "w")
                    for i in range(start, end+1):
                        element = child_lines[i]
                        func_file.write(child_lines[i])
                        print(child_lines[i])
                    func_file.close()
                    func_index_c += 1
        index_patches += 1
    vul_index += 1
# Elimino quelle funzioni uguali
path_functions_p = os.path.join("./functions/", "functions_p")
path_functions_c = os.path.join("./functions/", "functions_c")
delete_same_functions(path_functions_c)
delete_same_functions(path_functions_p)


