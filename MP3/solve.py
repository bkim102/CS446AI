import numpy as np
import time

def transpose_map(input_map, orig_ori_size, result_ori_size):
    total_col_map = [] # we basically transposing fixed_col_map
    for x in range(orig_ori_size):
        col_map = []
        for y in range(result_ori_size):
            col_map.append(input_map[y][x])
        total_col_map.append(col_map)
    return total_col_map

#row_permutations- input the permutations for one row/col
#fixed_row_map- output the always true for a row.

def find_always_element_row(row_permutations, fixed_row_map):
    col_len = len(row_permutations[0])
    for i in range(col_len):
        always_1_fl = 1
        always_0_fl = 1
        for k in range(len(row_permutations)):
            if row_permutations[k][i] == 1:
                always_0_fl = 0
            if row_permutations[k][i] == -1:
                always_1_fl = 0
        if always_0_fl:
            fixed_row_map.append(-1)
        elif always_1_fl:
            fixed_row_map.append(1)
        else:
            fixed_row_map.append(0)

def update_permutations(permutation, fixed_map):
    ret_arr = []
    for i in range(len(permutation)):
        is_consistent_flag = 1
        for k in range(len(fixed_map)):
            if (fixed_map[k] == 1 and permutation[i][k] == -1) or (fixed_map[k] == -1 and permutation[i][k] == 1):
                is_consistent_flag = 0
        if is_consistent_flag != 0:
            ret_arr.append(permutation[i])
    return ret_arr


