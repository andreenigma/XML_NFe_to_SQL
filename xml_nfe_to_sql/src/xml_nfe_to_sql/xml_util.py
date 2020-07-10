#!Python3

from lxml import etree

class ParentMapTree:

    def __init__(self, element_tree: etree._ElementTree):
        self.tree = element_tree
        self.parent_map_list = []
        self._map()

    def _map(self):
        self.parent_map_list = []        
        for el in self.tree.iter():
            for sub_el in el:
                aux_dictionary = {}
                aux_dictionary['element'] = sub_el
                aux_dictionary['parent_element'] = el
                self.parent_map_list.append(aux_dictionary)

    def print_map(self):        
        for el_map in self.parent_map_list:
            clean_ns_parent_tag = etree.QName(el_map['parent_element']).localname
            clean_ns_el_tag = etree.QName(el_map['element']).localname
            print ('parent_element: ' + clean_ns_parent_tag + '-> child_element: ' + clean_ns_el_tag)



def parent_map(element_tree: etree._ElementTree) -> dict:
    """Considerando que a estrutura etree._Element não quarda ponteiro para parent, esta função
    retorna um dicionário com a estrutura {child : parent , child2 : parent2, ...}, onde 'child'
    e 'parent' são objetos do tipo lxml.etree._Element. 

    Args:
        element_tree (etree._ElementTree): Arvore xml gerada no "parser" da biblioteca lxml.

    Returns:
        dict: Dicionário que relaciona os elementos da arvore do tipo _ElementTree com seus nós
        pais.
    """
    parent_map = dict((c, p) for p in element_tree.iter() for c in p)
    return parent_map

