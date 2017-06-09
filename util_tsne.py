import numpy as np
import matplotlib.pyplot as plt
from matplotlib import offsetbox
from sklearn import (manifold, datasets, decomposition, ensemble,
                     discriminant_analysis, random_projection)

from mpl_toolkits.mplot3d import Axes3D
import pylab

## interactive in notebook
#%matplotlib notebook


def predit_bs_tsne(X, bs):
    
    #from scipy.spatial import distance
    
    rows, cols = X.shape
    print('input X dims : {} x {}'.format(rows, cols))
    
    print 'Warning: the input kernel should be in the last row'
    inputX = X[-1,:]
    
    dist_dd = {}

    for i in range(rows - 1):
        data = X[i,:]
        dist = np.linalg.norm(data - inputX)
        #dist = distance.euclidean(data, inputX)
                              
        print('row {} : dist={}'.format(i, dist))
        dist_dd[i] = dist

    #print dist_dd

    # sort the distance
    from operator import itemgetter
    dist_sort = sorted(dist_dd.items(), key=itemgetter(1))
    
    print('Top 3 distance : {} , {} ,{}'.format(dist_sort[0][1], dist_sort[1][1], dist_sort[2][1]))
    
    # select the nearest three
    r1,r2,r3 = dist_sort[0][0], dist_sort[1][0], dist_sort[2][0]
    
    print('Top 3 rows : {} , {} ,{}'.format(r1, r2, r3))
    print('Top 3 ranking : {} , {} ,{}'.format(bs[r1], bs[r2], bs[r3] ))
    
    # return top 3 neighours, their block size
    return [r1,r2,r3], [bs[r1], bs[r2], bs[r3]]



#------------------------------------------------------------------------------
# plot tsne in 3d
#------------------------------------------------------------------------------
def plot_tsne_3d(X_tsne, y):
    
    # http://stackoverflow.com/questions/10374930/matplotlib-annotating-a-3d-scatter-plot
    # area = np.pi * (15 * np.random.rand(10))**2
    area = np.pi * (15 * 0.5)**2
    
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    
    
    # annotate: for each training kernel
    for i, bs in enumerate(y):
        data_color = None
        sym = None
        if bs == 32:
            data_color = 'b'; sym = ">"
        elif bs == 64:
            data_color = 'g'; sym = (5, 0)
        elif bs == 128:
            data_color = 'r'; sym = (5, 1)
        elif bs == 256:
            data_color = 'c'; sym = (5, 2)
        elif bs == 512:
            data_color = 'm'; sym = 'o'
        elif bs == 1024:
            data_color = 'y'; sym = 'v'
        elif bs == 16:
            data_color = 'k'; sym = (5, 3)
        elif bs == 768:
            data_color = '#4568a0'; sym = "1" 
        else:
            raise Exception('Unknow block size')

    #     ax.scatter(X_tsne[i,0], X_tsne[i,1], X_tsne[i,2],
    #               c=data_color,
    #               s=area,
    #               alpha=0.5,
    #               marker=sym)

    
        # note: marker could be added, but here we simplified the figure
        ax.scatter(X_tsne[i,0], X_tsne[i,1], X_tsne[i,2],  # coord for each data point
              c=data_color,
              s=area,
              alpha=0.5)

        # annotate the block size for each data point
        ax.text(X_tsne[i,0], X_tsne[i,1], X_tsne[i,2],
                '%s' % (str(bs)), size=10, zorder=1,color='k') 
    
    
    # annotate the input kernel (last kernel)
    ax.scatter(X_tsne[-1,0], X_tsne[-1,1], X_tsne[-1,2],
              c='k',
              s=area,
              alpha=0.9,
              marker=(5, 1))
    
    plt.show()


