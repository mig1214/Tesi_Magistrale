import os

def convert_to_vector(list_lines :list, vulnerable: int ):
    n_if = 0
    n_for = 0
    n_while = 0
    exist_int = 0
    exist_unsigned = 0
    exist_char = 0
    call_size_of = 0
    call_mutex_lock = 0
    call_unlikely = 0
    call_spin_lock = 0
    call_spin_unlock = 0
    call_printk = 0
    call_lock_sock = 0
    call_memcpy = 0
    call_memset = 0
    call_list_del_rcu = 0

    for element in list_lines:
        el = element
        if "if" in element.strip():
            n_if += 1
        if "for" in element:
            n_for += 1
        if "while" in element:
            n_while += 1
        if "int" in element:
            exist_int = 1
        if "unsigned" in element:
            exist_unsigned = 1
        if "char" in element:
            exist_char = 1
        if "sizeof(" in element:
            call_size_of = 1
        if "mutex_lock(" in element:
            call_mutex_lock = 1
        if "unlikely(" in element:
            call_unlikely = 1
        if "spin_lock(" in element:
            call_spin_lock = 1
        if "spin_unlock(" in element:
            call_spin_unlock = 1
        if "printk(" in element:
            call_printk = 1
        if "lock_sock(" in element:
            call_lock_sock = 1
        if "memcpy(" in element:
            call_memcpy = 1
        if "memset(" in element:
            call_memset = 1
        if "list_del_rcu(" in element:
            call_list_del_rcu = 1

    vector = [n_if, n_for, n_while, exist_int, exist_unsigned, exist_char, call_size_of, call_mutex_lock, call_unlikely,
              call_spin_lock, call_spin_unlock, call_printk, call_lock_sock, call_memcpy, call_memset,
              call_list_del_rcu,
              vulnerable]
    return vector



# Creo il nuovo file dove salvare tutti i vettori del file CON patch
file_name_c = "c_vectors.txt"
vector_path_c = os.path.join("./vectors/c_vectors/", file_name_c)
vector_file_c = open(vector_path_c, "w")

# Creo il nuovo file dove salvare tutti i vettori del file SENZA patch
file_name_p = "p_vectors.txt"
vector_path_p = os.path.join("./vectors/p_vectors/", file_name_p)
vector_file_p = open(vector_path_p, "w")

# Cerco i file delle funzioni
path_functions_p = os.path.join("./functions/", "functions_p/")
path_functions_c = os.path.join("./functions/", "functions_c/")

functions_p = os.listdir(path_functions_p)
functions_c = os.listdir(path_functions_c)

for element in functions_p:
    parent_file = open(path_functions_p + element)
    with parent_file as pf:
        parent_lines = pf.readlines()
    list_p = convert_to_vector(parent_lines, 1)
    vector_file_p.write(", ".join(str(element) for element in list_p))
    vector_file_p.write("\n")


for element in functions_c:
    child_file = open(path_functions_c + element)
    with child_file as cf:
        child_lines = cf.readlines()
    list_c = convert_to_vector(child_lines, 0)
    vector_file_c.write(", ".join(str(element) for element in list_c))
    vector_file_c.write("\n")


vector_file_p.close()
vector_file_c.close()



