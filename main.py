import json
import requests
import random
import discord

#Functionality:
# - Gives random question based on difficulty of question
# - Search for title ???
# - Add paid/non-paid problems
# - Add help option

client = discord.Client()
TOKEN = "ODcxNDYxMTEyOTMwMDAwOTg2.YQbpaA.n5yamWEscZ02kb9XXRYbbxvDqMI"

ALGORITHMS_ENDPOINT_URL = "https://leetcode.com/api/problems/algorithms/"

algorithms_problems_json = requests.get(ALGORITHMS_ENDPOINT_URL).content
data = json.loads(algorithms_problems_json)

print(data["user_name"])


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user: #checking to see if message is from someone other than our bot user
        return

    command = message.content.lower()

    if command.startswith('$random'):
        if 'easy' in command:
            easy = return_problem('easy')
            await message.channel.send(easy[0] + ' - ' + str(easy[2]) + '\n' + easy[1])
        elif 'medium' in command:
            medium = return_problem('medium')
            await message.channel.send(medium[0] + ' - ' +  str(medium[2]) + '\n' + medium[1])
        elif 'hard' in command:
            hard = return_problem('hard')
            await message.channel.send(hard[0] + ' - ' + str(hard[2]) + '\n' + hard[1])
        elif command == '$random':
            rand = return_problem('na')
            await message.channel.send(rand[0] + ' - ' + str(rand[2]) + '\n' + rand[1])
        else:
            await message.channel.send('Invalid command!')
    elif command.startswith("$num_solved"):
        await message.channel.send("Total number of questions solved: " + str(data["num_solved"]) + "\n" + 
                                    "Number of easies solved: " + str(data["ac_easy"]) + "\n" + 
                                    "Number of mediums solved: " + str(data["ac_medium"]) + "\n" +
                                    "Number of hards solved: " + str(data["ac_hard"]))
    else:
        await message.channel.send('Invalid command!')


            

def return_problem(difficulty):
    

    difficulty = difficulty.lower()

    difficulty_map = {
        "na" : 0,
        "easy" : 1,
        "medium" : 2,
        "hard" : 3
    }

    difficulty_int = difficulty_map[difficulty]

    stat_status_pairs = data["stat_status_pairs"]

    while True:
        rand = random.randint(0, len(stat_status_pairs)) #This is the random index of the list of questions
        if not stat_status_pairs[rand]["paid_only"]: #only free problems
            if stat_status_pairs[rand]["difficulty"]["level"] == difficulty_int:
                question__title_slug = stat_status_pairs[rand]["stat"]["question__title_slug"]
                question__article__slug = stat_status_pairs[rand]["stat"]["question__article__slug"]
                question__title = stat_status_pairs[rand]["stat"]["question__title"]
                frontend_question_id = stat_status_pairs[rand]["stat"]["frontend_question_id"]
                break
            elif difficulty_int == 0: #If user doesn't specify the difficulty
                question__title_slug = stat_status_pairs[rand]["stat"]["question__title_slug"]
                question__article__slug = stat_status_pairs[rand]["stat"]["question__article__slug"]
                question__title = stat_status_pairs[rand]["stat"]["question__title"]
                frontend_question_id = stat_status_pairs[rand]["stat"]["frontend_question_id"]

                if (stat_status_pairs[rand]["difficulty"]["level"] == 1):
                    difficulty = "easy"
                elif (stat_status_pairs[rand]["difficulty"]["level"] == 2):
                    difficulty = "medium"
                elif (stat_status_pairs[rand]["difficulty"]["level"] == 3):
                    difficulty = "hard"
                else:
                    raise Exception("Could not match difficulty!")
                break


    print(question__title)
    url = f"https://leetcode.com/problems/{question__title_slug}/"
    print(url)

    difficulty = difficulty[0].upper() + difficulty[1:] #uppercasing difficulty for display

    return question__title, url, difficulty

client.run(TOKEN)



    
