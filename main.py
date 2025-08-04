import discord
from discord.ext import commands
import random
import time
import os
import json
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
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

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 or not parts:
        parts.append(f"{secs}s")
    return " ".join(parts)

cooldowns_file = "cooldowns.json"

cooldowns_file = "cooldowns.json"

def load_cooldowns():
    if os.path.exists(cooldowns_file):
        with open(cooldowns_file, "r") as f:
            data = json.load(f)
            return data.get("cast", {}), data.get("adventure", {})
    return {}, {}

def save_cooldowns():
    with open(cooldowns_file, "w") as f:
        json.dump({
            "cast": cooldowns,
            "adventure": adventure_cooldowns
        }, f)

# ✅ Correct placement
global cooldowns, adventure_cooldowns
cooldowns, adventure_cooldowns = load_cooldowns()

bot = commands.Bot(command_prefix=case_insensitive_prefix, intents=intents, help_command=None)

users_file = "users.json"

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
        "description": "Automatically sell any fish you catch from 'sq cast' for 1 hour"
    }
}

emissaries_data = {
    "treasure seekers": {
        "emoji": "<:treasure_seekers:1399452871660933213>",
        "short_description": "Where treasure hunters seek extra--well--treasure.",
    },
    "the anglers": {
        "emoji": "<:anglers:1399452850018320404>",
        "short_description": "Masters of fishing, seeking to get even better at their craft.",
    }
}

treasure_index = {
    "amber pendant": {"emoji": "<:amber_pendant:1400307044514533386>", "value": 75, "tier": 1},
    "apatite shard": {"emoji": "<:apatite_shard:1400306918634819604>", "value": 130, "tier": 2},
    "pearl necklace": {"emoji": "<:pearl_necklace:1400306812435300393>", "value": 150, "tier": 3},
    "ruby ring": {"emoji": "<:ruby_ring:1400307346093117624>", "value": 500, "tier": 1},
    "golden chalice": {"emoji": "<:golden_chalice:1400306658995081247>", "value": 1000, "tier": 4},
    "glass eye": {"emoji": "<:glass_eye:1400306719275487322>", "value": 1500, "tier": 5}
    
}

chests = {
    "classic chest": {
        "emoji": "<:chest:1399491916978192406>",
        "rewards": {
            "gold": (50, 100),
            "xp": (75, 150),
            "treasures": {
                "count": (1, 1),
                "max_tier": 2,
                "rarity_bias": 0.5
            }
        },
    },
    "silver chest": {
        "emoji": "<:silver_chest:1399491978835660881>",
        "rewards": {
            "gold": (150, 350),
            "xp": (225, 500),
            "treasures": {
                "count": (1, 2),
                "max_tier": 3,
                "rarity_bias": 0.8
            }
        },
    },
    "ruby chest": {
        "emoji": "<:ruby_chest:1399492078593118239>",
        "rewards": {
            "gold": (425, 750),
            "xp": (525, 775),
            "treasures": {
                "count": (1, 2),
                "max_tier": 4,
                "rarity_bias": 1.0
            }
        },
    },
    "diamond chest": {
        "emoji": "<:diamond_chest:1399492027607027732>",
        "rewards": {
            "gold": (1000, 2000),
            "xp": (1000, 2000),
            "treasures": {
                "count": (2, 2),
                "max_tier": 5,
                "rarity_bias": 1.3
            }
        },
    },
    "godly chest": {
        "emoji": "<:godly_chest:1399492135769739336>",
        "rewards": {
            "gold": (2000, 3000),
            "xp": (2000, 3000),
            "treasures": {
                "count": (2, 2),
                "max_tier": 5,
                "rarity_bias": 1.7
            }
        },
    }
}

chest_emissary_xp = {
    "classic chest": 0, #6
    "silver chest": 0, #13
    "ruby chest": 0, #20
    "diamond chest": 0, #32
    "godly chest": 0 #50
}

special_gems = {
    5: "red gem",
    10: "green gem",
    15: "blue gem",
    20: "purple gem"
}

