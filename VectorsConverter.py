import os


# --------------------------- VectorsConverter----------------------

def convert_to_vector(list_lines: list, vulnerable: int ):
    n_if = 0
    n_for = 0
    n_while = 0
    exist_int = 0
    exist_unsigned = 0
    exist_char = 0
    call_size_of = 0
    call_verbose = 0
    call_is_bad_offset = 0
    call_b_imm = 0
    call_emit_reg_move = 0
    call_emit_b = 0
    call_emit_nop = 0
    call_emit_bcond = 0
    call_pr_debug = 0
    call_rcu_read_unlock = 0

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
        if "verbose(" in element:
            call_verbose = 1
        if "is_bad_offset(" in element:
            call_is_bad_offset = 1
        if "b_imm(" in element:
            call_b_imm = 1
        if "pr_debug(" in element:
            call_pr_debug = 1
        if "emit_bcond(" in element:
            call_emit_bcond = 1
        if "emit_reg_move(" in element:
            call_emit_reg_move = 1
        if "emit_b(" in element:
            call_emit_b = 1
        if "emit_nop(" in element:
            call_emit_nop = 1
        if "rcu_read_unlock(" in element:
            call_rcu_read_unlock = 1

    vector = [n_if, n_for, n_while, exist_int, exist_unsigned, exist_char, call_size_of, call_verbose, call_is_bad_offset,
              call_b_imm, call_pr_debug, call_emit_bcond, call_emit_reg_move, call_emit_b,
              call_emit_nop, call_rcu_read_unlock, vulnerable]
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
path_functions_p = os.path.join("./old_functions/union_functions/", "union_functions_p/")
path_functions_c = os.path.join("./old_functions/union_functions/", "union_functions_c/")

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



