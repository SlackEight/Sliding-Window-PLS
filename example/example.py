import sliding_window
from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D

def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)


with open("example_data/s&p500.csv") as f:
    file_lines = f.readlines()
time_series = [float(x) for x in file_lines[1100:1200]]


trends = sliding_window.sliding_window(time_series, 100)

figure()
draw_plot(time_series,"Sliding window")
draw_segments(trends)

show()