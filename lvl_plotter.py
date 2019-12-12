import numpy as np
import weakref
from numpy import random
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

#the class level inhabits the characteristics of a level, energy,spin, parity, band and decays
#and additionally the maximal energy of a state in the level scheme
class level(object):
    energies = []
    
    try:    
        max_en = max(energies)
    except:
        print('')
        
        
    _instances = set()

    
        

     
    def __init__(self, energy, spin, parity, number):
        self.energies.append(energy)
        self.en = energy
        self.spin = spin
        self.par = parity
        self.num = np.abs(number)
        self.sig = np.sign(number)
        self.decay = []
        self._instances.add(weakref.ref(self))

    def add_decay(self,t_en,t_int):
        if t_en not in [self.decay[l][0] for l in range(len(self.decay))]:
            self.decay.append([t_en,t_int])
      
    @classmethod
    def getinstances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead    
           


            
            
    
def plotter(lvl_list,onoff,name,onoff_pic,onoff_tick,fontsize):
    
    ##################
    #default parameter
    #change the parameter like you want
    ##################
    
    arrow_angle = 0.0002					#angle of the transitions
    lvl_width = 1							#width of a level
    transition_space = 0.5 *lvl_width		#default space between decays from one level
    fontsize = fontsize						#Fontsize
    lvl_space = .75*lvl_width				#space between levels
    lvl_short = 0.0							#
    tran_width = 20							#width of the transitions
    dist_2_axis = lvl_space + 0.5*lvl_width		#space between level of the western most and the y-axis 
    ylim_up = 100							#In addition with the highest energy = upper limit of the yaxis
    ylim_down= -150 						#lower limit of the yaxis
    figsize = (4,4)							#absolute size of the plot
    shrink_factor = 25						#shrinks the arrow, so there is no overlap between the starting and ending point and the levels
    
    
    ######################################
    #Plot statrts
    ######################################
        
    fig,ax = plt.subplots(figsize=figsize)
    parameter = [arrow_angle,transition_space,fontsize,lvl_width,lvl_space,lvl_short,tran_width]
    tranni = trans(lvl_list,onoff,*parameter,fig,ax,shrink_factor)
    maxi = lvl_scheme(lvl_list,onoff,*parameter,*tranni)
    maxi[4].set_ylim(ylim_down,maxi[2]+ylim_up)
    maxi[4].set_xlim(maxi[0]-dist_2_axis,maxi[1]+dist_2_axis)
    #maxi[4].plot([maxi[0]-0.75,maxi[0]-.75], [-150, maxi[2]+100], color='k', linestyle='-', linewidth=1)
    
    ###########
    #Tick and label setup
    ###########
    
    if onoff_tick:
        maxi[4].set_ylabel(r'Energy (keV)',size = fontsize)
    maxi[4].tick_params(top=False, bottom=False, left=onoff_tick, right=False, labelleft=onoff_tick, labelbottom=False)
    maxi[4].spines['top'].set_visible(False)
    maxi[4].spines['right'].set_visible(False)
    maxi[4].spines['bottom'].set_visible(False)
    maxi[4].spines['left'].set_visible(onoff_tick)   
    
    ###########
    #saving yes or no
    ###########
    
    if onoff_pic:
        maxi[3].savefig(name,bbox_inches="tight")
    else:
        print("sorry,no picture for you")
    #plt.show()
    
    return [maxi[3],maxi[4]]

#This function is used to connect the parity sign to a state
def parity(x):
    if x == 1:
        par = '+'
    elif x == -1:
        par = '-'
    else:
        par = ' '
    return par


#finding the smallest distance between to lines in a MC mehtod
#stupid, but it works fast
def r2distance_2lines(x_start1,x_end1,x_start2,x_end2,en11,en12,en21,en22):
    
    #which lines is in front of the other?
    sign = np.sign(x_start1+en11/10000-x_start2+en12/10000)
    
    iterations = 100000
    
    ##############
    #starting the distance determination
    ##############
    
    #random positions on the arrows
    rd1 = np.random.uniform(0,1,iterations)
    rd2 = np.random.uniform(0,1,iterations)
    point1x = x_start1+rd1*(-x_start1+x_end1)
    point1y = en11+rd1*(-en11+en12)
    point2x = x_start2+rd2*(-x_start2+x_end2)
    point2y = en21+rd2*(-en21+en22)
    
    #distance between two random points in different arrows
    dist_x = (point1x-point2x)**2
    dist_y = (point1y-point2y)**2
    
    #smallest distance
    dist = np.min(np.sqrt(dist_y+dist_x))
    return [dist,sign]