treasure_index.update({
    #"red gem": {"emoji": "<:red_gem:1400305184525258926>", "value": 100, "tier": 3},
    #"green gem": {"emoji": "<:green_gem:1400305261578817637>", "value": 120, "tier": 3},
    #"blue gem": {"emoji": "<:blue_gem:1400305224131805226>", "value": 140, "tier": 4},
    #"purple gem": {"emoji": "<:purple_gem:1400305310823878786>", "value": 160, "tier": 5},
})

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
            "boosts": {},
            "emissaries": {
                "the anglers": {"level": 0, "xp": 0},
                "treasure seekers": {"level": 0, "xp": 0}
            },
            
            "emissary": None,
            "emissary_level": 0,
            "chests": {},
            "treasures": {}
        }
    else:
        
        if "emissaries" not in users[uid]:
            users[uid]["emissaries"] = {}

        if "the anglers" not in users[uid]["emissaries"]:
            users[uid]["emissaries"]["the anglers"] = {"level": 0, "xp": 0}
        if "treasure seekers" not in users[uid]["emissaries"]:
            users[uid]["emissaries"]["treasure seekers"] = {"level": 0, "xp": 0}

        if "emissary" not in users[uid]:
            users[uid]["emissary"] = None
        if "emissary_level" not in users[uid]:
            users[uid]["emissary_level"] = 0
        if "chests" not in users[uid]:
            users[uid]["chests"] = {}
        if "treasures" not in users[uid]:
            users[uid]["treasures"] = {}

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

def choose_treasures(max_tier, count_range, rarity_bias):
    # Filter treasures by max tier
    eligible = [name for name, info in treasure_index.items() if info["tier"] <= max_tier]
    count = random.randint(*count_range)
    selected = []

    # Calculate weights so higher tier = rarer (lower weight)
    weights = []
    for name in eligible:
        tier = treasure_index[name]["tier"]
        # Weight inversely proportional to tier ^ rarity_bias
        weight = 1 / (tier ** rarity_bias)
        weights.append(weight)

    for _ in range(count):
        chosen = random.choices(eligible, weights=weights, k=1)[0]
        selected.append(chosen)

    return selected
    
def roll_fish():
    roll = random.uniform(0, 100)
    total = 0
    for fish in fish_pool:
        total += fish["chance"]
        if roll <= total:
            return fish
    return fish_pool[0]

for uid, user_data in users.items():
    if "emissaries" in user_data:
        for em in user_data["emissaries"]:
            user_data["emissaries"][em]["xp"] = 0

save_users()

def update_player_emissary_level(user_id: int, emissary_name: str, new_level: int):
    user_id_str = str(user_id)
    if user_id_str not in player_emissary_levels:
        player_emissary_levels[user_id_str] = {}
    capped_level = min(new_level, 25)  # cap the level at 25
    player_emissary_levels[user_id_str][emissary_name] = capped_level
    save_emissary_levels()

def get_required_emissary_xp(level):
    if level >= 25:
        return float('inf')  # prevent leveling past 25
    return level * 100

def has_boost(user_data, boost_name):
    return boost_name in user_data["boosts"] and time.time(
    ) < user_data["boosts"][boost_name]

@bot.command()
async def debug_inventory(ctx):
    user_data = get_user_data(ctx.author)
    await ctx.send(f"```{json.dumps(user_data['inventory'], indent=2)}```")

@bot.command(name="goon")
async def goon_corner(ctx, *, arg=None):
    if arg == "corner":
        await ctx.send(f"no {ctx.author.display_name}, you a freak")

