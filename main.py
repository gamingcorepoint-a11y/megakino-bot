import asyncio

from irc_client import IRCClient
from systems.race_system.race_system import join_race, auto_race_loop
from systems.xp import handle_xp, command_level


def parse_privmsg(line: str):
    """
    Erwartet z.B.:
    :username!username@username.tmi.twitch.tv PRIVMSG #channel :nachricht
    Gibt (user, message) zurück oder (None, None) wenn nicht parsebar.
    """
    if "PRIVMSG" not in line:
        return None, None

    try:
        prefix = line.split("!", 1)[0]          # ":username"
        user = prefix.lstrip(":")               # "username"
        message = line.split("PRIVMSG", 1)[1]   # " #channel :nachricht"
        message = message.split(":", 1)[1].strip()
        return user, message
    except Exception:
        return None, None


async def handle_message(line: str, client: IRCClient):
    user, message = parse_privmsg(line)
    if not user or not message:
        return

    msg = message.strip()
    msg_lower = msg.lower()

    # optional: Ausgabe im Terminal (nicht in Twitch-Chat!)
    print(f"[CHAT] {user}: {msg}")

    # XP bei jeder Nachricht
    await handle_xp(user, client.send)

    # Commands
    if msg_lower == "!level":
        await command_level(user, client.send)
        return

    # Autorennen: !g = Join + ggf. Start
    if msg_lower == "!g":
        await join_race(user, client.send)
        return


async def main():
    client = IRCClient()
    await client.connect()
    print("✅ Bot verbunden!")

    # Auto-Rennen Loop (alle 23 Minuten)
    asyncio.create_task(auto_race_loop(client.send))

    # IRC Listen loop
    await client.listen(lambda line: handle_message(line, client))


if __name__ == "__main__":
    asyncio.run(main())
