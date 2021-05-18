import random


def generate_random_friendships(users, friendships_count=None):
    for i in range(friendships_count or len(users)):
        user, friend = random.sample(users, 2)
        user.friends.add(friend)
