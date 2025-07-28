import discord
from discord.ext import commands
import random
import time
import os
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

def case_insensitive_prefix(bot, message):
    prefixes = ["sq "]
    msg = message.content.lower()
    for prefix in prefixes:
        if msg.startswith(prefix):
            # Return the actual prefix length from the original message (to preserve case)
            return message.content[:len(prefix)]
    return None  # No prefix matched

bot = commands.Bot(command_prefix=case_insensitive_prefix, intents=intents, help_command=None)

users_file = "users.json"
cooldowns = {}

fish_pool = [{
    "name": "fish",
    "emoji": "<:fish:1399192790797127861>",
    "xp": 1,
    "chance": 59.00
}, {
    "name": "chad fish",
    "emoji": "<:chadfish:1399043761413292103>",
    "xp": 30,
    "chance": 9.00
}, {
    "name": "bebeto bass",
    "emoji": "<:bebeto_bass:1399043708879376405>",
    "xp": 50,
    "chance": 7.00
}, {
    "name": "superman shark",
    "emoji": "<:superman_shark:1399164285657022566>",
    "xp": 60,
    "chance": 6.00
}, {
    "name": "benjafish",
    "emoji": "<:benjafish:1399050676063043594>",
    "xp": 70,
    "chance": 5.00
}, {
    "name": "puffer sid",
    "emoji": "<:sid_pufferfish:1399144009175138426>",
    "xp": 80,
    "chance": 4.00
}, {
    "name": "slamuel sunny",
    "emoji": "<:slamuel_sunny:1399043599445790800>",
    "xp": 100,
    "chance": 3.00
}, {
    "name": "nateinator",
    "emoji": "<:nateinator:1399043897044369440>",
    "xp": 125,
    "chance": 2.00
}, {
    "name": "kermit lefish",
    "emoji": "<:kermit_lefish:1399158630023954452>",
    "xp": 150,
    "chance": 1.00
}, {
    "name": "mojicuslitus",
    "emoji": "<:mojicuslitus:1399194815517688052>",
    "xp": 250,
    "chance": 0.90
}, {
    "name": "SUPER RARE LAM CHAD FISH EXTREME",
    "emoji": "<:slam_extreme:1399043820884066344>",
    "xp": 1000,
    "chance": 0.09
}, {
    "name": "fih",
    "emoji": "<:fih:1399044570888671262>",
    "xp": 5000,
    "chance": 0.01
}]

rods = {
    "wooden rod": {
        "emoji": "<:wooden_rod:1399044497068920912>",
        "price": 0,
        "bonus": 0.00
    },
    "golden rod": {
        "emoji": "<:golden_rod:1399160694536146954>",
        "price": 750,
        "bonus": 0.10,
        "rarity_bonus": 0.01
    },
    "diamond rod": {
        "emoji": "<:diamond_rod:1399162231962341466>",
        "price": 1500,
        "bonus": 0.20,
        "rarity_bonus": 0.02
    },
    "brick rod": {
        "emoji": "<:brick_rod:1399163039781228607>",
        "price": 3000,
        "bonus": 0.35,
        "rarity_bonus": 0.03
    },
    "the henry fancy rod": {
        "emoji": "<:henry_rod:1399168206412841011>",
        "price": 7500,
        "bonus": 0.50,
        "rarity_bonus": 0.05
    },
    "godly rod": {
        "emoji": "<:godly_rod:1399163746626043946>",
        "price": 12000,
        "bonus": 0.70,
        "rarity_bonus": 0.07
    },
    "tryhard rod": {
        "emoji": "<:tryhard_rod:1399176725283471411>",
        "price": 20000,
        "bonus": 1.00,
        "rarity_bonus": 0.10
    },
}

boosts = {
    "double cast": {
        "emoji": "<:double_cast:1399044646700716154>",
        "price": 300,
        "duration": 60 * 60 * 3,
        "description": "Cast twice per 'sq cast' command for 3 hours"
    },
    "autosell": {
        "emoji": "<:autosell:1399198067533680741>",
        "price": 100,
        "duration": 60 * 60,
        "description": "Automatically sell any fish you catch for 1 hour"
    }
}


def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}


def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)


users = load_users()