#------------------------------------------------------------------------------
# plot tsne in 2d
#------------------------------------------------------------------------------
def plot_tsne_2d(X_tsne_2d, y, top3rows):
    area = np.pi * (20 * 0.6)**2
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    
    # annotate
    for i, bs in enumerate(y):
        data_color = None
        sym = None
        lb = None
        if bs == 32:
            data_color = 'b'; sym = ">"; lb = 'bs-32'
        elif bs == 64:
            data_color = 'g'; sym = (5, 0); lb = 'bs-64'
        elif bs == 128:
            data_color = 'r'; sym = (5, 1); lb = 'bs-128'
        elif bs == 256:
            data_color = 'c'; sym = (5, 2); lb = 'bs-256'
        elif bs == 512:
            data_color = 'm'; sym = 'o'; lb = 'bs-512'
        elif bs == 1024:
            data_color = 'y'; sym = 'v'; lb = 'bs-1024'
        elif bs == 16:
            data_color = 'k'; sym = (5, 3); lb = 'bs-16'
        elif bs == 768:
            data_color = '#4568a0'; sym = "1"; lb = 'bs-768' 
        else:
            raise Exception('Unknow block size')


        ax.scatter(X_tsne_2d[i,0], X_tsne_2d[i,1],
              c=data_color,
              s=area,
              alpha=0.5,
              label=lb     # label for different block size
              )

        ax.text(X_tsne_2d[i,0], X_tsne_2d[i,1],
                '%s' % (str(bs)), size=30, zorder=3,color='k')
    
   # annotate the input kernel (last kernel)
    ax.scatter(X_tsne_2d[-1,0], X_tsne_2d[-1,1],
              c='k',
              s=area,
              alpha=0.9,
              marker=(5, 1)) 

    #
    # legend for different block size
    #
    #ax.legend()
    #plt.legend(loc='upper left', numpoints=1, ncol=3, fontsize=8, bbox_to_anchor=(0, 0))

    
    #
    # draw a line between input_kernel and the top3 nearest node
    #
    import matplotlib.patches as mpatches
    el = mpatches.Ellipse((0.3, 0.3), 0.3, 0.4, angle=30, alpha=0.2)
    
    # top 3 connection
    for pos in top3rows:
        ax.annotate("", 
                xy=(X_tsne_2d[pos, 0], X_tsne_2d[pos,1]), 
                xytext=(X_tsne_2d[-1,0], X_tsne_2d[-1,1]),
                arrowprops=dict(arrowstyle="-", 
                                color="0.6",
                                patchB=el,
                                shrinkB=5,  connectionstyle="arc3,rad=0.1",),
                )

    # bold the axis line
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(3)
        
    # remove ticks
    plt.xticks([])
    plt.yticks([])
    
    plt.show()



