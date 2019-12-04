from anytree import NodeMixin


class StructHolder(NodeMixin):
    def __init__(self, parent, children, prop=str, sign=str, str_found=int, position=int,
                 path=None, comment=str, scope=bool, is_closed=bool, mod=int, doc_comment=str(), row=str(), file_name=str()):
        self.is_closed = False
        self.scope = scope  # true = global, false = local
        self.comment = comment
        self.doc_comment = doc_comment
        self.row = row
        self.pathf = path
        self.sign = sign
        self.str_found = str_found
        self.position = position
        self.prop = prop
        self.mod = mod  # 0 = method, 1 = class, 2 = struct, 3 = interface, 4 = namespace, 5 = import, 6 = variable
        self.file_name = file_name
        self.parent = parent
        if children:
            self.children = children


class CatalogHierarchy(NodeMixin):
    def __init__(self, name, pathf, parent, children, file, way):
        self.name = name
        self.pathf = pathf
        self.parent = parent
        if children:
            self.children = children
        if file:
            self.file = file
        self.way = way

