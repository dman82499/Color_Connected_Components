






def color_connected_components(image):
    labels = []
    connected_index = 0
    index = 0
    mapping_dict = {}
    #image = eight_by_eight_image_gen()
    #veiwing_image = numpy.flip(image, axis=0)
    #veiwing_image = opencv_preprocessing.rescale_image(veiwing_image, 800)
    #cv2.imshow("test", veiwing_image)
    #cv2.waitKey(0)
    # we will use the first_pass_through just like the normal algorithm.
    # the only difference is we include this other step of checking for component color equality as well
    # and that's the only difference I think between the binary version
    first_pass_through = numpy.zeros((image.shape[0], image.shape[1]), dtype=int)
    for y in range(image.shape[0] -1 , -1, -1):
        for x in range(image.shape[1]):
            index, connected_index = is_connected(image, first_pass_through, y, x, mapping_dict,
                                           index)
            first_pass_through[y][x] = connected_index
            # don't update the index

    # second pass through
    for y in range(image.shape[0]-1, -1, -1):
        for x in range(image.shape[1]):
            if first_pass_through[y][x] in mapping_dict:
                first_pass_through[y][x] = mapping_dict[first_pass_through[y][x]]


    first_pass_through *= 20
    first_pass_through = numpy.flip(first_pass_through, axis=0)
    first_pass_through = first_pass_through.astype("uint8")
    first_pass_through = cv2.cvtColor(first_pass_through, cv2.COLOR_GRAY2RGB)
    first_pass_through = opencv_preprocessing.rescale_image(first_pass_through, 200)

    cv2.imshow("random", first_pass_through)
    cv2.waitKey(1)
    return first_pass_through



#@numba.jit("int64[:](uint8[:,:,:], int32[:,:], int64, int64, int64, int64)")
def is_connected(image, first_pass_through, y, x,  mapping_dict, current_idx):
    current_color = image[y][x]
    # scan left, and up
    left_idx = x - 1
    top_idx = y + 1
    # update the mapping dict as well
    # in this algorithm, the color version uses the "connected" bool as a color equivalency
    # statement.

    left_color = image[y][left_idx]

    left_number = first_pass_through[y][left_idx]
    # our image is flipped, so top index is going to be the size of the image
    if top_idx < image.shape[0]:
        top_color = image[top_idx][x]
        top_number = first_pass_through[top_idx][x]
    else:
        top_color = [-1, -1, -1]
        top_number = -1
    #make sure we aren't on borders
    if left_idx <= -1:
        left_color = [-1,-1,-1]
        left_number = -1



    #first check for conflicts
    # now check left first\
    left_color_equal = numpy.all(left_color == current_color)
    top_color_equal= numpy.all(top_color == current_color)
    connected = left_color_equal or top_color_equal
    
    if connected:
        #wait, if we are connected, can't we just default to the pixel that we are on and check color equality?
        #check for conflicts between the pixels
        number_equal = numpy.all(left_number == top_number)
        if number_equal or left_number == -1 or top_number == -1:
            #no conflict, assign value
            if left_number == -1:
                return current_idx, top_number
            else:
                return current_idx, left_number

        else:
            if left_color_equal and top_color_equal and not number_equal:
                # update our label dictionary to reflect
                if left_number > top_number:
                    mapping_dict[left_number] = top_number
                else:
                    mapping_dict[top_number] = left_number


            # we have a conflict: update to center pixel
            #first check to see if the conflict can be resolved
            if left_color_equal:
                return current_idx, left_number
            elif top_color_equal:
                return current_idx, top_number
            #else:
            #    print("conflict")
            # choose randomly
    else:
        current_idx += 1

        return current_idx, current_idx




def reigion_segment_simple(image):
    reigions = dict()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            color_arr = tuple(image[y][x])

            cordinate = (x, y, color_arr[0], color_arr[1], color_arr[2])
            if color_arr in reigions:
                reigions[color_arr].append(cordinate)
            else:
                reigions[color_arr] = [cordinate]



    return reigions


def reigion_segment_colorcc(image, labeled_image):
    reigions = dict()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            color_arr = tuple(image[y][x])

            cordinate = (x, y, color_arr[0], color_arr[1], color_arr[2])
            if color_arr in reigions:
                reigions[color_arr].append(cordinate)
            else:
                reigions[color_arr] = [cordinate]



    return reigions