# this function provides us with a hopefully partially filled map
# in addition to a reduced set of row & column permutations
def possible_configuration(constraints):
    num_row = len(constraints[0])
    num_col = len(constraints[1])
    fixed_row_map = []
    fixed_col_map = []
    row_permutations_map = []
    col_permutations_map = []
    for i in range(len(constraints[0])):
        print(constraints[0][i])
    print("     break      ")

    for i in range(len(constraints[1])):
        print(constraints[1][i])
    ###### PROCESS ROW  ######
    print("###### GENERATING ROW PERMUTATIONS ######")
    for i in range(num_row):
        num_elem = len(constraints[0][i])
        sum_elem = 0
        for k in range(num_elem):
            sum_elem += constraints[0][i][k][0]

        min_occupied = sum_elem + num_elem - 1
        free_space = num_col - min_occupied
        zero_arr = []
        slot_arr = []
        row_permutations = []
        fixed_row = []


        zero_distributor(zero_arr, slot_arr, free_space, num_elem+1, 0)
        if(num_elem == 0):
            zero_arr[0][0] = num_col
        row_combinations(zero_arr, constraints[0][i], row_permutations)
        row_permutations_map.append(row_permutations)

        find_always_element_row(row_permutations, fixed_row)
        fixed_row_map.append(fixed_row)


    print("###### GET COLUMN DATA ######")
    extrapolated_col_map = [] # we basically transposing fixed_row_map
    for x in range(num_col):
        extrapolated_col = []
        for y in range(num_row):
            extrapolated_col.append(fixed_row_map[y][x])
        extrapolated_col_map.append(extrapolated_col)

    print("###### GENERATING COLUMN PERMUTATIONS ######")
    for i in range(num_col):
        num_elem = len(constraints[1][i])
        sum_elem = 0
        for k in range(num_elem):
            sum_elem += constraints[1][i][k][0]
        min_occupied = sum_elem + num_elem - 1
        free_space = num_row - min_occupied
        zero_arr = []
        slot_arr = []
        col_permutations = []
        fixed_col = []
        zero_distributor(zero_arr, slot_arr, free_space, num_elem+1, 0)
        row_combinations(zero_arr, constraints[1][i], col_permutations)
        col_permutations_map.append(col_permutations)

        find_always_element_row(col_permutations, fixed_col)
        fixed_col_map.append(fixed_col)

    print("###### UPDATE COLUMN PERMUTATIONS #######")
    updated_cols = []
    for idx in range(0, num_col):
        updated_col = update_permutations(col_permutations_map[idx], extrapolated_col_map[idx])
        updated_cols.append(updated_col)

    ###### GET ROW DATA ######
    extrapolated_row_map = [] # we basically transposing fixed_col_map
    for y in range(num_row):
        extrapolated_row = []
        for x in range(num_col):
            extrapolated_row.append(fixed_col_map[x][y])
        extrapolated_row_map.append(extrapolated_row)

    ###### UPDATE ROW PERMUTATIONS #######
    updated_rows = []
    for idx in range(0, num_row):
        updated_row = update_permutations(row_permutations_map[idx], extrapolated_row_map[idx])
        updated_rows.append(updated_row)

    print("###### MERGE (fixed map and extrapolated map) ######")
    for ii in range(0, num_row):
        for jj in range(0, num_col):
            if fixed_row_map[ii][jj] != extrapolated_row_map[ii][jj]:
                fixed_row_map[ii][jj] += extrapolated_row_map[ii][jj]


    output_map = fixed_row_map
    prev_map = []
    # prev_map = output_map
    updated_rows_cycle = updated_rows
    updated_cols_cycle = updated_cols
    ####################  CYCLING HAPPENS BELOW #######################

    while prev_map != output_map:
        print("--cycle--")
        ###### PROCESS ROW  ######
        fixed_row_map_cycle = []
        for i in range(num_row):
            fixed_row_cycle = []
            find_always_element_row(updated_rows[i], fixed_row_cycle)
            fixed_row_map_cycle.append(fixed_row_cycle)

        ###### GET COLUMN DATA ######
        extrapolated_col_map_cycle = [] # we basically transposing fixed_row_map_cycle
        for x in range(num_col):
            extrapolated_col_cycle = []
            for y in range(num_row):
                extrapolated_col_cycle.append(fixed_row_map_cycle[y][x])
            extrapolated_col_map_cycle.append(extrapolated_col_cycle)

        ###### PROCESS COLUMN ######
        fixed_col_map_cycle = []
        for i in range(num_col):
            fixed_col_cycle = []
            find_always_element_row(updated_cols[i], fixed_col_cycle)
            fixed_col_map_cycle.append(fixed_col_cycle)

        ###### UPDATE COLUMN PERMUTATIONS #######
        updated_cols_cycle = []
        for idx in range(0, num_col):
            updated_col_cycle = update_permutations(updated_cols[idx], extrapolated_col_map_cycle[idx])
            updated_cols_cycle.append(updated_col_cycle)

        ###### GET ROW DATA ######
        extrapolated_row_map_cycle = [] # we basically transposing fixed_col_map_cycle
        for y in range(num_row):
            extrapolated_row_cycle = []
            for x in range(num_col):
                extrapolated_row_cycle.append(fixed_col_map_cycle[x][y])
            extrapolated_row_map_cycle.append(extrapolated_row_cycle)

        ###### UPDATE ROW PERMUTATIONS #######
        updated_rows_cycle = []
        for idx in range(0, num_row):
            updated_row_cycle = update_permutations(updated_rows[idx], extrapolated_row_map_cycle[idx])
            updated_rows_cycle.append(updated_row_cycle)

        ###### MERGE (fixed map and extrapolated map) ######
        for ii in range(0, num_row):
            for jj in range(0, num_col):
                if fixed_row_map_cycle[ii][jj] != extrapolated_row_map_cycle[ii][jj]:
                    fixed_row_map_cycle[ii][jj] += extrapolated_row_map_cycle[ii][jj]

        updated_rows = updated_rows_cycle
        updated_cols = updated_cols_cycle
        prev_map = output_map
        output_map = fixed_row_map_cycle


    return output_map, updated_rows, updated_cols


