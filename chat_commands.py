from minecraft.networking.packets import ChatPacket
from utils import distance

class ChatCommandHandler:
    def __init__(self, bot):
        self.bot = bot

    def handle_chat(self, packet: ChatPacket):
        message = packet.json_data.get('text', '').strip()
        sender = packet.json_data.get('extra', [{}])[0].get('text', '')

        if sender == self.bot.username:
            return

        if message == "/fight":
            self.handle_fight(sender)
        elif message == "/wait":
            self.handle_wait(sender)

    def handle_fight(self, sender):
        player_pos = self.bot.get_player_position(sender)
        bot_pos = self.bot.spawn_position

        if player_pos and distance(bot_pos, player_pos) <= self.bot.movement.roam_radius:
            if self.bot.is_fighting:
                self.send_chat(f"SenshiPvpBot is already fighting {self.bot.target_player}!")
            else:
                self.bot.is_fighting = True
                self.bot.target_player = sender
                self.send_chat(f"SenshiPvpBot entered PvP! Target: {sender}")
        else:
            self.send_chat(f"{sender} is too far away to fight.")

    def handle_wait(self, sender):
        if self.bot.is_fighting and self.bot.target_player == sender:
            self.bot.is_fighting = False
            self.bot.target_player = None
            self.send_chat("SenshiPvpBot stopped fighting.")

    def send_chat(self, message):
        try:
            self.bot.safe_send(self.bot.connection.create_packet('chat_message', message=message))
        except:
            pass
