import lvl_plotter as ls

#transition for normalization
tran2_0 = 1178/5

#ground state
lvl0 = ls.Level(0,0,1,1)
#first excited state 2+
lvl1 = ls.Level(774,2,1,1)
lvl1.add_decay(0,1)
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
#unknown spin and parity
lvl11 = ls.Level(3222,"3224(2)\,\mathrm{keV}",1,-2)
lvl11.add_decay(1802,0.4/tran2_0)
#lvl11.add_decay(0,0.4/tran2_0)

#lvl12 = ls.level(2500,3,-1,2)
#lvl12.add_decay(1935,0.05/tran2_0)

lvl_list = [lvl for lvl in ls.level.getinstances()]

ls.plotter(lvl_list,1,"./140nd_ls.pdf",True,True,14)
