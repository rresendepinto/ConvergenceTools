# ConvergenceTools
Collection of scripts to analyse convergent traits. work in progress, right now it still only has one tool 

## Plot convergence

With a list of species presenting a certain trait and a phylogenetic tree in newick format, will plot tree with highlighted branches for monophylectic groups that contain the target trait. It will also output a file where the species are attributed to the monophylectic groups where the trait appeared.

```
 python plot_convergence.py -t {tree.nwk} -s {target_species.tsv}
 ```
