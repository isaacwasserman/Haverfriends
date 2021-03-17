from scipy.spatial import distance  
import random
# this function will be used to match the first user in the queue with other users in the queue.
# it returns the index for the matched user to be popped. Match_user_dict will get a new key (user_id for one of the indivs in the pair)
# and the value will be the user_id for the other party + chat_id (the concatenation of their user_ids)
def find_match_in_group(user_group, match_user_dict):
    current_user_detail = user_group[0][1]
    match_rank_dataset = [(None, None, None), (None, None, None), (None, None, None)] # Inside each tuple, [0]: euclidean distance score, [1]: match's id, [2]: match's index
    for i in range(1, len(user_group)):
        if user_group[0][0] in user_group[i][2]: # if current user has already been matched with this user, skip
            continue 
        dst = distance.euclidean(user_group[0][1]['questionnaire_scores'], user_group[i][1]['questionnaire_scores'])
        if match_rank_dataset[0][0] is None: # fill up the three slots first before we start comparing distance values
            match_rank_dataset[0] = (dst, user_group[i][0], i)
        elif match_rank_dataset[1][0] is None:
            match_rank_dataset[1] = (dst, user_group[i][0], i)
        elif match_rank_dataset[2][0] is None:
            match_rank_dataset[2] = (dst, user_group[i][0], i)
        else:
            if dst < match_rank_dataset[0][0]: # shuffle the ranking depending on the distance score for the matches
                match_rank_dataset[1], match_rank_dataset[2] = match_rank_dataset[0], match_rank_dataset[1]
                match_rank_dataset[0] = (dst, user_group[i][0], i)
            elif dst < match_rank_dataset[1][0]:
                match_rank_dataset[2] = match_rank_dataset[1]
                match_rank_dataset[1] = (dst, user_group[i][0], i)
            elif dst < match_rank_dataset[2][0]:
                match_rank_dataset[2] = (dst, user_group[i][0], i)
        if match_rank_dataset[0][0] == 0 and match_rank_dataset[1][0] == 0 and match_rank_dataset[2][0] == 0: # If we have found three matches with perfect score, we stop looking for people
            break
    # compile final matches (removing None data if we were not able to find 3 matches) as (user_id, chat_id)
    final_matches_for_current_user = [(x[1], str(min(x[1], user_group[0][0])) + '_' + str(max(x[1], user_group[0][0])))  for x in match_rank_dataset if x[0] is not None]
    # add final matches to match_uer_dict[current_user]. At the api level, the dictionary will be iterated through and match relationship will be updated and mirrored
    match_user_dict[user_group[0][0]] = final_matches_for_current_user
    # append matched user_ids for all involved users to track accumulated matches for this cycle
    user_group[0][2].append([x[0] for x in final_matches_for_current_user])

    other_users_to_be_removed_from_user_group = [] # basically all users that do not need matches anymore. 
    for user in match_rank_dataset: # add one more match (current user) to the other users
        if user[2] is not None:
            user_group[user[2]][2].append(user_group[0][0]) 
            if len(user_group[user[2]][2]) >= 3:
                other_users_to_be_removed_from_user_group.append(user[2]) # add user to list of users who don't need matches
    return other_users_to_be_removed_from_user_group

def form_groups(all_users_dict):
    platonic_users = []
    non_platonic_users = []
    for user_id, user_details in all_users_dict.items():
        if user_details['want_match'] and len(user_details['questionnaire_scores']) == 5:
            if user_details['want_platonic']:
                platonic_users.append((user_id, user_details, [])) # the empty list added in the tuple is meant to track the number of new matches a user has
            else:
                non_platonic_users.append((user_id, user_details, []))
    return platonic_users, non_platonic_users

def find_unmatched_users(user_group):
    main_user = user_group[0]
    other_users = user_group[1:]
    former_matches_of_main_user = set(main_user[1]['active_chat_partners'])
    unmatched_users = [main_user]
    unmatched_user_indexes = [0]
    for index, other_user in enumerate(other_users):
        other_user_id = other_user[0]
        other_user_new_matches = other_user[2]
        if other_user_id not in former_matches_of_main_user and len(other_user_new_matches) < 3: # make sure we only matched people whom the main user have not interacted with before and the person must also not have 3 matches in this matching cycle
            unmatched_users.append(other_user)
            unmatched_user_indexes.append(index+1)
    return unmatched_user_indexes, unmatched_users

