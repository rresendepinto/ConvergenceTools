from ete3 import Tree, NodeStyle
import argparse as ap
import pandas as pd

parser= ap.ArgumentParser(description='show the multiple independent nodes in a tree where a convergent trait arose')

parser.add_argument('-s', '--trait', help='trait matrix showing the species where the trait is present')
parser.add_argument('-t', '--tree', default=None, help='tree file in newick or tree file suffix eg: *_filtTree.treefile')
parser.add_argument('-o', '--outfile', default='foreground.txt' ,  help='name of output file with the species ordered by monophylectic groups')

args = parser.parse_args()



def check_node_children(node, species_trait, nodes_origin):
    #list of nodes where trait originated
        
    node_children = node.get_children()
    
    #iterate through children nodes 
    for node in node_children:

        #if it is already in a terminal branch stop
        if node.is_leaf():
            #if terminal branch has trait, add to list of nodes 
            if node.name in species_trait:
                nodes_origin.append(node)

            continue
         
        species_node = node.get_leaf_names()

        #if species descendant of this node have the trait
        if any(sp in species_trait for sp in species_node):
            
            #if all species in this node have the trait
            if all(sp in species_trait for sp in species_node):

                nodes_origin.append(node)
                
            else:  
                #recursively check descendant nodes
                check_node_children(node, species_trait, nodes_origin)

        
#create a style for nodes where the trait arose and descendant nodes
style1 = NodeStyle()
style1["fgcolor"] = "red"
style1["vt_line_color"] = "red"
style1["hz_line_color"] = "red"
style1["vt_line_width"] = 2
style1["hz_line_width"] = 2
style1["vt_line_type"] = 2 # 0 solid, 1 dashed, 2 dotted
style1["hz_line_type"] = 2

t=Tree(args.tree, format=1) 


f = open(args.trait)
lines = f.readlines()

#this is the list of species that present the target trait
species_trait = [sp.strip() for sp in lines]

#check for monophyly in case species that present trait 
results = t.check_monophyly(species_trait, "name", ignore_missing=True)

if results[0]:
    #only present in one node     
    print('No convergence! Species with the trait form a monophylectic group')

else:
    
    common_ancestor = t.get_common_ancestor(species_trait)
    
    #list of nodes where the trait appeared independently
    nodes_origin = []

    check_node_children(common_ancestor, species_trait, nodes_origin)

    for node in nodes_origin:
        #change style of nodes of origin and descendant branches
        node.img_style = style1

        for desc_node in node.iter_descendants():

            desc_node.img_style = style1

    i = 1

    ##outfile with monophylectic group species for each node of origin
    with open(args.output, 'wt') as handle:
        for node in nodes_origin:
            
            for sp in node.get_leaf_names():

                handle.write(f'{str(i)}\t{sp}\n')

            i += 1
     



    
    t.show()