def get_user_data(user):
    global users
    uid = str(user.id)

    # Load fresh users data to avoid stale cache
    users = load_users()

    # Initialize new user data if missing
    if uid not in users:
        users[uid] = {
            "xp": 0,
            "gold": 0,
            "level": 1,
            "inventory": {},
            "rods": {
                "wooden rod": 1
            },
            "rod": "wooden rod",
            "total_fish": 0,
            "boosts": {}
        }
    else:
        # Ensure keys exist for old users
        if "rod" not in users[uid]:
            users[uid]["rod"] = "wooden rod"
        if "rods" not in users[uid]:
            users[uid]["rods"] = {"wooden rod": 1}
        if "gold" not in users[uid]:
            users[uid]["gold"] = 0
        if "level" not in users[uid]:
            users[uid]["level"] = 1
        if "total_fish" not in users[uid]:
            users[uid]["total_fish"] = 0
        if "boosts" not in users[uid]:
            users[uid]["boosts"] = {}
        if "inventory" not in users[uid]:
            users[uid]["inventory"] = {}

    save_users()
    return users[uid]


def get_level_info(xp):
    level = 1
    required_xp = 100
    while xp >= required_xp:
        xp -= required_xp
        level += 1
        required_xp = 100 * level
    return level, xp, required_xp


def roll_fish():
    roll = random.uniform(0, 100)
    total = 0
    for fish in fish_pool:
        total += fish["chance"]
        if roll <= total:
            return fish
    return fish_pool[0]


def has_boost(user_data, boost_name):
    return boost_name in user_data["boosts"] and time.time(
    ) < user_data["boosts"][boost_name]


@bot.command(name="goon")
async def goon_corner(ctx, *, arg=None):
    if arg == "corner":
        await ctx.send(f"no {ctx.author.display_name}, you a freak")


@bot.command()
async def cast(ctx):
    user_id = str(ctx.author.id)
    user_data = get_user_data(ctx.author)
    now = time.time()

    if user_id in cooldowns and now - cooldowns[user_id] < 30:
        remaining = round(30 - (now - cooldowns[user_id]), 1)
        await ctx.send(
            f"⏳ {ctx.author.display_name}, you need to wait {remaining}s before fishing again."
        )
        return

    casts = 2 if has_boost(user_data, "double cast") else 1
    cooldowns[user_id] = now
    level_ups = 0

    # 🎣 Get rod bonuses
    equipped_rod = user_data.get("rod", "wooden rod")
    rod_data = rods.get(equipped_rod, {})
    gold_bonus = rod_data.get("bonus", 0)
    rarity_bonus = rod_data.get("rarity_bonus", 0)

    results = []
    for _ in range(casts):
        # 🎯 Apply rarity bonus to fish roll
        total_chance = sum(f["chance"] for f in fish_pool)
        roll = random.uniform(0, total_chance * (1 + rarity_bonus))

        cumulative = 0
        fish = None
        for f in fish_pool:
            cumulative += f["chance"]
            if roll <= cumulative:
                fish = f
                break

        if fish is None:
            await ctx.send("<:fish:1399192790797127861> You didn't catch anything!")
            continue

        name = fish["name"]
        emoji = fish["emoji"]
        xp = fish["xp"]

        user_data["xp"] += xp
        user_data["total_fish"] += 1

        gold_earned = 0

        if has_boost(user_data, "autosell"):
            gold_earned = int(xp * (1 + gold_bonus))
            user_data["gold"] += gold_earned
        else:
            user_data["inventory"][name] = user_data["inventory"].get(name,
                                                                      0) + 1
            gold_earned = int(xp * (1 + gold_bonus))

        new_level, xp_into_level, next_level_xp = get_level_info(user_data["xp"])
        if new_level > user_data.get("level", 1):
            level_ups += new_level - user_data.get("level", 1)
            user_data["level"] = new_level
            results.append(f"🎉 {ctx.author.display_name} leveled up to **Level {new_level}**!")

        result = f"<:cast_bobber:1399044610684096726> {ctx.author.display_name} caught a **{emoji} {name}**!\n<:level:1399200622779302004> XP: +{xp}"
        if has_boost(user_data, "autosell"):
            result += f"\n💰 Sold instantly for {gold_earned} <:coin:1399146146315894825> (Autosell Active)"
        results.append(result)

    embed = discord.Embed(color=discord.Color.yellow())
    embed.description = "\n".join(results)
    await ctx.send(embed=embed)
    save_users()


