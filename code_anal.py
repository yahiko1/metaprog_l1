import re
from pp import *
from anytree import *
from queue import *
import os
import HTMLmaker


# access_modifiers
a_m = ['public', 'private', 'protected', 'internal', 'protected internal', 'private protected']
# basic data_types
d_t = ['bool', 'byte', 'sbyte', 'short', 'ushort', 'int', 'uint', 'long', 'float', 'double',
       'decimal', 'char', 'string', 'object']
rexId = re.compile(r'^[a-zA-Z]\w*$')
all_token_list = []


def run(filename):
    token_list = []
    path = []
    comment_buff = ""
    doc_comment_buff = ""
    state = 0
    flag = False
    f = open(filename, "r", encoding='utf-8')
    file = f.readlines()
    line_index = 0
    for l in file:
        line = l

        # is comment
        if state == 0:
            if is_doc_comment(line):
                flag = True
                doc_comment_buff += line
                line_index += 1
                continue
            if is_single_string_comment(line):
                flag = True
                comment_buff += line
                line_index += 1
                continue
            elif is_inline_comment(line):
                flag = True
                pos = is_comment_present(line)
                comment_buff += line[pos:len(line)]
                line = l[0:pos]
                # print(line)
            elif is_multy_string_comment_begin(line):
                # flag = True
                comment_buff += line
                if re.search("\*/ ?$", line):
                    line_index += 1
                    continue
                else:
                    state = 1
                    line_index += 1
                    continue
        if state == 1:
            comment_buff += line
            if is_multy_string_comment_end(line):
                state = 0
                line_index += 1
                continue

        # try to find and of some scope
        if re.search('}', line) and len(path) != 0:
            g = re.search('}', line).start()
            for each in token_list:
                if each.sign == path[len(path)-1] and each.position == g:
                    each.is_closed = True
                    path.pop(len(path)-1)
                    g = None
                    break

        # class pattern search
        if re.search(class_pattern, line) and not re.search(";$", line):
            if re.search("{$", line) or re.search("^ *{", file[file.index(l) + 1]):
                p = re.search(class_pattern, line)
                path.append(p.group(0))
                mod = 1  # class mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)
                p = None
                new_path = None

        # struct pattern search
        if re.search(struct_pattern, line) and not re.search(";$", line):
            if re.search("{$", line) or re.search("^ *{", file[file.index(l) + 1]):
                p = re.search(struct_pattern, line)
                path.append(p.group(0))
                mod = 2  # struct mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)
                p = None
                new_path = None

        # interface pattern search
        if re.search(interface_pattern, line) and not re.search(";$", line):
            if re.search("{$", line) or re.search("^ *{", file[file.index(l) + 1]):
                p = re.search(interface_pattern, line)
                path.append(p.group(0))
                mod = 3  # class mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)
                p = None
                new_path = None

        # namespace pattern search
        if re.search(namespace_pattern, line) and not re.search(";$", line):
            if re.search("{$", line) or re.search("^ *{", file[file.index(l) + 1]):
                p = re.search(namespace_pattern, line)
                path.append(p.group(0))
                mod = 4  # class mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)
                p = None
                new_path = None

        # import pattern search
        if re.search(import_pattern, line) and re.search(";$", line):
            p = re.search(import_pattern, line)
            mod = 5  # import mod ident
            token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
            token_list.append(token)
            all_token_list.append(token)
            line_index += 1
            continue

        # method pattern search
        if re.search(method_pattern, line) and re.search(";$", line) is None:
            if re.search(key_words, line) is None:
                if re.search("{$", line) or re.search("^ *{", file[file.index(l)+1]):
                    p = re.search(method_pattern, line)
                    path.append(p.group(0))
                    mod = 0  # method mod ident
                    token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                    token_list.append(token)
                    all_token_list.append(token)
                    p = None
                    new_path = None

        if re.search(method_group_pattern, line) and not re.search(";$", line):
            if re.search(key_words, line) is None:
                if re.search("{$", line) or re.search("^ *{", file[file.index(l)+1]):
                    p = re.search(method_group_pattern, line)
                    path.append(p.group(0))
                    mod = 0  # method mod ident
                    token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                    token_list.append(token)
                    all_token_list.append(token)
                    p = None
                    new_path = None

        # non indent var pattern search
        if re.search(non_indent_var_pattern, line):
            if re.search(key_words, line) is None:
                p = re.search(non_indent_var_pattern, line)
                mod = 6  # var mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)
                line_index += 1
                continue

        # var pattern
        if re.search(var_pattern, line):
            if re.search(key_words, line) is None:
                p = re.search(var_pattern, line)
                mod = 6  # var mod ident
                token = fill_struct_holder(line, p, mod, line_index, path, comment_buff, doc_comment_buff, line, filename)
                token_list.append(token)
                all_token_list.append(token)

        # comment buff cleaning stat
        if flag is False or state != 1:
            comment_buff = ""
            doc_comment_buff = ""
        flag = False

        # next line
        line_index += 1

    return token_list


