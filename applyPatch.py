import os

# Cerco le cartelle Vulnerabilita XX
index_vulnerabilities = 1
path_vulnerabilities = os.path.join("./list_vulnerabilities/", "Vulnerabilita " + str(index_vulnerabilities))
while os.path.exists(path_vulnerabilities):
    # Cerco le carelle Patch XX
    path_vulnerabilities = os.path.join("./list_vulnerabilities/", "Vulnerabilita " + str(index_vulnerabilities))
    index_patches = 1
    path_patches = os.path.join(path_vulnerabilities, "Patch " + str(index_patches))
    while os.path.exists(path_patches):
        path_patches = os.path.join(path_vulnerabilities, "Patch " + str(index_patches))
        codeFile = ""
        patchFile = ""
        if os.path.exists(path_patches):
            files = os.listdir(path_patches)
            # Memorizzo i percorsi dei file parent e patchfile
            for file in files:
                if "p_" in file:
                    codeFile = os.path.join(path_patches, file)
                if ".patch" in file:
                    patchFile = os.path.join(path_patches, file)
            AP_file = "AP_" + codeFile.split('\\')[-1].removeprefix("p_")
            file_path = os.path.join(path_patches, AP_file)
            file_1 = open(file_path, "w")

            # ----Applicazione della patch sul file parent ----

            # Lista delle righe del file
            firstList_remove = []  # Lista di indici e istruzioni inalterate e vecchie
            firstList_add = []  # Lista di indici e istruzioni inalterate e nuove
            secondList = []  # Lista A delle istruzioni in cambiate
            new_list = []  # Lista dove verranno inserite le nuove istruzioni
            index_list = []  # Lista per memorizzare coppie di indici del/add
            patch_list = []

            # Individuazione indici e istruzioni

            with open(patchFile) as fp:  # Lettura del file
                patch = fp.readlines()  # Righe della patch
                count = 2
                collect = False
                while count < len(patch):
                    if patch[count].startswith("@"):  # Individuazione inizio cambiamenti
                        collect = True
                        start_del = patch[count].split()[1]
                        start_add = patch[count].split()[2]
                        # index_remove = int(start_del.split(",")[0].removeprefix("-"))    # Indice per eliminare elementi
                        index_add = int(start_add.split(",")[0].removeprefix(
                            "+"))  # Indice per raggiungere il blocco istruzioni interessate
                        # index_list.append(index_remove)
                        # index_list.append(index_add)
                        patch_list.append(index_add)
                        # index_list = []
                        count += 1
                    if not patch[count].startswith("@"):
                        c = count
                        while c < len(patch) and not patch[c].startswith("@"):
                            secondList.append(patch[c])  # salvataggio istruzioni
                            c += 1
                        patch_list.append(secondList)
                        secondList = []
                        count = c
            print(patch_list)

            with open(codeFile) as cf:
                code_lines = cf.readlines()

            #### Indici per debug ####
            t = 0
            #########################
            initial_index = 0
            j = 0
            while j < len(patch_list):
                if isinstance(patch_list[j], int):
                    initial_index = patch_list[j]  # Cattura inidice da dove inserire/eliminare istruzioni
                if isinstance(patch_list[j], list):
                    index_change = 0
                    index = 0
                    z = 0
                    while z < len(patch_list[j]):
                        t = patch_list[j][z]
                        if patch_list[j][z].startswith("+"):
                            index_change = initial_index + index - 1
                            code_lines.insert(index_change, patch_list[j][z].removeprefix("+"))
                            patch_list[j][z] = "%+" + patch_list[j][z].removeprefix("+")  # Marco l'istruzione come DONE
                            z = 0
                            index = 0
                        elif patch_list[j][z].startswith("-"):
                            index_change = initial_index + index - 1
                            del code_lines[index_change]  # Elimina riga
                            patch_list[j][z] = "%-" + patch_list[j][z].removeprefix("-")  # Sostituisci carattere con %-
                            z = 0  # Ricomincia da capo
                            index = 0
                        elif patch_list[j][z].startswith("%-"):
                            z += 1  # ignora senza contarla come riga
                        else:
                            index += 1  # Conta righe
                            z += 1
                    index = 0
                j += 1

            for riga in code_lines:
                file_1.write(riga)  # Creazione file con le istruzioni vecchie eliminate e sostituite da
                # Spazio bianco
        index_patches += 1
    index_vulnerabilities += 1

'''
codeFile = "patches/route_c/route_eb9da2c1b60390802c48354f7d5c644c26a9e56f.c"
#testFile = "patches/route_c/route_aa6dd211e4b1dde9d5dc25d699d35f789ae7eeba.c"

patchFile = 'patches/route_c/patchfile.patch'
file_1 = open("file_1.c", "w+")     # Creazione di file_1 inizialmente vuoto
                              # Lista delle righe del file
firstList_remove = []                   # Lista di indici e istruzioni inalterate e vecchie
firstList_add = []                      # Lista di indici e istruzioni inalterate e nuove
secondList = []                         # Lista A delle istruzioni in cambiate
new_list = []                           # Lista dove verranno inserite le nuove istruzioni
index_list = []                         # Lista per memorizzare coppie di indici del/add
patch_list = []

# Individuazione indici e istruzioni

with open(patchFile) as fp:                     # Lettura del file
    patch = fp.readlines()                # Righe della patch
    count = 2
    collect = False
    while count < len(patch):
        if patch[count].startswith("@"):             # Individuazione inizio cambiamenti
            collect = True
            start_del = patch[count].split()[1]
            start_add = patch[count].split()[2]
            #index_remove = int(start_del.split(",")[0].removeprefix("-"))    # Indice per eliminare elementi
            index_add = int(start_add.split(",")[0].removeprefix("+"))  # Indice per raggiungere il blocco istruzioni interessate
            #index_list.append(index_remove)
            #index_list.append(index_add)
            patch_list.append(index_add)
            #index_list = []
            count += 1
        if not patch[count].startswith("@"):
            c = count
            while c < len(patch) and not patch[c].startswith("@"):
                secondList.append(patch[c])       # salvataggio istruzioni
                c += 1
            patch_list.append(secondList)
            secondList = []
            count = c
print(patch_list)

with open(codeFile) as cf:
    code_lines = cf.readlines()

#### Indici per debug ####
t = 0
#########################
initial_index = 0
j = 0
while j < len(patch_list):
    if isinstance(patch_list[j], int):
        initial_index = patch_list[j]              # Cattura inidice da dove inserire/eliminare istruzioni
    if isinstance(patch_list[j], list):
        index_change = 0
        index = 0
        z = 0
        while z < len(patch_list[j]):
            t = patch_list[j][z]
            if patch_list[j][z].startswith("+"):
                index_change = initial_index + index - 1
                code_lines.insert(index_change, patch_list[j][z].removeprefix("+"))
                patch_list[j][z] = "%+" + patch_list[j][z].removeprefix("+")        # Marco l'istruzione come DONE
                z = 0
                index = 0
            elif patch_list[j][z].startswith("-"):
                index_change = initial_index + index - 1
                del code_lines[index_change]                               # Elimina riga
                patch_list[j][z] = "%-" + patch_list[j][z].removeprefix("-")   # Sostituisci carattere con %-
                z = 0                                                       # Ricomincia da capo
                index = 0
            elif patch_list[j][z].startswith("%-"):
                z += 1                                          # ignora senza contarla come riga
            else:
                index += 1                                      # Conta righe
                z += 1
        index = 0
    j += 1

for riga in code_lines:
    file_1.write(riga)                          # Creazione file con le istruzioni vecchie eliminate e sostituite da
                                                # Spazio bianco
'''
