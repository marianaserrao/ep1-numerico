from item_a import *
from item_b_c import *

item=input("Qual o item a ser solucionado (a, b ou c)?\n").lower()

if item=='a':
    item_a()
else:

    item_b_c(0 if item=='b' else 1)