def matching_algo_for_user_group(usergroup, match_user_dict):
    user_group = usergroup.copy()
    while len(user_group) > 0:
        unmatched_user_indexes, unmatched_users = find_unmatched_users(user_group)
        if len(unmatched_users) == 1 and len(unmatched_users[0][2]) == 0:
            if match_user_dict.get('unmatched') is None:
                match_user_dict['unmatched'] = [unmatched_users[0]]
            else:
                match_user_dict['unmatched'].append(unmatched_users[0])
            del user_group[0]
        else:
            index_to_be_removed = find_match_in_group(unmatched_users, match_user_dict) #the index here refers to the index of the unmatched_users list
            # print('index_to_be_removed', index_to_be_removed)
            # print('unmatched_user_indexes', unmatched_user_indexes)
            # print('user_group', user_group)
            for index in sorted(index_to_be_removed, reverse=True): # sort the indices so that we remove from the back so we don't mess up the order/index
                del user_group[unmatched_user_indexes[index]] # translate unmatched_user_group id to normal user id and delete user from user_group
            del user_group[0] # removed current user from user_group since they either have 3 matches or can't be matched with anyone already (not enough people)



# takes in a dictionary with user_ids as keys and user_details as value
# returns a dictionary with key (user_id for one of the indivs in the pair)
# and the value will be the user_id for the other party + chat_id (the concatenation of their user_ids)
# it also returns a list of tuples (user_id, user_details) that contain individuals who are not matched
def matching_algo(all_users_dict):
    match_user_dict = dict()
    platonic_users, non_platonic_users = form_groups(all_users_dict)
    matching_algo_for_user_group(platonic_users, match_user_dict)
    matching_algo_for_user_group(non_platonic_users, match_user_dict)
    still_unmatched = []
    if match_user_dict.get('unmatched') is not None:
        unmatched = match_user_dict['unmatched']
        for indiv in unmatched:
            indiv_id = indiv[0]
            random.shuffle(non_platonic_users)
            for non_platonic_user in non_platonic_users:
                if indiv_id not in set(non_platonic_user[1]['active_chat_partners']) and indiv_id != non_platonic_user[0] :
                    match_user_dict[indiv_id] = (non_platonic_user[0], str(min(indiv[0], non_platonic_user[0])) + '_' + str(max(indiv[0], non_platonic_user[0])))
                    break
            if match_user_dict.get(indiv_id) is None:
                still_unmatched.append(indiv)
            else:
                break
    return match_user_dict, still_unmatched

def find_match_for_new_user(new_user_id, all_users_dict):
    match_user_dict = dict()
    still_unmatched = []
    platonic_users, non_platonic_users = form_groups(all_users_dict)
    # we are only working with platonic users for this version
    users_pool = platonic_users.copy()
    print(users_pool)
    users_pool = sorted(users_pool, key=lambda tup: len(tup[1]['matched_count'])) # sort to ascending order of number of match_counts. The goal is to match new user with old users with low match counts
    for index, value in enumerate(users_pool): # swap new user to the front of the list. The user that was originally at the start of the list should either have zero or a really low match count
        if value[0] == new_user_id:
            users_pool[index], users_pool[0] = users_pool[0], users_pool[index]
            break
    index_to_be_removed = find_match_in_group(users_pool, match_user_dict) #the index here refers to the index of the unmatched_users list
    return match_user_dict, still_unmatched


if __name__ == "__main__":
    # PYTHONHASHSEED=1833

    # random.seed(10)
    def create_all_users_dict(num_users):
        users_dict = dict()
        for i in range(num_users):
            users_dict[i] = {'want_match': True, 'want_platonic': False, 'questionnaire_scores': [random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5), random.randint(0, 5)], 'active_chat_partners':[]}
        return users_dict
    user_dict = create_all_users_dict(30)

    # print(user_dict)
    print(matching_algo(user_dict))
            



