import sys

original_data_dict = {}
all_clusters_dict = {}
final_clusters_dict = {}
clusters_list = []
gen_uid_dict = {}


def process_data(file):
    with open(file) as my_file:
        for line in my_file:
            splited = line.split("#")
            genome_number = splited[1]
            line_of_uid = splited[-2]
            splited_uid_line = line_of_uid.split("_")
            my_uid = splited_uid_line[-1]
            word_segment = splited[-1]
            gen_uid_dict[genome_number] = my_uid
            splited_word = word_segment.split("\t")
            my_str = ""
            my_list = []
            for i in range(1, len(splited_word) - 1):
                if splited_word[i] != "X":
                    my_str += splited_word[i]
                else:
                    if my_str != "":
                        if genome_number in original_data_dict:
                            original_data_dict[genome_number].append(my_str)
                        else:
                            if my_str != "":
                                my_list.append(my_str)
                                original_data_dict[genome_number] = my_list
                        my_str = ""
            if my_str != "":
                if genome_number in original_data_dict:
                    original_data_dict[genome_number].append(my_str)
                else:
                    my_list.append(my_str)
                    original_data_dict[genome_number] = my_list


def find_clusters(s, d, q):
    for curr_genome in s:
        genome_substrings_dict = {}
        for segment in s[curr_genome]:
            for i in range(0, len(segment) - 4, 4):
                curr_order = segment[i:i + 4 * d]
                my_set = set()
                for j in range(i, i + 4 * d, 4):
                    my_set.add(segment[j:j + 4])
                my_frozen = frozenset(my_set)
                if my_frozen not in genome_substrings_dict:
                    if len(my_set) == d:
                        genome_substrings_dict[my_frozen] = curr_order

        for cluster in genome_substrings_dict:
            my_hashmap = {}
            if cluster not in all_clusters_dict:
                my_hashmap[curr_genome] = genome_substrings_dict[cluster]
                all_clusters_dict[cluster] = my_hashmap
            else:
                all_clusters_dict[cluster][curr_genome] = genome_substrings_dict[cluster]

    for cluster in all_clusters_dict:
        if len(all_clusters_dict[cluster]) >= q:
            clusters_list.append(cluster)
            final_clusters_dict[cluster] = all_clusters_dict[cluster]

    return clusters_list


rank_dict = {}


def create_clusters_rank_dict():  # C1
    sorted_list = sorted(final_clusters_dict, key=lambda key: len(final_clusters_dict[key]), reverse= True)
    for i in range(len(sorted_list)):
        rank_dict[sorted_list[i]] = i+1


cog_dict = {}


def create_cog_dict():  # C2
    with open("COG_INFO_TABLE.txt") as my_file:
        for line in my_file:
            splited = line.split(";")
            cog_number = splited[0]
            cog_dict[cog_number] = line


def get_pattern_info(cluster):
    create_cog_dict()
    for cog in cluster:
        key = "COG" + cog
        print(cog, cog_dict[key], end="")


taxa_dict = {}


def create_taxa_dict():  # C3A
    with open("taxa.txt") as my_file:
        lines = my_file.readlines()
        for i in range(1, len(lines)):
            splited = lines[i].split(",")
            uid_line = splited[-4]
            uid_word = uid_line.split("_")
            uid = uid_word[-1]
            taxa_dict[uid] = lines[i]


habitat_dict = {}


def create_habitat_dict():  # C3A
    with open("habitat.txt") as my_file:
        lines = my_file.readlines()
        for i in range(1, len(lines)):
            splited = lines[i].split(";")
            my_habitat = splited[-1]
            uid_line = splited[1]
            splited_uid = uid_line.split("_")
            uid = splited_uid[-1]
            habitat_dict[uid] = my_habitat


def get_taxa(cluster):
    create_taxa_dict()
    genome_dict = final_clusters_dict[cluster]
    for genome in genome_dict:
        line = taxa_dict[gen_uid_dict[genome]]
        print(genome, line, end='')


def get_habitat(cluster):
    create_habitat_dict()
    genome_dict = final_clusters_dict[cluster]
    habitats = {}
    for genome in genome_dict:
        habitat = habitat_dict[gen_uid_dict[genome]]
        if habitat in habitats:
            habitats[habitat] += 1
        else:
            habitats[habitat] = 1
    total = len(genome_dict)
    for habitat in habitats:
        percent = round(habitats[habitat] / total * 100)
        print("environment: ", habitat, end="")
        print("percentage: ", percent, "%")


def get_various_gene_orders(cluster):
    my_dict = final_clusters_dict[cluster]
    orders = {}
    total = len(my_dict)
    for gene in my_dict:
        if my_dict[gene] in orders:
            orders[my_dict[gene]] += 1
        else:
            orders[my_dict[gene]] = 1
    for order in orders:
        percent = round(orders[order] / total * 100)
        print(order, "percentage of order: ", percent, "%")


def get_cluster_profile(cluster):
    # check whether the function of rank needed to be called more than once
    create_clusters_rank_dict()
    print( set(cluster))
    print("Rank: ", rank_dict[cluster])
    print("")
    print("Pattern info: ")
    get_pattern_info(cluster)
    print("")
    print("Instance information: ")
    print("")
    print("Taxonomical info: ")
    get_taxa(cluster)
    print("")
    print("Various gene_order: ")
    get_various_gene_orders(cluster)
    print("")
    print("environmental description: ")
    get_habitat(cluster)
    print("")


# process_data("cog_words_plasmid.txt")
# find_clusters(original_data_dict, 2, 5)
# create_clusters_rank_dict()


def run_program(data_file):
    orig_stdout = sys.stdout
    process_data(data_file)
    for d_val in range(2,11):
        find_clusters(original_data_dict, d_val, 5)
        create_clusters_rank_dict()
        file_name = "gene_clusters_report_d=%s.txt" %d_val
        with open(file_name, 'w') as output_file:
            sys.stdout = output_file
            ranks = [key for key in rank_dict]
            my_ranks = ranks[:21]
            index = 1
            for cluster in my_ranks:
                to_print = str(index) + ")Cluster: "
                print(to_print, end="")
                get_cluster_profile(cluster)
                index +=1
        sys.stdout = orig_stdout
        output_file.close()


run_program("cog_words_plasmid.txt")

