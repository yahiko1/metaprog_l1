import os
from sys import argv
from datetime import datetime
from anytree import *


path = ''
left_block = ''
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
            'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
alphabet_up = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def html_template(file):
    file.write(
        '''<!DOCTYPE html>
        <html lang="en">
        <head>
            <title>doc_builder</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
        </head>
        <body>
                ''')


def html_cs_template(file, html_name):
    answer = ""
    for pre, fill, node in RenderTree(file):
        treestr = u"%s%s  %s" % (pre, node.prop, node.sign)
        answer += treestr
        answer += '\n'
        answer += node.doc_comment.replace('<', '%')
    f = open(html_name, "w", encoding='utf-8')
    html_template(f)
    f.write('''
        <div class="container-fluid">
            <h1>C#Doc</h1>
            <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('''</p></div>
        <div class="row">
            <div class="col-sm-15 list-group" style="overflow: auto; margin: 10px;"> <h4>html_name</h4>
                ''')
    lines = answer.splitlines()
    for line in lines:
        f.write('<p>' + line.replace(' ', '&nbsp;') + '</p>')
    # f.write(answer.replace('\n', '<br>'))
    f.write('</div> </div>  </body>')
    f.close()


def create_article(answer, res_dir, ways):
    f = open(res_dir + r'\article.html', "w", encoding='utf-8')
    html_template(f)
    f.write('''
    <div class="container-fluid">
        <h1>C#Doc</h1>
        <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('''</p></div>
    <div class="row">
        <div class="col-sm-15 list-group" style="overflow: auto; margin: 10px;"> <h4>Article</h4>
            ''')
    lines = answer.splitlines()
    way = ways.splitlines()
    for i in range(len(lines)):
        w = way[i]
        # w.replace('\\', '.')
        f.write('<a href="' + res_dir + r'\ ' + w + 'html' + '" style="width:auto; font-size:10px">' +
                lines[i].replace(' ', '&nbsp;') + '</a>')
    # f.write(answer.replace('\n', '<br>'))
    f.write('</div> </div>  </body>')
    f.close()


def create_index(res_dir):
    f = open(res_dir + r'\index.html', "w", encoding='utf-8')
    html_template(f)
    f.write('''
        <div class="container-fluid">
            <h1>C#Doc</h1>
            <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('</div> </p> <div> <p>')
    f.write('<a href="' + res_dir + r'\article.html' + '" style="width:auto; font-size:40px">' + 'article' + '</a>')
    f.write('</p> </div> <div> <p>')
    f.write('<a href="' + res_dir + r'\dir_tree.html' + '" style="width:auto; font-size:40px">' +
            'directory tree' + '</a>')
    f.write('</p> </div> <div> <p>')
    f.write('<a href="' + res_dir + r'\alphabet.html' + '" style="width:auto; font-size:40px">' +
            'alphabetic index' + '</a>')
    f.write('</p> </div>  </body>')
    f.close()


def create_root(res_dir):
    f = open(res_dir + r'\dir_tree.html', "w", encoding='utf-8')
    html_template(f)
    f.write('''
           <div class="container-fluid">
               <h1>C#Doc</h1>
               <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('</div> </p> <div> <p>')
    f.write('<a href="' + res_dir + r'\ root.html' + '" style="width:auto; font-size:40px">' + 'root' + '</a>')
    f.write('</p> </div>   </body>')
    f.close()


def create_target_html(res_dir, node):
    child = node.children
    if len(child) == 0 and node.way.find('.cs') != -1:
        w = node.way.replace('\\', '.')
        name = res_dir + r'\ ' + w + ".html"
        # print(name, w)
        html_cs_template(node.file, name)
    else:
        w = node.way.replace('\\', '.')
        # print(w)
        f = open(res_dir + r'\ ' + w + '.html', "w", encoding='utf-8')
        html_template(f)
        f.write('''
                        <div class="container-fluid">
                            <h1>C#Doc</h1>
                            <div><p>''')
        f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
        f.write('</div> </p> <div> <p>')
        for ch in child:
            w = ch.way.replace('\\', '.')
            # print(w)
            f.write('<p>' + '<a href=" ' + res_dir + r'\ ' + w + ".html"
                    + ' " style="width:auto; font-size:40px">' + ch.name + '</a>' + '</p>')
        f.write('</div> </p>')


def create_dir_tree(res_dir, catalog_root):
    for pre, fill, node in RenderTree(catalog_root):
        create_target_html(res_dir, node)


def create_alphabet(all_token_list, res_dir):
    f = open(res_dir + r'\alphabet.html', "w", encoding='utf-8')
    html_template(f)
    f.write('''
               <div class="container-fluid">
                   <h1>C#Doc</h1>
                   <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('</div> </p> <div>')
    for it in range(len(alphabet)):
        f.write('<p>' + '<a href=" ' + res_dir + r'\ ' + alphabet[it] + ".html"
                + ' " style="width:auto; font-size:20px">' + alphabet[it] + '</a>' + '</p>')
        create_alphabetic_target(res_dir, alphabet[it], alphabet_up[it], all_token_list)


def create_alphabetic_target(res_dir, alpha, alpha_up, all_token_list):
    f = open(res_dir + r'\ ' + alpha + '.html', "w", encoding='utf-8')
    html_template(f)
    f.write('''
                   <div class="container-fluid">
                       <h1>C#Doc</h1>
                       <div><p>''')
    f.write('Date of generation - ' + str(datetime.utcnow()) + '<br>Version of generator - 2.1')
    f.write('</div> </p> <div>')
    for token in all_token_list:
        if token.sign.startswith(alpha) or token.sign.startswith(alpha_up):
            f.write('<p>' + token.sign + ' (' + str(token.mod) + ') ' + '<p>')