@bot.command(aliases=["adv"])
async def adventure(ctx):
    user = ctx.author
    user_id = str(user.id)
    user_data = get_user_data(user)
    now = time.time()

    # ⏳ Cooldown logic (30 min)
    if user_id in adventure_cooldowns:
        elapsed = now - adventure_cooldowns[user_id]
        if elapsed < 7200:
            remaining = int((7200 - elapsed) // 60)
            await ctx.send("🕓 You can not adventure again yet, check cooldown with 'sq cd'")
            return

    adventure_cooldowns[user_id] = now
    save_cooldowns()
    
    chest_names = list(chests.keys())
    weights = [75, 12, 8, 4, 1]  # adjust to match rarity by order in `chests`

    chosen_name = random.choices(chest_names, weights=weights)[0]
    chest_data = chests[chosen_name]
    emoji = chest_data["emoji"]

    user_data["chests"][chosen_name] = user_data["chests"].get(chosen_name, 0) + 1

    embed = discord.Embed(
        title="🗺️ Adventure Complete!",
        description=f"{ctx.author.display_name} found a {emoji} **{chosen_name.title()}**!",
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed)
    save_users()

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
    cooldowns[user_id] = now
    save_cooldowns()


    casts = 2 if has_boost(user_data, "double cast") else 1
    cooldowns[user_id] = now
    level_ups = 0

    equipped_rod = user_data.get("rod", "wooden rod")
    rod_data = rods.get(equipped_rod, {})
    gold_bonus = rod_data.get("bonus", 0)
    rarity_bonus = rod_data.get("rarity_bonus", 0)

    results = []
    for _ in range(casts):
        # 🎯 Apply rarity bonus to fish roll
        adjusted_chances = [f["chance"] * (1 + rarity_bonus) for f in fish_pool]
        fish = random.choices(fish_pool, weights=adjusted_chances)[0]

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
    
import os

EMISSARY_LEVELS_FILE = "emissary_levels.json"

if os.path.exists(EMISSARY_LEVELS_FILE):
    with open(EMISSARY_LEVELS_FILE, "r") as f:
        player_emissary_levels = json.load(f)
else:
    player_emissary_levels = {}

def save_emissary_levels():
    with open(EMISSARY_LEVELS_FILE, "w") as f:
        json.dump(player_emissary_levels, f, indent=4)
        
@bot.command(aliases=["em"])
async def emissary(ctx, *, name: str = None):
    if name is None:
        embed = discord.Embed(
            title="Emissaries",
            description="Use `sq em <name>` for more info.",
            color=discord.Color.from_rgb(255, 255, 255)
        )

        embed.set_thumbnail(url="https://www.pngmart.com/files/11/Jolly-Roger-Transparent-Background.png")

        for em, data in emissaries_data.items():
            emoji = data.get("emoji", "")
            short_desc = data.get("short_description", "No description available.")
            embed.add_field(name=f"{emoji} {em.title()}", value=short_desc, inline=False)
        await ctx.send(embed=embed)
        return

    name = name.lower().strip()
    if name not in emissaries_data:
        valid = ", ".join(f"`{e.title()}`" for e in emissaries_data.keys())
        await ctx.send(f"❌ `{name.title()}` is not a valid emissary.\nAvailable emissaries: {valid}")
        return

    data = emissaries_data[name]
    emoji = data.get("emoji", "")
    title = name.title()

    embed = discord.Embed(
        title=f"{emoji} {title}",
        description="Emissary Info",
        color=discord.Color.from_rgb(255, 255, 255)
    )

    user_id = str(ctx.author.id)
    user_data = users.get(user_id, {})

    emissaries = user_data.get("emissaries", {})
    emissary_data = emissaries.get(name, {"level": 0, "xp": 0})
    level = emissary_data.get("level", 0)
    xp = emissary_data.get("xp", 0)

    def xp_to_next_level(level):
        base_xp = 100
        growth_factor = 1.5
        if level <= 0:
            return base_xp
        return int(base_xp * (growth_factor ** (level - 1)))

    xp_needed = xp_to_next_level(level)
    percent = int((xp / xp_needed) * 100) if xp_needed else 0

    progress_str = f"Level {level} ({percent}%)"

    embed.add_field(name="Emissary Level", value=progress_str, inline=False)

    await ctx.send(embed=embed)

@bot.command(aliases=["open"])
async def open_chest(ctx, *, args: str):
    args_list = args.lower().split()

    if not args_list:
        await ctx.send("❌ Please specify a chest name")
        return

    if args_list[-1] == "all":
        amount = "all"
        chest_name_words = args_list[:-1]
    else:
        try:
            amount = int(args_list[-1])
            chest_name_words = args_list[:-1]
        except ValueError:
            amount = 1
            chest_name_words = args_list

    chest_name = " ".join(chest_name_words).strip()
    if not chest_name:
        await ctx.send("❌ Please specify a chest name")
        return

    if chest_name not in chests:
        await ctx.send("❌ Not a valid chest type")
        return

    user_data = get_user_data(ctx.author)
    user_chests = user_data.get("chests", {})
    user_chest_count = user_chests.get(chest_name, 0)

    if user_chest_count <= 0:
        await ctx.send(f"❌ You don't have any **{chest_name.title()}** to open")
        return

    if amount == "all":
        to_open = user_chest_count
    else:
        to_open = amount
        if to_open < 1:
            await ctx.send("bro, you can't have a negative or decimal amount of chests")
            return
        if to_open > user_chest_count:
            await ctx.send(f"❌ You only have {user_chest_count} **{chest_name.title()}** to open, don't get ahead of yourself")
            return

    chest = chests[chest_name]
    emoji = chest["emoji"]
    rewards = chest["rewards"]

    total_gold = 0
    total_xp = 0
    total_emissary_xp = 0
    found_treasures = []

    for _ in range(to_open):
        gold = random.randint(*rewards.get("gold", (0, 0)))
        xp = random.randint(*rewards.get("xp", (0, 0)))
        total_gold += gold
        total_xp += xp

        treasure_config = rewards.get("treasures")
        if treasure_config:
            count_range = treasure_config["count"]
            max_tier = treasure_config["max_tier"]
            rarity_bias = treasure_config["rarity_bias"]
            selected = choose_treasures(max_tier, count_range, rarity_bias)

            if "treasures" not in user_data:
                user_data["treasures"] = {}
            inventory = user_data.setdefault("inventory", {})

            for name in selected:
                user_data["inventory"][name] = user_data["inventory"].get(name, 0) + 1
                user_data["treasures"][name] = user_data["treasures"].get(name, 0) + 1
                found_treasures.append(name)

    if user_data.get("emissary") == "treasure seekers":
        emissary_xp = chest_emissary_xp.get(chest_name, 0) * to_open
        total_emissary_xp += emissary_xp

    user_data["gold"] += total_gold
    user_data["xp"] += total_xp
    user_chests[chest_name] -= to_open

    # Emissary XP and level up with gem rewards
    if total_emissary_xp > 0:
        em_data = user_data.setdefault("emissaries", {}).setdefault("treasure seekers", {"level": 0, "xp": 0})
        old_level = em_data["level"]
        em_data["xp"] += total_emissary_xp

        while em_data["level"] < 25 and em_data["xp"] >= get_required_emissary_xp(em_data["level"]):
            em_data["xp"] -= get_required_emissary_xp(em_data["level"])
            em_data["level"] += 1

        # special_gems dictionary must be defined somewhere globally
        for milestone_level, gem_name in special_gems.items():
            if old_level < milestone_level <= em_data["level"]:
                inventory = user_data.setdefault("inventory", {})
                inventory[gem_name] = inventory.get(gem_name, 0) + 1
                await ctx.send(f"🎉 Congrats! You reached level {milestone_level} in Treasure Seekers and received a **{gem_name.title()}**!")

    new_level, xp_into_level, next_level_xp = get_level_info(user_data["xp"])
    level_up_text = ""
    if new_level > user_data.get("level", 1):
        level_up_text = f"\n🎉 You leveled up to **Level {new_level}**!"
        user_data["level"] = new_level

    embed = discord.Embed(
        title=f"{emoji} {ctx.author.display_name} opened {to_open} {chest_name.title()}{'s' if to_open > 1 else ''}!",
        color=discord.Color.gold()
    )

    lines = []
    if found_treasures:
        treasure_lines = [f"{treasure_index[t]['emoji']} **{t.title()}**" for t in found_treasures]
        lines.extend(treasure_lines)

    lines.append(f"<:coin:1399146146315894825> Gold: +{total_gold}")
    lines.append("")
    lines.append(f"<:level:1399200622779302004> XP: +{total_xp}{level_up_text}")

    embed.description = "\n".join(lines)

    await ctx.send(embed=embed)
    save_users()

@bot.command(aliases=["cd", "cooldown"])
async def cooldown_check(ctx):
    user_id = str(ctx.author.id)
    now = time.time()
    user_data = get_user_data(ctx.author)

    cast_remaining = 0
    if user_id in cooldowns and now - cooldowns[user_id] < 30:
        cast_remaining = 30 - (now - cooldowns[user_id])
        
    adventure_remaining = 0
    if user_id in adventure_cooldowns and now - adventure_cooldowns[user_id] < 7200:
        adventure_remaining = 7200 - (now - adventure_cooldowns[user_id])

    active_boosts = []
    emoji_map = {
        "double cast": "<:double_cast:1399044646700716154>",
        "autosell": "<:autosell:1399198067533680741>",
    }

    for boost in user_data.get("boosts", {}):
        remaining = user_data["boosts"][boost] - time.time()
        if remaining > 0:
            boost_name = boost.title() if boost != "autosell" else "Autosell"
            emoji = emoji_map.get(boost, "")
            active_boosts.append(f"{emoji} {boost_name} ({format_duration(remaining)} left)")

    boost_text = "\n".join(active_boosts) if active_boosts else "No boosts active"

    desc_lines = [
        f"{'✅ -- Cast' if cast_remaining == 0 else f'🕓 -- Cast ({format_duration(cast_remaining)})'}",
        f"{'✅ -- Adventure' if adventure_remaining == 0 else f'🕓 -- Adventure ({format_duration(adventure_remaining)})'}"
    ]

    embed = discord.Embed(
        title="━━━━ Cooldown Check ━━━━",
        description="\n".join(desc_lines),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="━━━━ <:boosts:1399198567486197791> Active Boosts ━━━━",
        value=boost_text,
        inline=False
    )

    await ctx.send(embed=embed)

@bot.command(aliases=[""])
async def pledge(ctx, *, emissary: str):
    emissary = emissary.lower().strip()

    if emissary not in emissaries_data:
        valid = ", ".join(e.title() for e in emissaries_data.keys())
        await ctx.send(f"❌ `{emissary.title()}` is not a valid emissary. Please choose one of: {valid}")
        return

    user_data = get_user_data(ctx.author)
    user_data["emissary"] = emissary
    user_data["emissary_level"] = user_data.get("emissary_level", 0) or 0
    save_users()

    emoji = emissaries_data[emissary]["emoji"]
    await ctx.send(f"✅ You pledged allegiance to {emoji} **{emissary.title()}**!")

@bot.command(aliases=["p"])
async def profile(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    user_data = get_user_data(member)
    level, xp_into_level, next_level_xp = get_level_info(user_data["xp"])
    percent = int((xp_into_level / next_level_xp) * 100) if next_level_xp > 0 else 0
    avatar = member.avatar.url if member.avatar else None

    embed = discord.Embed(title=f"{member.display_name}'s Profile",
                          color=discord.Color.blue())
    if avatar:
        embed.set_thumbnail(url=avatar)

    emissary = user_data.get("emissary")
    emissary_level = user_data.get("emissary_level", 0)
    if emissary:
        emissary_title = emissary.title()
        emissary_emoji = emissaries_data.get(emissary, {}).get("emoji", "")
        embed.add_field(name="Current Emissary",
                        value=f"{emissary_emoji} **{emissary_title}** (Level {emissary_level})",
                        inline=False)
    else:
        embed.add_field(name="Current Emissary",
                        value="None",
                        inline=False)

    rod = user_data.get("rod", None)
    rod_data = rods.get(rod, rods["wooden rod"])
    gold_bonus = int(rod_data.get("bonus", 0) * 100)
    gold = user_data.get("gold", 0)
    embed.add_field(name="<:coin:1399146146315894825> Gold",
                    value=f"{gold} (+{gold_bonus}% boost)",
                    inline=False)

    embed.add_field(name="<:level:1399200622779302004> XP",
                    value=f"Level {level} | {xp_into_level}/{next_level_xp} XP ({percent}%)",
                    inline=False)
    
    total_fish = user_data.get("total_fish", 0)
    embed.add_field(name="<:wooden_rod:1399044497068920912> Total Fish Caught",
                    value=f"{total_fish} <:fish:1399192790797127861>",
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
        embed.add_field(name="━━━━ Rods for sale ━━━━",
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
        embed.add_field(name="━━━━ <:boosts:1399198567486197791> Boosts for sale ━━━━",
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
    sold_message = ""

    if args == ["all", "fish"]:
        sold_fish = []
        for fish in fish_pool:
            name = fish["name"]
            count = inv.get(name, 0)
            if count > 0:
                gold = int(fish["xp"] * count * (1 + rods.get(
                    user_data.get("rod", "wooden rod"), {}).get("bonus", 0)))
                total += gold
                inv[name] = 0
                sold_fish.append(f"{count} {name.title()}")
        if not sold_fish:
            await ctx.send("❌ You have no fish to sell.")
            return
        sold_message = f"{ctx.author.display_name} sold {', '.join(sold_fish)} to the fisherman for {total} gold <:coin:1399146146315894825>"

    else:
        if len(args) < 2:
            await ctx.send("❌ Please specify the item name and the amount (or 'all'). Example: `sq sell chadfish 3` or `sq sell amber pendant all`")
            return

        name = " ".join(args[:-1])
        amount_arg = args[-1]

        if amount_arg == "all":
            count = inv.get(name, 0)
        elif amount_arg.isdigit():
            count = int(amount_arg)
        else:
            await ctx.send("❌ Amount must be a number or the word 'all'.")
            return

        if name not in inv or inv[name] < count or count <= 0:
            await ctx.send("❌ Check the amount of that item you have.")
            return

        fish = next((f for f in fish_pool if f["name"] == name), None)
        if fish:
            gold = int(fish["xp"] * count * (1 + rods.get(
                user_data.get("rod", "wooden rod"), {}).get("bonus", 0)))
            total = gold
            inv[name] -= count
            sold_message = f"{ctx.author.display_name} sold {count} {name.title()} to the fisherman for {total} gold <:coin:1399146146315894825>"
        
        elif name in treasure_index:
            value = treasure_index[name]["value"]
            total = value * count
            inv[name] -= count
            sold_message = f"{ctx.author.display_name} sold {count} {name.title()} to the treasure trader for {total} gold <:coin:1399146146315894825>"
        else:
            await ctx.send("❌ That item can't be sold here.")
            return

    user_data["gold"] = user_data.get("gold", 0) + total
    await ctx.send(sold_message)
    save_users()

@bot.command()
@commands.has_permissions(administrator=True)
async def clear_all_stats(ctx):
    global users
    users = {}
    save_users()
    await ctx.send("✅ All user stats cleared.")

@bot.command(aliases=["i", "inv"])
async def inventory(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author

    user_data = get_user_data(member)
    inventory = user_data.get("inventory", {})
    rod = user_data.get("rod", None)
    avatar = member.avatar.url if member.avatar else None

    fish_lines = []
    for fish in fish_pool:
        name = fish["name"]
        emoji = fish["emoji"]
        count = inventory.get(name, 0)
        if count > 0:
            fish_lines.append(f"{emoji} {name} — {count}")

    treasure_lines = []
    for treasure_name, treasure_data in treasure_index.items():
        count = inventory.get(treasure_name, 0)
        if count > 0:
            treasure_lines.append(f"{treasure_data['emoji']} {treasure_name.title()} — {count}")

    embed = discord.Embed(
        title=f"{member.display_name}'s Inventory",
        color=discord.Color.green()
    )
    if avatar:
        embed.set_thumbnail(url=avatar)

    embed.add_field(
        name="━━━━ <:backpack:1399064953239109723> Backpack ━━━━",
        value="\n".join(fish_lines) if fish_lines else "Inventory is empty.",
        inline=False
    )

    if treasure_lines:
        embed.add_field(
            name="━━━━ Treasures ━━━━",
            value="\n".join(treasure_lines),
            inline=False
        )

    chest_lines = []
    for name, data in chests.items():
        count = user_data.get("chests", {}).get(name, 0)
        if count > 0:
            chest_lines.append(f"{data['emoji']} {name.title()} — {count}")

    if chest_lines:
        embed.add_field(
            name="━━━━ Chests ━━━━",
            value="\n".join(chest_lines),
            inline=False
        )

    if rod and rod in rods:
        rod_data = rods[rod]
        gold_bonus_percent = int(rod_data.get("bonus", 0) * 100)
        rarity_bonus_percent = int(rod_data.get("rarity_bonus", 0) * 100)
        rarity_text = f"\n*+ {rarity_bonus_percent}% rarity chance*" if rarity_bonus_percent > 0 else ""
        embed.add_field(
            name="━━━━ Equipped Rod ━━━━",
            value=f"{rod_data['emoji']} {rod.title()}\n*+ {gold_bonus_percent}% gold*{rarity_text}",
            inline=False
        )
    else:
        embed.add_field(
            name="Equipped Rod",
            value="**<:wooden_rod:1399044497068920912> Wooden Rod**",
            inline=False
        )

    await ctx.send(embed=embed)

@bot.command(aliases=["fishindex", "fi"])
async def fish_index(ctx):
    lines = []
    for fish in fish_pool:
        emoji = fish["emoji"]
        name = fish["name"].title()
        rarity = fish["chance"]
        base_gold = fish["xp"]  # or multiply if you want
        lines.append(f"{emoji} **{name}** — {rarity}% chance — {base_gold} <:coin:1399146146315894825>")

    embed = discord.Embed(
        title="Fish Index",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    embed.set_footer(text="*Coins represent base selling price before boosts. XP values are equivalent to base gold price")

    await ctx.send(embed=embed)

@bot.command(aliases=["ci", "chestindex"])
async def chest_index(ctx):
    lines = []
    for name, chest in chests.items():
        emoji = chest["emoji"]
        gold_min, gold_max = chest["rewards"]["gold"]
        xp_min, xp_max = chest["rewards"]["xp"]
        lines.append(
            f"{emoji} **{name.title()}**\n<:coin:1399146146315894825> Gold: {gold_min}–{gold_max} | <:level:1399200622779302004> XP: {xp_min}–{xp_max}"
        )

    embed = discord.Embed(
        title="Chest Index",
        description="\n\n".join(lines),
        color=discord.Color.gold()
    )
    embed.set_footer(text="Rewards are randomized within listed ranges")
    await ctx.send(embed=embed)

@bot.command()
async def guide(ctx):
    embed = discord.Embed(title="📘 Ship Quest Guide", color=discord.Color.green())

    fishing_cmds = [
        "sq cast – Cast your rod for a fish",
        "sq adv / sq adventure – Go on an adventure to find chests",
        "sq fi / sq fish index – View list of fish and their stats",
        "sq ci / sq chest index – View list of chests and their possible contents",
        "sq open <chest> – Open a chest from your inventory",
        "sq sell fish all or sq sell <fish> <amount> – Sell fish"
    ]
    embed.add_field(name="━━━━ <:wooden_rod:1399044497068920912> Fishing & Loot Commands <:chest:1399491916978192406> ━━━━", value="\n".join(fishing_cmds), inline=False)

    inventory_cmds = [
        "sq p / sq profile – View profile",
        "sq i / sq inventory – View Inventory",
        "sq shop rods – View rod shop",
        "sq shop boosts – View boost shop",
        "sq buy <item> – Buy rods or boosts",
        "sq cd / sq cooldown – Check cooldowns & see active boosts"
    ]
    embed.add_field(name="━━━━ 🛍️ Inventory & Shops ━━━━", value="\n".join(inventory_cmds), inline=False)

    emissary_cmds = [
        "sq em / sq emissaries – View list of emissaries",
        "sq pledge <emissary> – Pledge allegiance to an emissary (coming soon...)"
    ]
    embed.add_field(name="━━━━ 🏴‍☠️ Emissary Commands━━━━", value="\n".join(emissary_cmds), inline=False)

    misc_cmds = [
        "sq guide – You're already here brev so idk what to tell u"
    ]
    embed.add_field(name="━━━━ Miscellaneous ━━━━", value="\n".join(misc_cmds), inline=False)

    await ctx.send(embed=embed)

keep_alive()

bot.run(TOKEN)
