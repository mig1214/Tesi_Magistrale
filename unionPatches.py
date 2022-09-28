import os
from natsort import os_sorted


# --------------------------- Union Patches -----------------------------------
path_vul = "./list_vulnerabilities/"
list_directories = os_sorted(os.listdir(path_vul))

all_patches = os.path.join(path_vul, "all_patches.txt")
file_all_patches = open(all_patches, "w")
for directory in list_directories:
    path_patch = path_vul + directory
    list_patches = os_sorted(os.listdir(path_patch))
    print(directory)
    for element in list_patches:
        if "Patch " in element:
            print(element)
            files_patch = os.listdir(path_patch+"/"+element)
            for patchfile in files_patch:
                if ".patch" in patchfile:
                    name_patch = path_patch+"/"+element+"/"+patchfile
                    patch = open(name_patch)
                    with patch as pt:
                        patch_lines = pt.readlines()
                    for istruction in patch_lines[2:]:
                        print(istruction)
                        row = istruction.replace("\t", "")
                        if istruction.startswith("-"):
                            row = row.removeprefix("-")
                        if istruction.startswith("+"):
                            row = row.removeprefix("+")
                        file_all_patches.write(row)
                        file_all_patches.write("\n")