def plot_tsne_2d_v1(X_tsne_2d, y, y_name, top3rows, figname=None, kernelname=None,
        xtitle=None):
    area = np.pi * (15 * 0.6)**2

    txtFont = 13
    legFont = 11
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    x_bs16,   y_bs16   = [], []
    x_bs32,   y_bs32   = [], []
    x_bs64,   y_bs64   = [], []
    x_bs128,  y_bs128  = [], []
    x_bs256,  y_bs256  = [], []
    x_bs512,  y_bs512  = [], []
    x_bs768,  y_bs768  = [], []
    x_bs1024, y_bs1024 = [], []

    bs_dd = {} 

    # annotate
    for i, bs in enumerate(y):
        data_color = None
        sym = None
        lb = None
        if bs == 32:
            data_color = 'b'; sym = ">"; lb = 'bs-32'
            x_bs32.append(X_tsne_2d[i,0])
            y_bs32.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 64:
            data_color = 'g'; sym = (5, 0); lb = 'bs-64'
            x_bs64.append(X_tsne_2d[i,0])
            y_bs64.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 128:
            data_color = 'r'; sym = (5, 1); lb = 'bs-128'
            x_bs128.append(X_tsne_2d[i,0])
            y_bs128.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 256:
            data_color = 'c'; sym = (5, 2); lb = 'bs-256'
            x_bs256.append(X_tsne_2d[i,0])
            y_bs256.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 512:
            data_color = 'm'; sym = 'o'; lb = 'bs-512'
            x_bs512.append(X_tsne_2d[i,0])
            y_bs512.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 1024:
            data_color = 'y'; sym = 'v'; lb = 'bs-1024'
            x_bs1024.append(X_tsne_2d[i,0])
            y_bs1024.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 16:
            data_color = 'k'; sym = (5, 3); lb = 'bs-16'
            x_bs16.append(X_tsne_2d[i,0])
            y_bs16.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 768:
            data_color = '#4568a0'; sym = "1"; lb = 'bs-768' 
            x_bs768.append(X_tsne_2d[i,0])
            y_bs768.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        else:
            raise Exception('Unknow block size')


        # annotate Kernel Name
        ax.text(X_tsne_2d[i,0]+15, X_tsne_2d[i,1]-5,
                #'%s' % (str(y_name[i])), size=17, zorder=2, color='k')
                '%s' % (str(y_name[i])), size=txtFont, zorder=2, color='k')

    
   # annotate the input kernel (last kernel)
    ax.scatter(X_tsne_2d[-1,0], X_tsne_2d[-1,1],
              c='k',
              s=area,
              alpha=0.9,
              marker=(5, 1)) 

    if kernelname <> None:
        ax.text(
                #X_tsne_2d[-1,0]-50, X_tsne_2d[-1,1]+40,   # hmm_gammaobs
                #X_tsne_2d[-1,0]-50, X_tsne_2d[-1,1]-40,   # hmm_expectmu
                X_tsne_2d[-1,0]-20, X_tsne_2d[-1,1]+40,    # mcx
                '%s' % (str(kernelname)), size=txtFont, zorder=2, color='k')



    for key, val in bs_dd.iteritems():
        #print key, val
        if key == 'bs-32':
            data_color = '#66c2ff'; sym = ">";
            b32 = ax.scatter(x_bs32, y_bs32, c=data_color, s=area,  alpha=0.9, label="bs-32", hatch='/////')
        elif key == 'bs-64':
            data_color = '#4dffa6';
            b64 = ax.scatter(x_bs64, y_bs64, c=data_color, s=area, alpha=0.8, label="bs-64", hatch='***')
        elif key == 'bs-128':
            data_color = 'r'; sym = (5, 1);
            b128 = ax.scatter(x_bs128, y_bs128, c=data_color, s=area, alpha=0.4, label="bs-128", lw=2)
        elif key == 'bs-256':
            data_color = 'c'; sym = (5, 2);
            b256 = ax.scatter(x_bs256, y_bs256, c=data_color, s=area, alpha=0.99, label="bs-256", hatch='xxx')
        elif key == 'bs-512':
            data_color = 'm'; sym = 'o';
            b512= ax.scatter(x_bs512, y_bs512, c=data_color, s=area, alpha=0.3, label="bs-512")
        elif key == 'bs-1024':
            data_color = 'y'; sym = 'v';
            b1024= ax.scatter(x_bs1024, y_bs1024, c=data_color, s=area, alpha=0.9, label="bs-1024", hatch='----')
        elif key == 'bs-16':
            data_color = '#cce6ff';
            b16 = ax.scatter(x_bs16, y_bs16, c=data_color, s=area, alpha=0.9, label="bs-16", hatch='++++')
        elif key == 'bs-768':
            data_color = '#4568a0';
            b768 = ax.scatter(x_bs768, y_bs768, c=data_color, s=area, alpha=0.5, label="bs-768")
        else:
            pass

    #--------------------------------------------------------------------------
    # legend for different block size
    #--------------------------------------------------------------------------
    #
    # cite: http://stackoverflow.com/questions/6146778/matplotlib-legend-markers-only-once
    # cite: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
    # example: http://matplotlib.org/users/legend_guide.html
    # manual: https://matplotlib.org/api/legend_api.html
    leg = ax.legend(
            ncol=3, 
            #scatterpoints=1, # the number of points in the legend for scatter plot
            labelspacing=1,     # the vertical space between the legend entries
            loc='upper center',
            #bbox_to_anchor=(0., 1.02, 1., 0.05),
            bbox_to_anchor=(0., 0.95, 1., 0.05),
            #bbox_to_anchor=(0., 1.02, 1., 0.04),
            #fancybox=True, 
            #shadow=True,
            #fancybox=False, shadow=False,
            fontsize=legFont
            #fontsize=15
            )

    leg.get_frame().set_alpha(1)
    leg.get_frame().set_linewidth(1.0)
    leg.get_frame().set_edgecolor("k")

    
    #
    # draw a line between input_kernel and the top3 nearest node
    #
    import matplotlib.patches as mpatches
    el = mpatches.Ellipse((0.3, 0.3), 0.3, 0.4, angle=30, alpha=0.8)

    
    # top 3 connection
    for pos in top3rows:
        ax.annotate("", 
                xy=(X_tsne_2d[pos, 0], X_tsne_2d[pos,1]), 
                xytext=(X_tsne_2d[-1,0], X_tsne_2d[-1,1]),
                arrowprops=dict(arrowstyle="-", 
                                color="0.6",
                                patchB=el,
                                shrinkB=5,  connectionstyle="arc3,rad=0.1",),
                )

    # bold the axis line
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)
        

    #--------------------------------------------------------------------------
    # adjust the xlim to adjust the text into the figure box
    #--------------------------------------------------------------------------
    #print ax.get_xlim()
    #print ax.get_ylim()
    xMin, xMax = ax.get_xlim()
    print xMin, xMax
    ax.set_xlim([xMin, xMax * 1.40])
    
    yMin, yMax = ax.get_ylim()
    print yMin, yMax
    ax.set_ylim([yMin, yMax * 1.45])

    # add x title
    if xtitle:
        ax.set_xlabel(xtitle, labelpad=10, fontsize=16)

    # remove ticks
    plt.xticks([])
    plt.yticks([])


    aspectratio=0.68
    ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    ax.set_aspect(ratio_default*aspectratio)
    
    
    plt.show()

    if figname == None:
        #fig.savefig('tsne.png', dpi=300, transparent = True, bbox_inches='tight')
        fig.savefig('tsne.pdf', transparent = True, bbox_inches='tight')
    else:
        fig.savefig(figname + '.pdf',  transparent = True, bbox_inches='tight')
        #fig.savefig(figname + '.png',  dpi=300, transparent = True, bbox_inches='tight')
        


