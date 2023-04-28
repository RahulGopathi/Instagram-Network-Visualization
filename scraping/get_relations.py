from bot import Bot
import argparse
import os.path


def generate_txt(relations_file, my_followers_arr, username):
    relations = open(relations_file, 'w+')
    for key in my_followers_arr:
        line = "https://www.instagram.com/" + key + "/ " + "https://www.instagram.com/" + username + "/\n" + "https://www.instagram.com/" + username + "/ " + "https://www.instagram.com/" + key + "/\n"
        relations.write(line)


def get_start_profile():
    with open('start_profile.txt') as f:
        return int(f.readline())


def get_my_followers_from_txt():
    my_followers_arr = []
    with open('my_followers.txt') as f:
        for line in f:
            my_followers_arr.append(line.rstrip('\n'))
    return my_followers_arr


def get_relations(config):
    relations_file = "relations.txt"
    username = config.username
    password = config.password
    b = Bot()

    b.setUp()
    b.login(username, password)

    my_followers_arr = get_my_followers_from_txt()
    if not os.path.isfile(relations_file):
        generate_txt(relations_file, my_followers_arr, username)

    b.get_followers(my_followers_arr, relations_file)


if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    # input parameters
    parser.add_argument('--username', type=str)
    parser.add_argument('--password', type=str)

    config = parser.parse_args()

    get_relations(config)
