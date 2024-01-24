from re import M

# program to print all subsequence of a
# given string.

# set to store all the subsequences
counter_substring_dict = {}
source_of_substr_dict = {}
temp_set = {}

# Function computes all the subsequence of an string
def create_subsequence_dict(str, d, line_number):
    # Iterate over the entire string
    for i in range(0, len(str), 4):

        # Iterate from the end of the string
        # to generate substrings
        for j in range(len(str), i, -4):
            sub_str = str[i: i + j]
            if len(sub_str) == 4 * d:
                my_set = set()
                my_str = sub_str
                for i in range(0, len(sub_str), 4):
                    my_item = sub_str[i:i + 4]
                    my_set.add(my_item)
                    if len(my_set) == d:
                        if not sub_str in temp_set:
                            my_frozen = frozenset(my_set)
                            if my_frozen in counter_substring_dict:
                                counter_substring_dict[my_frozen] += 1
                            else:
                                counter_substring_dict[my_frozen] = 1
                            temp_set.add(my_str)

            # Drop kth character in the substring
            # and if its not in the set then recur
            for k in range(4, len(sub_str), 4):
                sb = sub_str

                # Drop character from the string
                sb = sb.replace(sb[k:k + 4], "")
                create_subsequence_dict(sb, d, line_number)


def process_input_line(my_line, d):
    # Split the line and ignore the first element
    splited = my_line.split()[1:]

    my_str = ""
    x_counter = 0

    for item in splited:
        if item == "X":
            x_counter += 1
        else:
            if x_counter <= 2:
                my_str += item
            else:
                # Process the extracted string
                create_subsequence_dict(my_str, d, line_number)
                my_str = ""
            x_counter = 0
    if my_str != "":
        create_subsequence_dict(my_str, d, line_number)


with open("cog_words_bac.txt") as my_file:
    for line_number, my_line in enumerate(my_file, start=1):
        process_input_line(my_line, 2)
        temp_set = {}




# def all_genomes_subtrings(s,d):
#  genome_words_dict = {}
#  with open(s) as my_file:
#     for my_line in my_file:
#       splited = my_line.split()
#       x_counter = 0
#       for j in range(1,len(splited)):
#         my_str = ""
#         if splited[j] == "x":
#             x_counter += 1
#         else:
#           if x_counter <= 2:
#             my_str += splited[j]
#           else:
#             genome_words_dict[my_str] = my_line
#             print("my string is:")
#             print(my_str)
#             my_str = ""
#           x_counter = 0

#   for word in genome_words_dict.keys():
#     create_subsequence_dict(word, d, genome_words_dict[word])


# all_genomes_subtrings("cog_words_bac.txt",2)

