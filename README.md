# Sliding Window Piecewise Linear Segmentation
An optimized O(N) implementation of the sliding window algorithm for piecewise linear segmentation of a time series. This algorithm will fit trend lines to a series and can be used online or offline.

![alt text](https://github.com/SlackEight/sliding-window-pls/blob/main/example/segmentation.png?raw=true)


### Usage guide:
* Add sliding_window.py to your project folder
* from sliding_window.py import sliding_window, sliding_window_online
* To use the offline segmentation, pass the time_series as a list of points
* To use the online segmentation, pass one point to the function and repeat as new points become available.

Read about this algorithm in [Lovrić et al. 2014's paper](https://www.econstor.eu/bitstream/10419/147468/1/868006483.pdf)