#spits out possible configurations
# blank_distrtibuted- the array of zero distribution permutations [[2,0,0],[1,1,0],[1,0,1] ....]
# row_constraint- constraint blocks given for a single row/col [[3,1], [2,1] ] like this
# row_permutations- output array with all possible row setup.
# num_col
def row_combinations(blank_distributed, row_constraint, row_permutations):
    if(len(blank_distributed[0]) == 1 ):
        cur_row_arr = []
        print(blank_distributed)
        for i in range(blank_distributed[0][0]):
            cur_row_arr.append(-1)
        row_permutations.append(cur_row_arr)
        return
    for i in range(len(blank_distributed)):
        cur_row_arr = []
        for k in range(len(blank_distributed[i]) * 2 - 1):
            if 0 == (k % 2):
                for l in range(blank_distributed[i][int(k/2)]):
                    cur_row_arr.append(-1)
            else:
                for l in range(row_constraint[int((k-1)/2)][0]):
                    cur_row_arr.append(1)
                if ((k-1)/2) < (len(blank_distributed[i]) - 2):
                    cur_row_arr.append(-1)

        row_permutations.append(cur_row_arr)

		#figure out how to divide free spaces
#distributes number of blank spaces to each slots.
# total_arr- output array
# slots_arr- used in recursion. for initial put empty array.
# num_zeros- put in num of extra zeros/-1s we can put, except the default one -1 in between blocks
# cur_box_index- used in recursion, put 0 for init.
def zero_distributor(total_arr, slots_arr, num_zeros, num_slots, cur_box_index):
    cur_num_zeros = num_zeros
    cur_slots_arr = slots_arr.copy()
    if(cur_box_index + 1 == num_slots):
        cur_slots_arr.append(cur_num_zeros)
        total_arr.append(cur_slots_arr)
    else:
        for i in range(num_zeros+1):
            cur_slots_arr = slots_arr.copy()
            cur_slots_arr.append(cur_num_zeros)
            zero_distributor(total_arr, cur_slots_arr, num_zeros - cur_num_zeros, num_slots, cur_box_index + 1)
            cur_num_zeros -= 1
    return

#search stack ( current row/col permus,
#  whether row(=1) col (= 0) was updated, remaining num permutations)