def build_file_tree(t_l, filename):
    # build tree
    root = StructHolder(None, None, 'root', filename, -1, -1, None, None, True, True, -1)

    q = Queue()
    for i in range(0, len(t_l)):
        if len(t_l[i].pathf) == 0 or len(t_l[i].pathf) == 1:
            t_l[i].parent = root
            q.put(t_l[i])

    while not q.empty():
        target = q.get()
        lngs = len(target.pathf)
        for t in t_l:
            if len(t.pathf) == lngs + 1:
                flag = True
                for i in range(lngs):
                    if t.pathf[i] != target.pathf[i]:
                        flag = False
                if flag:
                    q.put(t)
                    t.parent = target

    return root


def build_catalog_tree(catalog_name):
    path_list = []
    for root, dirs, files in os.walk(catalog_name):
        way = os.path.join(root)
        w = way
        way = way.split('\\')
        path_list.append(fill_catalog_hierarchy(way, w))
        for file in files:
            if file.endswith(".cs"):
                way = os.path.join(root, file)
                w = way
                way = way.split('\\')
                path_list.append(fill_catalog_hierarchy(way, w))

    q = Queue()
    root = CatalogHierarchy('root', 'src', None, None, None, 'root')
    for token in path_list:
        if len(token.pathf) == 2:
            token.parent = root
            if not token.name.endswith(".cs"):
                q.put(token)

    while not q.empty():
        target = q.get()
        lngs = len(target.pathf)
        for t in path_list:
            if len(t.pathf) == lngs + 1:
                flag = True
                for i in range(lngs):
                    if t.pathf[i] != target.pathf[i]:
                        flag = False
                if flag:
                    t.parent = target
                    if not t.name.endswith(".cs"):
                        q.put(t)

    ways = ""
    answer = ""
    for pre, fill, node in RenderTree(root):
        treestr = u"%s%s  (%s)" % (pre, node.name, node.way)
        answer += treestr
        answer += '\n'
        ways += node.way
        ways += '\n'
        if node.is_leaf:
            w = node.way
            # token_list = run(node.way)
            # node.file = build_file_tree(token_list, node.way)

        print(treestr.ljust(8))

    return path_list, root, answer, ways


def show_file(root):
    for pre, fill, node in RenderTree(root):
        if node.sign == 'root':
            treestr = u"%s  (%s)" % (pre, node.sign)
        treestr = u"%s%s%s" % (pre, node.row, node.doc_comment)
        print(treestr.ljust(8))


def show_all_files(catalog_root):
    for pre, fill, node in RenderTree(catalog_root):
        if node.is_leaf and node.way.find('.cs') != -1:
            # print(node.way)
            token_list = run(node.way)
            node.file = build_file_tree(token_list, node.way)
            # show_file(node.file)


# res_dir = r'C:\yahiko\python_things\l1_v2\res'
res_dir = r'C:\yato\python_things\l1_v2\srcAzur'


def make_way(ways):
    way = ways.splitlines()
    new_way = ""
    for i in range(len(way)):
        w = str(way[i])
        aps = w.split('\\')
        word = ""
        for a in aps:
            word += a
            word += '.'
        new_way += word
        new_way += '\n'
    return new_way


def main():
    print("type key(f, c, cr): ")
    mode = input()
    print('type short path to "ANYNAME" crs folder (only name of src folder)')
    src = input()
    print('type full path to "ANYNAME" result folder')
    res = input()
    print('processing...')

    # src = r'srcAzur'
    # res = r'C:\yato\python_things\l1_v2\tazasho'

    p_l, catalog_root, answer, ways = build_catalog_tree(src)
    way = make_way(ways)

    show_all_files(catalog_root)
    HTMLmaker.create_index(res)
    HTMLmaker.create_article(answer, res, way)
    HTMLmaker.create_alphabet(all_token_list, res)
    HTMLmaker.create_root(res)
    HTMLmaker.create_dir_tree(res, catalog_root)

    # filename = r'PSObjectExtensions.cs'
    # token_list = run(filename)
    # root = build_file_tree(token_list, filename)
    # show_file(root)


main()