#Determination of the right place of the transitions (x and y coordinates)
#return "tran_param", which is a list of the initial and final energy and the band (first, second .... state of a certain spin and parity)
def trans(lvl_list,onoff,arrow_angle,transition_space,fontsize,lvl_width,lvl_space,lvl_short,tran_width,fig,ax,shrink_factor):
    tran_param = []
    neg_shift,pos_shift = 0,0
    x_end_list = []
    

    
    ###################################################
    #start of the Iteration over all levels (inital states)
    ###################################################
    
    for i in lvl_list:
        
        k = 0
        
        #################
        #Every Transition gets a default location, suited to the energy,spin,number and parity of the initial level
        #################
        
        if i.par != -1:
            xdata = [(i.num-neg_shift)*lvl_width-lvl_width+(lvl_space*(i.num-1)),(i.num+pos_shift)*lvl_width+(lvl_space*(i.num-1))]
        else:
            xdata = [-(i.num)*(lvl_width+lvl_space),-(i.num)*(lvl_width+lvl_space) + lvl_width]
        
        ydata = [i.en,i.en]
        
        ###################################################
        #start of the Iteration over all potential decays (final states)
        ###################################################

        for j in lvl_list:
            
            #number of decays
            num_tran = len(i.decay)
            
            for l in range(num_tran):
                
                #############
                #detailed placement. It depends on the number of decays of a state and potential overlaps
                #############
                
                x_offset = (lvl_width-(num_tran-1)*transition_space)/2
                
                #the (head) width is proportional to the intensity
                width = tran_width * i.decay[l][1]
                headwidth = np.max([2 * width,5])
                
                ###########
                #It is a final level of a initial state's decay
                ###########
                
                if j.en == i.decay[l][0]:
                    
                    #the k-th decay of the inital state
                    k += 1
                    
                    #X shift. It depends on k
                    if i.par == -1:
                        x_start = xdata[0]+(transition_space*(num_tran-k))+x_offset
                    else:
                        x_start = xdata[0]+(transition_space*(k-1))+x_offset
                    
                    tran_param.append([j.en,i.num,i.par,j.num,j.par])
                    
                    ################
                    #Plot starts
                    ################
                    
                    #plot parameters
                    shrink = shrink_factor / abs(i.en-j.en)
                    arrow_angle_temp = arrow_angle
                    
                    #If the flag onoff is "1", than the transitions will be included in the level scheme
                    if onoff == 1:
                        
                        #vertical arrows for transitions inside a band.
                        if i.num == j.num and i.par==j.par:
                            arrow_angle_temp = 0
                        
                        #x pos for the end of the arrow
                        x_end = x_start-(i.par*arrow_angle_temp*(i.en-j.en))
                        
                        ##################
                        #Avoiding overlap of arrows
                        ##################
                        
                        #3 loops to ensure, that a shifted arrow does not overlap with another arrow, which was in the loop before the shift happens
                        for lolli in range(3):
                            
                            for p in x_end_list:
                                
                                #distance between the actual transition (p) and transitions which were in the loop before (x_end_list)
                                dist,sign = r2distance_2lines(x_start,x_end,p[0],p[1],i.en,j.en,p[2],p[3])
                                
                                #the x coordinates will be changed until the distance condition is finally fullfilled
                                while dist < 0.49*transition_space and (i.en >= p[3] or j.en <= p[3]):
                                    x_end += (sign*0.01*transition_space)
                                    x_start += (sign*0.01*transition_space)
                                    dist = r2distance_2lines(x_start,x_end,p[0],p[1],i.en,j.en,p[2],p[3])[0]
                        
                        #If the starting point of the arrow is shifted away from the level line, it is shifted by the length of the level line back            
                        if x_start > xdata[1]:
                            x_start = x_start - lvl_width
                            x_end = x_end - lvl_width
                        
                        #stats of the transition
                        x_end_list.append([x_start,x_end,i.en,j.en])
                        
                        ########
                        #actual plot of one arrow...
                        ########
                        
                        ax.annotate("", xy=(x_end, j.en), xytext=(x_start, i.en),arrowprops=dict(width=width,headwidth=headwidth,facecolor='black',shrink=shrink))
                    
    return [tran_param,fig,ax]
    


