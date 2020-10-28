import random
import math
import time


movie_pool = ['D2: The Mighty Ducks', 'D2: The Mighty Ducks', 'D2: The Mighty Ducks', 'D2: The Mighty Ducks',
              'Toy story 2', 'Toy story 2', 'Toy story 2',
              'Captain America: Winter Soldier', 'Captain America: Winter Soldier', 'Captain America: Winter Soldier',
              'Guardians 2', 'Guardians 2', 'Guardians 2',
              'Empire Strikes Back', 'Empire Strikes Back',
              'Frozen II', 'Frozen II',
              'Incredibles 2', 'Incredibles 2',
              'Three men and a little lady',
              'Rescuers down under',
              'Star Wars: The Last Jedi',
              'Tron legacy',
              'Alice through the looking glass',
              'National treasure 2',
              'Pirates of the Carribean: Dead Man\'s Chest',
              'Gremlins 2', 'Gremlins 2', 'Gremlins 2', 'Gremlins 2',
              'Teenage Mutant Ninja Turtles II', 'Teenage Mutant Ninja Turtles II', 'Teenage Mutant Ninja Turtles II',
              'Lord of the Rings: The Two Towers', 'Lord of the Rings: The Two Towers', 'Lord of the Rings: The Two Towers',
              'Lethal weapon 2', 'Lethal weapon 2', 'Lethal weapon 2',
              'Matrix Reloaded', 'Matrix Reloaded', 'Matrix Reloaded',
              'Austin Powers: The Spy Who Shagged Me', 'Austin Powers: The Spy Who Shagged Me', 'Austin Powers: The Spy Who Shagged Me',
              'Flintstones: Viva rock Vegas', 'Flintstones: Viva rock Vegas', 'Flintstones: Viva rock Vegas',
              'Superman II', 'Superman II', 'Superman II',
              'Lego Movie 2', 'Lego Movie 2', 'Lego Movie 2',
              'Home Alone 2: Lost in NY', 'Home Alone 2: Lost in NY', 'Home Alone 2: Lost in NY',
              'Dirty Dancing: Havana Nights', 'Dirty Dancing: Havana Nights', 'Dirty Dancing: Havana Nights',
              'Batman Returns', 'Batman Returns', 'Batman Returns',
              'Sherlock Holmes: a Game of Shadows', 'Sherlock Holmes: a Game of Shadows',
              'Die Hard 2', 'Die Hard 2',
              'City Slickers 2', 'City Slickers 2',
              'Babe: Pig in the city',
              'Aliens',
              'Next Friday',
              'Oceans Twelve', 'Oceans Twelve', 'Oceans Twelve', 'Oceans Twelve',
              'Back To The Future II', 'Back To The Future II', 'Back To The Future II',
              'Indiana Jones and the Temple of Doom', 'Indiana Jones and the Temple of Doom', 'Indiana Jones and the Temple of Doom',
              'Ace Ventura when nature calls', 'Ace Ventura when nature calls', 'Ace Ventura when nature calls',
              'Ralph breaks the internet', 'Ralph breaks the internet', 'Ralph breaks the internet',
              'The never ending story II: the next chapter', 'The never ending story II: the next chapter',
              'How to train your dragon 2',
              'Johnny English reborn',
              'Tomorrow never dies',
              'Meet the fockers', 'Meet the fockers', 'Meet the fockers',
              'Star Trek II: The Wrath of Khan', 'Star Trek II: The Wrath of Khan',
              'Quantum of solace', 'Quantum of solace']

count = 0
bracket = []
randomized_pool = movie_pool[:]
random.shuffle(randomized_pool)


def check(movie):
    if movie in bracket:
        return True
    return False


while count < 32:
    idx = random.randint(0, len(randomized_pool)-1)
    pick = movie_pool[idx]
    if check(pick):
        continue
    else:
        bracket.append(pick)
        count += 1


print(len(bracket))
cnt = 1
for movie in bracket:
    print(f"{cnt}:{movie}")
    if cnt % 2 == 0:
        time.sleep(10)
    cnt += 1
