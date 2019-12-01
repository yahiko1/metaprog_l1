
# from code_anal import *
# from classess import *
#
# filename = r'src\Новая папка\5.txt'
# token_list = run(filename)

from pp import *

key_words = ''' as | base | break | case | catch | checked | continue 
| default | do | else | event | explicit | extern | false | fixed 
| for | foreach | goto | if | implicit | in | is | lock | new | null |
| operator | verride | params | ref | sealed 
| sizeof | stackalloc | switch | this | throw | try | typeof | uint 
| unchecked | unsafe | while '''

str1 = '        public static bool TryGetProperty<T>(this PSObject source, string null name, out T propertyValue)'

if re.search(key_words, str1) is None:
    print(re.search(key_words, str1))