# level_scheme
#
#This script produces level schemes
#
#IMPORT lvl_plotter.py file (The MAGIC happens there)
import lvl_plotter as ls
#First, you have to add levels (at least 2, otherwise it is pointless) to the class
#
#lvl = ls.level(ENERGY,SPIN,PARITY(0 or 1),i-th state with this SPIN and PARITY)
#
#lets produce a ground state
lvl0 = ls.Level(0,0,1,1)
#
#and a feeding state is necessary (first 2+ at 750 keV)
lvl1 = ls.Level(750,2,1,1)
#
#now let's add a decay
#lvl.add_decay(ENERGY OF FINAL STATE,WIDTH=corresponding to intensity)
lvl1.add_decay(0,1)
#
#List of all added levels
lvl_list = [lvl for lvl in ls.Level.getinstances()]
#
#Plot
#ls.plotter(LIST of LEVELS,BOOL(Transitions),FILENAME,BOOL(SAVEFIG),BOOL(TICKS),FONTSIZE)
#
ls.plotter(lvl_list, "./140nd_README.pdf")