#
# for hmm results: we use different fonts and label size
#
def plot_tsne_2d_v2(X_tsne_2d, y, y_name, top3rows, figname=None, kernelname=None,
        xtitle=None):
    area = np.pi * (18 * 0.6)**2

    txtFont = 17
    legFont = 14
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    x_bs16,   y_bs16   = [], []
    x_bs32,   y_bs32   = [], []
    x_bs64,   y_bs64   = [], []
    x_bs128,  y_bs128  = [], []
    x_bs256,  y_bs256  = [], []
    x_bs512,  y_bs512  = [], []
    x_bs768,  y_bs768  = [], []
    x_bs1024, y_bs1024 = [], []

    bs_dd = {} 

    # annotate
    for i, bs in enumerate(y):
        data_color = None
        sym = None
        lb = None
        if bs == 32:
            data_color = 'b'; sym = ">"; lb = 'bs-32'
            x_bs32.append(X_tsne_2d[i,0])
            y_bs32.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 64:
            data_color = 'g'; sym = (5, 0); lb = 'bs-64'
            x_bs64.append(X_tsne_2d[i,0])
            y_bs64.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 128:
            data_color = 'r'; sym = (5, 1); lb = 'bs-128'
            x_bs128.append(X_tsne_2d[i,0])
            y_bs128.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 256:
            data_color = 'c'; sym = (5, 2); lb = 'bs-256'
            x_bs256.append(X_tsne_2d[i,0])
            y_bs256.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 512:
            data_color = 'm'; sym = 'o'; lb = 'bs-512'
            x_bs512.append(X_tsne_2d[i,0])
            y_bs512.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 1024:
            data_color = 'y'; sym = 'v'; lb = 'bs-1024'
            x_bs1024.append(X_tsne_2d[i,0])
            y_bs1024.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 16:
            data_color = 'k'; sym = (5, 3); lb = 'bs-16'
            x_bs16.append(X_tsne_2d[i,0])
            y_bs16.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        elif bs == 768:
            data_color = '#4568a0'; sym = "1"; lb = 'bs-768' 
            x_bs768.append(X_tsne_2d[i,0])
            y_bs768.append(X_tsne_2d[i,1])
            bs_dd[lb] = 1

        else:
            raise Exception('Unknow block size')


        # annotate Kernel Name
        ax.text(X_tsne_2d[i,0]+15, X_tsne_2d[i,1]-5,
                #'%s' % (str(y_name[i])), size=17, zorder=2, color='k')
                '%s' % (str(y_name[i])), size=txtFont, zorder=2, color='k')

    
   # annotate the input kernel (last kernel)
    ax.scatter(X_tsne_2d[-1,0], X_tsne_2d[-1,1],
              c='k',
              s=area,
              alpha=0.9,
              marker=(5, 1)) 

    if kernelname <> None:
        ax.text(
                #X_tsne_2d[-1,0]-20, X_tsne_2d[-1,1]-70,   # new gammaobs loc 
               X_tsne_2d[-1,0]+10, X_tsne_2d[-1,1]-40,   # hmm_expectmu
                #X_tsne_2d[-1,0]-20, X_tsne_2d[-1,1]+40,    # mcx
                '%s' % (str(kernelname)), size=txtFont, zorder=2, color='k')



    for key, val in bs_dd.iteritems():
        #print key, val
        if key == 'bs-32':
            data_color = '#66c2ff'; sym = ">";
            b32 = ax.scatter(x_bs32, y_bs32, c=data_color, s=area,  alpha=0.9, label="bs-32", hatch='/////')
        elif key == 'bs-64':
            data_color = '#4dffa6';
            b64 = ax.scatter(x_bs64, y_bs64, c=data_color, s=area, alpha=0.8, label="bs-64", hatch='***')
        elif key == 'bs-128':
            data_color = 'r'; sym = (5, 1);
            b128 = ax.scatter(x_bs128, y_bs128, c=data_color, s=area, alpha=0.4, label="bs-128", lw=2)
        elif key == 'bs-256':
            data_color = 'c'; sym = (5, 2);
            b256 = ax.scatter(x_bs256, y_bs256, c=data_color, s=area, alpha=0.99, label="bs-256", hatch='xxx')
        elif key == 'bs-512':
            data_color = '#ffff66';
            b512= ax.scatter(x_bs512, y_bs512, c=data_color, s=area, alpha=0.99, label="bs-512", hatch='OO')
        elif key == 'bs-1024':
            data_color = 'y'; sym = 'v';
            b1024= ax.scatter(x_bs1024, y_bs1024, c=data_color, s=area, alpha=0.9, label="bs-1024", hatch='----')
        elif key == 'bs-16':
            data_color = '#cce6ff';
            b16 = ax.scatter(x_bs16, y_bs16, c=data_color, s=area, alpha=0.9, label="bs-16", hatch='++++')
        elif key == 'bs-768':
            data_color = '#b380ff';
            b768 = ax.scatter(x_bs768, y_bs768, c=data_color, s=area, alpha=0.9, label="bs-768", hatch='|||')
        else:
            pass

    #--------------------------------------------------------------------------
    # legend for different block size
    #--------------------------------------------------------------------------
    #
    # cite: http://stackoverflow.com/questions/6146778/matplotlib-legend-markers-only-once
    # cite: http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
    # example: http://matplotlib.org/users/legend_guide.html
    # manual: https://matplotlib.org/api/legend_api.html
    leg = ax.legend(
            ncol=3, 
            #scatterpoints=1, # the number of points in the legend for scatter plot
            labelspacing=1,     # the vertical space between the legend entries
            loc='upper center',
            #bbox_to_anchor=(0., 1.02, 1., 0.05),
            bbox_to_anchor=(0., 0.95, 1., 0.05),
            fontsize=legFont
            )

    leg.get_frame().set_alpha(1)
    leg.get_frame().set_linewidth(1.0)
    leg.get_frame().set_edgecolor("k")

    
    #
    # draw a line between input_kernel and the top3 nearest node
    #
    import matplotlib.patches as mpatches
    el = mpatches.Ellipse((0.3, 0.3), 0.3, 0.4, angle=30, alpha=0.8)

    
    # top 3 connection
    for pos in top3rows:
        ax.annotate("", 
                xy=(X_tsne_2d[pos, 0], X_tsne_2d[pos,1]), 
                xytext=(X_tsne_2d[-1,0], X_tsne_2d[-1,1]),
                arrowprops=dict(arrowstyle="-", 
                                color="0.6",
                                patchB=el,
                                shrinkB=5,  connectionstyle="arc3,rad=0.1",),
                )

    # bold the axis line
    for axis in ['top','bottom','left','right']:
        ax.spines[axis].set_linewidth(1.5)
        

    #--------------------------------------------------------------------------
    # adjust the xlim to adjust the text into the figure box
    #--------------------------------------------------------------------------
    #print ax.get_xlim()
    #print ax.get_ylim()
    xMin, xMax = ax.get_xlim()
    print xMin, xMax
    #ax.set_xlim([xMin, xMax * 1.40])
    ax.set_xlim([xMin, xMax * 1.6])    # expectmu
    #ax.set_xlim([xMin, xMax * 1.83]) # gammaobs
    
    yMin, yMax = ax.get_ylim()
    print yMin, yMax
    ax.set_ylim([yMin, yMax * 1.45])

    # add x title
    if xtitle:
        ax.set_xlabel(xtitle, labelpad=20, fontsize=(txtFont + 5) )

    # remove ticks
    plt.xticks([])
    plt.yticks([])


    aspectratio=0.68
    ratio_default=(ax.get_xlim()[1]-ax.get_xlim()[0])/(ax.get_ylim()[1]-ax.get_ylim()[0])
    ax.set_aspect(ratio_default*aspectratio)
    
    
    plt.show()

    if figname == None:
        #fig.savefig('tsne.png', dpi=300, transparent = True, bbox_inches='tight')
        fig.savefig('tsne.pdf', transparent = True, bbox_inches='tight')
    else:
        fig.savefig(figname + '.pdf',  transparent = True, bbox_inches='tight')
        #fig.savefig(figname + '.png',  dpi=300, transparent = True, bbox_inches='tight')
        