@bot.command(aliases=["cd", "cooldown"])
async def cooldown_check(ctx):
    user_id = str(ctx.author.id)
    now = time.time()
    user_data = get_user_data(ctx.author)

    remaining = 0
    if user_id in cooldowns and now - cooldowns[user_id] < 30:
        remaining = round(30 - (now - cooldowns[user_id]), 1)

    active_boosts = []
    emoji_map = {
        "double cast": "<:double_cast:1399044646700716154>",
        "autosell": "<:autosell:1399198067533680741>",
    }

    for boost in user_data.get("boosts", {}):
        if time.time() < user_data["boosts"][boost]:
            mins = int((user_data["boosts"][boost] - time.time()) // 60)
            boost_name = boost.title() if boost != "autosell" else "Autosell"
            emoji = emoji_map.get(boost, "")
            active_boosts.append(f"{emoji} {boost_name} ({mins}m left)")

    boost_text = "\n".join(
        active_boosts) if active_boosts else "No boosts active"

    embed = discord.Embed(
        title="Cooldown Check",
        description=
        f"{'✅ Cast is ready!' if remaining == 0 else f'⏳ Wait {remaining}s before fishing again.'}",
        color=discord.Color.purple())
    embed.add_field(name="<:boosts:1399198567486197791> Active Boosts",
                    value=boost_text)
    await ctx.send(embed=embed)


@bot.command(aliases=["p"])
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author  # Default to command user if no mention

    user_data = get_user_data(member)
    level, xp_into_level, next_level_xp = get_level_info(user_data["xp"])
    percent = int(
        (xp_into_level / next_level_xp) * 100) if next_level_xp > 0 else 0
    rod = user_data.get("rod", None)
    avatar = member.avatar.url if member.avatar else None

    inv_lines = []
    for fish in fish_pool:
        name = fish["name"]
        emoji = fish["emoji"]
        count = user_data["inventory"].get(name, 0)
        if count > 0:
            inv_lines.append(f"- **{emoji} {name}**: {count}")

    embed = discord.Embed(title=f"{member.display_name}'s Profile",
                          color=discord.Color.blue())
    if avatar:
        embed.set_thumbnail(url=avatar)

    if rod and rod in rods:
        rod_data = rods[rod]
        gold_bonus_percent = int(rod_data.get("bonus", 0) * 100)
        rarity_bonus_percent = int(rod_data.get("rarity_bonus", 0) * 100)
        rarity_text = f"\n*+ {rarity_bonus_percent}% rarity chance*" if rarity_bonus_percent > 0 else ""
        embed.add_field(
            name="Equipped Rod",
            value=f"**{rod_data['emoji']} {rod.title()}**\n"
                  f"*+ {gold_bonus_percent}% gold*{rarity_text}",
            inline=False)
    else:
        embed.add_field(
            name="Equipped Rod",
            value="**<:wooden_rod:1399044497068920912> Wooden Rod**",
            inline=False)

    embed.add_field(name="<:coin:1399146146315894825> Gold",
                    value=f"{user_data.get('gold', 0)}",
                    inline=False)
    embed.add_field(
        name="<:level:1399200622779302004> XP",
        value=
        f"Level {level} | {xp_into_level}/{next_level_xp} XP ({percent}%)",
        inline=False)

    if inv_lines:
        embed.add_field(name="<:backpack:1399064953239109723> Backpack",
                        value="\n".join(inv_lines),
                        inline=False)
    else:
        embed.add_field(name="<:backpack:1399064953239109723> Backpack",
                        value="Inventory is empty.",
                        inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def shop(ctx, category: str = None):
    user_data = get_user_data(ctx.author)
    user_gold = user_data.get("gold", 0)
    gold_display = f"{user_gold} <:coin:1399146146315894825>"

    if category is None:
        await ctx.send(
            "❌ Please specify a category: `sq shop rods` or `sq shop boosts`.")
        return

    category = category.lower()

    if category in ["rods", "rod"]:
        rod_lines = []
        for name, b in rods.items():
            bonus_percent = int(b.get("bonus", 0) * 100)
            rarity_percent = int(b.get("rarity_bonus", 0) * 100)

            rarity_text = f"\n*+ {rarity_percent}% rarity chance*" if rarity_percent > 0 else ""
            line = f"**{b['emoji']} {name.title()}** - {b['price']} <:coin:1399146146315894825>\n*+ {bonus_percent}% gold*{rarity_text}"
            rod_lines.append(line)

        embed = discord.Embed(title="🛍️ Rod Shop", color=discord.Color.red())
        embed.add_field(name="Your Gold", value=gold_display, inline=False)
        embed.add_field(name="Rods for sale",
                        value="\n".join(rod_lines),
                        inline=False)
        await ctx.send(embed=embed)

    elif category in ["boosts", "boost"]:
        boost_lines = []
        for name, b in boosts.items():
            line = f"**{b['emoji']} {name.title()}** - {b['price']} <:coin:1399146146315894825>\n*{b['description']}*"
            boost_lines.append(line)

        embed = discord.Embed(title="🛍️ Boost Shop", color=discord.Color.red())
        embed.add_field(name="Your Gold", value=gold_display, inline=False)
        embed.add_field(name="<:boosts:1399198567486197791> Boosts for sale",
                        value="\n".join(boost_lines),
                        inline=False)
        await ctx.send(embed=embed)

    else:
        await ctx.send(
            "❌ Invalid shop category. Use `sq shop rods` or `sq shop boosts`.")


@bot.command()
async def buy(ctx, *, item: str):
    user_data = get_user_data(ctx.author)
    item = item.lower()

    if item in boosts:
        boost = boosts[item]
        if user_data.get("gold", 0) >= boost["price"]:
            user_data["gold"] -= boost["price"]
            user_data["boosts"][item] = time.time() + boost["duration"]
            await ctx.send(
                f"✅ {ctx.author.display_name} bought **{item.title()}**!")
        else:
            await ctx.send("❌ Not enough gold.")
    elif item in rods:
        rod = rods[item]
        if user_data.get("gold", 0) >= rod["price"]:
            user_data["gold"] -= rod["price"]
            user_data["rods"][item] = user_data["rods"].get(item, 0) + 1
            user_data["rod"] = item
            await ctx.send(
                f"✅ {ctx.author.display_name} equipped **{item.title()}**!")
        else:
            await ctx.send("❌ Not enough gold.")
    else:
        await ctx.send("❌ Item not found.")
    save_users()


@bot.command()
async def sell(ctx, *, args: str):
    user_data = get_user_data(ctx.author)
    args = args.lower().split()
    inv = user_data["inventory"]

    total = 0

    # Handle "sell all" to sell all fish regardless of "fish" keyword
    if args == ["all"] or args == ["fish", "all"]:
        for fish in fish_pool:
            name = fish["name"]
            count = inv.get(name, 0)
            if count > 0:
                gold = int(fish["xp"] * count * (1 + rods.get(
                    user_data.get("rod", "wooden rod"), {}).get("bonus", 0)))
                total += gold
                inv[name] = 0
    else:
        name = " ".join(args[:-1]) if args[-1].isdigit() else " ".join(args)
        count = int(args[-1]) if args[-1].isdigit() else inv.get(name, 0)
        if name in inv and inv[name] >= count:
            fish = next((f for f in fish_pool if f["name"] == name), None)
            if fish:
                gold = int(fish["xp"] * count * (1 + rods.get(
                    user_data.get("rod", "wooden rod"), {}).get("bonus", 0)))
                total = gold
                inv[name] -= count
        else:
            await ctx.send("❌ Invalid fish or not enough quantity.")
            return

    user_data["gold"] = user_data.get("gold", 0) + total
    await ctx.send(
        f"{ctx.author.display_name} sold fish to the fisherman for {total} gold <:coin:1399146146315894825>"
    )
    save_users()


@bot.command()
async def stats(ctx):
    user_data = get_user_data(ctx.author)
    rod = user_data.get("rod", None)
    bonus = rods.get(rod, {}).get("bonus", 0) * 100 if rod else 0
    total = user_data.get("total_fish", 0)

    embed = discord.Embed(title=f"{ctx.author.display_name}'s Stats",
                          color=discord.Color.gold())
    embed.add_field(name="<:coin:1399146146315894825> Gold Boost",
                    value=f"+{int(bonus)}%",
                    inline=False)
    embed.add_field(name="<:wooden_rod:1399044497068920912> Total Fish Caught",
                    value=f"{total} <:fish:1399192790797127861>",
                    inline=False)
    await ctx.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear_all_stats(ctx):
    global users
    users = {}
    save_users()
    await ctx.send("✅ All user stats cleared.")


@bot.command()
async def guide(ctx):
    cmds = [
        "sq cast – Go fishing", "sq p / sq profile – View profile",
        "sq shop rods – View rod shop", "sq shop boosts – View boost shop",
        "sq buy <item> – Buy rods or boosts",
        "sq sell fish all or sq sell <fish> <amount> – Sell fish",
        "sq stats – Show stats",
        "sq cd / sq cooldown – Check casting cooldown & see active boosts",
        "sq guide – you're already here brev so idk what to tell u"
    ]
    fish_list = [
        f"- {f['emoji']} {f['name'].title()} ({f['chance']}%)"
        for f in fish_pool
    ]
    embed = discord.Embed(title="📘 Ship Quest Guide", color=discord.Color.green())
    embed.add_field(name="Commands", value="\n".join(cmds), inline=False)
    embed.add_field(name="Fish Types",
                    value="\n".join(fish_list),
                    inline=False)
    await ctx.send(embed=embed)


bot.run(
    "MTM5ODQ5OTE4OTEzODI2NDE1NQ.G4F1Eg.ar_-u9cjH9UosjiwWEXFCXAuzsq6bTR6bm1oso")
