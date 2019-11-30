import re
from classess import *


method_pattern = r'[a-zA-Z<>]+ [a-zA-Z][a-zA-Z0-9<>]* ?\(.*\)'
method_group_pattern = r'\(.*\) [a-zA-Z][a-zA-Z0-9<>]* ?\(.*\)'
class_pattern = r"class [A-Z][a-zA-Z0-9]*"
import_pattern = r'using [a-zA-Z][a-zA-Z0-9.]*'
namespace_pattern = r'namespace [A-Z][a-zA-Z0-9.]*'
struct_pattern = r'struct [a-zA-Z][a-zA-Z0-9]*'
interface_pattern = r'interface [a-zA-Z][a-zA-Z0-9]*'
non_indent_var_pattern = r'[a-zA-Z<>]+ [_a-zA-Z][a-zA-Z0-9<>.]* *;'
var_pattern = r'var [_a-zA-Z][a-zA-Z0-9<>]* = '


def is_comment_present(line=str()):
    pos = line.find('//')
    return pos


def is_single_string_comment(line=str()):
    pos = is_comment_present(line)
    if pos == -1:
        return False
    for ch in line[0:pos]:
        if ch != ' ':
            return False
    return True


def is_not_inside_a_string(line, pos):
    kcounter = 0
    jcounter = 0
    lcounter = 0
    for ch in line[0:pos]:
        if ch == '"':
            kcounter += 1
        if ch == "'":
            jcounter += 1
        if ch == "'":
            lcounter += 1
    if kcounter % 2 == 0 and jcounter % 2 == 0 and lcounter % 2 == 0:
        return True
    return False


def is_inline_comment(line=str()):
    pos = is_comment_present(line)
    if pos == -1:
        return False
    if is_not_inside_a_string(line, pos):
        return pos
    return False


def is_multy_string_comment_begin(line=str()):
    pos = line.find("/*")
    if pos == -1:
        return False
    for ch in line[0:pos]:
        if ch != ' ':
            return False
    return True


def is_multy_string_comment_end(line=str()):
    pos = line.find("*/")
    if pos == -1:
        return False
    if is_not_inside_a_string(line, pos):
        return pos
    return False


def is_doc_comment(line=str()):
    pos = line.find('///')
    if pos == -1:
        return False
    if is_not_inside_a_string(line, pos):
        return pos
    return False


def fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, row):
    prop = line[0:p.start() - 1]
    for ch in prop:
        if ch != ' ':
            prop = prop[prop.index(ch):len(prop)]
            break
    str_found = line_index
    # sign = line[p.start():len(line)-1]
    sign = p.group(0)
    flag = True
    for ch in prop:
        if ch != ' ':
            flag = False
    if flag:
        prop = ''
    position = 0
    new_path = list(path)
    if mod == 5 or mod == 4:
        prop = ' '
    if mod == 6 or mod == 5:
        new_path.append('var')
    scope = False
    if len(path) == 0 or len(path) == 1:
        scope = True
    if len(path) == 2:
        if re.search('namespace ', path[0]):
            scope = True
    for ch in line:
        if ch != ' ':
            position = line.index(ch)
            break
    return StructHolder(None, None, prop, sign, str_found, position, new_path, comment_buff, scope, False, mod, doc_comment_buff, row)


def fill_catalog_hierarchy(way, w):
    name = None
    if len(way) >= 1:
        n = way[len(way)-1]
        # if n.endswith(".cs"):
        #     name = n
        name = n
    return CatalogHierarchy(name, way, None, None, None, w)

strung = """ "" ''  //fdkindjgnfdjgd fgghfg drh"""

# print(is_single_string_comment(strung))
# print(is_inline_comment(strung))