def search_in_the_dark(fixed_map, row_permu, col_permu):
    search_stack = []
    row_size = len(row_permu[0][0])
    col_size = len(col_permu[0][0])
    min_permu = 55
    min_permu_row_index = -1
    total_permu = 0
    for i in range(len(row_permu)):
        total_permu += len(row_permu[i])
        if(len(row_permu[i]) > 1 and len(row_permu[i]) < min_permu):
            min_permu_row_index = i
            min_permu = len(row_permu[i])
    if(min_permu_row_index == -1):
        #print("nothing to do here")
        return fixed_map

    for k in range(len(col_permu)):
        total_permu += len(col_permu[k])
    rem_permu = total_permu - len(row_permu[min_permu_row_index]) + 1
    rc_update = 1
    cur_col_permu = col_permu.copy()
    cur_fixed_map = fixed_map.copy()

    for j in range(len(row_permu[min_permu_row_index])):

        cur_row_permu = row_permu.copy()
        garbage = []
        garbage.append(row_permu[min_permu_row_index][j])
        cur_row_permu[min_permu_row_index] = garbage
        search_stack.append((cur_row_permu.copy(), cur_col_permu.copy(), rc_update, rem_permu))

    while(1):
        if(len(search_stack) == 0):
            #print("no solution found")
            return
        # sort stack according to remaining permutation MAYBE
        cur_row_permu, cur_col_permu, rc_update, rem_permu = search_stack.pop()
        cur_fixed_map =[]
        if(rc_update):
            for i in range(len(cur_row_permu)):
                row_fixed_map = []
                find_always_element_row(cur_row_permu[i], row_fixed_map)
                cur_fixed_map.append(row_fixed_map)

            # update cur_col_permu. if any one of the col permu goes down to zero, continue
                ###### GET ROW DATA ######
            total_fixed_col_map = transpose_map(cur_fixed_map, row_size, col_size)

            was_bad_guess = 0
            for i in range(len(cur_col_permu)):
                cur_col_permu[i] = update_permutations(cur_col_permu[i], total_fixed_col_map[i])
                if len(cur_col_permu[i]) == 0:
                    was_bad_guess = 1
                    break
            if(was_bad_guess):
                #print("wrong guess, column options depleted, trying other")
                continue
                # return
            # find the col with least permu still greater than 1, then push all into stack
            zero_count = 0
            for i in range(len(cur_fixed_map)):
                for j in range(len(cur_fixed_map[0])):
                    if(cur_fixed_map[i][j] == 0):
                        zero_count += 1
            if zero_count == 0:
                return transpose_map(total_fixed_col_map, col_size, row_size)

            min_permu = 999
            min_permu_col_index = -1
            total_permu = 0
            for i in range(len(cur_col_permu)):
                total_permu += len(cur_col_permu[i])
                if(len(cur_col_permu[i]) > 1 and len(cur_col_permu[i]) < min_permu):
                    min_permu_col_index = i
                    min_permu = len(cur_col_permu[i])
            if(min_permu_col_index == -1):
                #print("done")
                return transpose_map(total_fixed_col_map, col_size, row_size)
            for k in range(len(cur_row_permu)):
                total_permu += len(cur_row_permu[k])
            rem_permu = total_permu - len(cur_col_permu[min_permu_col_index]) + 1
            rc_update = 0
            next_row_permu = cur_row_permu.copy()

            for j in range(len(cur_col_permu[min_permu_col_index])):
                next_col_permu = cur_col_permu.copy()
                garbage = []
                garbage.append(cur_col_permu[min_permu_col_index][j])
                next_col_permu[min_permu_col_index] = garbage
                search_stack.append((next_row_permu.copy(), next_col_permu.copy(), rc_update, rem_permu))




        else:
            #print("narrow row option")
            for i in range(len(cur_col_permu)):
                col_fixed_map = []
                find_always_element_row(cur_col_permu[i], col_fixed_map)
                cur_fixed_map.append(col_fixed_map)

            # update cur_row_permu. if any one of the col permu goes down to zero, continue
                ###### GET ROW DATA ######
            total_fixed_row_map = transpose_map(cur_fixed_map, col_size, row_size)
            was_bad_guess = 0
            for i in range(len(cur_row_permu)):
                cur_row_permu[i] = update_permutations(cur_row_permu[i], total_fixed_row_map[i])
                if len(cur_row_permu[i]) == 0:
                    was_bad_guess = 1
                    break
            if(was_bad_guess):
                #print("wrong guess, row options depleted, trying other")
                continue
                # return
            zero_count = 0
            for i in range(len(total_fixed_row_map)):
                for j in range(len(total_fixed_row_map[0])):
                    if(total_fixed_row_map[i][j] == 0):
                        zero_count += 1
            if zero_count == 0:
                return total_fixed_row_map

            # find the row with least permu still greater than 1, then push all into stack
            min_permu = 999
            min_permu_row_index = -1
            total_permu = 0
            for i in range(len(cur_row_permu)):
                total_permu += len(cur_row_permu[i])
                if(len(cur_row_permu[i]) > 1 and len(cur_row_permu[i]) < min_permu):
                    min_permu_row_index = i
                    min_permu = len(cur_row_permu[i])

            for k in range(len(cur_col_permu)):
                total_permu += len(cur_col_permu[k])
            rem_permu = total_permu - len(cur_row_permu[min_permu_row_index]) + 1
            rc_update = 1
            next_col_permu = cur_col_permu.copy()
            # rc_update should be 1


            for j in range(len(cur_row_permu[min_permu_row_index])):
                next_row_permu = cur_row_permu.copy()
                garbage = []
                garbage.append(cur_row_permu[min_permu_row_index][j])
                next_row_permu[min_permu_row_index] = garbage
                search_stack.append((next_row_permu.copy(), next_col_permu.copy(), rc_update, rem_permu))




def solve(constraints):
    start_time = time.time()
    #print("SOLVING...")
    #print("pure constraint propagation")
    starting_map, row_permutations, col_permutations = possible_configuration(constraints)
    #for i in range(len(starting_map)):
        #print("row ", i,":", starting_map[i])
    #print("try guessing some")

    final_map = search_in_the_dark(starting_map, row_permutations, col_permutations)
    for i in range(len(final_map)):
        for k in range(len(final_map[i])):
            if final_map[i][k] == -1:
                final_map[i][k] = 0
        print("row ", i,":", final_map[i])

    end_time = time.time()
    print("TOTAL TIME ELAPSED: ", end_time - start_time, " seconds")
    return np.asarray(final_map)
