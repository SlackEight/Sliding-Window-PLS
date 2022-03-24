def calculate_values(values, point, trends):
    '''
        Calculates the values for E_x, E_y, etc. We need to do this fairly often so might
        as well encapsulate it.
    '''    
    values[0] =  (trends[-1][0]+trends[-1][2])/2 # E_x
    values[1] = (trends[-1][1] + point[1])/2 # E_y
    values[2] = (trends[-1][1]*trends[-1][0] + point[1]*point[0])/2 # E_xy
    values[3] = (trends[-1][0]**2+point[0]**2)/2 # E_x2
    values[4] = (trends[-1][1]**2+point[1]**2)/2 # E_y2
    values[5] = (point[1]-trends[-1][1]) # m
    values[6] = (point[1]-values[5]*point[0]) # b
    values[7] = values[4] - 2 * (values[5] * values[2] + values[6] * values[1]) +  values[5]**2 * values[3] + 2 * values[5] * values[6] * values[0] + values[6]**2
    return values

def sliding_window(time_series, max_error):
    # A trend looks like this: [start x, start y, end x, end y]
    values = [0,0,0,0,0,0,0,0] # E_x, E_y, E_xy, E_x2, E_y2, m, b, loss
    trends = []
    current_trend_index = -1
    
    for point in time_series:
        if len(trends) == 0:  # after first run we have one point, add it
            trends.append([0, point, 0, point])
            current_trend_index = 0

        elif trends[-1][0] == trends[-1][2]: # in the case our current latest trend has only one point, make it a line with the next point
            point = [trends[-1][2]+1, point]
            trends[-1] = [trends[-1][0],trends[-1][1], point[0], point[1]]
            values = calculate_values(values, point, trends)
            values[7] = 0 # loss


        else: # otherwise we're in the middle of a normal trend
            current_trend = trends[-1]
            window_size = current_trend[2] - current_trend[0] + 2
            N = window_size-1
            new_x = current_trend[2]+1
            new_y = point
            E_x = values[0]*N/(N+1) + new_x*1/(N+1)
            E_y = values[1]*N/(N+1) + new_y*1/(N+1)
            E_xy = values[2]*N/(N+1) + new_x*new_y/(N+1)
            E_x2 = values[3]*N/(N+1) + new_x*new_x/(N+1)
            E_y2 = values[4]*N/(N+1) + new_y*new_y/(N+1)
            t_m = (E_x*E_y-E_xy)/(E_x**2-E_x2)
            t_b = E_y-t_m*E_x
            loss = E_y2 - 2 * (t_m * E_xy + t_b * E_y) + t_m**2 * E_x2 + 2 * t_m * t_b * E_x + t_b**2
            if loss*window_size < max_error:
                m = t_m
                b = t_b
                values = [E_x, E_y, E_xy, E_x2, E_y2, m, b, loss]
                trends[-1] = [current_trend[0], b+m*current_trend[0], current_trend[0]+window_size-1, b+m*(current_trend[2]+1)]

            else:
                # trend is over finalise previous trend and add the new point to a new trend
                b = values[6]
                m = values[5]
                trends.append([trends[-1][2],trends[-1][3], new_x, new_y])

                point = [trends[-1][2], point]
                values = calculate_values(values, point, trends)
                values[7] = 0 # loss
    output = trends
    return output

values = [0,0,0,0,0,0,0,0] # E_x, E_y, E_xy, E_x2, E_y2, m, b, loss
trends = []
def sliding_window_online(point, max_error):
    # A trend looks like this: [start x, start y, end x, end y]
    global trends
    global values
    
    if len(trends) == 0:  # after first run we have one point, add it
        trends.append([0, point, 0, point])

    elif trends[-1][0] == trends[-1][2]: # in the case our current latest trend has only one point, make it a line with the next point
        point = [trends[-1][2]+1, point]
        trends[-1] = [trends[-1][0],trends[-1][1], point[0], point[1]]
        values = calculate_values(values, point, trends)
        values[7] = 0 # loss


    else: # otherwise we're in the middle of a normal trend
        current_trend = trends[-1]
        window_size = current_trend[2] - current_trend[0] + 2
        N = window_size-1
        new_x = current_trend[2]+1
        new_y = point
        E_x = values[0]*N/(N+1) + new_x*1/(N+1)
        E_y = values[1]*N/(N+1) + new_y*1/(N+1)
        E_xy = values[2]*N/(N+1) + new_x*new_y/(N+1)
        E_x2 = values[3]*N/(N+1) + new_x*new_x/(N+1)
        E_y2 = values[4]*N/(N+1) + new_y*new_y/(N+1)
        t_m = (E_x*E_y-E_xy)/(E_x**2-E_x2)
        t_b = E_y-t_m*E_x
        loss = E_y2 - 2 * (t_m * E_xy + t_b * E_y) + t_m**2 * E_x2 + 2 * t_m * t_b * E_x + t_b**2
        if loss*window_size < max_error:
            m = t_m
            b = t_b
            values = [E_x, E_y, E_xy, E_x2, E_y2, m, b, loss]
            trends[-1] = [current_trend[0], b+m*current_trend[0], current_trend[0]+window_size-1, b+m*(current_trend[2]+1)]

        else:
            # trend is over finalise previous trend and add the new point to a new trend
            b = values[6]
            m = values[5]
            trends.append([trends[-1][2],trends[-1][3], new_x, new_y])

            point = [trends[-1][2], point]
            values = calculate_values(values, point, trends)
            values[7] = 0 # loss

    output = trends
    return output