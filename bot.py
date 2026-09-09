#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Discord Event Bot - All-in-one
クイズ、くじ、イベント管理機能を備えたDiscord bot
"""

import discord
from discord.ext import commands
from discord import app_commands
import json
import os
from datetime import datetime
import random

# ============================================================================
# Bot Setup
# ============================================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Data file paths
EVENTS_FILE = 'events.json'
QUIZ_FILE = 'quizzes.json'
LOTTERY_FILE = 'lotteries.json'

# ============================================================================
# Utility Functions
# ============================================================================

def init_files():
    """Initialize JSON data files"""
    for file in [EVENTS_FILE, QUIZ_FILE, LOTTERY_FILE]:
        if not os.path.exists(file):
            with open(file, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

def load_data(file):
    """Load data from JSON file"""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_data(file, data):
    """Save data to JSON file"""
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ============================================================================
# Bot Events
# ============================================================================

@bot.event
async def on_ready():
    """Called when bot is ready"""
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Failed to sync commands: {e}')

# ============================================================================
# Event Management Commands
# ============================================================================

@bot.tree.command(name='event_create', description='新しいイベントを作成')
@app_commands.describe(
    event_name='イベント名',
    description='イベントの説明',
    date='開催日時 (YYYY-MM-DD HH:MM)'
)
async def event_create(interaction: discord.Interaction, event_name: str, description: str, date: str):
    """Create a new event"""
    init_files()
    events = load_data(EVENTS_FILE)
    
    event_id = str(len(events) + 1)
    events[event_id] = {
        'name': event_name,
        'description': description,
        'date': date,
        'creator': str(interaction.user.id),
        'participants': [],
        'created_at': datetime.now().isoformat()
    }
    
    save_data(EVENTS_FILE, events)
    
    embed = discord.Embed(title='✅ イベント作成完了', color=discord.Color.green())
    embed.add_field(name='イベント名', value=event_name, inline=False)
    embed.add_field(name='説明', value=description, inline=False)
    embed.add_field(name='開催日時', value=date, inline=False)
    embed.add_field(name='イベントID', value=event_id, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='event_list', description='イベント一覧を表示')
async def event_list(interaction: discord.Interaction):
    """List all events"""
    init_files()
    events = load_data(EVENTS_FILE)
    
    if not events:
        await interaction.response.send_message('🗑️ イベントはまだ登録されていません')
        return
    
    embed = discord.Embed(title='📅 イベント一覧', color=discord.Color.blue())
    for event_id, event in events.items():
        participants_count = len(event.get('participants', []))
        embed.add_field(
            name=f"ID: {event_id} - {event['name']}",
            value=f"日時: {event['date']}\n説明: {event['description']}\n参加者: {participants_count}人",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='event_join', description='イベントに参加')
@app_commands.describe(event_id='参加するイベントのID')
async def event_join(interaction: discord.Interaction, event_id: str):
    """Join an event"""
    init_files()
    events = load_data(EVENTS_FILE)
    
    if event_id not in events:
        await interaction.response.send_message('❌ そのイベントは存在しません', ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    if user_id in events[event_id]['participants']:
        await interaction.response.send_message('❌ 既に参加しています', ephemeral=True)
        return
    
    events[event_id]['participants'].append(user_id)
    save_data(EVENTS_FILE, events)
    
    embed = discord.Embed(title='✅ 参加完了', color=discord.Color.green())
    embed.add_field(name='イベント', value=events[event_id]['name'])
    embed.add_field(name='参加者数', value=len(events[event_id]['participants']))
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='event_leave', description='イベントから退出')
@app_commands.describe(event_id='退出するイベントのID')
async def event_leave(interaction: discord.Interaction, event_id: str):
    """Leave an event"""
    init_files()
    events = load_data(EVENTS_FILE)
    
    if event_id not in events:
        await interaction.response.send_message('❌ そのイベントは存在しません', ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    if user_id not in events[event_id]['participants']:
        await interaction.response.send_message('❌ 参加していません', ephemeral=True)
        return
    
    events[event_id]['participants'].remove(user_id)
    save_data(EVENTS_FILE, events)
    
    embed = discord.Embed(title='✅ 退出完了', color=discord.Color.green())
    embed.add_field(name='イベント', value=events[event_id]['name'])
    embed.add_field(name='残り参加者', value=len(events[event_id]['participants']))
    
    await interaction.response.send_message(embed=embed)

# ============================================================================
# Quiz Commands
# ============================================================================

@bot.tree.command(name='quiz_create', description='クイズを作成')
@app_commands.describe(
    quiz_name='クイズ名',
    question='問題文',
    option_a='選択肢A',
    option_b='選択肢B',
    option_c='選択肢C',
    option_d='選択肢D',
    answer='答え (A, B, C, D)'
)
async def quiz_create(interaction: discord.Interaction, quiz_name: str, question: str, 
                      option_a: str, option_b: str, option_c: str, option_d: str, answer: str):
    """Create a new quiz"""
    init_files()
    quizzes = load_data(QUIZ_FILE)
    
    if answer.upper() not in ['A', 'B', 'C', 'D']:
        await interaction.response.send_message('❌ 答えは A, B, C, D のいずれかで指定してください', ephemeral=True)
        return
    
    quiz_id = str(len(quizzes) + 1)
    quizzes[quiz_id] = {
        'name': quiz_name,
        'question': question,
        'options': {'A': option_a, 'B': option_b, 'C': option_c, 'D': option_d},
        'answer': answer.upper(),
        'creator': str(interaction.user.id),
        'created_at': datetime.now().isoformat()
    }
    
    save_data(QUIZ_FILE, quizzes)
    
    embed = discord.Embed(title='✅ クイズ作成完了', color=discord.Color.green())
    embed.add_field(name='クイズ名', value=quiz_name, inline=False)
    embed.add_field(name='クイズID', value=quiz_id, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='quiz_start', description='クイズを開始')
@app_commands.describe(quiz_id='開始するクイズのID')
async def quiz_start(interaction: discord.Interaction, quiz_id: str):
    """Start a quiz"""
    init_files()
    quizzes = load_data(QUIZ_FILE)
    
    if quiz_id not in quizzes:
        await interaction.response.send_message('❌ そのクイズは存在しません', ephemeral=True)
        return
    
    quiz = quizzes[quiz_id]
    
    embed = discord.Embed(title=f"🧠 {quiz['name']}", color=discord.Color.purple())
    embed.add_field(name='問題', value=quiz['question'], inline=False)
    embed.add_field(name='A', value=quiz['options']['A'], inline=True)
    embed.add_field(name='B', value=quiz['options']['B'], inline=True)
    embed.add_field(name='C', value=quiz['options']['C'], inline=True)
    embed.add_field(name='D', value=quiz['options']['D'], inline=True)
    embed.set_footer(text='リアクションで回答してください')
    
    msg = await interaction.response.send_message(embed=embed)
    
    # Add reaction options
    await msg.add_reaction('🇦')
    await msg.add_reaction('🇧')
    await msg.add_reaction('🇨')
    await msg.add_reaction('🇩')

@bot.tree.command(name='quiz_answer', description='クイズの答えを表示')
@app_commands.describe(quiz_id='クイズID')
async def quiz_answer(interaction: discord.Interaction, quiz_id: str):
    """Show quiz answer"""
    init_files()
    quizzes = load_data(QUIZ_FILE)
    
    if quiz_id not in quizzes:
        await interaction.response.send_message('❌ そのクイズは存在しません', ephemeral=True)
        return
    
    quiz = quizzes[quiz_id]
    correct_answer = quiz['answer']
    
    embed = discord.Embed(title=f"📝 クイズ結果 - {quiz['name']}", color=discord.Color.gold())
    embed.add_field(name='問題', value=quiz['question'], inline=False)
    embed.add_field(name='正解', value=f"{correct_answer}: {quiz['options'][correct_answer]}", inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='quiz_list', description='クイズ一覧を表示')
async def quiz_list(interaction: discord.Interaction):
    """List all quizzes"""
    init_files()
    quizzes = load_data(QUIZ_FILE)
    
    if not quizzes:
        await interaction.response.send_message('🗑️ クイズはまだ登録されていません')
        return
    
    embed = discord.Embed(title='📚 クイズ一覧', color=discord.Color.blue())
    for quiz_id, quiz in quizzes.items():
        embed.add_field(
            name=f"ID: {quiz_id} - {quiz['name']}",
            value=f"問題: {quiz['question']}",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# ============================================================================
# Lottery Commands
# ============================================================================

@bot.tree.command(name='lottery_create', description='くじを作成')
@app_commands.describe(
    lottery_name='くじ名',
    description='くじの説明',
    prizes='景品 (カンマ区切り)',
    quantity='各景品の数'
)
async def lottery_create(interaction: discord.Interaction, lottery_name: str, description: str, prizes: str, quantity: int):
    """Create a new lottery"""
    init_files()
    lotteries = load_data(LOTTERY_FILE)
    
    prize_list = [p.strip() for p in prizes.split(',')]
    
    lottery_id = str(len(lotteries) + 1)
    lotteries[lottery_id] = {
        'name': lottery_name,
        'description': description,
        'prizes': prize_list,
        'quantity_per_prize': quantity,
        'tickets': [],
        'winners': [],
        'creator': str(interaction.user.id),
        'created_at': datetime.now().isoformat()
    }
    
    save_data(LOTTERY_FILE, lotteries)
    
    embed = discord.Embed(title='✅ くじ作成完了', color=discord.Color.green())
    embed.add_field(name='くじ名', value=lottery_name, inline=False)
    embed.add_field(name='説明', value=description, inline=False)
    embed.add_field(name='景品', value=', '.join(prize_list), inline=False)
    embed.add_field(name='くじID', value=lottery_id, inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='lottery_draw', description='くじに参加')
@app_commands.describe(lottery_id='くじID')
async def lottery_draw(interaction: discord.Interaction, lottery_id: str):
    """Join a lottery"""
    init_files()
    lotteries = load_data(LOTTERY_FILE)
    
    if lottery_id not in lotteries:
        await interaction.response.send_message('❌ そのくじは存在しません', ephemeral=True)
        return
    
    user_id = str(interaction.user.id)
    lottery = lotteries[lottery_id]
    
    if user_id in lottery['tickets']:
        await interaction.response.send_message('❌ 既にこのくじに参加しています', ephemeral=True)
        return
    
    lottery['tickets'].append(user_id)
    save_data(LOTTERY_FILE, lotteries)
    
    embed = discord.Embed(title='✅ くじに参加しました', color=discord.Color.green())
    embed.add_field(name='くじ名', value=lottery['name'])
    embed.add_field(name='参加者数', value=len(lottery['tickets']))
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='lottery_winner', description='くじの当選者を抽選')
@app_commands.describe(lottery_id='くじID')
async def lottery_winner(interaction: discord.Interaction, lottery_id: str):
    """Draw winners from a lottery"""
    init_files()
    lotteries = load_data(LOTTERY_FILE)
    
    if lottery_id not in lotteries:
        await interaction.response.send_message('❌ そのくじは存在しません', ephemeral=True)
        return
    
    lottery = lotteries[lottery_id]
    
    if len(lottery['tickets']) == 0:
        await interaction.response.send_message('❌ 参加者がいません', ephemeral=True)
        return
    
    # Draw winners
    winners_list = []
    tickets = lottery['tickets'].copy()
    
    for prize in lottery['prizes']:
        for _ in range(lottery['quantity_per_prize']):
            if not tickets:
                break
            winner_id = random.choice(tickets)
            winners_list.append((winner_id, prize))
            tickets.remove(winner_id)
    
    lottery['winners'] = winners_list
    save_data(LOTTERY_FILE, lotteries)
    
    embed = discord.Embed(title=f"🎉 {lottery['name']} - 抽選結果", color=discord.Color.gold())
    
    for winner_id, prize in winners_list:
        embed.add_field(name='当選者', value=f"<@{winner_id}>", inline=True)
        embed.add_field(name='景品', value=prize, inline=True)
        embed.add_field(name='', value='', inline=False)
    
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='lottery_list', description='くじ一覧を表示')
async def lottery_list(interaction: discord.Interaction):
    """List all lotteries"""
    init_files()
    lotteries = load_data(LOTTERY_FILE)
    
    if not lotteries:
        await interaction.response.send_message('🗑️ くじはまだ登録されていません')
        return
    
    embed = discord.Embed(title='🎰 くじ一覧', color=discord.Color.blue())
    for lottery_id, lottery in lotteries.items():
        embed.add_field(
            name=f"ID: {lottery_id} - {lottery['name']}",
            value=f"説明: {lottery['description']}\n景品: {', '.join(lottery['prizes'])}\n参加者: {len(lottery['tickets'])}人",
            inline=False
        )
    
    await interaction.response.send_message(embed=embed)

# ============================================================================
# Main
# ============================================================================

if __name__ == '__main__':
    init_files()
    # Replace with your bot token
    bot.run('YOUR_BOT_TOKEN_HERE')
