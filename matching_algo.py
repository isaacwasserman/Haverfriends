from scipy.spatial import distance  

# this function will be used to match the first user in the queue with other users in the queue.
# it returns the index for the matched user to be popped. Match_user_dict will get a new key (user_id for one of the indivs in the pair)
# and the value will be the user_id for the other party + chat_id (the concatenation of their user_ids)
def find_match_in_group(user_group, match_user_dict):
    current_user_detail = user_group[0][1]
    best_match_id_and_index = (None, None)
    lowest_euclidean_distance = 999
    for i in range(1, len(user_group[0][0])):
        dst = distance.euclidean(user_group[0][1]['questionnaire_scores'], user_group[i][1]['questionnaire_scores'])
        if dst == 0:
            best_match_id_and_index = (user_group[i][0], i)
            lowest_euclidean_distance = 0
            break
        if dst < lowest_euclidean_distance:
            best_match_id_and_index = (user_group[i][0], i)
            lowest_euclidean_distance = dst
    match_user_dict[best_match_id_and_index[0]] = (user_group[0][0], str(min(best_match_id_and_index[0], user_id_list[0])) + '-' + str(max(best_match_id_and_index[0], user_id_list[0])))
    return best_match_id_and_index[1]

def form_groups(all_users_dict):
    platonic_users = []
    non_platonic_users = []
    for user_id, user_details in all_users_dict.items():
        if user_details['want_platonic']:
            platonic_users.append((user_id, user_details))
        else:
            non_platonic_users.append((user_id, user_details))
    return platonic_users, non_platonic_users

def find_unmatched_users(user_group):
    main_user = user_group[0]
    other_users = user_group[1:]
    former_matches_of_main_user = set(main_user[1]['active_chat_partners'])
    unmatched_users = [main_user]
    unmatched_user_indexes = [0]
    for index, other_user in enumerate(other_users):
        other_user_id = other_user[0]
        if other_user_id not in former_matches_of_main_user:
            unmatched_users.append(other_user)
            unmatched_user_indexes.append(index)
    return unmatched_user_indexes, unmatched_users

def matching_algo_for_user_group(user_group, match_user_dict):
    while len(user_group) > 0:
        unmatched_user_indexes, unmatched_users = find_unmatched_users(user_group)
        if len(unmatched_users) == 1:
            if match_user_dict.get('unmatched') is None:
                match_user_dict['unmatched'] = [unmatched_users[0]]
            else:
                match_user_dict['unmatched'].append(unmatched_users[0])
            del user_group[0]
        else:
            for index in unmatched_user_indexes:
                del user_group[index]
            index_to_be_removed = find_match_in_group(unmatched_users, match_user_dict) 
            del user_group[index_to_be_removed]



def matching_algo(all_users_dict):
    match_user_dict = dict()
    platonic_users, non_platonic_users = form_groups(all_users_dict)
    matching_algo_for_user_group(platonic_users, match_user_dict)
    matching_algo_for_user_group(non_platonic_users, match_user_dict)
    if match_user_dict.get('unmatched') is not None:
        unmatched = match_user_dict['unmatched']
        matching_algo_for_user_group(unmatched)



