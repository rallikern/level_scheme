import lvl_plotter as ls

#transition for normalization
tran2_0 = 1178/5
#ground state
lvl0 = ls.Level(0,0,1,1)
#first excited state 2+
lvl1 = ls.Level(774,2,1,1)
lvl1.add_decay(0,1)
#second 0+
lvl2 = ls.Level(1300,0,1,2)
lvl2.add_decay(774,3.3/tran2_0,ind_energy=639)
#second 2+
lvl3 = ls.Level(1490,2,1,2)
lvl3.add_decay(774,16/tran2_0)
lvl3.add_decay(0,30/tran2_0)
#first 4+
lvl4 = ls.Level(1802,4,1,1)
lvl4.add_decay(774,105/tran2_0)
#first 3-
lvl5 = ls.Level(1935,3,-1,1)
lvl5.add_decay(774,3.3/tran2_0)
lvl5.add_decay(0,0.5/tran2_0)
#third 2+
lvl6 = ls.Level(2140,2,1,3)
lvl6.add_decay(0,0.75/tran2_0)
lvl6.add_decay(774,2.8/tran2_0)
#second 4+
lvl7 = ls.Level(2264,4,1,2)
lvl7.add_decay(774,4/tran2_0)
#third 3+
lvl8 = ls.Level(2400,4,1,3)
lvl8.add_decay(1490,3.6/tran2_0)
lvl8.add_decay(774,2.7/tran2_0)
# 6+
lvl9 = ls.Level(2950,(5,6),1,-1)
lvl9.add_decay(1802,3.4/tran2_0)
# 6+
lvl10 = ls.Level(2333,2,1,4)
#lvl10.add_decay(774,1.4/tran2_0)
#lvl10.add_decay(0,0.4/tran2_0)
# 6+
lvl11 = ls.Level(3222,"3224(2)\,\mathrm{keV}",1,-2)
lvl11.add_decay(1802,0.4/tran2_0)
#lvl11.add_decay(0,0.4/tran2_0)


lvl_list = [lvl for lvl in ls.Level.getinstances()]

ls.plotter(lvl_list, "./140nd_ls1.pdf", transition_label=True)