#Plotting of the final levels. It depends also on the transitions
def lvl_scheme(lvl_list,onoff,arrow_angle,transition_space,fontsize,lvl_width,lvl_space,lvl_short,tran_width,tran_param,fig,ax):
    
    y_max = []
    x_max = []
    x_min = []
    
    ###########
    #Loop over all levels
    ###########
    
    for i in lvl_list:
        
        #same default location as in function trans
        if i.par != -1:
            xdata = [ (i.num-1)*(lvl_width+lvl_space), (i.num-1)*(lvl_width+lvl_space) + lvl_width]
        else:
            xdata = [-(i.num)*(lvl_width+lvl_space),-(i.num)*(lvl_width+lvl_space) + lvl_width]
        ydata = [i.en,i.en]
        
        xdata_def,ydata_def = xdata,ydata
        
        
        ##############
        #Enlargement of the level line due to arrows decaying on this state
        ##############
        
        if i.par != -1:
            
            #enlargement to the right
            try:
                pos_shift = (np.max([tran_param[l][1] for l in range(len(tran_param)) if tran_param[l][0] == i.en and tran_param[l][2] == 1])-i.num)*((lvl_width+lvl_space)/lvl_width) - lvl_short
            except:
                pos_shift = 0
            
            #enlargement to the left
            try:
                neg_shift = (np.max([tran_param[l][1] for l in range(len(tran_param)) if tran_param[l][0] == i.en and tran_param[l][2] == -1])+i.num) + lvl_short
            except:
                neg_shift = 0
            
            #no transitions -> no enlargements
            if onoff == 0:
                pos_shift,neg_shift = 0,0
            
            #I don't know anymore why this is necessary, but an enlargement should not be a shortage
            if pos_shift < 0:
                pos_shift = 0
            
            #new xdata
            xdata = [(i.num-neg_shift-1)*lvl_width+(lvl_space*(i.num)),(i.num+pos_shift)*lvl_width+(lvl_space*(i.num-1))]
        else:
            
            #the same for negative parity bands
            try:
                pos_shift = (np.max([tran_param[l][1] for l in range(len(tran_param)) if tran_param[l][0] == i.en and tran_param[l][2] == 1])-1)*((lvl_width+lvl_space)/lvl_width) - lvl_short
            except:
                pos_shift = 0
            try:
                neg_shift = np.max([tran_param[l][1] for l in range(len(tran_param)) if tran_param[l][0] == i.en and tran_param[l][2] == -1])-i.num-lvl_short
            except:
                neg_shift = 0
            if onoff == 0:
                pos_shift,neg_shift = 0,0
            xdata = [-(i.num+neg_shift)*(lvl_width+lvl_space),-(i.num-pos_shift)*(lvl_width+lvl_space)]
                
        ydata = [i.en,i.en]
        
        #################
        #Plot starts
        #################
        
        #minima and maxima. Necessary for the size of the plot
        y_max.append(ydata[0])
        x_max.append(xdata[1])
        x_min.append(xdata[0])
        
        #
        #Position of the states' labels
        #
        #If the number of a state is negative, it is only used for positioning, not for labeling
        #
        
        if i.sig == 1:
            indice = '_'+str(i.num)
        else:
            indice = ' '
        
        if i.par == -1:
            shifty = xdata[0]-0.5*lvl_width
        else:
            shifty = xdata[1]+0.1*lvl_width
        #If the the spin is unknown, the parity is probably also unknown
        if isinstance(i.spin,str): 
        	pari = ''
        else:
            pari = '^'+parity(i.par)
        
        ax.text(shifty, i.en-50, r"$"+str(i.spin)+pari+indice+"$",size=fontsize)
        ax.plot(xdata_def,ydata_def,'-',color='black',lw=2)
        ax.plot(xdata,ydata,'--',color='black')
    return [np.min(x_min),np.max(x_max),np.max(y_max),fig,ax]

