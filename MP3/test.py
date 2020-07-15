#spits out possible configurations
def row_combinations(blank_distributed, row_constraint, row_permutations, num_col):
    constraint_block_num = len(row_constraint)
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
def zero_distributor(total_arr, slots_arr, num_zeros, num_slots, cur_box_index):
    cur_num_zeros = num_zeros
    cur_slots_arr = slots_arr.copy()
    if(cur_box_index + 1 == num_slots):
        cur_slots_arr.append(cur_num_zeros)
        total_arr.append(cur_slots_arr)
    else:
        for i in range(num_zeros+1):
            # print(slots_arr)
            cur_slots_arr = slots_arr.copy()
            cur_slots_arr.append(cur_num_zeros)
            zero_distributor(total_arr, cur_slots_arr, num_zeros - cur_num_zeros, num_slots, cur_box_index + 1)
            cur_num_zeros -= 1
    return

def find_always_element(permutations, fixed_row_map):
    row_len = len(permutations[0])
    for i in range(row_len):
        always_1_fl = 1
        always_0_fl = 1
        for k in range(len(permutations)):
            if permutations[k][i] == 1:
                always_0_fl = 0
            if permutations[k][i] == -1:
                always_1_fl = 0
        if always_0_fl:
            fixed_row_map.append(-1)
        elif always_1_fl:
            fixed_row_map.append(1)
        else:
            fixed_row_map.append(0)


# permutation matrix [  [[row0_permu], [row1_permu]],
                #       [[col0_permu], [col1_permu]]    ]
                # [row/col][row/colnum][whichpermu]
# fixed_map_matrix   [[0,1,1,1,-1,-1,0,0,],
#                     [0,1,1,1,0,0,0,0,],
#                     [0,1,1,1,-1,-1,0,0,]]
#
def update_permutations(permutation, fixed_map):
    for a_perm in permutation:
        for k in range(len(fixed_map)):
            if (fixed_map[k] == 1 and a_perm[k] == -1) or (fixed_map[k] == -1 and a_perm[k] == 1):
                permutation.remove(a_perm)

# permutation = [[1,1,-1],[1,-1,1],[-1,1,1]]
# fixed_map = [1,0,0]
# update_permutations(permutation, fixed_map)



#test 10 long row, [2,1] [3,1] [1,1]
#10 - 6 - 2 = 2
# # rowLength = 10
# row_constraint = [[2,1], [3,1], [1,1]]
# total_arr = []
# slots_arr = []
# permutations = []
# fixed_row_map = []
# num_zeros = 2
# num_slots = 4
# cur_box_index = 0

# zero_distributor(total_arr, slots_arr, num_zeros, num_slots, cur_box_index)
# print("total_arr:\n", total_arr)
# row_combinations(total_arr, row_constraint, permutations, rowLength)
# print("permutations:\n", permutations)
# find_always_element(permutations, fixed_row_map)
# print("fixed_row_map:\n", fixed_row_map)

input_map = [[0, 1, 1, 0],[0, 0, 0, 0],[1, 1, 1, 0]]
orig_ori_size = 4
result_ori_size = 3




def transpose_map(input_map, orig_ori_size, result_ori_size):
    total_col_map = [] # we basically transposing fixed_col_map
    for x in range(orig_ori_size):
        col_map = []
        for y in range(result_ori_size):
            col_map.append(input_map[y][x])
        total_col_map.append(col_map)
    return total_col_map


print(transpose_map(input_map, orig_ori_size, result_ori_size))
