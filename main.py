import discord
import os
from dotenv import load_dotenv
import requests
import json
from datetime import datetime
import random
from discord.ext import commands
from keep_alive import keep_alive

keep_alive()

# Load environment variables from .env file
load_dotenv(override=True)
TOKEN = os.getenv('DISCORD_TOKEN')
print(TOKEN)

# Create a new Discord client
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='$', intents=intents)


def get_token_price(symbol, category='spot'):
    response = None
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        params = {'category': category, 'symbol': symbol}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()

            if data['retCode'] == 0 and 'result' in data and 'list' in data[
                    'result']:
                token_data = data['result']['list'][0]
                price = token_data['lastPrice']
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Create a comprehensive price info
                price_info = {
                    'symbol': symbol,
                    'timestamp': current_time,
                    'lastPrice': float(token_data['lastPrice'])
                }

                return price_info
            else:
                print(f'Error in API response format: {data}')
                return None
        else:
            print(
                f'Error: API request failed with status code {response.status_code}'
            )
            return None

    except requests.exceptions.RequestException as e:
        print(f'Request error: {str(e)}')
        return None
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {str(e)}')
        return None
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None


def get_all_tokens():
    tokens = [
        'BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'ADAUSDT', 'DOTUSDT', 'LINKUSDT',
        'XRPUSDT', 'UNIUSDT', 'AVAXUSDT', 'ATOMUSDT', 'ORDIUSDT', 'DOGEUSDT'
    ]

    token_prices = {}

    for token in tokens:
        price_info = get_token_price(token)
        if price_info:
            token_prices[token] = price_info
    return token_prices


def get_btc_price():
    response = None
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        # Bybit v5 API endpoint for BTC/USDT price
        params = {'category': 'spot', 'symbol': 'BTCUSDT'}

        # Make the request
        response = requests.get(url, params=params, timeout=10)

        # check
        if response.status_code == 200:
            data = response.json()

            if data['retCode'] == 0 and 'result' in data and 'list' in data[
                    'result']:
                btc_data = data['result']['list'][0]
                price = btc_data['lastPrice']

                # Get current time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Print Result
                print(f'Bitoy Price Data from Bybit:')
                print(f'Time: {current_time}')
                print(f'BTC/USDT: ${price}')
                print(f"24h High ${btc_data['highPrice24h']}")
                print(f"24h Low ${btc_data['lowPrice24h']}")

                return float(price)
            else:
                print(f'Error in API response format: {data}')
                return None
        else:
            print(
                f'Error: API request failed with status code {response.status_code}'
            )
            return None

    except requests.exceptions.RequestException as e:
        print(f'Request error: {str(e)}')
        return None
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {str(e)}')
        return None
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None


def get_eth_price():
    response = None
    try:
        url = "https://api.bybit.com/v5/market/tickers"
        # Bybit v5 API endpoint for ETH/USDT price
        params = {'category': 'spot', 'symbol': 'ETHUSDT'}

        # Make the request
        response = requests.get(url, params=params, timeout=10)

        # check
        if response.status_code == 200:
            data = response.json()

            if data['retCode'] == 0 and 'result' in data and 'list' in data[
                    'result']:
                eth_data = data['result']['list'][0]
                price = eth_data['lastPrice']

                # Get current time
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # Print Result
                print(f'ETH Price Data from Bybit:')
                print(f'Time: {current_time}')
                print(f'ETH/USDT: ${price}')
                print(f"24h High ${eth_data['highPrice24h']}")
                print(f"24h Low ${eth_data['lowPrice24h']}")

                return float(price)
            else:
                print(f'Error in API response format: {data}')
                return None
        else:
            print(
                f'Error: API request failed with status code {response.status_code}'
            )
            return None

    except requests.exceptions.RequestException as e:
        print(f'Request error: {str(e)}')
        return None
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {str(e)}')
        return None
    except Exception as e:
        print(f'An error occurred: {str(e)}')
        return None


@client.event
async def on_ready():  # When the bot is ready
    print(f"I'm in as {client.user}")


@bot.command()
async def price(ctx, token='all'):
    try:
        if token.upper() == 'ALL':
            prices = get_all_tokens()
            message = "🚀 Current Token Prices 💹:\n"
            for symbol, price_info in prices.items():
                message += f"• {symbol}: ${price_info['lastPrice']:,.2f}\n"
            await ctx.send(message)
        else:
            token_price = get_token_price(f"{token.upper()}USDT")
            if token_price:
                await ctx.send(
                    f"💰 {token.upper()} Price: ${token_price['lastPrice']:,.2f}"
                )
            else:
                await ctx.send(f"❌ Could not fetch price for {token.upper()}")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")


@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$test'):
        await message.channel.send('testing bot succsessful')
    # Convert message to lowercase for case-insensitive matching
    msg = message.content.lower()

    # Price command for specific token
    if msg.startswith('$price '):
        token = msg.split('$price ')[1].upper()

        # Check for 'all' command
        if token == 'ALL':
            try:
                prices = get_all_tokens()
                message_text = "🚀 Current Token Prices 💹:\n"
                for symbol, price_info in prices.items():
                    message_text += f"• {symbol}: ${price_info['lastPrice']:,.2f}\n"
                await message.channel.send(message_text)
            except Exception as e:
                await message.channel.send(
                    f"Error fetching all prices: {str(e)}")
        else:
            # Fetch price for specific token
            try:
                token_price = get_token_price(f"{token}USDT")
                if token_price:
                    await message.channel.send(
                        f"💰 {token} Price: ${token_price['lastPrice']:,.2f}")
                else:
                    await message.channel.send(
                        f"❌ Could not fetch price for {token}")
            except Exception as e:
                await message.channel.send(
                    f"Error fetching {token} price: {str(e)}")


keep_alive()
client.run(TOKEN)