def mean_reigion_from_color_cc(first_passthrough, image):

    centers = []

    for x in range(first_passthrough.max()):
        indexes = numpy.argwhere(first_passthrough == x)
        if len(indexes) == 0:
            # we did not find a region, continue
            continue
        color = image[indexes[0][0], indexes[0][1]]
        location = numpy.mean(indexes, axis=0, dtype=int)
        location = pixel_trim(location)
        vector = numpy.append(location, color)
        # append the number of pixels as well

        vector = numpy.append(vector, indexes.shape[0])
        centers.append(vector)



        #indexes = numpy.argwhere(first_passthrough == connected_index)
    return centers



def pixel_trim(pixel):

    x_max = settin.x_size
    y_max = settin.y_size

    pixel[0] = size_reduction(pixel[0], y_max, 20)
    pixel[1] = size_reduction(pixel[1], x_max, 20)
    return pixel


def compute_centroid(image_arr):
    result = numpy.mean(image_arr, axis=0)
    result = result.astype("int")
    return result

'''A speed up (thanks to numba) version of color connected components, that is fast enough to run
in real time for most images.'''
@numba.njit()
def numba_color_connected_components(image):

    connected_index = 0
    mapping_dict = {}
    # image = eight_by_eight_image_gen()
    # veiwing_image = numpy.flip(image, axis=0)
    # veiwing_image = opencv_preprocessing.rescale_image(veiwing_image, 800)
    # cv2.imshow("test", veiwing_image)
    # cv2.waitKey(0)
    # we will use the first_pass_through just like the normal algorithm.
    # the only difference is we include this other step of checking for component color equality as well
    # and that's the only difference I think between the binary version
    first_pass_through = numpy.zeros((image.shape[0], image.shape[1]), dtype="int16")
    for y in range(image.shape[0] - 1, -1, -1):
        for x in range(image.shape[1]):
            current_color = image[y][x]
            left_idx = x - 1
            top_idx = y + 1
            # update the mapping dict as well
            # in this algorithm, the color version uses the "connected" bool as a color equivalency
            # statement.

            left_color = image[y][left_idx]

            left_number = first_pass_through[y][left_idx]
            # our image is flipped, so top index is going to be the size of the image
            if top_idx < image.shape[0]:
                top_color = image[top_idx][x]
                top_number = first_pass_through[top_idx][x]
            else:
                top_color = numpy.array([-1, -1, -1], dtype="int16")
                top_number = -1
            # make sure we aren't on borders
            if left_idx <= -1:
                left_color = numpy.array([-1, -1, -1], dtype="int16")
                left_number = -1

            # first check for conflicts
            # now check left first\
            left_color_equal = numpy.all(left_color == current_color)
            top_color_equal = numpy.all(top_color == current_color)
            connected = left_color_equal or top_color_equal

            if connected:
                # wait, if we are connected, can't we just default to the pixel that we are on and check color equality?
                # check for conflicts between the pixels
                number_equal = left_number == top_number
                if number_equal or left_number == -1 or top_number == -1:
                    # no conflict, assign value
                    if left_number == -1:
                        first_pass_through[y][x] = top_number
                    else:
                        first_pass_through[y][x] = left_number

                else:
                    if left_color_equal and top_color_equal and not number_equal:
                        # update our label dictionary to reflect
                        if left_number > top_number:
                            mapping_dict[left_number] = top_number
                        else:
                            mapping_dict[top_number] = left_number

                    # we have a conflict: update to center pixel
                    # first check to see if the conflict can be resolved
                    if left_color_equal:
                        first_pass_through[y][x] = left_number
                    elif top_color_equal:
                        first_pass_through[y][x] = top_number
                    # else:
                    #    print("conflict")
                    # choose randomly
            else:
                connected_index += 1
                first_pass_through[y][x] = connected_index




            #first_pass_through[y][x] = connected_index
            # don't update the index

    # second pass through
    for y in range(image.shape[0] - 1, -1, -1):
        for x in range(image.shape[1]):
            if first_pass_through[y][x] in mapping_dict:
                first_pass_through[y][x] = mapping_dict[first_pass_through[y][x]]


    return first_pass_through


def size_reduction(value, value_max, num_of_values):
    percent = value/value_max
    return int(percent*num_of_values)

