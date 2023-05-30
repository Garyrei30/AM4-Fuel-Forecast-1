import database
import os
import discord
from discord.ext import commands
from keep_alive import keep_alive
from discord import Embed

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


def get_discord_time(time):
        clock_emojis = {
                '00:00': '<t:0:t>',
                '00:30': '<t:1800:t>',
                '01:00': '<t:3600:t>',
                '01:30': '<t:5400:t>',
                '02:00': '<t:7200:t>',
                '02:30': '<t:9000:t>',
                '03:00': '<t:10800:t>',
                '03:30': '<t:12600:t>',
                '04:00': '<t:14400:t>',
                '04:30': '<t:16200:t>',
                '05:00': '<t:18000:t>',
                '05:30': '<t:19800:t>',
                '06:00': '<t:21600:t>',
                '06:30': '<t:23400:t>',
                '07:00': '<t:25200:t>',
                '07:30': '<t:27000:t>',
                '08:00': '<t:28800:t>',
                '08:30': '<t:30600:t>',
                '09:00': '<t:32400:t>',
                '09:30': '<t:34200:t>',
                '10:00': '<t:36000:t>',
                '10:30': '<t:37800:t>',
                '11:00': '<t:39600:t>',
                '11:30': '<t:41400:t>',
                '12:00': '<t:43200:t>',
                '12:30': '<t:45000:t>',
                '13:00': '<t:46800:t>',
                '13:30': '<t:48600:t>',
                '14:00': '<t:50400:t>',
                '14:30': '<t:52200:t>',
                '15:00': '<t:54000:t>',
                '15:30': '<t:55800:t>',
                '16:00': '<t:57600:t>',
                '16:30': '<t:59400:t>',
                '17:00': '<t:61200:t>',
                '17:30': '<t:63000:t>',
                '18:00': '<t:64800:t>',
                '18:30': '<t:66600:t>',
                '19:00': '<t:68400:t>',
                '19:30': '<t:70200:t>',
                '20:00': '<t:72000:t>',
                '20:30': '<t:73800:t>',
                '21:00': '<t:75600:t>',
                '21:30': '<t:77400:t>',
                '22:00': '<t:79200:t>',
                '22:30': '<t:81000:t>',
                '23:00': '<t:82800:t>',
                '23:30': '<t:84600:t>',
        }
        return clock_emojis.get(time, '⏰')


def create_embed(data, daily:int = 0, date:int=1):
        if daily==1:
                embed = Embed(title=f"Fuel & CO2 price forecast for Day {date}", color=discord.Color.green())
        else:
                embed = Embed(title="Fuel & CO2 price forecast for the next 5 hours", color=discord.Color.blurple())
        embed.set_author(name="Regius Fuel Bot")
        embed.set_footer(text="By Ben Airways")

        description = ""
        for entry in data:
                time = entry[0]
                fuel_price = entry[1]
                co2_price = entry[2]

                discord_time = get_discord_time(time)
                formatted_entry = f"🕑 {discord_time}\n⛽️: {fuel_price.ljust(8)}  ♻️: {co2_price}\n\n"
                description += formatted_entry

        embed.description = description

        return embed


@bot.event
async def on_ready():
        print("Bot is connected and ready.")


@bot.command()
async def fuel(ctx, message: str = ""):
        if message.upper() == "DAILY" and (ctx.channel.id == os.environ['BotServer'] or ctx.channel.id == os.environ['RegiusTest'] or ctx.channel.id == os.environ['RegiusFuel']):
                data, date = database.getDailyPrice()

                # Create a new embed message
                # Create the embed message using the data
                embed = create_embed(data,1,date)
                message = await ctx.send(embed=embed)
                
                # Clear all the pins
                pins = await bot.get_channel(ctx.channel.id).pins()
                for message in pins:
                        await message.unpin()
                
                # Create a new Pin
                await message.pin()

        elif ctx.channel.id == os.environ['BotServer'] or ctx.channel.id == os.environ['RegiusTest'] or ctx.channel.id == os.environ['RegiusFuel']:
                data = database.getPrice()
                # Create a new embed message
                embed = create_embed(data)
                await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.channel.id == os.environ['GetFuelID'] and message.content.startswith('$Fuel&CO2!'):
        content = message.content.split(" ")
        fuel = content[1]
        co2 = content[2]
        dbData, table_name = database.getCurrentPrice()
        dbTime = dbData[0]
        dbFuel = dbData[1]
        dbCO2 = dbData[2]
        if int(fuel) != int(dbFuel) and int(co2) != int(dbCO2):
           text = database.updateBoth(table_name, dbTime, fuel, co2)
           channel = bot.get_channel(os.environ['LogFuelID'])
           await channel.send(text)

        elif int(fuel) != int(dbFuel):
            text = database.updateFuel(table_name,dbTime,fuel)
            channel = bot.get_channel(os.environ['LogFuelID'])
            await channel.send(text)
        elif int(co2) != int(dbCO2):
            text = database.updateCO2(table_name,dbTime,co2)
            channel = bot.get_channel(os.environ['LogFuelID'])
            await channel.send(text)
    await bot.process_commands(message)
                        
# Keep the main thread alive with a Flask web server
keep_alive()

# Run the Bot
bot.run(os.environ['DISCORDKEY'])
